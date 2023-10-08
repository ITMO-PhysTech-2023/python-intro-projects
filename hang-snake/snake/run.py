from pynput import keyboard
import time
import os
from random import randint
from common.providers import LetterProvider, RandomLetterProvider
from common.rules import first_message, wrong_input, rules


class Snakegame:
    def __init__(self, letter_provider: LetterProvider):
        self.WIDTH = 30
        self.HEIGHT = 15
        self.snake = [(5, self.HEIGHT // 2), (4, self.HEIGHT // 2), (3, self.HEIGHT // 2)]
        self.apples = [(14, 7), (10, 7), (21, 7), (12, 12), (18, 3)]
        self.special_apple = []
        self.CELLS = [(col, row) for row in range(self.HEIGHT) for col in range(self.WIDTH)]
        self.eat = False
        self.flag_end = False
        self.direction = (1, 0)
        self.provider = letter_provider
        self.letters_eaten = []
        self.letters_on_field = ['a', 'a', 'a', 'a', 'a']
        self.special_letter =
        self.letters_counter = 0

    def random_position(self):
        while True:
            x = randint(0, self.WIDTH-1)
            y = randint(0, self.HEIGHT-1)
            if (x, y) not in self.snake and (x, y) not in self.apples:
                return x, y

    def apple_random(self):
        for i in range(4):
            if self.apples[i] == self.snake[0]:
                self.apples[i] = self.random_position()
                self.eat = True
                self.letters_counter += 1
                self.letters_eaten.append(self.letters_on_field[i])

    def create_field_matrix(self):
        matrix = []
        for row in range(self.HEIGHT):
            if row == 0 or row == self.HEIGHT - 1:
                matrix.append(['+' for _ in range(self.WIDTH)])
            else:
                matrix.append(['+'] + [' ' for _ in range(self.WIDTH - 2)] + ['+'])
        return matrix

    def print_snake_and_apples(self, matrix):
        for y, row in enumerate(matrix):
            for x, char in enumerate(row):
                if (x, y) in self.snake:
                    print('■', end='')
                elif (x, y) in self.apples:
                    print(self.letters_on_field[self.apples.index((x, y))], end='')
                elif (x, y) in self.special_apple:
                    print(self.special_letter, end='')
                else:
                    print(char, end='')
            print('')

    def snake_move(self):
        head_snake = self.snake[0][0] + self.direction[0], self.snake[0][1] + self.direction[1]
        self.snake.insert(0, head_snake)
        if not self.eat:
            self.snake.pop()
        else:
            self.eat = False

    def make_move(self):
        return self.letters_counter == 3

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
                self.flag_end = True

    def is_lost(self) -> bool:
        return self.snake[0][0] in (0, self.WIDTH) or\
                self.snake[0][1] in (0, self.HEIGHT) or\
                self.snake[0] in self.snake[1:] or self.flag_end

    def run(self):
        with keyboard.Listener(on_press=self.process_press):
            print(first_message)
            start = int(input())
            if start == 1:
                while True:
                    os.system('cls')
                    self.print_snake_and_apples(self.create_field_matrix())
                    self.apple_random()
                    self.snake_move()
                    if self.is_lost():
                        os.system('cls')
                        print('Game Over')
                        break
                    elif self.make_move():
                        self.letters_counter = 0
                        for i in range(4):
                            self.letters_on_field[i] = self.provider.get_next_letter().lower()
                        if self.letters_eaten == ['a', 'a', 'a']:
                            print(rules)
                            resume = int(input())
                            self.apples.remove(18, 3)
                            self.letters_on_field.pop()
                            if resume == 1:
                                continue
                            else:
                                print(wrong_input)


                    time.sleep(0.3)
            else:
                print(wrong_input)


provider = RandomLetterProvider()
game = Snakegame(provider)

game.run()
# self.letters_on_field[i] = self.provider.get_next_letter().lower()