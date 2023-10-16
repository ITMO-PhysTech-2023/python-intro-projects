from typing import Callable
from pynput import keyboard
import time
from random import randint
from common.providers import LetterProvider, RandomLetterProvider, SecretLetterProvider
from common.rules import first_message, wrong_input, rules
from common.printer import DefaultPrinter, Printer
from common.util import clear_terminal


class Snake:
    SNAKE = '■'

    def __init__(self, initial_cell: tuple[int, int]):
        self.cells = [initial_cell]

    def snake_step(self, direction):
        head_snake = self.cells[0][0] + direction[0], self.cells[0][1] + direction[1]
        self.cells.insert(0, head_snake)

    def fix_to_bounds(self, height: int, width: int):
        row, col = self.cells[0]
        self.cells[0] = (row % height, col % width)

    def snake_die(self):
        return self.cells[0] in self.cells[1:]

    def draw_on(self, matrix: list[list[str]]):
        for row, col in self.cells:
            matrix[row][col] = Snake.SNAKE


class Field:
    EMPTY = '.'

    def __init__(self,
                 letter_provider1: LetterProvider,
                 letter_provider2: LetterProvider):
        self.HEIGHT = 20
        self.WIDTH = 20
        self.snake = Snake((self.WIDTH // 4, self.HEIGHT // 2))
        self.apples = [(self.WIDTH // 2 + 1, self.HEIGHT // 2),
                       (3*self.WIDTH // 4, self.HEIGHT // 2),
                       (5*self.WIDTH // 8, self.HEIGHT // 2),
                       (self.WIDTH // 2, self.HEIGHT // 4),
                       (self.WIDTH // 2, 3*self.HEIGHT // 4)]
        self.hangman_apple = [(), ()]

        self.letters_on_field = ['a', 'a', 'a', 'a', 'a']
        self.letters_eaten = []
        self.discarded_letters = []
        self.hangman_letter_on_field = None

        self.eat = False
        self.letters_counter = 0

        self.provider_random = letter_provider1
        self.provider_hangman = letter_provider2

    def random_position(self) -> tuple[int, int]:
        while True:
            position = (randint(2, self.WIDTH-2)), (randint(2, self.HEIGHT-2))
            if position in self.snake.cells:
                position = self.random_position()
            if position not in self.apples and position not in self.hangman_apple:
                return position

    def update_apple(self, x: int):
        self.apples[x] = self.random_position()
        while True:
            self.letters_on_field[x] = self.provider_random.get_next_letter()
            if self.letters_on_field[x] in self.discarded_letters:
                continue
            else:
                break

    def eating_apple(self, x: int):
        self.eat = True
        self.letters_counter += 1
        self.letters_eaten.append(self.letters_on_field[x])

    def generate_hangman_apple(self):
        if self.hangman_apple == self.snake.cells[0]:
            self.letters_counter += 1
            self.eat = True
            self.hangman_apple = self.random_position()
            self.letters_eaten.append(self.hangman_letter_on_field)
            while True:
                self.hangman_letter_on_field = self.provider_hangman.get_next_letter()
                if self.hangman_letter_on_field in self.discarded_letters or\
                        self.hangman_letter_on_field in self.letters_on_field:
                    continue
                else:
                    break

    def generate_apples_start(self):
        for i in range(4):
            if self.apples[i] == self.snake.cells[0]:
                self.eating_apple(i)
                self.apples[i] = self.random_position()

    def generate_apples_game(self):
        for i in range(4):
            if self.apples[i] == self.snake.cells[0]:
                self.eating_apple(i)
                self.update_apple(i)

    def move_snake(self, direction: tuple[int, int]):
        self.snake.snake_step(direction)
        self.snake.fix_to_bounds(self.HEIGHT, self.WIDTH)
        if not self.eat:
            self.snake.cells.pop()
        else:
            self.eat = False

    def clear_stats(self):
        self.letters_eaten = []
        self.letters_counter = 0
        for i in range(4):
            self.update_apple(i)
        self.hangman_apple = self.random_position()
        while True:
            self.hangman_letter_on_field = self.provider_hangman.get_next_letter()
            if self.hangman_letter_on_field in self.discarded_letters:
                continue
            else:
                break

    def build_matrix(self):
        matrix = [
            [Field.EMPTY for _ in range(self.WIDTH)]
            for _2 in range(self.HEIGHT)
        ]
        self.snake.draw_on(matrix)
        for i in range(4):
            row, col = self.apples[i]
            matrix[row][col] = self.letters_on_field[i]
        if self.hangman_apple != [(), ()]:
            row, col = self.hangman_apple
            matrix[row][col] = self.hangman_letter_on_field
        return matrix


class Snakegame:
    def __init__(self, printer: Printer):

        self.field = Field(RandomLetterProvider(), SecretLetterProvider())
        self.direction = (1, 0)
        self.printer = printer

        self.index_letter = 0
        self.chosen_letter = None
        self.callbacks = []

        self.flag_end = False
        self.game = 0

    def choose_letter(self):
        while True:
            self.index_letter = int(input())
            if self.index_letter <= 3:
                self.chosen_letter = self.field.letters_eaten[self.index_letter-1]
                self.field.discarded_letters.append(self.chosen_letter)
                for callback in self.callbacks:
                    callback()
                self.index_letter = 0
                break
            else:
                print(wrong_input)

    def add_object_eaten_callback(self, callback: Callable[[str], ...]):
        self.callbacks.append(callback)

    def process_press(self, key):
        match key:
            case keyboard.Key.left:
                self.direction = (0, -1)
            case keyboard.Key.up:
                self.direction = (-1, 0)
            case keyboard.Key.right:
                self.direction = (0, 1)
            case keyboard.Key.down:
                self.direction = (1, 0)

    def start_rules(self) -> int:
        resume = int(input())
        return resume

    def step_start(self):
        self.field.move_snake(self.direction)
        self.field.generate_apples_start()

    def step_game(self):
        self.field.move_snake(self.direction)
        self.field.generate_apples_game()
        self.field.generate_hangman_apple()

    def messages(self):
        if self.field.snake.snake_die():
            return 'Game Over'
        if self.game == 2 and self.field.letters_counter == 3:
            return ('Eaten letters: ', ', '.join(self.field.letters_eaten), ' ',
                    'Enter the number of the letter you selected')
        if self.field.letters_counter == 3 and self.game == 1:
            return rules
        if self.game == 0:
            return first_message
        while self.index_letter > 3:
            return wrong_input

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
            self.print()
            start = int(input())
            if start == 1:
                self.game += 1
                while True:
                    clear_terminal()
                    while self.game == 1:
                        self.step_start()
                        self.print()
                        if self.field.letters_counter == 3:
                            self.field.apples.pop()
                            if self.field.snake.snake_die():
                                break
                            if self.start_rules() == 1:
                                self.field.clear_stats()
                                self.game += 1
                            else:
                                print(wrong_input)
                                continue
                        time.sleep(0.3)
                    while self.game == 2:
                        self.step_game()
                        self.print()
                        if self.field.letters_counter == 3:
                            self.choose_letter()
                            self.field.clear_stats()
                        time.sleep(0.3)
                        if self.field.snake.snake_die():
                            break
                    if self.field.snake.snake_die():
                        break
                    time.sleep(0.3)
            else:
                print(wrong_input)


if __name__ == '__main__':
    printer = DefaultPrinter()
    game = Snakegame(printer)
    game.run()
