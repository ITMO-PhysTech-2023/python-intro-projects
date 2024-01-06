import random
import time
from pynput import keyboard


class Game:
    WIDTH = 20
    HEIGHT = 10
    snake = [(4, 4)]
    food = (9, 9)
    dx, dy = 1, 0

    def on_key_press(self, key):
        try:
            if key == keyboard.Key.right and self.dx != -1:
                self.dx, self.dy = 1, 0
            elif key == keyboard.Key.left and self.dx != 1:
                self.dx, self.dy = -1, 0
            elif key == keyboard.Key.up and self.dy != 1:
                self.dx, self.dy = 0, -1
            elif key == keyboard.Key.down and self.dy != -1:
                self.dx, self.dy = 0, 1
        except AttributeError:
            pass

    def launching_the_game(self):
        game_board = Board(self.WIDTH, self.HEIGHT)
        listener = keyboard.Listener(on_press=self.on_key_press)
        listener.start()
        while True:
            x, y = self.snake[-1]
            new_head = (x + self.dx, y + self.dy)
            if new_head in self.snake or new_head[0] < 0 or new_head[0] >= self.WIDTH or new_head[1] < 0 or new_head[1] >= self.HEIGHT:
                print('Игра окончена!')
                break
            self.snake.append(new_head)
            if new_head == self.food:
                self.food = (random.randint(0, self.WIDTH - 1), random.randint(0, self.HEIGHT - 1))
            else:
                self.snake.pop(0)
            game_board.draw_board(self.snake, self.food)
            time.sleep(0.3)


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def draw_board(self, snake, food):
        print('+' + '-' * self.width + '+')
        for y in range(self.height):
            row = '|'
            for x in range(self.width):
                if (x, y) in snake:
                    row += 'O'
                elif (x, y) == food:
                    row += 'x'
                else:
                    row += ' '
            row += '|'
            print(row)
        print('+' + '-' * self.width + '+')