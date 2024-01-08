from common.util import clear_terminal
import time
import random
import pathlib


class Secret:
    @staticmethod
    def create_secret():
        with open(pathlib.Path(pathlib.Path.cwd(), 'hangman', 'secrets.txt')) as secrets:
            secrets = secrets.readlines()
            secret_number = random.randint(0, len(secrets) - 1)
            return secrets[secret_number][:-1]


class Game:
    global secret_word, number_of_letters, eng_alphabet
    eng_alphabet = "abcdefghijklmnopqrstuvwxyz"
    secret_word = Secret().create_secret()
    number_of_letters = len(secret_word)
    def __init__(self):
        self.used_letters = ""
        self.guessed_letters = ""
        self.mistakes = 0

        self.fields = [r'''
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
        ''']

    def game_start(self):
        while True:
            if len(set(self.guessed_letters)) == len(set(secret_word)) or self.mistakes == 6:
                break
            clear_terminal()
            print(self.fields[0])

            time.sleep(1)

            clear_terminal()
            print('Word: ', end='')
            for i in range(len(secret_word)):
                if secret_word[i] in self.guessed_letters:
                    print(secret_word[i], end='')
                else:
                    print('_', end='')
            print('\nUsed letters: ', self.used_letters)
            letter = input('Enter Your guess: ').lower()

            if not(letter in eng_alphabet):
                print('Invalid guess! Try again')
                time.sleep(0.7)
                continue

            if not(letter in self.used_letters):
                self.used_letters += letter + ","

            if not (letter in secret_word):
                self.fields.pop(0)
                self.mistakes += 1
            else:
                self.guessed_letters += letter

        clear_terminal()
        print(self.fields[0])
        time.sleep(1)
        if self.mistakes == 6:
            print('You lose!')
        else:
            print('You won!')
        print('The hidden word was', secret_word)
