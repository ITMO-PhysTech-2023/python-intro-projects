dictionary = ['capybara', 'giraffe', 'bear', 'horse', 'cat']
import random

FIELDS = [
   ' +-----+\n' + 
   ' |     |\n' +
   ' o     |\n' +
  '/|\    |\n' +
  '/ \    |\n' +
'______/|\_\n'
,

   ' +-----+\n' + 
   ' |     |\n' +
   ' o     |\n' +
  '/|\    |\n' +
  '       |\n' +
'______/|\_\n'
,

   ' +-----+\n' + 
   ' |     |\n' +
   ' o     |\n' +
  '       |\n' +
  '       |\n' +
'______/|\_\n'
,

   ' +-----+\n' + 
   ' |     |\n' +
   '       |\n' +
  '       |\n' +
  '       |\n' +
'______/|\_\n'
,

   '       \n' + 
   '       |\n' +
   '       |\n' +
  '       |\n' +
  '       |\n' +
'______/|\_\n'
,

   '       \n' + 
   '       \n' +
   '       \n' +
  '       \n' +
  '       \n' +
'______/|\_\n'
,

   '\n' + 
   '\n' +
   '\n' +
  '\n' +
  '\n' +
'\n'
,
]

import os


def terminal_size():
    return os.get_terminal_size()


def clear_terminal():
    cmd = 'cls' if os.name == 'nt' else 'clear'
    os.system(cmd)


incorrect_msg = 'Не угадал'
incorrect_msg_rep = 'Эта буква уже оказалась неверной! Выберите другую!'
correct_msg = 'Молодец!'
correct_msg_rep = 'Вы уже угадали эту букву! Выберите другую!'
gameover_msg = r'''К сожалению, вы проиграли! Увидимся в аду!
            Начинаем новую игру?'''
win_msg = 'Поздравляю! Начинаем новую игру?'

def create_secret():
    return dictionary[random.randint(0, len(dictionary) - 1)]

tries = 6

#word, guessed, correct, incorrect, tries = '', [], [], [], 6

def user_input(inp):
    global word, guessed, correct, incorrect, tries
    letter = inp
    if (letter not in word.upper()) or letter == '':
        if letter not in incorrect:
            tries -= 1
            incorrect.append(letter)
            answer = incorrect_msg
        else:
            answer = incorrect_msg_rep
    elif letter in word.upper() and letter != '':
        if letter not in correct:
            correct.append(letter)
            answer = correct_msg
            for i in range(len(word)):
                if letter == word[i].upper():
                    guessed[i] = letter
        else:
            answer = correct_msg_rep
    
    if tries <= 0:
            answer = gameover_msg
    return answer, correct, incorrect, guessed

def hang_init():
    global word, correct, incorrect, guessed

    word = create_secret()
    correct = []
    incorrect = []
    guessed = ['_' for _ in range(len(word))]
    return word, guessed


def print_hang_field(guessed, correct, incorrect, tries):
        #clear_terminal()
        strings = []
        string = 'Осталось попыток: ' + str(tries)
        strings.append(string)
        word_print = ''
        for i in guessed:
             word_print += i

        strings.append(word_print)
        correct_print = ''
        for i in correct:
            correct_print += i + ' '
        incorrect_print = ''
        for i in incorrect:
            incorrect_print += i + ' '
        strings.append(print_green(correct_print) + "\033[37m {}" .format(''))
        strings.append(print_red(incorrect_print) + "\033[37m {}" .format(''))
        string = ''
        for i in FIELDS[tries].split('\n'):
            string = i
            strings.append(string)

        return strings


def print_red(text):
    return "\033[31m {}" .format(text)

def print_green(text):
    return "\033[32m {}" .format(text)
