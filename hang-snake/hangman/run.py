import time
from common.util import clear_terminal
from hangman.provider import LetterProvider, KeyboardLetterProvider, RandomLetterProvider
from printer.secret import Secret




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
    def print(self):
        for row in self.matrix:
            print(''.join(row))
        print()

    def add_human_part(self):
        row, col = HUMAN[-self.remaining_fails]
        self.remaining_fails -= 1
        self.matrix[row][col] = FINAL_FIELD[row][col]


class HangmanGame:
    def __init__(self, letter_provider: LetterProvider, secrword: Secret, step_sleep: int, let):
        self.field = Field()
        self.step_sleep = step_sleep
        self.provider = letter_provider
        self.secret = secrword.create_secret()
        self.guessed = ['_' for _ in range(len(self.secret))]
        self.red = (255, 0, 0)
        self.let = let
        self.count = 0
    def read_guess(self) -> str:
        while True:
            letter = self.let[self.count]
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

    def show(self):
        clear_terminal()
        self.field.print()
        print(''.join(self.guessed))

    def run(self):
        #game_over = False
        self.show()
        for t in range(len(self.let)):
            self.step()
            if self.is_won():
                self.show()
                print('Cool! You won!')
                # break
            if self.is_lost():
                 self.show()
                 print('Wow, you lost! Sad :(')
                 # break
            self.show()
            self.count+=1
provider = RandomLetterProvider()
secr = Secret()
#game = HangmanGame(provider, secr,1)
#game.run()