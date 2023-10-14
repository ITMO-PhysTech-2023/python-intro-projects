from typing import Callable
from pynput import keyboard
import time
from random import randint
from common.providers import LetterProvider, RandomLetterProvider, SecretLetterProvider
from common.rules import first_message, wrong_input, rules
from common.printer import DefaultPrinter, Printer
from common.util import clear_terminal
import os


class Snake:
    SNAKE = '■'

    def __init__(self, initial_cell: tuple[int, int]):
        self.cells = [initial_cell]

    def snake_step(self, direction):
        head_snake = self.cells[0][0] + direction[0], self.cells[0][1] + direction[1]
        self.cells.insert(0, head_snake)

    def draw_on(self, matrix: list[list[str]]):
        for row, col in self.cells:
            matrix[row][col] = Snake.SNAKE


class Field:
    EMPTY = ' '

    def __init__(self,
                 letter_provider1: LetterProvider,
                 letter_provider2: LetterProvider):
        self.HEIGHT = 30
        self.WIDTH = 15
        self.snake = Snake(tuple((self.WIDTH // 8, self.HEIGHT // 2)))
        self.apples = [(self.WIDTH // 2, self.HEIGHT // 2),
                       (3*self.WIDTH // 4, self.HEIGHT // 2),
                       (5*self.WIDTH // 8, self.HEIGHT // 2),
                       (self.WIDTH // 2, self.HEIGHT // 4),
                       (self.WIDTH // 2, 3*self.HEIGHT // 4)]
        self.hangman_apple = []

        self.letters_on_field = ['a', 'a', 'a', 'a', 'a']
        self.letters_eaten = []
        self.hangman_letter_on_field = None

        self.eat = False
        self.letters_counter = 0

        self.provider_random = letter_provider1
        self.provider_hangman = letter_provider2

    def random_position(self):
        while True:
            position = [randint(2, self.WIDTH-2), randint(2, self.HEIGHT-2)]
            if position not in self.snake and position not in self.apples and position not in self.hangman_apple:
                return position

    def generate_hangman_apple(self):
        if self.hangman_apple == self.snake.cells[0]:
            self.letters_counter += 1
            self.eat = True
            self.hangman_apple = self.random_position()
            self.letters_eaten.append(self.hangman_letter_on_field)
            self.hangman_letter_on_field = self.provider_hangman.get_next_letter()

    def generate_apples_start(self):
        for i in range(4):
            if self.apples[i] == self.snake.cells[0]:
                self.eat = True
                self.letters_counter += 1
                self.letters_eaten.append(self.letters_on_field[i])
                self.apples[i] = self.random_position()

    def generate_apples_game(self):
        for i in range(4):
            if self.apples[i] == self.snake.cells[0]:
                self.eat = True
                self.letters_counter += 1
                self.letters_eaten.append(self.letters_on_field[i])
                self.apples[i] = self.random_position()
                self.letters_on_field[i] = self.provider_random.get_next_letter()

    def move_snake(self, direction: tuple[int, int]):
        self.snake.snake_step(direction)
        if not self.eat:
            self.snake.cells.pop()
        else:
            self.eat = False

    def is_lost(self) -> bool:
        return self.snake.cells[0][0] in (0, self.WIDTH) or\
                self.snake.cells[0][1] in (0, self.HEIGHT) or\
                self.snake.cells[0] in self.snake[1:]

    def delete_apple(self):
        self.apples.pop()

    def counter(self):
        return self.letters_counter

    def return_eaten(self):
        return self.letters_eaten

    def clear_eaten(self):
        self.letters_eaten = []

    def build_matrix(self):
        matrix = [
            [Field.EMPTY for _ in range(self.WIDTH)]
            for _2 in range(self.HEIGHT)
        ]
        self.snake.draw_on(matrix)
        for i in range(4):
            row, col = self.apples[i]
            matrix[row][col] = self.letters_on_field[i]
        for row, col in self.hangman_apple:
            matrix[row][col] = self.hangman_letter_on_field

        return matrix


class Snakegame:
    def __init__(self, printer: Printer):

        self.field = Field(RandomLetterProvider(), SecretLetterProvider())
        self.direction = (1, 0)
        self.printer = printer

        self.index_letter = None
        self.chosen_letter = None
        self.callbacks = []

        self.flag_end = False
        self.game = 1

    def choose_letter(self):
        self.index_letter = int(input()) - 1
        if self.index_letter <= 2:
            self.chosen_letter = self.field.return_eaten()[self.index_letter]
            for callback in self.callbacks:
                callback()
            return self.chosen_letter
        else:
            print(wrong_input)

    def add_object_eaten_callback(self, callback: Callable[[str], ...]):
        self.callbacks.append(callback)

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

    def start_rules(self) -> int:
        print(rules)
        resume = int(input())
        return resume

    def step_start(self):
        self.field.move_snake(self.direction)
        self.field.generate_apples_start()

    def step_game(self):
        self.field.move_snake(self.direction)
        self.field.generate_apples_game()

    def messages(self):
        if self.field.is_lost():
            return 'Game Over'
        if self.game == 2 and self.field.counter() == 3:
            return ('Eaten letters: ', ', '.join(self.field.return_eaten()),
                    'Enter the number of the letter you selected')

    def print(self):
        extra_lines = []
        if (message := self.messages()) is not None:
            extra_lines.append(message)
        matrix = self.field.build_matrix()
        for line in extra_lines:
            matrix += [list(line)]
        self.printer.print_field(matrix)

    def run(self):
        with keyboard.Listener(on_press=self.process_press):
            print(first_message)
            start = int(input())
            if start == 1:
                while True:
                    clear_terminal()
                    while self.game == 1:
                        self.step_start()
                        self.print()
                        if self.field.counter() == 3:
                            self.field.delete_apple()
                            if self.start_rules() == 1:
                                self.field.clear_eaten()
                                self.game += 1
                            else:
                                print(wrong_input)
                                continue
                    while self.game == 2:
                        self.step_game()
                        self.print()
                        if self.field.counter() == 3:
                            self.choose_letter()
                            self.field.clear_eaten()
                    time.sleep(0.3)
            else:
                print(wrong_input)


if __name__ == '__main__':
    printer = DefaultPrinter()
    game = Snakegame(printer)
    game.run()
