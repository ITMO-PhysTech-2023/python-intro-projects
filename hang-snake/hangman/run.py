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

while True:
    # make a move!
    print(fields[mistakes])
    print(guess_field)
    letter = input('Enter your guess: ')
    if ...:
        FIELD = ...  # если не угадали, то надо обновить поле
    else:
        ...  # мало ли, понадобится...
    clear_terminal()

    # print(FIELD)
