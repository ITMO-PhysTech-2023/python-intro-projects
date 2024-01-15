from words_and_alphabet import *
import random
from parts_of_image import *
import time

import os


def terminal_size():
    return os.get_terminal_size()


def clear_terminal():
    cmd = 'cls' if os.name == 'nt' else 'clear'
    os.system(cmd)


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
