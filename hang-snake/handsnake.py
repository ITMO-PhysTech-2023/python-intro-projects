from pynput import keyboard
import random
import time
from hangman.parts_of_image import *
from hangman.words_and_alphabet import *
import os


def create_secret():
    return random.choice(ListOfWords)


def gallow_printing(gallow, letters, tries_left, tries):
    if tries_left > 0:
        print(gallow[tries - tries_left - 1])
        print(''.join(letters))


def result(letters, tries_left):
    if ("_ " not in letters) and tries_left > 0:
        print("WIN!!!")
        time.sleep(10)
    if tries_left == 0:
        print(gallow[-1])
        print('YOU LOSE!!!')
        time.sleep(10)


def new_alphabet(word, alphabet):
    ans = []
    for i in alphabet:
        if i not in word:
            ans.append(i)
    return ans


SECRET = create_secret()
n = len(SECRET)
tries = len(gallow)
tries_left = len(gallow) - 1
letters = ['_ '] * n
h = 10
w = 30
snake = [[random.randint(1, h - 4), random.randint(1, w - 4)]]
Apples = 0
not_Apples = 0
direction = (1, 0)
New_alphabet = new_alphabet(SECRET, alphabet)
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


def terminal_size():
    return os.get_terminal_size()


def clear_terminal():
    cmd = 'cls' if os.name == 'nt' else 'clear'
    os.system(cmd)


def fielding():
    for i in range(h):
        if i > 0:
            print()
        for j in range(w):
            print(Field[i][j], end='')
    print()


def add_letter(alphabet):
    global not_Apples
    for i in range(2 - not_Apples):
        coord = list()
        good_apple = True
        while good_apple:
            coord = [random.randint(1, h - 2), random.randint(1, w - 2)]
            if Field[coord[0]][coord[1]] not in (borders and alphabet):
                good_apple = False
        Field[coord[0]][coord[1]] = alphabet[random.randint(0, len(alphabet) - 1)]
    not_Apples = 2


def add_secret_letter(letters):
    global Apples
    coord = list()
    if Apples == 0:
        good_apple = True
        while good_apple:
            coord = [random.randint(1, h - 2), random.randint(1, w - 2)]
            if Field[coord[0]][coord[1]] not in (borders and alphabet):
                good_apple = False
        good_letter = True
        while good_letter:
            if '_ ' not in letters:
                break
            Field[coord[0]][coord[1]] = SECRET[random.randint(0, len(SECRET) - 1)]
            if Field[coord[0]][coord[1]] not in letters:
                good_letter = False
        Apples += 1


def crawl(snake, direction, tries_left, letters):
    global Apples
    global last_position
    global not_Apples
    barriers = ['|', '<', '>', '^', 'v', '-', '_']
    new_snake = [[snake[0][0] + direction[0], snake[0][1] + direction[1]]] + snake
    if Field[new_snake[0][0]][new_snake[0][1]] in barriers:
        print(gallow[-1])
        print('YOU LOSE!!!')
        time.sleep(10)
    if Field[new_snake[0][0]][new_snake[0][1]] in alphabet:
        if Field[new_snake[0][0]][new_snake[0][1]] in SECRET:
            for i in range(len(letters)):
                if SECRET[i] == Field[new_snake[0][0]][new_snake[0][1]]:
                    letters[i] = Field[new_snake[0][0]][new_snake[0][1]]
            Apples -= 1
        else:
            last_position = [new_snake[len(new_snake) - 1][0], new_snake[len(new_snake) - 1][1]]
            new_snake.pop()
            tries_left -= 1
            not_Apples -= 1
    else:
        last_position = [new_snake[len(new_snake) - 1][0], new_snake[len(new_snake) - 1][1]]
        new_snake.pop()
    return new_snake, tries_left, letters


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
        if '_ ' not in letters:
            exit()
            break
        snake, tries_left, letters = crawl(snake, direction, tries_left, letters)
        snake_field(snake, direction)
        add_secret_letter(letters)
        add_letter(New_alphabet)
        time.sleep(0.05)
        fielding()
        gallow_printing(gallow, letters, tries_left, tries)
        time.sleep(0.15)
        clear_terminal()
        result(letters, tries_left)
