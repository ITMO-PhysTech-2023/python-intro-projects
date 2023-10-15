import os
from pynput import keyboard
from random import randint
from time import sleep
width, height = 30, 15


def clear_terminal():
    cmd = 'clear'
    os.system(cmd)


def print_field():
    cells = [(col, row) for row in range(height) for col in range(width)]
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


def random_position(sn):
    col = randint(1, width - 2)
    row = randint(1, height - 2)
    while (col, row) in sn:
        col = randint(1, width - 2)
        row = randint(1, height - 2)
    return col, row


def grow(direct):
    new_head = snake[0][0] + direct[0], snake[0][1] + direct[1]
    snake.insert(0, new_head)


def process_press(key):
    global direction
    match key:
        case keyboard.Key.left:
            direction = (-1, 0)
        case keyboard.Key.up:
            direction = (0, -1)
        case keyboard.Key.right:
            direction = (1, 0)
        case keyboard.Key.down:
            direction = (0, 1)


direction = (1, 0)
snake = [(14, height//2), (13, height//2), (12, height//2)]
apple_position = random_position(snake)
with keyboard.Listener(on_press=process_press) as listener:
    while True:
        clear_terminal()
        print_field()
        sleep(0.3)
        if apple_position == snake[0]:
            grow(direction)
            apple_position = random_position(snake)
        else:
            grow(direction)
            snake.pop(-1)
        if snake[0][0] == (width - 1) or snake[0][1] == (height - 1) or snake[0][0] == 0 or snake[0][1] == 0:
            print('looser')
            break