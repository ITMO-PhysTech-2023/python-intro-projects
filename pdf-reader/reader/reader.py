import enum
import os
import typing


class HookType(enum.Enum):
    ON_SELECT = 'on-select'
    ON_CLICK = 'on-click'


class HookAction(enum.Enum):
    STORE = 'store'
    CALLBACK = 'callback'


class Reader:
    def __init__(self, filename: str | os.PathLike):
        self.filename = filename
        with open(filename, 'rb') as file:
            self.content = ...
        self._hooks: list[tuple[HookType, HookAction, typing.Any]] = []

    def hook_store(self, _type: HookType, name: str):
        self._hooks.append((_type, HookAction.STORE, name))

    def hook_callback(self, _type: HookType, callback: typing.Callable):
        self._hooks.append((_type, HookAction.CALLBACK, callback))

    def _store(self, name: str, value: typing.Any):
        setattr(self, name, value)

    def run(self):
        pass  # TODO реализовать создание окна и поддержку хуков
