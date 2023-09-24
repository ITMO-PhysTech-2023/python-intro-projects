import random
from tkinter import *

from common.util import clear_terminal


WIDTH = 700
HEIGHT = 700

words = ['programming', 'python', 'laptop', 'coffee']  # Список слов


def create_secret():
    return random.choice(words)  # Выбор случайного слова из списка


SECRET = create_secret()
n = len(SECRET)
guess_field = '_' * n  # Создание слова и поля для ответа

mistakes = 0  # Счет количества ошибок, от которого зависит какое поле выведено на экран

fields = [
    r'''
   +----+
   |    |
        |
        |
        |
_______/|\_
''',
    r'''
   +----+
   |    |
   o    |
        |
        |
_______/|\_
''',
    r'''
   +----+
   |    |
   o    |
   |    |
        |
_______/|\_
''',
    r'''
   +----+
   |    |
   o    |
  /|\   |
        |
_______/|\_
''',
    r'''
   +----+
   |    |
   o    |
  /|\   |
  /     |
_______/|\_
''',
    r'''
   +----+
   |    |
   o    |
  /|\   |
  / \   |
_______/|\_
'''
]  # Все возможные состояния игры

def output():
    canvas.delete("guess")
    canvas.create_text(350, 500,
                       text=guess_field,
                       justify=CENTER, font="Verdana 20", tags="guess")

def move():
    letter = letter_window.get()
    global guess_field, mistakes
    #letter = input('Enter your guess: ')
    if letter in SECRET:  # Если буква правильная, выполняем соответствующую функцию
        guess_field = correct_answer(letter)  # Изменяем поле для ответа
    else:
        mistakes = mistakes + 1  # Если буква неправильная, добавляем ошибку
    window.after(1, output)

def correct_answer(letter):  # Добавление правильной буквы в поле ответа
    new_guess_field = ''
    for i in range(n):  # Если буква правильная, "открываем" её в поле ответа
        if SECRET[i] == letter:
            new_guess_field = new_guess_field + letter
        else:
            new_guess_field = new_guess_field + guess_field[i]
    return new_guess_field


window = Tk()
window.title('Hangman')

canvas = Canvas(window, bg="white", height=HEIGHT, width=WIDTH)
canvas.pack()

window.geometry(f"{700}x{700}+{400}+{100}")

canvas.create_text(350, 550,
                       text="Enter your guess:",
                       justify=CENTER, font="Verdana 14")
letter_window = Entry(window)
canvas.create_window(350, 580, window=letter_window)
button_widget = Button(text='GUESS',
                           command=move)
canvas.create_window(350, 620, window=button_widget)

output()
#move()

window.mainloop()
while False:
    # make a move!
    print(fields[mistakes])
    print(guess_field)
    letter = input('Enter your guess: ')
    if letter in SECRET:  # Если буква правильная, выполняем соответствующую функцию
        guess_field = correct_answer(letter)  # Изменяем поле для ответа
    else:
        mistakes = mistakes + 1  # Если буква неправильная, добавляем ошибку
    clear_terminal()
    if SECRET == guess_field:  # Если поле для ответа совпадает с загаданным словом - победа
        print(guess_field)
        print("You won!")
        break
    if mistakes == 5:  # Если 5 ошибок - проигрыш
        print(fields[mistakes])
        print("You lost!")
        break
    # print(FIELD)
