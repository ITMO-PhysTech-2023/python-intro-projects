import nest_asyncio
from pyngrok import ngrok
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, Union, List
from fastapi import FastAPI, HTTPException, Query, Request


import os
import torch
import json

from typing import List, Union, Dict, FrozenSet, Set, Iterable
import numpy as np
import tqdm
import nltk
import torch.multiprocessing as mp
import queue
import math
import re
import logging
import time

import requests
import importlib
import sys

import time
from transformers import MarianMTModel, MarianTokenizer
import torch
from typing import List
import logging

logger = logging.getLogger(__name__)


class OpusMT:
    def __init__(self, easynmt_path: str = None, max_loaded_models: int = 10):
        self.models = {}
        self.max_loaded_models = max_loaded_models
        self.max_length = None

    def load_model(self, model_name):
        if model_name in self.models:
            self.models[model_name]['last_loaded'] = time.time()
            return self.models[model_name]['tokenizer'], self.models[model_name]['model']
        else:
            logger.info("Load model: "+model_name)
            tokenizer = MarianTokenizer.from_pretrained(model_name)
            model = MarianMTModel.from_pretrained(model_name)
            model.eval()

            if len(self.models) >= self.max_loaded_models:
                oldest_time = time.time()
                oldest_model = None
                for loaded_model_name in self.models:
                    if self.models[loaded_model_name]['last_loaded'] <= oldest_time:
                        oldest_model = loaded_model_name
                        oldest_time = self.models[loaded_model_name]['last_loaded']
                del self.models[oldest_model]

            self.models[model_name] = {'tokenizer': tokenizer, 'model': model, 'last_loaded': time.time()}
            return tokenizer, model

    def translate_sentences(self, sentences: List[str], source_lang: str, target_lang: str, device: str, beam_size: int = 5, **kwargs):
        model_name = 'Helsinki-NLP/opus-mt-{}-{}'.format(source_lang, target_lang)
        tokenizer, model = self.load_model(model_name)
        model.to(device)

        inputs = tokenizer(sentences, truncation=True, padding=True, max_length=self.max_length, return_tensors="pt")

        for key in inputs:
            inputs[key] = inputs[key].to(device)

        with torch.no_grad():
            translated = model.generate(**inputs, num_beams=beam_size, **kwargs)
            output = [tokenizer.decode(t, skip_special_tokens=True) for t in translated]

        return output

    def save(self, output_path):
        return {"max_loaded_models": self.max_loaded_models}

def http_get(url, path):
    """
    Downloads a URL to a given path on disc
    """
    if os.path.dirname(path) != '':
        os.makedirs(os.path.dirname(path), exist_ok=True)

    req = requests.get(url, stream=True)
    if req.status_code != 200:
        print("Exception when trying to download {}. Response {}".format(url, req.status_code), file=sys.stderr)
        req.raise_for_status()
        return

    download_filepath = path+"_part"
    with open(download_filepath, "wb") as file_binary:
        content_length = req.headers.get('Content-Length')
        total = int(content_length) if content_length is not None else None
        progress = tqdm.tqdm(unit="B", total=total, unit_scale=True)
        for chunk in req.iter_content(chunk_size=1024):
            if chunk: # filter out keep-alive new chunks
                progress.update(len(chunk))
                file_binary.write(chunk)

    os.rename(download_filepath, path)
    progress.close()

def fullname(o):
  """
  Gives a full name (package_name.class_name) for a class / object in Python. Will
  be used to load the correct classes from JSON files
  """

  module = o.__class__.__module__
  if module is None or module == str.__class__.__module__:
    return o.__class__.__name__  # Avoid reporting __builtin__
  else:
    return module + '.' + o.__class__.__name__

def import_from_string(dotted_path):
    """
    Import a dotted module path and return the attribute/class designated by the
    last name in the path. Raise ImportError if the import failed.
    """
    try:
        module_path, class_name = dotted_path.rsplit('.', 1)
    except ValueError:
        msg = "%s doesn't look like a module path" % dotted_path
        raise ImportError(msg)

    module = importlib.import_module(module_path)

    try:
        return getattr(module, class_name)
    except AttributeError:
        msg = 'Module "%s" does not define a "%s" attribute/class' % (module_path, class_name)
        raise ImportError(msg)

def fullname(o):
  """
  Gives a full name (package_name.class_name) for a class / object in Python. Will
  be used to load the correct classes from JSON files
  """

  module = o.__class__.__module__
  if module is None or module == str.__class__.__module__:
    return o.__class__.__name__  # Avoid reporting __builtin__
  else:
    return module + '.' + o.__class__.__name__

