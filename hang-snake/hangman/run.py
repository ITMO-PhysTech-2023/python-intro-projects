
import os
import random

def create_secret():
    words = ['capybara', 'dog', 'cat', 'rat', 'night', 'flash', 'wolverine']
    return random.choice(words)



SECRET = create_secret()
n = len(SECRET)
GUESSED = ['_' for i in range(n)]

FINAL_FIELD = r'''
   +----+
   |    | 
   o    |
  /|\   |
  / \   |
_______/|\_
'''.split('\n')

FIELD = FINAL_FIELD
HUMAN = [
    (3, 3),
    (4, 3),
    (4, 2),
    (4, 4),
    (5, 2),
    (5, 4)
]
FIELD = [
    list(row)
    for row in FINAL_FIELD
]

human_parts = 0
for cell in HUMAN:
    FIELD[cell[0]][cell[1]] = ' '

while True:
    os.system('cls')
    for row in FIELD:
        print(''.join(row))
    print()
    print(''.join(GUESSED))
    if '_' not in GUESSED:
        print('Вы выиграли!')
        break
    if human_parts == len(HUMAN):
        print('Вы проиграли!')
        print('Верное слово было:', SECRET)
        break
    letter = input('Введите букву: ').lower()
    if len(letter) != 1 and ord(letter) < ord('a') or ord(letter) > ord('z'):
        print('Неправильный синтаксис! Попробуйте снова')
        continue
    if letter in SECRET:
        for i in range(n):
            if SECRET[i] == letter:
                GUESSED[i] = letter
    else:
        coordinates_of_part = HUMAN[human_parts]
        human_parts += 1
        FIELD[coordinates_of_part[0]][coordinates_of_part[1]] = FINAL_FIELD[coordinates_of_part[0]][
            coordinates_of_part[1]]
