from pynput import keyboard
from random import randint
import os
from time import sleep


class Apple:
    def __init__(self, symbol='A'):
        self.cords = ()
        self.symbol = symbol


class Snake:
    def __init__(self):
        self.cords = []

    def add_element(self):
        self.cords.append(())

    def process_move(self, direction):
        for i in range(len(self.cords) - 1, 0, -1):
            self.cords[i] = self.cords[i - 1]
        self.cords[0] = (self.cords[0][0] + direction[0], self.cords[0][1] + direction[1])


class SnakeGame:
    def __init__(self, width: int, height: int, amount_of_apples=1):
        self.width = width
        self.height = height
        self.field = []
        for i in range(self.height):
            self.field.append(['_'] * self.width)
        self.direction = (1, 0)
        self.snake = Snake()
        self.apples = [Apple() for _ in range(amount_of_apples)]

    def print_field(self):
        for x in range(self.width):
            for y in range(self.height):
                cords = (x, y)
                it_was_apple = False
                for apple in self.apples:
                    if cords == apple.cords:
                        print(apple.symbol, end='')
                        it_was_apple = True
                        break
                if it_was_apple:
                    continue
                if cords == self.snake.cords[0]:
                    print('0', end='')
                elif cords in self.snake.cords:
                    print('o', end='')
                else:
                    print('_', end='')
            print()

    def random_snake_head_position(self):
        self.snake.cords.append((randint(0, self.width - 1), randint(0, self.height - 1)))

    def create_new_apples_positions(self, *new_symbols):
        for apple in enumerate(self.apples):
            apple[1].cords = (randint(0, self.width - 1), randint(0, self.height - 1))
        for i in enumerate(new_symbols):
            self.apples[i[0]].symbol = i[1]

    def process_eat(self):
        for apple in self.apples:
            if apple.cords == self.snake.cords[0]:
                self.create_new_apples_positions()
                self.snake.add_element()
                return apple.symbol
        return None

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

    def precess_loose_conditionals(self):
        if (self.snake.cords[0][1] == self.height or self.snake.cords[0][1] == -1 or self.snake.cords[0][0] == -1 or
                self.snake.cords[0][0] == self.width) or (self.snake.cords[0] in self.snake.cords[1:]):
            print("You loose")
            exit()

    def run(self):
        self.random_snake_head_position()
        self.create_new_apples_positions()
        with keyboard.Listener(on_press=self.process_press):
            while True:
                self.print_field()
                sleep(1)
                self.precess_loose_conditionals()
                self.process_eat()
                self.snake.process_move(self.direction)
                os.system('cls' if os.name == 'nt' else 'clear')
