from pynput import keyboard
import time
import os
from random import randint
from common.run import LetterProvider, RandomLetterProvider


class Snakegame:
    def __init__(self, letter_provider: LetterProvider):
        self.WIDTH = 30
        self.HEIGHT = 15
        self.CELLS = [(col, row) for row in range(self.HEIGHT) for col in range(self.WIDTH)]
        self.snake = [(5, self.HEIGHT // 2), (4, self.HEIGHT // 2), (3, self.HEIGHT // 2)]
        self.apple = self.random_position()
        self.eat = False
        self.flag = False
        self.direction = (1, 0)
        self.provider = letter_provider
        self.letter = 'a'

    def random_position(self):
        row = randint(1, self.HEIGHT - 2)
        col = randint(1, self.WIDTH - 2)
        while (col, row) in self.snake:
            row = randint(1, self.HEIGHT - 2)
            col = randint(1, self.WIDTH - 2)
        return col, row

    def apple_random(self):
        if self.apple == self.snake[0]:
            self.apple = self.random_position()
            self.eat = True
            self.letter = self.provider.get_next_letter().lower()

    def print_field(self):
        for cell in self.CELLS:
            if cell in self.snake:
                print('s', end='')
            elif cell[0] in (0, self.WIDTH - 1):
                print('|', end='')
            elif cell[1] in (0, self.HEIGHT - 1):
                print('_', end='')
            elif cell == self.apple:
                print(self.letter, end='')
            else:
                print(' ', end='')

            if cell[0] == self.WIDTH - 1:
                print('')

    def snake_move(self):
        head_snake = self.snake[0][0] + self.direction[0], self.snake[0][1] + self.direction[1]
        self.snake.insert(0, head_snake)
        if not self.eat:
            self.snake.pop()
        else:
            self.eat = False

    def process_press(self, key):
        match key:
            case keyboard.Key.left:
                self.direction = (-1, 0)
            case keyboard.Key.up:
                self.direction = (0, -1)
            case keyboard.Key.right:
                self.direction = (1, 0)
            case keyboard.Key.down:
                self.direction = (0, 1)
            case keyboard.Key.esc:
                self.flag = True

    def is_lost(self) -> bool:
        return self.snake[0][0] in (0, self.WIDTH) or\
                self.snake[0][1] in (0, self.HEIGHT) or\
                self.snake[0] in self.snake[1:] or self.flag

    def run(self):
        with keyboard.Listener(on_press=self.process_press) as listener:
            while True:
                os.system('cls')
                self.print_field()
                self.apple_random()
                self.snake_move()
                if self.is_lost():
                    os.system('cls')
                    print('Game Over')
                    break
                time.sleep(0.3)


provider = RandomLetterProvider()
game = Snakegame(provider)
game.run()
