import time

from common.printer import DefaultPrinter, Printer
from hangman.provider import KeyboardLetterProvider, LetterProvider, RandomLetterProvider


def create_secret():
    return 'cat'


FINAL_FIELD = r'''
   +----+
   |    |
   o    |
  /|\   |
  / \   |
_______/|\_
'''.split('\n')

HUMAN = [
    (3, 3),
    (4, 3),
    (4, 2),
    (4, 4),
    (5, 2),
    (5, 4)
]
HUMAN_PARTS = len(HUMAN)


class Field:
    def __init__(self):
        self.remaining_fails = HUMAN_PARTS
        self.matrix = [
            list(row)
            for row in FINAL_FIELD
        ]
        for row, col in HUMAN:
            self.matrix[row][col] = ' '

    @property
    def width(self):
        return max([len(row) for row in FINAL_FIELD])

    def add_human_part(self):
        row, col = HUMAN[-self.remaining_fails]
        self.remaining_fails -= 1
        self.matrix[row][col] = FINAL_FIELD[row][col]


class HangmanGame:
    def __init__(
            self,
            letter_provider: LetterProvider, step_sleep: float,
            printer: Printer
    ):
        self.field = Field()
        self.step_sleep = step_sleep
        self.provider = letter_provider
        self.printer = printer
        self.secret = create_secret()
        self.guessed = ['_' for _ in range(len(self.secret))]

    def read_guess(self) -> str:
        while True:
            letter = self.provider.get_next_letter().lower()
            if len(letter) != 1 and ord(letter) < ord('a') or ord(letter) > ord('z'):
                print('Invalid guess! Try again (enter a letter)')
                continue
            return letter

    def check_guess(self, letter: str):
        if letter in self.secret:
            for i in range(len(self.secret)):
                if self.secret[i] == letter:
                    self.guessed[i] = letter
        else:
            self.field.add_human_part()

    def is_won(self) -> bool:
        return '_' not in self.guessed

    def is_lost(self) -> bool:
        return self.field.remaining_fails == 0

    def step(self):
        letter = self.read_guess()
        self.check_guess(letter)
        time.sleep(self.step_sleep)

    def build_matrix(self):
        delta = self.field.width - len(self.guessed)
        last_row = [' ' for _ in range(delta // 2)] + self.guessed
        out = self.field.matrix + [
            [],
            last_row
        ]
        return out

    def status(self):
        if self.is_won():
            return 'Cool! You won!'
        if self.is_lost():
            return 'You lost :('

    def print(self):
        extra_lines = []
        if (status := self.status()) is not None:
            extra_lines.append(status)
        matrix = self.build_matrix()
        for line in extra_lines:
            matrix += [list(line)]
        self.printer.print_field(matrix)

    def run(self):
        self.print()
        while True:
            self.step()
            self.print()
            if self.status() is not None:
                self.print()
                break


if __name__ == '__main__':
    # provider = RandomLetterProvider()
    provider = KeyboardLetterProvider()
    printer = DefaultPrinter()
    # printer = ReversePrinter()
    game = HangmanGame(provider, 0.5, printer)
    game.run()
