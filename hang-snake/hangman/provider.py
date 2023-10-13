import random
from abc import ABC, abstractmethod
from queue import Queue


class LetterProvider(ABC):
    @abstractmethod
    def get_next_letter(self) -> str:
        pass


class KeyboardLetterProvider(LetterProvider):
    def get_next_letter(self) -> str:
        return input('Enter next letter: ')


class RandomLetterProvider(LetterProvider):
    def get_next_letter(self) -> str:
        return chr(random.randint(ord('a'), ord('z')))


class QueueProvider(LetterProvider):
    def __init__(self):
        self.queue = Queue()

    def add_letter(self, letter: str):
        self.queue.put(letter)

    def get_next_letter(self) -> str:
        return self.queue.get()
