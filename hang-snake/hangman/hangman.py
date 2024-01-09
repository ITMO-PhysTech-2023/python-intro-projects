from random import randint
import os


class HangmanGame:
    def __init__(self):
        self.field = [r'''
               +----+
               |    |
                    |
                    |
                    |
            _______/|\_
            ''', r'''
               +----+
               |    |
               o    |
                    |
                    |
            _______/|\_
            ''', r'''
               +----+
               |    |
               o    |
               |    |
                    |
            _______/|\_
            ''', r'''
               +----+
               |    |
               o    |
              /|    |
                    |
            _______/|\_
            ''', r'''
               +----+
               |    |
               o    |
              /|\   |
                    |
            _______/|\_
            ''', r'''
               +----+
               |    |
               o    |
              /|\   |
              /     |
            _______/|\_
            ''', r'''
               +----+
               |    |
               o    |
              /|\   |
              / \   |
            _______/|\_
            ''']
        self.secret = self.create_secret()
        self.conditions = 0
        self.answer = list('_' * len(self.secret))

    def create_secret(self):
        dictionary = ['CAPYBARA', 'PHYSICS', 'POLINA']
        return list(dictionary[randint(0, 2)])

    def check_letter(self, letter, secret, answer):
        for i in range(len(secret)):
            if letter == secret[i]:
                answer[i] = secret[i]
        return answer

    def run(self):
        print(self.field[0])
        while True:
            print(*self.answer)
            letter = input('Enter your guess: ')
            new_answer = self.check_letter(letter, self.secret, self.answer.copy())
            if new_answer == self.answer:
                self.conditions += 1
            self.answer = new_answer
            os.system('cls' if os.name == 'nt' else 'clear')
            print(self.field[self.conditions])
            if self.conditions == 6:
                print('YOU LOSE')
                break
            if self.answer == self.secret:
                print('TUTURU')
                break
