from common.util import clear_terminal
from random_word import RandomWords #библиотека рандомных слов

randomWords = RandomWords()

FINAL_FIELD = r'''
   +----+
   |    |
   o    |
  /|\   |
  / \   |
_______/|\_
'''.split('\n')

HUMAN = [
    (3, 3),
    (4, 3),
    (4, 2),
    (4, 4),
    (5, 2),
    (5, 4)
]
human_parts = 0


def create_secret_word():
    return randomWords.get_random_word()


def global_variables():
    secret = create_secret_word()
    n = len(secret)
    guessed = ['_' for i in range(n)]
    field = [list(row) for row in FINAL_FIELD]
    for cell in HUMAN:
        field[cell[0]][cell[1]] = ' '
    return secret, guessed, field, n


SECRET, GUESSED, FIELD, n = global_variables()


def play_again():
    global SECRET, GUESSED, FIELD, n, human_parts
    while True:
        play_again = input('Want to play again? enter yes or no ').lower()
        if play_again == 'yes':
            SECRET, GUESSED, FIELD, n = global_variables()
            human_parts = 0
            return True
        elif play_again == 'no':
            return False
        else:
            print('Invalid enter. Please try again')


FLAG = True
while FLAG:
    # 1
    clear_terminal()
    for row in FIELD:
        print(''.join(row))
    print()
    print(''.join(GUESSED))

    # 2 and 3
    letter = input('Enter your guess: ').lower()
    if len(letter) != 1 and ord(letter) < ord('a') or ord(letter) > ord('z'):
        print('Try again. Enter a letter')
        continue
    # 4
    if letter in SECRET:
        print('Great job!')
        for i in range(n):
            if SECRET[i] == letter:
                GUESSED[i] = letter
    else:
        print('What a pity :(')
        cell = HUMAN[human_parts]
        human_parts += 1
        FIELD[cell[0]][cell[1]] = FINAL_FIELD[cell[0]][cell[1]]

    # 5
    if '_' not in GUESSED:
        print('You won!')
        FLAG, SECRET, FIELD = play_again()

    if human_parts == len(HUMAN):
        print('You lose!')
        FLAG = play_again()
