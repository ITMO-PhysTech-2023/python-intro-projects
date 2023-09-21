from common.util import clear_terminal
from random import randint


def create_secret():
    dictionary = ['capybara', 'physics', 'polina']
    return dictionary[randint(0, 2)]
def check_letter(letter, secret, answer):
    for i in range (len(secret)):
        if (letter == secret[i]):
            answer[i] = secret[i]
    return answer

SECRET = list(create_secret())
n = len(SECRET)

FIELD = [r'''
   +----+
   |    |
        |
        |
        |
_______/|\_
''', r'''
   +----+
   |    |
   o    |
        |
        |
_______/|\_
''', r'''
   +----+
   |    |
   o    |
   |    |
        |
_______/|\_
''', r'''
   +----+
   |    |
   o    |
  /|    |
        |
_______/|\_
''', r'''
   +----+
   |    |
   o    |
  /|\   |
        |
_______/|\_
''', r'''
   +----+
   |    |
   o    |
  /|\   |
  /     |
_______/|\_
''',  r'''
   +----+
   |    |
   o    |
  /|\   |
  / \   |
_______/|\_
''']

answer = list('_' * n)
conditions = 0
print(FIELD[0])

while True:
    print( *answer )
    letter = input('Enter your guess: ')
    new_answer = check_letter( letter, SECRET, answer.copy() )
    #print(*answer, *new_answer)
    if( new_answer == answer ):
        conditions+=1

    answer = new_answer

    clear_terminal()
    print( FIELD[conditions] )
    if( conditions == 6 ):
        print( 'YOU LOSE' )
        break
    if( answer == SECRET):
        print( 'TUTURU' )
        break