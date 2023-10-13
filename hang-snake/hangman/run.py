# from common.util import clear_terminal
from random import randint


a = [str(i) for i in open('dictionary.txt').readlines()]
def create_secret():
    i = randint(1, len(a))
    return a[i][:-1]
def field(x):
    if x == 1:
        print('           ')
        print('           ')
        print('           ')
        print('           ')
        print('           ')
        print('_______/|\_')
    elif x == 2:
        print('        +')
        print('        |')
        print('        |')
        print('        |')
        print('        |')
        print('_______/|\_')
    elif x == 3:
        print('   +----+')
        print('        |')
        print('        |')
        print('        |')
        print('        |')
        print('_______/|\_')
    elif x == 4:
        print('   +----+')
        print('   |    |')
        print('        |')
        print('        |')
        print('        |')
        print('_______/|\_')
    elif x == 5:
        print('   +----+')
        print('   |    |')
        print('   o    |')
        print('        |')
        print('        |')
        print('_______/|\_')
    elif x == 6:
        print('   +----+')
        print('   |    |')
        print('   o    |')
        print('  /|\   |')
        print('  / \   |')
        print('_______/|\_')


word = create_secret()
cor_letters = []
to_show = ['_']*len(word)
incor_letters = ''
tries = 6
flag = False
while tries>0 and to_show != list(word):
    print('Enter your letter please:')
    a = str(input())
    if len(a) != 1 or (a not in 'qwertyuiopasdfghjklzxcvbnm'):
        print('incorrect input, try again')
    elif a not in word:
        incor_letters = incor_letters + a + ' '
        tries -= 1
    else:
        cor_letters.append(a)
        for i in range(len(word)):
            if word[i] == a:
                to_show[i] = a

    print('word:')
    print(*to_show)
    print('gallows:')
    field(6-tries)
    if to_show == list(word):
        print('YOU WON!')
        flag = True
    else:
        print('Incorrect letters:')
        print(incor_letters)
    print()
    print()
if not flag:
    print('YOU LOSE!', 'word was:', word)
