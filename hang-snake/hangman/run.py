from common.util import clear_terminal
def create_secret():
    return 'capybara'
SECRET = create_secret()
n = len(SECRET)
GUESSED=['_' for _ in range(n)]

FINAL_FIELD = r'''
   +----+
   |    |
   o    |
  /|\   |
  / \   |
_______/|\_
'''.split('\n')

HUMAN=[
    (3,3),
    (4,3),
    (4,2),
    (4,4),
    (5,2),
    (5,4)
]
FIELD=[
    list(row)
    for row in FINAL_FIELD
]
human_parts=0
for cell in HUMAN:
    FIELD[cell[0]][cell[1]]=' '
while True:
    #1
    clear_terminal()
    for row in FIELD:
        print(''.join(row))
    print()
    print(''.join(GUESSED))
    #2 and 3
    letter = input('Enter your guess: ').lower()
    if len(letter)!=1 and ord(letter)<ord('a') or ord(letter)>ord('z'):
        print('Invalid guess!Try again')
        continue
    #4
    if letter in SECRET:
        for i in range(n):
            if SECRET[i]==letter:
                GUESSED[i]=letter
    else:
        cell=HUMAN[human_parts]
        human_parts+=1
        FIELD[cell[0]][cell[1]]=FINAL_FIELD[cell[0]][cell[1]]
    #5
    if '_' not in GUESSED:
        print('You won!')
        break
    if human_parts == len(HUMAN):
        print('You lose!')
        break
