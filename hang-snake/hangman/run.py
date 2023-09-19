from common.util import clear_terminal
import random

def field(a):

    f0 = r'''
       +----+
       |    |
       o    |
      /|\   |
      / \   |
    _______/|\_
    '''
    f1 = r'''
       +----+
       |    |
       o    |
      /|\   |
            |
    _______/|\_
    '''
    f2 = r'''
       +----+
       |    |
       o    |
            |
            |
    _______/|\_
    '''
    f3 = r'''
       +----+
       |    |
            |
            |
            |
    _______/|\_
    '''
    f4 = r'''
       +----+
            |
            |
            |
            |
    _______/|\_
    '''
    f5 = r'''
            +
            |
            |
            |
            |
    _______/|\_
    '''
    f6 = r'''
            
            
            
            
            
    _______/|\_
    '''
    f7 = " "
    arr=[f0, f1, f2, f3, f4, f5, f6, f7]
    return arr[a]

def create_secret():
    dict = [i for i in open("dictionary")]
    i = random.randint(0, len(dict))
    return dict[i]


SECRET = create_secret()
WORD = ['_' for i in range(len(SECRET)-1)]

already_named = set()
TRIES = 7
FIELD = field(TRIES)
print(*WORD)
while TRIES>0:
    # make a move!
    letter = input('Enter your guess: ')
    if letter not in SECRET:
        TRIES -= 1
        already_named.add(letter)
        FIELD = field(TRIES)  # если не угадали, то надо обновить поле

    else:
        unknown_let = 0
        for i in range(len(SECRET)-1):
            if SECRET[i]==letter:
                WORD[i]=letter
            if WORD[i]=='_':
                unknown_let+=1

        if unknown_let==0:
            print(*WORD)
            print("YOU WIN!!")
            break
    print("не подошли: ", *already_named)
    print(*WORD)

    clear_terminal()
    print(FIELD)
if TRIES==0:
    print(SECRET)
    print("YOU'VE LOST\n"+"DON'T WORRY, TRY AGAIN!")