logger = logging.getLogger(__name__)

__DOWNLOAD_SERVER__ = 'http://easynmt.net/models/v2'
class EasyNMT:
    def __init__(self, model_name: str = None, cache_folder: str = None, translator=None, load_translator: bool = True,
                 device=None, max_length: int = None, **kwargs):
        """
        Easy-to-use, state-of-the-art machine translation
        :param model_name:  Model name (see Readme for available models)
        :param cache_folder: Which folder should be used for caching models. Can also be set via the EASYNMT_CACHE env. variable
        :param translator: Translator object. Set to None, to automatically load the model via the model name.
        :param load_translator: If set to false, it will only load the config but not the translation engine
        :param device: CPU / GPU device for PyTorch
        :param max_length: Max number of token per sentence for translation. Longer text will be truncated
        :param kwargs: Further optional parameters for the different models
        """
        self._model_name = model_name
        self._fasttext_lang_id = None
        
        self._lang_pairs = frozenset()

        if device is None:
            device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.device = device

        self.config = None

        if cache_folder is None:
            if 'EASYNMT_CACHE' in os.environ:
                cache_folder = os.environ['EASYNMT_CACHE']
            else:
                cache_folder = os.path.join(torch.hub._get_torch_home(), 'easynmt_v2')
        self._cache_folder = cache_folder

        if translator is not None:
            self.translator = translator
        else:
            if os.path.exists(model_name) and os.path.isdir(model_name):
                model_path = model_name
            else:
                model_name = model_name.lower()
                model_path = os.path.join(cache_folder, model_name)

                if not os.path.exists(model_path) or not os.listdir(model_path):
                    logger.info("Downloading EasyNMT model {} and saving it at {}".format(model_name, model_path))

                    model_path_tmp = model_path.rstrip("/").rstrip("\\") + "_part"
                    os.makedirs(model_path_tmp, exist_ok=True)

                    # Download easynmt.json
                    config_url = __DOWNLOAD_SERVER__ + "/{}/easynmt.json".format(model_name)
                    config_path = os.path.join(model_path_tmp, 'easynmt.json')
                    http_get(config_url, config_path)

                    with open(config_path) as fIn:
                        downloaded_config = json.load(fIn)

                    if 'files' in downloaded_config:
                        for filename, url in downloaded_config['files'].items():
                            logger.info("Download {} from {}".format(filename, url))
                            http_get(url, os.path.join(model_path_tmp, filename))

                    ##Rename tmp path
                    try:
                        os.rename(model_path_tmp, model_path)
                    except Exception:
                        pass

            with open(os.path.join(model_path, 'easynmt.json')) as fIn:
                self.config = json.load(fIn)

            if 'lang_pairs' in self.config:
                self._lang_pairs = frozenset(self.config['lang_pairs'])

            if load_translator:
                module_class = import_from_string(self.config['model_class'])
                self.translator = module_class(easynmt_path=model_path, **self.config['model_args'])
                self.translator.max_length = max_length

    def translate(self, documents: Union[str, List[str]], target_lang: str, source_lang: str = None,
                  show_progress_bar: bool = False, beam_size: int = 5, batch_size: int = 16,
                  perform_sentence_splitting: bool = True, paragraph_split: str = "\n", sentence_splitter=None,
                  document_language_detection: bool = True,
                  **kwargs):
        """
        This method translates the given set of documents
        :param documents: If documents is a string, returns the translated document as string. If documents is a list of strings, translates all documents and returns a list.
        :param target_lang: Target language for the translation
        :param source_lang: Source language for all documents. If None, determines the source languages automatically.
        :param show_progress_bar: If true, plot a progress bar on the progress for the translation
        :param beam_size: Size for beam search
        :param batch_size: Number of sentences to translate at the same time
        :param perform_sentence_splitting: Longer documents are broken down sentences, which are translated individually
        :param paragraph_split: Split symbol for paragraphs. No sentences can go across the paragraph_split symbol.
        :param sentence_splitter: Method used to split sentences. If None, uses the default self.sentence_splitting method
        :param document_language_detection: Perform language detection on document level
        :param kwargs: Optional arguments for the translator model
        :return: Returns a string or a list of string with the translated documents
        """

        # Method_args will store all passed arguments to method
        method_args = locals()
        del method_args['self']
        del method_args['kwargs']
        method_args.update(kwargs)

        if source_lang == target_lang:
            return documents

        is_single_doc = False
        if isinstance(documents, str):
            documents = [documents]
            is_single_doc = True

        if source_lang is None and document_language_detection:
            src_langs = [self.language_detection(doc) for doc in documents]

            # Group by languages
            lang2id = {}
            for idx, lng in enumerate(src_langs):
                if lng not in lang2id:
                    lang2id[lng] = []
                lang2id[lng].append(idx)

            # Translate language wise
            output = [None] * len(documents)
            for lng, ids in lang2id.items():
                logger.info("Translate documents of language: {}".format(lng))
                try:
                    method_args['documents'] = [documents[idx] for idx in ids]
                    method_args['source_lang'] = lng
                    translated = self.translate(**method_args)
                    for idx, translated_sentences in zip(ids, translated):
                        output[idx] = translated_sentences
                except Exception as e:
                    logger.warning("Exception: " + str(e))
                    raise e

            if is_single_doc and len(output) == 1:
                output = output[0]

            return output

        if perform_sentence_splitting:
            if sentence_splitter is None:
                sentence_splitter = self.sentence_splitting

            # Split document into sentences
            start_time = time.time()
            splitted_sentences = []
            sent2doc = []
            for doc in documents:
                paragraphs = doc.split(paragraph_split) if paragraph_split is not None else [doc]
                for para in paragraphs:
                    for sent in sentence_splitter(para.strip(), source_lang):
                        sent = sent.strip()
                        if len(sent) > 0:
                            splitted_sentences.append(sent)
                sent2doc.append(len(splitted_sentences))
            # logger.info("Sentence splitting done after: {:.2f} sec".format(time.time() - start_time))
            # logger.info("Translate {} sentences".format(len(splitted_sentences)))

            translated_sentences = self.translate_sentences(splitted_sentences, target_lang=target_lang,
                                                            source_lang=source_lang,
                                                            show_progress_bar=show_progress_bar, beam_size=beam_size,
                                                            batch_size=batch_size, **kwargs)

            # Merge sentences back to documents
            start_time = time.time()
            translated_docs = []
            for doc_idx in range(len(documents)):
                start_idx = sent2doc[doc_idx - 1] if doc_idx > 0 else 0
                end_idx = sent2doc[doc_idx]
                translated_docs.append(
                    self._reconstruct_document(documents[doc_idx], splitted_sentences[start_idx:end_idx],
                                               translated_sentences[start_idx:end_idx]))

            # logger.info("Document reconstruction done after: {:.2f} sec".format(time.time() - start_time))
        else:
            translated_docs = self.translate_sentences(documents, target_lang=target_lang, source_lang=source_lang,
                                                       show_progress_bar=show_progress_bar, beam_size=beam_size,
                                                       batch_size=batch_size, **kwargs)

        if is_single_doc:
            translated_docs = translated_docs[0]

        return translated_docs

    @staticmethod
    def _reconstruct_document(doc, org_sent, translated_sent):
        """
        This method reconstructs the translated document and
        keeps white space in the beginning / at the end of sentences.
        """
        sent_idx = 0
        char_idx = 0
        translated_doc = ""
        while char_idx < len(doc):
            if sent_idx < len(org_sent) and doc[char_idx] == org_sent[sent_idx][0]:
                translated_doc += translated_sent[sent_idx]
                char_idx += len(org_sent[sent_idx])
                sent_idx += 1
            else:
                translated_doc += doc[char_idx]
                char_idx += 1
        return translated_doc

    def translate_sentences(self, sentences: Union[str, List[str]], target_lang: str, source_lang: str = None,
                            show_progress_bar: bool = False, beam_size: int = 5, batch_size: int = 32, **kwargs):
        """
        This method translates individual sentences.

        :param sentences: A single sentence or a list of sentences to be translated
        :param source_lang: Source language for all sentences. If none, determines automatically the source language
        :param target_lang: Target language for the translation
        :param show_progress_bar: Show a progress bar
        :param beam_size: Size for beam search
        :param batch_size: Mini batch size
        :return: List of translated sentences
        """

        if source_lang == target_lang:
            return sentences

        is_single_sentence = False
        if isinstance(sentences, str):
            sentences = [sentences]
            is_single_sentence = True

        output = []
        if source_lang is None:
            # Determine languages for sentences
            src_langs = [self.language_detection(sent) for sent in sentences]
            logger.info("Detected languages: {}".format(set(src_langs)))

            # Group by languages
            lang2id = {}
            for idx, lng in enumerate(src_langs):
                if lng not in lang2id:
                    lang2id[lng] = []

                lang2id[lng].append(idx)

            # Translate language wise
            output = [None] * len(sentences)
            for lng, ids in lang2id.items():
                logger.info("Translate sentences of language: {}".format(lng))
                try:
                    grouped_sentences = [sentences[idx] for idx in ids]
                    translated = self.translate_sentences(grouped_sentences, source_lang=lng, target_lang=target_lang,
                                                          show_progress_bar=show_progress_bar, beam_size=beam_size,
                                                          batch_size=batch_size, **kwargs)
                    for idx, translated_sentences in zip(ids, translated):
                        output[idx] = translated_sentences
                except Exception as e:
                    logger.warning("Exception: " + str(e))
                    raise e
        else:
            # Sort by length to speed up processing
            length_sorted_idx = np.argsort([-len(sen) for sen in sentences])
            sentences_sorted = [sentences[idx] for idx in length_sorted_idx]

            iterator = range(0, len(sentences_sorted), batch_size)
            if show_progress_bar:
                scale = min(batch_size, len(sentences))
                iterator = tqdm.tqdm(iterator, total=len(sentences) / scale, unit_scale=scale, smoothing=0)

            for start_idx in iterator:
                output.extend(self.translator.translate_sentences(sentences_sorted[start_idx:start_idx + batch_size],
                                                                  source_lang=source_lang, target_lang=target_lang,
                                                                  beam_size=beam_size, device=self.device, **kwargs))

            # Restore original sorting of sentences
            output = [output[idx] for idx in np.argsort(length_sorted_idx)]

        if is_single_sentence:
            output = output[0]

        return output

    def start_multi_process_pool(self, target_devices: List[str] = None):
        """
        Starts multi process to process the encoding with several, independent processes.
        This method is recommended if you want to encode on multiple GPUs. It is advised
        to start only one process per GPU. This method works together with encode_multi_process
        :param target_devices: PyTorch target devices, e.g. cuda:0, cuda:1... If None, all available CUDA devices will be used
        :return: Returns a dict with the target processes, an input queue and and output queue.
        """
        if target_devices is None:
            if torch.cuda.is_available():
                target_devices = ['cuda:{}'.format(i) for i in range(torch.cuda.device_count())]
            else:
                logger.info("CUDA is not available. Start 4 CPU worker")
                target_devices = ['cpu'] * 4

        logger.info("Start multi-process pool on devices: {}".format(', '.join(map(str, target_devices))))

        ctx = mp.get_context('spawn')
        input_queue = ctx.Queue()
        output_queue = ctx.Queue()
        processes = []

        for cuda_id in target_devices:
            p = ctx.Process(target=EasyNMT._encode_multi_process_worker,
                            args=(cuda_id, self, input_queue, output_queue), daemon=True)
            p.start()
            processes.append(p)

        return {'input': input_queue, 'output': output_queue, 'processes': processes}

    def translate_multi_process(self, pool: Dict[str, object], documents: List[str], show_progress_bar: bool = True,
                                chunk_size: int = None, **kwargs) -> List[str]:
        """
        This method allows to run encode() on multiple GPUs. The sentences are chunked into smaller packages
        and sent to individual processes, which encode these on the different GPUs. This method is only suitable
        for encoding large sets of sentences
        :param pool: A pool of workers started with SentenceTransformer.start_multi_process_pool
        :param chunk_size: Sentences are chunked and sent to the individual processes. If none, it determine a sensible size.
        """

        if chunk_size is None:
            chunk_size = min(math.ceil(len(documents) / len(pool["processes"]) / 10), 1000)

        logger.info("Chunk data into packages of size {}".format(chunk_size))

        input_queue = pool['input']
        last_chunk_id = 0

        for start_idx in range(0, len(documents), chunk_size):
            input_queue.put([last_chunk_id, documents[start_idx:start_idx + chunk_size], kwargs])
            last_chunk_id += 1

        output_queue = pool['output']
        results_list = sorted([output_queue.get() for _ in
                               tqdm.tqdm(range(last_chunk_id), total=last_chunk_id, unit_scale=chunk_size, smoothing=0,
                                         disable=not show_progress_bar)], key=lambda chunk: chunk[0])
        translated = []
        for chunk in results_list:
            translated.extend(chunk[1])
        return translated

    def translate_stream(self, stream: Iterable[str], show_progress_bar: bool = True, chunk_size: int = 128,
                         **kwargs) -> List[str]:
        batch = []
        for doc in tqdm.tqdm(stream, smoothing=0.0, disable=not show_progress_bar):
            batch.append(doc)

            if len(batch) >= chunk_size:
                translated = self.translate(batch, show_progress_bar=False, **kwargs)
                for trans_doc in translated:
                    yield trans_doc
                batch = []

        if len(batch) > 0:
            translated = self.translate(batch, show_progress_bar=False, **kwargs)
            for trans_doc in translated:
                yield trans_doc

    @staticmethod
    def stop_multi_process_pool(pool):
        """
        Stops all processes started with start_multi_process_pool
        """
        for p in pool['processes']:
            p.terminate()

        for p in pool['processes']:
            p.join()
            p.close()

        pool['input'].close()
        pool['output'].close()

    @staticmethod
    def _encode_multi_process_worker(target_device: str, model, input_queue, results_queue):
        """
        Internal working process to encode sentences in multi-process setup
        """
        model.device = target_device
        while True:
            try:
                id, documents, kwargs = input_queue.get()
                translated = model.translate(documents, **kwargs)
                results_queue.put([id, translated])
            except queue.Empty:
                break

    def language_detection(self, text: Union[str, List[str]]) -> str:
        """
       Given a text, detects the language code and returns the ISO language code.
       It test different language detectors, based on what is available:
       fastText, langid, langdetect.

       You can change the language detector order by changing model._lang_detectors
       :param text: Text or a List of Texts for which we want to determine the language
       :return: ISO language code
       """
        if isinstance(text, list):
            return [self.language_detection(doc) for doc in text]

        for lang_detector in self._lang_detectors:
            try:
                return lang_detector(text)
            except:
                pass

        raise Exception(
            "No method for automatic language detection was found. Please install at least one of the following: fasttext (pip install fasttext), langid (pip install langid), or langdetect (pip install langdetect)")

    def language_detection_fasttext(self, text: str) -> str:
        """
        Given a text, detects the language code and returns the ISO language code. It supports 176 languages. Uses
        the fasttext model for language detection:
        https://fasttext.cc/blog/2017/10/02/blog-post.html
        https://fasttext.cc/docs/en/language-identification.html


        """
        if self._fasttext_lang_id is None:
            import fasttext
            fasttext.FastText.eprint = lambda \
                x: None  # Silence useless warning: https://github.com/facebookresearch/fastText/issues/1067
            model_path = os.path.join(self._cache_folder, 'lid.176.ftz')
            if not os.path.exists(model_path):
                http_get('https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.ftz', model_path)
            self._fasttext_lang_id = fasttext.load_model(model_path)

        return \
        self._fasttext_lang_id.predict(text.lower().replace("\r\n", " ").replace("\n", " ").strip())[0][0].split('__')[
            -1]



    @property
    def lang_pairs(self) -> FrozenSet[str]:
        """
        Returns all allowed languages directions for the loaded model
        """
        return self._lang_pairs

    def get_languages(self, source_lang: str = None, target_lang: str = None) -> List[str]:
        """
        Returns all available languages supported by the model
        :param source_lang:  If not None, then returns all languages to which we can translate for the given source_lang
        :param target_lang:  If not None, then returns all languages from which we can translate for the given target_lang
        :return: Sorted list with the determined languages
        """

        langs = set()
        for lang_pair in self.lang_pairs:
            source, target = lang_pair.split("-")

            if source_lang is None and target_lang is None:
                langs.add(source)
                langs.add(target)
            elif target_lang is not None and target == target_lang:
                langs.add(source)
            elif source_lang is not None and source == source_lang:
                langs.add(target)

        return sorted(list(langs))

    def save(self, output_path):
        os.makedirs(output_path, exist_ok=True)

        filepath = os.path.join(output_path, 'easynmt.json')

        config = {
            'model_class': fullname(self.translator),
            'lang_pairs': list(self.lang_pairs),
            'model_args': self.translator.save(output_path)
        }

        with open(filepath, 'w') as fOut:
            json.dump(config, fOut)




#///////////////////////////////////////////////////////////////////////////////////////
model = EasyNMT('opus-mt')

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.get("/")
def translate_get(target_lang: str, text: List[str] = Query([]), source_lang: Optional[str] = None):
  return model.translate(text, target_lang=target_lang, source_lang=source_lang)

@app.post("/")
async def translate_post(request: Request):
    data = await request.json()
    return translate_get(**data)

ngrok_tunnel = ngrok.connect(8000)
print("REST API started")
print("Your public API URL:", ngrok_tunnel.public_url)
print("You can for example open the following URL in your browser: {}?target_lang=en&text=Hallo%20Welt".format(ngrok_tunnel.public_url))

nest_asyncio.apply()
uvicorn.run(app, port=8000)