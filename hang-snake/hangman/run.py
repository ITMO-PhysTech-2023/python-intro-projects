from common.util import clear_terminal
import time
import random
import pathlib
def create_secret():
    with open(pathlib.Path(pathlib.Path.cwd(), 'hangman', 'secrets.txt')) as secrets:
        secrets = secrets.readlines()
        secret_number = random.randint(0, len(secrets) - 1)
        return secrets[secret_number] [:-1]

SECRET = create_secret()
n = len(SECRET)

used_letters = ""
guessed_letters = ""
eng_alphabet = "abcdefghijklmnopqrstuvwxyz"

c = 0

fields =[ r'''
   +----+
   |    |
        |
        |
        |
_______/|\_''', r'''
   +----+
   |    |
   o    |
        |
        |
_______/|\_''', r'''
   +----+
   |    |
   o    |
   |    |
        |
_______/|\_''', r'''
   +----+
   |    |
   o    |
  /|    |
        |
_______/|\_''', r'''
   +----+
   |    |
   o    |
  /|\   |
        |
_______/|\_''', r'''
   +----+
   |    |
   o    |
  /|\   |
  /     |
_______/|\_''', r'''
   +----+
   |    |
   o    |
  /|\   |
  / \   |
_______/|\_
''' ]

while True:
    if len(set(guessed_letters)) == len(set(SECRET)) or c == n:
        break
    clear_terminal()
    print(fields[0])

    time.sleep(1)

    clear_terminal()
    print('Word: ', end = '')
    for i in range (len(SECRET)):
        if SECRET[i] in guessed_letters:
            print (SECRET[i], end = '')
        else:
            print ('_', end = '')
    print ('\nUsed letters: ', used_letters)
    letter = input('Enter Your guess: ').lower()
    if not(letter in eng_alphabet):
        print('Invalid guess! Try again')
        time.sleep(0.7)
        continue
    if not(letter in used_letters):
        used_letters += letter + ","

    if not (letter in SECRET):
        fields.pop(0)
        c += 1

    else:
        guessed_letters += letter

print(fields[0])
time.sleep(1)
clear_terminal()
if c == 6:
    print('You lose!')
else:
    print('You won!')
print ('The hidden word was', SECRET)