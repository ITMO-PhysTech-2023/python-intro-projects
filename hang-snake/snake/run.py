from pynput import keyboard
import random
import time
from hangman.words_and_alphabet import *
from hangman.parts_of_image import *
import os


def terminal_size():
    return os.get_terminal_size()


def clear_terminal():
    cmd = 'cls' if os.name == 'nt' else 'clear'
    os.system(cmd)


h = 10
w = 30
apple = '$'
snake = [[random.randint(1, h - 2), random.randint(1, w - 2)]]
Apples = 0
borders = ['|', '<', '>', '^', 'v', '-']
global last_position

Field = [[' ' for i in range(w)] for j in range(h)]
for i in range(h):
    for j in range(w):
        if i == 0 or i == h - 1:
            Field[i][j] = '_'
        if j == 0 or j == w - 1:
            Field[i][j] = '|'
Field[0][0] = ' '
Field[0][w - 1] = ' '


def fielding():
    for i in range(h):
        if i > 0:
            print()
        for j in range(w):
            print(Field[i][j], end='')
    print()


def add_apple(apple):
    global Apples
    coord = list()
    if Apples == 0:
        good_apple = True
        while good_apple:

            coord = [random.randint(1, h - 2), random.randint(1, w - 2)]
            if Field[coord[0]][coord[1]] not in borders:
                good_apple = False
        Apples += 1
        Field[coord[0]][coord[1]] = apple


def crawl(snake, direction):
    global Apples
    global last_position
    barriers = ['|', '<', '>', '^', 'v', '-', '_']
    new_snake = [[snake[0][0] + direction[0], snake[0][1] + direction[1]]] + snake
    if Field[new_snake[0][0]][new_snake[0][1]] in barriers:
        exit()
    if Field[new_snake[0][0]][new_snake[0][1]] == '$':
        Apples -= 1
    else:
        last_position = [new_snake[len(new_snake) - 1][0], new_snake[len(new_snake) - 1][1]]
        new_snake.pop()
    return new_snake


def snake_field(snake, direction):
    for i in range(len(snake)):
        if i == 0:
            Field[snake[0][0]][snake[0][1]] = head(direction)
        else:
            if abs(snake[i][0] - snake[i - 1][0]) == 1:
                Field[snake[i][0]][snake[i][1]] = '|'
            elif abs(snake[i][1] - snake[i - 1][1]) == 1:
                Field[snake[i][0]][snake[i][1]] = '-'
    Field[last_position[0]][last_position[1]] = ' '


def head(direction):
    match direction:
        case (0, -1):
            return '<'
        case (0, 1):
            return '>'
        case (1, 0):
            return 'V'
        case (-1, 0):
            return '^'


def play(snake, direction, apple):
    while True:
        snake = crawl(snake, direction)
        snake_field(snake, direction)
        add_apple(apple)
        time.sleep(0.05)
        fielding()
        time.sleep(0.15)
        clear_terminal()


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


direction = (1, 0)

with keyboard.Listener(on_press=process_press) as listener:
    pass
    # play(snake, direction, apple)


def create_secret():
    return random.choice(ListOfWords)


def gallow_printing(gallow, letters, tries_left, tries):
    print(gallow[tries - tries_left])
    print(''.join(letters))
    print('Enter your letter:')


def in_alphabet(letter, alphabet):
    if letter not in alphabet:
        print("Oops!  That was no valid letter.  Try again...")
        return 1
    return 0


def result(letters, tries_left, in_or_not):
    if ("_ " not in letters) and tries_left > 0:
        print("WIN!!!")
        time.sleep(10)
        return True
    if tries_left == 1 and in_or_not == 0:
        print('YOU LOSE!!!')
        time.sleep(10)
        return True
    return False


def gameplay(tries, tries_left, gallow, letters, alphabet, SECRET):
    gallow_printing(gallow, letters, tries_left, tries)
    while tries_left > 0:
        ans = input()
        clear_terminal()
        in_or_not = in_alphabet(ans, alphabet)
        for i in range(len(SECRET)):
            if ans == SECRET[i]:
                letters[i] = ans
                in_or_not = 1
        if in_or_not == 0:
            tries_left -= 1
        gallow_printing(gallow, letters, tries_left, tries)
        if result(letters, tries_left, in_or_not):
            exit()


def play():
    while True:
        SECRET = create_secret()
        print(SECRET)
        n = len(SECRET)
        tries = len(gallow)
        tries_left = len(gallow)
        letters = ["_ "] * n
        gameplay(tries, tries_left, gallow, letters, alphabet, SECRET)


play()
