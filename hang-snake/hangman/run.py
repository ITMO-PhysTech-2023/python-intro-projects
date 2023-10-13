import sys

from common.util import clear_terminal
import hangman.states
import random
import time

alphabet = 'abcdefghijklmnopqrstuvwxyz'

def create_secret():
    r = random.randint(0,49)
    global SECRET
    global FIELD
    global n
    global guessed
    SECRET = open('secrets').readlines()[r]
    n = len(SECRET) - 1
    guessed = n
    FIELD = '_'*n


create_secret()

guessed_letters = list()

rem_tries = 7
while True:
    # make a move!
    print(hangman.states.STATES[7-rem_tries])
    print(FIELD)
    letter = ''
    while not letter:
        letter = input('Enter your guess: ')
        if not(letter in alphabet) or letter in guessed_letters:
            letter = ''
    letter = letter[0]
    if (letter in SECRET) and (letter != '\n') and not (letter in guessed_letters) and (letter != ''):
        guessed_letters.append(letter)
        for i in range(n):
            if SECRET[i] == letter:
                FIELD = FIELD[:i] + letter + FIELD[i+1:]
                guessed-=1
        if guessed == 0:
            clear_terminal()
            print('Damn dude thats impressing!')
            guessed_letters.clear()
            create_secret()
            time.sleep(3)
    else:
        rem_tries-=1
        if not rem_tries:
            clear_terminal()
            print('what a loser lul go learn some english\n')
            print('btw this is the word u needed to guess:\n' + SECRET)
            time.sleep(3)
            sys.exit()
    clear_terminal()