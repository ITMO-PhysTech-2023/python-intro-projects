import random


class LetterProvider:
    def get_next_letter(self) -> str:
        pass


class RandomLetterProvider(LetterProvider):
    def get_next_letter(self) -> str:
        return chr(random.randint(ord('a'), ord('z')))


class SecretLetterProvider(LetterProvider):
    def get_next_letter(self) -> str:
        return create_secret()[random.randint(0, len(create_secret())-1)]


def create_secret():
    return 'cat'

#
# class SnakeLetterProvider(LetterProvider):
#     def check_chosen_letter(self):
#
#     def get_next_letter(self):
#         return chr(self.letter)
