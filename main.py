hangman=['         \n         \n         \n         \n         \n           ', \
         '         \n         \n         \n         \n         \n__███__/|\_', \
         '         \n        |\n        |\n        |\n        |\n__███__/|\_', \
         '   +----+\n        |\n        |\n        |\n        |\n__███__/|\_', \
         '   +----+\n   |    |\n   o    |\n  /|\   |\n  / \   |\n__███__/|\_', \
         '   +----+\n   |    |\n   o    |\n  /|\   |\n  / \   |\n_______/|\_']
from random import randint
def cls():
    print('\n'*100)

with open('dict.txt') as f:
    dict = f.readlines()
    
word = dict[randint(0,len(dict)-1)]
word_X = '_'*(len(word)-1)
tries = len(hangman)
used_symb = ''
W=1

while tries!=0:
    print('- - - - - - - -')
    print(hangman[len(hangman)-tries])
    print('- - - - - - - -')
    print(word_X)
    if W==0:
        print('Вы уже использовали букву',symb)
        W=1
    print('У Вас осталось попыток:',tries)

    symb=input('Введите букву: ').lower()
    
    if symb in used_symb:
        W=0
        cls()
        continue
    else:
        used_symb = used_symb + symb

    if symb in word:
        for i in range(len(word)):
            if symb == word[i]:
                word_X=word_X[:i] + symb +word_X[i+1:]
    else:
        tries-=1
    if not('_' in word_X):
        print(word_X+'!!!!!')
        print('ТЫ ВЫЙГРАЛ, НЕВОЗМОЖНО!!!!!!!!!')
        break
    if tries!=0:
        cls()
else:
    print('Следующим будешь ты! Верное слово '+word)
