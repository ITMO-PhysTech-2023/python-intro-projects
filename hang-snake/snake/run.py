import copy
import os
import time
from pynput import keyboard
from random import randint
from os import system


class SnakeGame:
    def __init__(self, width, height, sleep_step):
        self.WIDTH = width
        self.HEIGHT = height
        self.SLEEP_STEP = sleep_step
        self.SCREEN = list()
        self.direction = (-1, 0)
        self.pause = False
        self.counter = 0
        self.snake_head = [int(self.HEIGHT / 2), int(self.HEIGHT / 2)]
        self.snake = [copy.deepcopy(self.snake_head)]
        self.apple = self.random_position()

# возвращает список из двух рандомных чисел (координаты на поле) V
    def random_position(self):
        return [randint(1, self.HEIGHT - 2), randint(1, self.WIDTH - 2)]

# считывает изменения direction и pause V
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
            case keyboard.Key.esc:
                if self.pause:
                    self.pause = False
                else:
                    self.pause = True

# создает поле в виде двумерного списка, к которому можно обращаться по координатам V
    def make_field(self):
        for i in range(self.HEIGHT - 1):
            self.SCREEN.append(self.WIDTH * ['.'])

# возвращает положение яблока вне змейки (координаты) V
    def apple_generation(self):
        while self.apple in self.snake:
            self.apple = self.random_position()

# обеспечивает движение змейки на один шаг + проверка на съеденное яблоко V
    def snake_move(self):
        if self.apple in self.snake:
            self.apple_generation()
            self.snake.insert(0, copy.deepcopy(self.snake_head))
            self.counter += 1
        else:
            self.snake.insert(0, copy.deepcopy(self.snake_head))
            self.snake.pop()
        self.snake_head[0] += self.direction[0]
        self.snake_head[1] += self.direction[1]

# проверка на проигрыш V
    def is_lost(self) -> bool:
        return (self.snake_head[0] not in range(len(self.SCREEN))) or \
                (self.snake_head[1] not in range(len(self.SCREEN[1]))) or \
                (self.snake_head in self.snake)

# печатание всякого на экран V
    def print_everything(self):
        field = ''
        screen = copy.deepcopy(self.SCREEN)
        screen[self.apple[0]][self.apple[1]] = 'a'
        for j in self.snake:
            screen[j[0]][j[1]] = 'o'
        screen[self.snake_head[0]][self.snake_head[1]] = 'S'
        for i in screen:
            field += ('  '.join(i) + '\n')
        print('\n' * 5)
        print(field)

# собственно, запускает игру
    def run(self):
        self.make_field()
        with keyboard.Listener(on_press=self.process_press):
            while True:
                if self.pause:
                    continue
                self.print_everything()
                self.snake_move()
                if self.is_lost():
                    print('Game over!\nYour score: ', self.counter)
                    break
                time.sleep(self.SLEEP_STEP)


s_game = SnakeGame(25, 25, 0.1)
s_game.run()