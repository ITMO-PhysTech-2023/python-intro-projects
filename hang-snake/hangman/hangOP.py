import time
from common.util import clear_terminal
def create_secret():
    return 'capybara'
SECRET = create_secret()
n = len(SECRET)
GUESSED = ['_' for _ in range(n)]
FINAL_FIELD = r'''
   +----+
   |    |
   o    |
  /|\   |
  / \   |
_______/|\_
'''.split('\n')
FIELD = FINAL_FIELD
HUMAN = [
    (3, 3),
    (4, 3),
    (4, 2),
    (4, 4),
    (5, 2),
    (5, 4)
]

human_parts = 0
ch = 0
chasti_tela = ['o', '|', '/', '\\', '/', '\\']

class Field2:
    def __init__(self):
        self.humpar = human_parts
        self.FIELD = [
            list(row)
            for row in FINAL_FIELD
        ]
        for cell in HUMAN:
            self.FIELD[cell[0]][cell[1]] = ' ' # закрасил человечка пустыми клетками

    def print(self):
        for i in self.FIELD:
            print(''.join(i))
        print()

    def add_human_part(self):
        a, b = HUMAN[self.humpar]
        self.FIELD[a][b] = FINAL_FIELD[a][b]
        self.humpar += 1


class HangmanGame:
    def __init__(self, step_sleep: float, life_count: int):
        self.field = Field2()
        self.life_count = life_count
        self.step_sleep = step_sleep
        self.secret = create_secret()
        self.ch=ch
        self.chasti=chasti_tela
        self.guessed = ['_' for _ in range(len(self.secret))]
    def check_guess(self, letter:str):
        if letter in self.secret:
            for i in range(len(self.secret)):
                if self.secret[i] == letter:
                    self.guessed[i] = letter
        else:
            if self.field!=self.final_field:
                self.field.add_human_part()

    def if_won(self) -> bool:
        return '_' not in self.guessed

    def if_lose(self) -> bool:
        return self.field==self.final_field

    def step(self):
        if self.field!=self.final_field:
            letter = input('Enter your guess: ')
        self.check_guess(letter)
        time.sleep(self.step_sleep)

    def show(self):
        clear_terminal()
        self.field.print()
        print(''.join(self.guessed))

    def run(self):
        self.show()
        self.final_field=FINAL_FIELD
        while True:
            self.step()
            if self.if_won():
                self.show()
                print('You won')
                break
            if self.if_lose():
                self.show()
                print('You lose!')
                break
            self.show()
game = HangmanGame(0.5)
game.run()

