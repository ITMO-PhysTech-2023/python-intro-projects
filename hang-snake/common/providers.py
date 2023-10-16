import random
from queue import Queue


class LetterProvider:
    def get_next_letter(self) -> str:
        pass


class RandomLetterProvider(LetterProvider):
    def get_next_letter(self) -> str:
        return chr(random.randint(ord('a'), ord('z')))


class SecretLetterProvider(LetterProvider):
    def get_next_letter(self) -> str:
        return create_secret()[random.randint(0, len(create_secret())-1)]


def create_secret() -> str:
    english_words = ['capybara', 'elephant', 'giraffe', 'chimpanzee', 'horse', 'monkey', 'scorpion',
                      'chicken', 'jaguar', 'chameleon', 'crocodile']
    return english_words[random.randint(0, len(english_words) - 1)]


class QueueProvider(LetterProvider):
    def __init__(self):
        self.queue = Queue()

    def add_letter(self, letter: str):
        self.queue.put(letter)

    def get_next_letter(self) -> str:
        return self.queue.get()
