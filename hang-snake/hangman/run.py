import os
from random import *


def create_secret(a: list):
    return a[randint(0, len(a))]


class HangmanGame:
    russian_words = ['капибара', 'аллигатор', 'черепаха', 'жираф', 'муравей', 'антилопа', 'медведь',
                     'обезьяна', 'ягуар', 'анаконда', 'выхухоль']
    english_words = ['capybara', 'elephant', 'giraffe', 'chimpanzee', 'horse', 'monkey', 'scorpion',
                     'chicken', 'jaguar', 'chameleon', 'crocodile']
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
           |\   |
                |
        _______/|\_
        ''',
        r'''
           +----+
           |    |
           o    |
          /|\   |
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

    def __init__(self):
        self.SECRET = ''
        self.letter_choosing = ''
        self.invalid_letter = ''
        self.wrong_letter = ''
        self.losing = ''
        self.winning = ''
        self.secret_letters = []
        self.turn_number = 0
        self.your_letters = []
        self.letter = ''
        self.language = ''
        self.again = ''

# Назначает переменные интерфейса для каждого языка
    def chose_language(self):
        while True:
            self.language = input('Select language/Выберите язык (Eng/Rus): ')
            if self.language == 'Eng':
                self.SECRET = create_secret(self.english_words)
                self.letter_choosing = 'Enter your letter: '
                self.invalid_letter = 'Invalid input! Try again'
                self.wrong_letter = "This letter isn't in the word"
                self.losing = 'GAME OVER!\n It was '
                self.winning = 'You won! Congratulations!'
                break
            elif self.language == 'Rus':
                self.SECRET = create_secret(self.russian_words)
                self.letter_choosing = 'Введите букву: '
                self.invalid_letter = 'Некорректный ввод. Попробуйте еще раз'
                self.wrong_letter = 'Этой буквы нет в слове'
                self.losing = 'ПОТРАЧЕНО.'
                self.winning = 'Победа!'
                break
            else:
                print('Invalid input! Try again/Некорректный ввод. Попробуйте еще раз')

# принимает букву и чекает ее корректность
    def check_incorrect(self) -> bool:
        return (len(self.letter)) != 1 or \
                (self.language == 'Eng' and (ord(self.letter) < ord('a') or ord(self.letter) > ord('z'))) or \
                (self.language == 'Rus' and (ord(self.letter) < ord('а') or ord(self.letter) > ord('я')))

# чекает правильность хода
    def chek_true(self):
        if self.letter in self.SECRET:
            for i in range(len(self.SECRET)):
                if self.SECRET[i] == self.letter:
                    self.secret_letters[i] = self.letter
        else:
            self.your_letters.append(self.letter)
            print(self.wrong_letter)
            self.turn_number += 1

# чекает, не проиграл ли игрок
    def check_losing(self):
        return self.turn_number == len(self.FIELDS) - 1

# поражение
    def you_lost(self):
        print(self.FIELDS[self.turn_number])
        print(self.losing)
        print(self.SECRET)

# чекает, не выиграл ли игрок
    def check_winning(self):
        return ''.join(self.secret_letters) == self.SECRET

# победа
    def you_won(self):
        print(self.winning)
        print(self.SECRET.upper())

# печатает всякое
    def print_everything(self):
        print(''.join(self.secret_letters))
        print(self.FIELDS[self.turn_number])
        print(', '.join(set(self.your_letters)))

# собственно, запускает игру
    def run(self):
        self.chose_language()
        self.secret_letters = ['_'] * len(self.SECRET)
        while True:
            os.system('cls')
            self.print_everything()
            self.letter = input(self.letter_choosing).lower()
            if self.check_incorrect():
                print(self.invalid_letter)
                self.letter = ''
                continue
            self.chek_true()
            if self.check_losing():
                self.you_lost()
                break
            if self.check_winning():
                self.you_won()
                break


if __name__ == '__main__':
    h_game = HangmanGame()
    h_game.run()