from common.util import clear_terminal


def create_secret():
    return 'capybara'


def vivod(x): # функция, кторая выводит field по строкам
    for i in range(len(x)):
        print(''.join(x[i]))

SECRET = create_secret()
n = len(SECRET)
GUESSED = ['_' for _ in range(n)]
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
for cell in HUMAN:
    FIELD[cell[0]][cell[1]] = ' '
human_parts = 0
ch=0 # индекс части тела
chasti_tela=['o','|','/','\\','/','\\']
while True:
    # make a move!
    letter = input('Enter your guess: ')
    if letter not in SECRET:
        a, b = HUMAN[human_parts]
        FIELD[a][b] = chasti_tela[ch]
        human_parts += 1
        ch += 1
        vivod(FIELD)
        print(GUESSED)
        if human_parts == 6:
            print('YOU LOSE')
            break

    else:
        for i in range(n):
            if SECRET[i] == letter:
                GUESSED[i] = letter
        print(GUESSED)
    if '_' not in GUESSED:
        print('You won!')
        break