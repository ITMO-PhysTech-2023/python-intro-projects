from util import clear_terminal
from words_and_alphabet import *
import random
from parts_of_image import *
def create_secret():
    return random.choice(ListOfWords)
SECRET = create_secret()
n = len(SECRET)
tries=len(field)
tries_left =len(field)
letters =["_ "]*n
while tries_left>0:
    in_or_not = 0
    print(field[tries_left-tries_left])
    print(''.join(letters))
    print('Enter your latter:')
    ans = input()
    if ans not in alphabet:
        try:
            x = int('a')
        except ValueError:
                in_or_not = 1
                error =  1
                print("Oops!  That was no valid letter.  Try again...")
    for i in range(len(SECRET)):
        if ans==SECRET[i]:
                letters[i]=ans
                in_or_not =1
    if "_ " not in letters and tries_left>0:
        print("WIN!!!")
        break
    if in_or_not == 0:
        tries_left-=1
clear_terminal()

