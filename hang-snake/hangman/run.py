from common.util import clear_terminal

from common.providers import create_secret
from common.providers import LetterProvider


class Hangmangame:
    def __init__(self):
        self.word = create_secret()
        self.n = len(self.word)
        self.guessed = ['_' for _ in range(self.n)]
        from hangman.FIELD import FIELD
        self.field = FIELD
        self.number_of_errors = 0
        self.MAX_ERRORS = 10

    def read_guess(self, letter) -> str:
        while True:
            if len(letter) != 1 and ord(letter) < ord('a') or ord(letter) > ord('z'):
                print('Invalid guess! Try again (enter a letter)')
                continue
            return letter

    def check_guess(self, letter: str):
        if letter in self.word:
            new = ""
            for i in range(len(self.word)):  # ищем место буквы в слове
                if letter == self.word[i]:
                    new += letter
                else:
                    new += self.guessed[i]
            self.guessed = new
        else:
            print('There is no such letter in word.')
            self.number_of_errors += 1

    def check_possibility(self):
        while True:
            if self.guessed != self.word and\
               self.number_of_errors < self.MAX_ERRORS:
                return

    def is_won(self) -> bool:
        return self.guessed == self.word

    def is_lost(self) -> bool:
        return self.MAX_ERRORS == self.number_of_errors

    def step(self):
        letter = self.read_guess()
        self.check_guess(letter)

    def show(self):
        clear_terminal()
        print(''.join(self.guessed))
        print(self.field[self.number_of_errors])

    def run(self):
        self.show()
        while True:
            self.check_possibility()
            self.step()
            if self.is_won():
                self.show()
                print("Congratulations!The word was", self.word)
                break
            if self.is_lost():
                self.show()
                print("Game over")
                break
            self.show()
