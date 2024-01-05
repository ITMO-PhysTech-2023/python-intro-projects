
#from common.util import clear_terminal


#from common.util import clear_terminal
from __init__ import dictionary, FIELDS, clear_terminal, incorrect_msg, incorrect_msg_rep, correct_msg, correct_msg_rep, gameover_msg, win_msg
import random


def create_secret():
    return 'capybara'


def user_input():
    global tries, word, correct, incorrect
    letter = input('Enter your guess: ')
    if (letter not in word) or letter == '':
        if letter not in incorrect:
            tries -= 1
            incorrect.append(letter)
            answer = incorrect_msg
        else:
            answer = incorrect_msg_rep
    elif letter in word and letter != '':
        if letter not in correct:
            correct.append(letter)
            answer = correct_msg
            for i in range(len(word)):
                if letter == word[i]:
                    guessed[i] = letter
        else:
            answer = correct_msg_rep
    
    if tries <= 0:
            answer = gameover_msg
    return answer

def hang_init():
    global word, correct, incorrect, guessed
    word = create_secret()
    correct = []
    incorrect = []
    guessed = ['_' for _ in range(len(word))]

FINAL_FIELD = r'''
   +----+
   |    |
   o    |
  /|\   |
  / \   |
_______/|\_
'''


# здесь мы наверное хотим иметь исходное поле
# и понимание, как оно меняется после каждого хода
FIELD = FINAL_FIELD

while True:
    # make a move!
    letter = input('Enter your guess: ')
    if ...:
        FIELD = ...  # если не угадали, то надо обновить поле
    else:
        ...  # мало ли, понадобится...

    clear_terminal()
    print(FIELD)


def print_hang_field(answer, guessed, tries):
        clear_terminal()
        print(answer)
        print('Осталось попыток: ' + str(tries))

        word_print = ''
        for i in guessed:
             word_print += i

        print(word_print)
        print(FIELDS[tries])

while True:
    word = create_secret()
    n = len(word)
    correct = []
    incorrect = []
    guessed = ['_' for _ in range(len(word))]
    tries = 6
    while True:
        
        answer = user_input()
    
        

        print_hang_field(answer, guessed, tries)

        if answer == gameover_msg:
            input(gameover_msg)
            break
        print(correct)
        if len(correct) == len(set(word)):
            print(win_msg)
            input()
            break

