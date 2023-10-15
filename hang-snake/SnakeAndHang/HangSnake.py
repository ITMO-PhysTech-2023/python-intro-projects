from time import sleep
from pytimedinput import timedInput
from utils import *
from random import choice, randint
mistakes = len(plate)
words = ('motorsport', 'elephant', 'physics', 'package', 'cortege', 'snitch')
word = choice(words)
word1 = '-' * len(word)
wrong = 0
direction = (1, 0)
snake = [(14, height//2), (13, height//2), (12, height//2)]


def random_position(sn):
    col = randint(1, width - 2)
    row = randint(1, height - 2)
    while (col, row) in sn:
        col = randint(1, width - 2)
        row = randint(1, height - 2)
    return col, row


apple_position = random_position(snake)


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


def grow(direct):
    new_head = snake[0][0] + direct[0], snake[0][1] + direct[1]
    snake.insert(0, new_head)


while True:
    clear_terminal()
    print_field()
    txt, _ = timedInput('', timeout=0.3)
    match txt:
        case 's': direction = (0, 1)
        case 'w': direction = (0, -1)
        case 'd': direction = (1, 0)
        case 'a': direction = (-1, 0)

    if apple_position == snake[0]:
        print(word1)
        letter = input('Дай мне букву: ')
        if letter in word:
            a = ''
            for i in range(len(word)):
                if letter == word[i]:
                    a += letter
                else:
                    a += word1[i]
            word1 = a
        else:
            mistakes = mistakes - 1
            wrong += 1
        print(word1)
        if mistakes == 0:
            print('лузер!')
            print(plate[4])
            break
        else:
            print(plate[wrong])
        if mistakes != 0 and word1 == word:
            print('ну лан, победил')
            break
        sleep(2)
        grow(direction)
        apple_position = random_position(snake)
    else:
        grow(direction)
        snake.pop(-1)
    if snake[0][0] == (width - 1) or snake[0][1] == (height - 1) or snake[0][0] == 0 or snake[0][1] == 0:
        print('looser')
        break