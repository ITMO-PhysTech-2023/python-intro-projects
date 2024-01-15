import os
import time
import random

def create_secret():
    words = ['embrace', 'capybara', 'haircut', 'charismatic', 'stress', 'construct', 'bike', 'mile', 'justify', 'clinic', 'colon', 'tooth']
    return random.choice(words)

human_parts = 0
SECRET = [elem for elem in create_secret()]
HUMAN = [(3, 3), (4, 3), (4, 2), (4, 4), (5, 2), (5, 4)]

FINAL_FIELD = r'''
   +----+
   |    |
   o    |
  /|\   |
  / \   |
_______/|\____
'''.split('\n')


class Field:
    def __init__(self):
        self.FIELD = [
            list(row)
            for row in FINAL_FIELD
            ]
        self.secret_word = [elem for elem in create_secret()]
        self.chasti_cheloveka = human_parts
        for cell in HUMAN:
            self.FIELD[cell[0]][cell[1]] = ' '

    def Vyvod_Polya(self):
        for row in self.FIELD:
            print(''.join(row))

    def Dorisovka_Polya(self):
        self.FIELD[HUMAN[self.chasti_cheloveka][0]][HUMAN[self.chasti_cheloveka][1]] = FINAL_FIELD[HUMAN[self.chasti_cheloveka][0]][
            HUMAN[self.chasti_cheloveka][1]]

class GameHangman:
    def __init__(self):
        self.field = Field()
        self.letter = ''
        self.secret_word = [elem for elem in create_secret()]
        self.guessed = ['_' for _ in self.secret_word]

    def OchistkaPolya(self):
        return os.system('cls')

    def Proverka_Na_Lose(self):
         if self.field.chasti_cheloveka == 6:
            return 0

    def Proverka_na_Pobedu(self):
        if '_' not in self.guessed:
            return 0

    def Vyvod_Ugadannyh_Bukv(self):
        print(''.join(self.guessed))

    def Vstav_Bukvu(self):
        self.letter = input('Введите буковку: ').lower()

    def Proverka_Na_Dlinu_simvola(self):
        if len(self.letter) != 1:
            self.field.Dorisovka_Polya()
            self.field.chasti_cheloveka += 1
            self.letter = '1'

    def Proverka_Na_Nalichie(self):
        if 123 > ord(str(self.letter)) > 96:
            if self.letter not in SECRET or self.letter in self.guessed:
                self.field.Dorisovka_Polya()
                self.field.chasti_cheloveka += 1
            else:
                for i in range(len(SECRET)):
                    if self.letter == SECRET[i]:
                        self.guessed[i] = self.letter
        else:
            print('НОРМАЛЬНО ОБЩАЙСЯ ЭЭЭЭЭЭЭЭЭ')
            time.sleep(1.5)

    def RunHangman(self):
        while True:
            self.OchistkaPolya()
            if self.Proverka_Na_Lose() == 0:
                print("Game Over!")
                print('Слово было:', ''.join(SECRET))
                self.field.Vyvod_Polya()
                break
            if self.Proverka_na_Pobedu() == 0:
                print('You won!')
                break
            self.field.Vyvod_Polya()
            self.Vyvod_Ugadannyh_Bukv()
            self.Vstav_Bukvu()
            self.Proverka_Na_Dlinu_simvola()
            self.Proverka_Na_Nalichie()
