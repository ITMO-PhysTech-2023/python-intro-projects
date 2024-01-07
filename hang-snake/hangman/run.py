import os
import time
import random

from hangmanclasses import GameHangman

game = GameHangman()
game.RunHangman()








'''from common.util import clear_terminal
import os
import time
import random

def create_secret():
    words = ['embrace', 'capybara', 'haircut', 'charismatic', 'stress', 'construct', 'bike', 'mile', 'justify', 'clinic', 'colon', 'tooth']
    return random.choice(words)


human_parts = 0
SECRET = [elem for elem in create_secret()]
guessed = ['_' for elem in SECRET]
HUMAN = [(3, 3), (4, 3), (4, 2), (4, 4), (5, 2), (5, 4)]

FINAL_FIELD = r
   +----+
   |    |
   o    |
  /|\   |
  / \   |
_______/|\____
.split(\n)

FIELD = [
    list(row)
    for row in FINAL_FIELD
]

for cell in HUMAN:
    FIELD[cell[0]][cell[1]] = ' '

while True:
    os.system('cls')
    if human_parts == 6:
        print("Game Over!")
        print('Слово было:', ''.join(SECRET))
        for row in FIELD:
            print(''.join(row))
        break
    if '_' not in guessed:
        print('You won!')
        break

    for row in FIELD:
        print(''.join(row))

    print(''.join(guessed))

    letter = input('Введите буковку: ').lower()

    if len(letter) != 1:
        FIELD[HUMAN[human_parts][0]][HUMAN[human_parts][1]] = FINAL_FIELD[HUMAN[human_parts][0]][HUMAN[human_parts][1]]
        human_parts += 1
        letter = '1'

    if 123 > ord(str(letter)) > 96:
        if letter not in SECRET or letter in guessed:
            FIELD[HUMAN[human_parts][0]][HUMAN[human_parts][1]] = FINAL_FIELD[HUMAN[human_parts][0]][HUMAN[human_parts][1]]
            human_parts += 1
            continue
        else:
            for i in range(len(SECRET)):
                if letter == SECRET[i]:
                    guessed[i] = letter
    else:
        print('НОРМАЛЬНО ОБЩАЙСЯ ЭЭЭЭЭЭЭЭЭ')
        time.sleep(1.5)
        continue'''