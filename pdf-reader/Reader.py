import enum
import os
import typing
from PyPDF2 import PdfReader



class HookType(enum.Enum):
    ON_SELECT = 'on-select'
    ON_CLICK = 'on-click'


class HookAction(enum.Enum):
    STORE = 'store'
    CALLBACK = 'callback'


class Reader:
    def __init__(self, filename: str | os.PathLike):
        self.filename = filename
        
        reader = PdfReader(self.filename)
        self.text = ''
        for i in range(len(reader.pages)):
            page = reader.pages[i]
            self.text += page.extract_text()

        self._hooks: list[tuple[HookType, HookAction, typing.Any]] = []

    def hook_store(self, _type: HookType, name: str):
        self._hooks.append((_type, HookAction.STORE, name))

    def hook_callback(self, _type: HookType, callback: typing.Callable):
        self._hooks.append((_type, HookAction.CALLBACK, callback))

    def _store(self, name: str, value: typing.Any):
        setattr(self, name, value)

    def return_pdf_text(self):
        return self.text

    def run(self):
        pass
        
          # TODO реализовать создание окна и поддержку хуков


def read_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ''
    for page in reader.pages:
        text += page.extract_text()
    return text


