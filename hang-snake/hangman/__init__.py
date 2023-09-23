from random import choice
from common.util import clear_terminal

FIELDS = [
   r'''
   +----+
        |
        |
        |
        |
_______/|\_
''',
   r'''
   +----+
   |    |
        |
        |
        |
_______/|\_
''',
   r'''
   +----+
   |    |
   o    |
        |
        |
_______/|\_
''',

   r'''
   +----+
   |    |
   o    |
   |    |
        |
_______/|\_
''',

   r'''
   +----+
   |    |
   o    |
  /|    |
        |
_______/|\_
''',

   r'''
   +----+
   |    |
   o    |
  /|\   |
        |
        |
_______/|\_
''',

   r'''
   +----+
   |    |
   o    |
  /|\   |
  /     |
_______/|\_
''',
   r'''
   +----+
   |    |
   o    |
  /|\   |
  / \   |
_______/|\_
'''
]
print(FIELDS[0])
words=['capybara', 'world', 'place', 'internet', 'programma']
word=choice(words)
beginword=[]
j=0
for i in range(len(word)):
   beginword.append('_')
while True:
    clear_terminal()
    letter = input('Your letter: ')
    if len(letter)!=1 and ord(letter)<ord('a') or ord(letter)>ord('z'):
        print('Invalid guess!Try again')
        continue
    if letter in word:
        for i in range(len(word)):
            if word[i]==letter:
                beginword[i]=letter
    else:
        j+=1
        print('YOU WILL SUCCEED!!!')
    print(*beginword)
    print(FIELDS[j])
    if '_' not in beginword:
        print('You won!!!')
        break
    if j==len(FIELDS)-1:
        print('You lose!')
        break

