from pynput import keyboard
from common.util import clear_terminal
import random
import time


class Apple:
    @staticmethod
    def create_apple(width, height):
        return random.randint(0, width - 1), random.randint(0, height - 1)


class Game:
    WIDTH = 15
    HEIGHT = 8
    apple = Apple().create_apple(WIDTH, HEIGHT)
    snake = [(1, 1)]
    move1 = 1
    move2 = 0

    def keyboard_check(self, press):
        try:
            if press == keyboard.Key.right and self.move1 != -1:
                self.move1, self.move2 = 1, 0
            elif press == keyboard.Key.left and self.move1 != 1:
                self.move1, self.move2 = -1, 0
            elif press == keyboard.Key.up and self.move2 != 1:
                self.move1, self.move2 = 0, -1
            elif press == keyboard.Key.down and self.move2 != -1:
                self.move1, self.move2 = 0, 1
        except AttributeError:
            pass

    def game_start(self):
        created_field = Field(self.WIDTH, self.HEIGHT)
        listener = keyboard.Listener(on_press=self.keyboard_check)
        listener.start()

        while True:
            x, y = self.snake[-1]
            snake_head = (x + self.move1, y + self.move2)
            if snake_head in self.snake or snake_head[0] >= self.WIDTH or snake_head[1] >= self.HEIGHT or \
                    snake_head[0] < 0 or snake_head[1] < 0:
                print('You lose!')
                break
            self.snake.append(snake_head)
            if snake_head == self.apple:
                self.apple = Apple.create_apple(self.WIDTH, self.HEIGHT)
            else:
                self.snake.pop(0)
            created_field.field(self.snake, self.apple)
            time.sleep(0.2)


class Field:
    def __init__(self, wid, hei):
        self.width = wid
        self.height = hei

    def field(self, snake, apple):
        clear_terminal()
        print('_' + '_' * self.width + '_')
        for y in range(self.height):
            place = '|'
            for x in range(self.width):
                if (x, y) in snake:
                    place += '$'
                elif (x, y) == apple:
                    place += 'x'
                else:
                    place += ' '
            place += '|'
            print(place)
        print('_' + '_' * self.width + '_')
