from common.util import clear_terminal


def create_secret():
    return 'capybara'


SECRET = create_secret()
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

    letter = input('Enter your guess: ').lower()

    #2
    if (len(letter)) != 1 or ord(letter) < ord('a') or ord(letter) > ord('z'):
        print('Invalid input! Try again')
        continue
    #3
    if letter in SECRET:
        for i in range(len(SECRET)):
            if SECRET[i] == letter:
                secret_letters[i] = letter
    else:
        print('Wrong letter')
        turn_number += 1

    #5
    if turn_number == len(FIELDS) - 1:
        print(FIELDS[turn_number])
        print('GAME OVER!!!')
        break
    if ''.join(secret_letters) == SECRET:
        print('You won!')
        print(SECRET.upper())
        break