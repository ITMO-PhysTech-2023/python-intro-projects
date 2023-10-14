from pynput import keyboard
from random import randint
from defSnake import clear_terminal
from time import sleep
width, height = 30, 15
direction = (1, 0)

cells = [(col, row) for row in range(height) for col in range(width)]


def print_field():
    for cell in cells:
        if cell[0] in (0, width - 1) or cell[1] in (0, height - 1):
            print('#', end='')
        elif cell == apple_position:
            print('a', end='')
        elif cell in snake:
            print('@', end='')
        else:
            print(' ', end='')
        if cell[0] == width - 1:
            print(' ')


snake = [(14, height//2), (13, height//2), (12, height//2)]


def random_position():
    return [randint(1, width - 2), randint(1, height - 2)]


def grow():
    new_head = snake[0][0] + direction[0], snake[0][1] + direction[1]
    snake.insert(0, new_head)


apple_position = random_position()


def opposite_directions(d1: tuple[int, int], d2: tuple[int, int]):
    return d1[0] == -d2[0] and d1[1] == -d2[1]


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


with keyboard.Listener(on_press=process_press) as listener:
    while True:
        clear_terminal()
        print_field()
        sleep(0.3)
        if apple_position in snake:
            grow()
        else:
            grow()
            snake.pop(-1)
        if snake[0] == (0, width - 1) or snake[0] == (0, height - 1):
            exit()