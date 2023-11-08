import time
import vars
from common.util import clear_terminal
from pynput import keyboard
from hangman.LetterInput import LetterInputByHands, LetterInputByRandom
from vars import repeat, proposal_repeat

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
    def __init__(self, letter_input, timeout):
        self.field = Field()
        self.secret = vars.secret_word
        self.enter_field = ['_' for _ in range(len(self.secret))]
        self.LetterInput = letter_input
        self.timeout = timeout
        self.letter = ''

    def get_letter(self):
        while True:
            if __name__ == '__main__':
                self.letter = self.LetterInput.input_letter()
                if len(self.letter) != 1 or ord(self.letter) < ord('a') or ord(self.letter) > ord('z'):
                    print('Error of the enter')
                    continue
                elif self.letter in vars.last_letter:
                    print('This letter was already entered. Try other.')
                    continue
                else:
                    break
            else:
                letter = vars.import_letter
                if letter in vars.last_letter:
                    print('This letter was already entered. Try other.')
                    continue
                else:
                    break

    def check_letter(self):
        if self.letter in self.secret:
            for i in range(len(self.secret)):
                if self.secret[i] == self.letter:
                    self.enter_field[i] = self.letter
        else:
            self.field.active_fail()

    def add_letter(self):
        vars.init_var()
        vars.last_letter.append(self.letter)

    def if_win(self):
        return '_' not in self.enter_field

    def if_lose(self):
        return len(loser) == self.field.fails_count

    def demonstrate(self):
        if __name__ == '__main__':
            clear_terminal()
            self.field.print()
            print(''.join(self.enter_field))
        else:
            vars.init_var()
            vars.field_hangman = self.field.picture
            vars.field_enter_p = self.enter_field

    def actions(self):
        self.check_letter()
        self.add_letter()
        if __name__ == '__main__' and SelectInput == LetterInputByRandom():
            time.sleep(self.timeout)

    def update(self):
        vars.init_var()
        vars.init_input_var()
        vars.last_letter = []
        vars.a = 0
        vars.secret_word = input('enter secret word: ').lower()
        self.letter = ''
        self.secret = vars.secret_word
        self.enter_field = ['_' for _ in range(len(self.secret))]
        for i in loser:
            self.field.picture[i[0]][i[1]] = ' '
        self.field.fails_count = 0

    def process(self):
        while True:
            self.demonstrate()
            self.get_letter()
            self.actions()
            if self.if_lose():
                print('You lose! Congratulations!')
                proposal_repeat()
                with keyboard.Listener(on_press=repeat):
                    time.sleep(3)
                    if vars.a == 'continue':
                        self.update()
                        continue
                    else:
                        break
            elif self.if_win():
                print(''.join(self.enter_field))
                print()
                print('You won! Congratulations!')
                proposal_repeat()
                with keyboard.Listener(on_press=repeat):
                    time.sleep(3)
                    if vars.a == 'continue':
                        self.update()
                        continue
                    else:
                        break


if __name__ == '__main__':
    SelectInput = LetterInputByHands()
    play = GameHangman(SelectInput, 1)
    play.process()
