from pynput import keyboard
from random import randint
import os
from time import sleep

class Apple:
    def __init__(self):
        self.cords = ()

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
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.field = []
        for i in range(self.height):
            self.field.append(['_'] * self.width)
        self.direction = (1, 0)
        self.snake = Snake()
        self.apple = Apple()

    def print_field(self):
        for x in range(self.width):
            for y in range(self.height):
                cords = (x, y)
                if (cords == self.snake.cords[0]):
                    print('0', end='')
                elif ((cords) in self.snake.cords):
                    print('o',end='')
                elif (cords == self.apple.cords):
                    print('A', end='')
                else:
                    print('_', end='')
            print()

    def random_snake_head_position(self):
        self.snake.cords.append((randint(0, self.width - 1), randint(0, self.height - 1)))

    def random_apple_position(self):
        self.apple.cords = (randint(0, self.width - 1), randint(0, self.height - 1))

    def process_eat(self):
        if (self.apple.cords == self.snake.cords[0]):
            self.random_apple_position()
            self.snake.add_element()

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
        if (self.snake.cords[0][1] == snakeGameA.height or self.snake.cords[0][1] == -1 or self.snake.cords[0][0] == -1 or self.snake.cords[0][0] == snakeGameA.width) or (self.snake.cords[0] in self.snake.cords[1:]):
            print("You loose")
            exit()

    def run(self):
        self.random_snake_head_position()
        self.random_apple_position()
        with keyboard.Listener(on_press=self.process_press) as listener:
            while True:
                self.print_field()
                sleep(1)
                self.precess_loose_conditionals()
                self.process_eat()
                self.snake.process_move(self.direction)
                os.system('cls' if os.name == 'nt' else 'clear')

snakeGameA = SnakeGame(width=int(input()), height=int(input()))

snakeGameA.run()