import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup
import json

def paraphraze(input_text):
    url = "https://bionic-reading1.p.rapidapi.com/convert"

    payload = {
        "content": input_text,
        "response_type": "html",
        "request_type": "html",
        "fixation": "1",
        "saccade": "10"
    }
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "X-RapidAPI-Key": "27288b43b9mshc4ba4819fb451c0p1b4611jsn8f9b4dd58d8d",
        "X-RapidAPI-Host": "bionic-reading1.p.rapidapi.com"
    }

    response = requests.post(url, data=payload, headers=headers)

    soup = BeautifulSoup(response.text, features="html.parser")

    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()    # rip it out

    # get text
    text = soup.get_text()

    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)

    return text


def summarize(input_text):

    url = "https://summarize-texts.p.rapidapi.com/pipeline"

    payload = { "input": translate(input_text, 'ru', 'en') }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "27288b43b9mshc4ba4819fb451c0p1b4611jsn8f9b4dd58d8d",
        "X-RapidAPI-Host": "summarize-texts.p.rapidapi.com"
    }

    response = requests.post(url, json=payload, headers=headers)
    
    return translate(response.json()['output'][0]['text'], 'en', 'ru')
'''
def translate(input_text):

    url = "https://google-translate1.p.rapidapi.com/language/translate/v2"

    payload = {
        "q": input_text,
        "target": "ru",
        "source": "en"
    }
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "Accept-Encoding": "application/gzip",
        "X-RapidAPI-Key": "27288b43b9mshc4ba4819fb451c0p1b4611jsn8f9b4dd58d8d",
        "X-RapidAPI-Host": "google-translate1.p.rapidapi.com"
    }

    response = requests.post(url, data=payload, headers=headers)

    return response.json()['data']['translations'][0]['translatedText']
'''

def translate(input_text, orig_lang, target_lang):
    url = "https://translate-plus.p.rapidapi.com/translate"

    payload = {
        "text": input_text,
        "source": orig_lang,
        "target": target_lang
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "27288b43b9mshc4ba4819fb451c0p1b4611jsn8f9b4dd58d8d",
        "X-RapidAPI-Host": "translate-plus.p.rapidapi.com"
    }

    response = requests.post(url, json=payload, headers=headers)

    return response.json()['translations']['translation']
#print(summarize('Hello!'))
#print(translate('Текст (от лат. textus — ткань; сплетение, сочетание) — зафиксированная на каком-либо материальном носителе человеческая мысль; в общем плане связная и полная последовательность символов.', 'ru', 'en'))

