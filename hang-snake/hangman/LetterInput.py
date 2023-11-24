import random
from abc import abstractmethod


class Letter_Input:
    @abstractmethod
    def input_letter(self):
        pass


class LetterInputByHands(Letter_Input):
    def input_letter(self):
        return input('enter letter: ').lower()


class LetterInputByRandom(Letter_Input):
    def input_letter(self):
        return chr(random.randint(ord('a'), ord('z')))
