import random


class LetterProvider:
    def get_next_letter(self) -> str:
        pass


class KeyboardLetterProvider(LetterProvider):
    def get_next_letter(self) -> str:
        return input('Enter next letter: ')


class RandomLetterProvider(LetterProvider):
    def get_next_letter(self) -> str:
        return chr(random.randint(ord('a'), ord('z')))
