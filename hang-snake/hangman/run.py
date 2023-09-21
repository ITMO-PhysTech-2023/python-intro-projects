from common.util import clear_terminal
from random import *

#Генератор слова:

russian_words = ['капибара', 'аллигатор', 'черепаха', 'жираф', 'муравей', 'антилопа', 'медведь', 'обезьяна', 'ягуар', \
                 'анаконда']
english_words = ['capybara', 'elephant', 'giraffe', 'chimpanzee', 'horse', 'monkey', 'scorpion', 'chiken', 'jaguar', \
                 'chameleon']


def create_secret_eng():
    return english_words[randint(0, len(english_words))]


def create_secret_rus():
    return russian_words[randint(0, len(russian_words))]


#Выбор языка:
while True:
    language = input('Select language/Выберите язык (Eng/Rus): ')
    if language == 'Eng':
        SECRET = create_secret_eng()
        lett_choosing = 'Enter your letter: '
        invalid_letter = 'Invalid input! Try again'
        wrong_letter = "This letter isn't in the word"
        losing = 'GAME OVER!'
        winning = 'You won! Congratulations!'

        break
    elif language == 'Rus':
        SECRET = create_secret_rus()
        lett_choosing = 'Введите букву: '
        invalid_letter = 'Некорректный ввод. Попробуйте еще раз'
        wrong_letter = 'Этой буквы нет в слове'
        losing = 'ПОТРАЧЕНО.'
        winning = 'Победа!'

        break
    else:
        print('Invalid input! Try again/Некорректный ввод. Попробуйте еще раз')


secret_letters = ['_'] * len(SECRET)

FIELDS = [
r'''
   +----+
        |
        |
        |
        |
_______/|\_
''',
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
   |\   |
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
]

turn_number = 0
while True:
    '''
    1. Вывести поле + вывести все известные буквы
    2. Запрашиваем ход
    3. Проверяем корректность хода
    4. Проверяем успешность хода
    5. Проверяем, наступил ли выигрыш или проигрыш
    '''

    #1
    clear_terminal()
    print(''.join(secret_letters))
    print(FIELDS[turn_number])

    #2
    letter = input(lett_choosing).lower()

    #3
    if (len(letter)) != 1 or (language == 'Eng' and (ord(letter) < ord('a') or ord(letter) > ord('z'))) or \
            (language == 'Rus' and (ord(letter) < ord('а') or ord(letter) > ord('я'))):

        print(invalid_letter)
        continue
    #4
    if letter in SECRET:
        for i in range(len(SECRET)):
            if SECRET[i] == letter:
                secret_letters[i] = letter
    else:
        print(wrong_letter)
        turn_number += 1

    #5
    if turn_number == len(FIELDS) - 1:
        print(FIELDS[turn_number])
        print(losing)
        break
    if ''.join(secret_letters) == SECRET:
        print(winning)
        print(SECRET.upper())
        break