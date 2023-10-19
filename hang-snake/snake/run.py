import time
from common.util import clear_terminal
from pynput import keyboard
from random import randint


def generate_position():
    return randint(0, width - 1), randint(0, height - 1)


direction = (1, 0)


def process_press(key):
    global direction
    match key:
        case keyboard.Key.left:
            direction = (0, -1)
        case keyboard.Key.up:
            direction = (-1, 0)
        case keyboard.Key.right:
            direction = (0, 1)
        case keyboard.Key.down:
            direction = (1, 0)


class Apple:
    def __init__(self):
        self.apple = generate_position()


class Snake:
    def __init__(self):
        self.snake = [generate_position()]
        self.body_snake = 0
        self.new_elem = (self.snake[0][0] + direction[0], self.snake[0][1] + direction[1])


class Field:
    def __init__(self, height: int, width: int):
        self.Apple_f = Apple()
        self.Snake_f = Snake()
        self.height = height
        self.width = width
        self.field = [['.' for i in range(width)] for i in range(height)]

    def put_apple(self):
        self.field[self.Apple_f.apple[0]][self.Apple_f.apple[1]] = 'a'

    def put_snake(self):
        for i in range(self.Snake_f.body_snake + 1):
            if i == 0:
                self.field[self.Snake_f.snake[0][0]][self.Snake_f.snake[0][1]] = 'O'
            else:
                self.field[self.Snake_f.snake[i][0]][self.Snake_f.snake[i][1]] = 'o'

    def print_f(self):
        for row in self.field:
            print(' '.join(row))


class GameSnake:
    def __init__(self, height_f: int, width_f: int, wait_time_repeat):
        self.Field = Field(height_f, width_f)
        # self.Snake = Snake()
        # self.Apple = Apple()
        self.l_width = [i for i in range(self.Field.width + 1)]
        self.l_height = [i for i in range(self.Field.height + 1)]
        self.wait_time = wait_time_repeat

    @property
    def Snake(self):
        return self.Field.Snake_f

    @property
    def Apple(self):
        return self.Field.Apple_f

    def check_to_eat(self):
        return self.Snake.new_elem == self.Apple.apple

    def create_new_pos(self):
        while self.Apple.apple in self.Snake.snake:
            self.Apple.apple = generate_position()

    def eat(self):
        self.Snake.snake.insert(0, self.Snake.new_elem)
        if self.check_to_eat():
            self.create_new_pos()
            self.Snake.body_snake += 1
        else:
            self.Snake.snake.pop(-1)

    def check_move(self):
        return (self.Snake.new_elem[0] not in self.l_height or self.Snake.new_elem[1] not in self.l_width or
                self.Snake.new_elem in self.Snake.snake)

    def update_var(self):
        self.Field.field = [['.' for i in range(width)] for i in range(height)]
        self.Snake.new_elem = (self.Snake.snake[0][0] + direction[0], self.Snake.snake[0][1] + direction[1])

    def do_change(self):
        if self.Snake.body_snake == 0:
            self.Field.field[self.Snake.snake[0][0]][self.Snake.snake[0][1]] = 'O'
        else:
            self.Field.put_snake()
        self.Field.put_apple()

    def run(self):
        with keyboard.Listener(on_press=process_press):
            while True:
                clear_terminal()
                self.update_var()
                if self.check_move():
                    print('You lost')
                    break
                self.do_change()
                self.Field.print_f()
                self.eat()
                time.sleep(self.wait_time)


if __name__ == '__main__':
    wait_time = 0.3
    width = 15
    height = 15
    game = GameSnake(height, width, wait_time)
    game.run()
