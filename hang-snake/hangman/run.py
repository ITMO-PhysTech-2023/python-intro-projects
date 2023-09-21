import random

from common.util import clear_terminal

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


def correct_answer(letter):  # Добавление правильной буквы в поле ответа
    new_guess_field = ''
    for i in range(n):  # Если буква правильная, "открываем" её в поле ответа
        if SECRET[i] == letter:
            new_guess_field = new_guess_field + letter
        else:
            new_guess_field = new_guess_field + guess_field[i]
    return new_guess_field


while True:
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
