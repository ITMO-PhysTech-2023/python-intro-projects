#from common.util import clear_terminal
from __init__ import dictionary, FIELDS, clear_terminal
import random



def create_secret():
    return dictionary[random.randint(0, len(dictionary) - 1)]


word = create_secret()
n = len(word)
correct = []
incorrect = []
guessed = ['_' for _ in range(n)]

while True:
    word = create_secret()
    n = len(word)
    correct = []
    incorrect = []
    guessed = ['_' for _ in range(n)]
    tries = 6
    while True:
        
        letter = input('Enter your guess: ')
        if letter not in word:
            if letter not in incorrect:
                tries -= 1
                incorrect.append(letter)
                answer = 'Не угадал'
            else:
                answer = 'Эта буква уже оказалась неверной! Выберите другую!'
                continue
        else:
            if letter not in correct:
                correct.append(letter)
                answer = 'Молодец!'
                for i in range(len(word)):
                    if letter == word[i]:
                        guessed[i] = letter
            else:
                answer = 'Вы уже угадали эту букву! Выберите другую!'
        if tries <= 0:
            answer = 'К сожалению, вы проиграли! Увидимся в аду!'
            break
        

        clear_terminal()
        print(answer)
        print('Осталось попыток: ' + str(tries))
        print(str(guessed))
        print(FIELDS[tries])

        if tries <= 0:
            answer = 'К сожалению, вы проиграли! Увидимся в аду!'
            break

        if len(correct) == len(set(word)):
            print('Поздравляю!')
            break