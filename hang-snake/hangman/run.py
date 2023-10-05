import time
from common.util import clear_terminal
from pynput import keyboard
from LetterInput import Letter_Input, LetterInputByHands, LetterInputByRandom

a = 0
'''def repeat(key):
    global a
    if key == keyboard.Key.space:
        a = 'continue'
    else:
        a = 'break'''


secret_word = input('enter secret word: ').lower()

lose_field = r'''
   +----+
   |    |
   o    |
  /|\   |
  / \   |
_______/|\_
'''.split('\n')

loser = [
    (3, 3),
    (4, 3),
    (4, 2),
    (4, 4),
    (5, 2),
    (5, 4)
]

class Field:
    def __init__(self, ):
        self.picture = [list(row) for row in lose_field]
        for i in loser:
            self.picture[i[0]][i[1]] = ' '
        self.fails_count = 0

    def print(self):
        for row in self.picture:
            print(''.join(row))
        print()
        print()

    def active_fail(self):
        part = loser[self.fails_count]
        self.picture[part[0]][part[1]] = lose_field[part[0]][part[1]]
        self.fails_count += 1


class GameHangman:
    def __init__(self, letter_input: Letter_Input, timeout):
        self.field = Field()
        self.secret = secret_word
        self.enter_field = ['_' for _ in range(len(self.secret))]
        self.last_letter = []
        self.LetterInput = letter_input
        self.timeout = timeout

    def get_letter(self):
        while True:
            letter = self.LetterInput.input_letter()
            if ord(letter) < ord('a') or ord(letter) > ord('z') and len(letter) != 1:
                print('Error of the enter')
                continue
            elif letter in self.last_letter:
                print('This letter was already entered. Try other.')
                continue
            else:
                break

        return letter

    def check_letter(self, letter):
        if letter in self.secret:
            for i in range(len(self.secret)):
                if self.secret[i] == letter:
                    self.enter_field[i] = letter
        else:
            self.field.active_fail()

    def add_letter(self, letter):
        self.last_letter.append(letter)

    def if_win(self):
        return '_' not in self.enter_field

    def if_lose(self):
        return len(loser) == self.field.fails_count

    def demonstrate(self):
        clear_terminal()
        self.field.print()
        print(''.join(self.enter_field))

    def actions(self):
        letter = self.get_letter()
        self.check_letter(letter)
        self.add_letter(letter)
        if SelectInput == LetterInputByRandom():
            time.sleep(self.timeout)

    def process(self):
        while True:
            self.demonstrate()
            self.actions()
            if self.if_lose():
                print('You lose! Congratulations!')
                print()
                print('If you want to try again press to space. If you want to stop press other')
                break
            elif self.if_win():
                print('You won! Congratulations!')
                print()
                print(''.join(self.enter_field))
                print()
                print('If you want to try again press to space. If you want to stop press other')
                '''with keyboard.Listener(on_press=repeat) as listener:
                    if a == 'continue':
                        continue
                time.sleep(3)'''
                break

SelectInput = LetterInputByHands()
play = GameHangman(SelectInput, 1)
play.process()
