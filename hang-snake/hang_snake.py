from snake.snake import SnakeGame
from hangman.hangman import HangmanGame
import os
from pynput import keyboard
from string import ascii_uppercase
from random import randint
from time import sleep


class HangSnakeGame:
    def __init__(self, width, height):
        self.hangman_game = HangmanGame()
        self.snake_game = SnakeGame(width, height, amount_of_apples=3)

    def run(self):
        print(self.hangman_game.field[0])
        self.snake_game.random_snake_head_position()
        with keyboard.Listener(on_press=self.snake_game.process_press):
            while True:
                print(*self.hangman_game.answer)
                self.snake_game.create_new_apples_positions(ascii_uppercase[randint(0, 25)],
                                                            ascii_uppercase[randint(0, 25)],
                                                            list(filter(lambda x: x not in self.hangman_game.answer,
                                                                        self.hangman_game.secret))[
                                                                randint(0,
                                                                        len(list(
                                                                            filter(lambda
                                                                                       x: x not in self.hangman_game.answer,
                                                                                   self.hangman_game.secret))) - 1)])
                while True:
                    self.snake_game.print_field()
                    sleep(1)
                    self.snake_game.precess_loose_conditionals()
                    letter = self.snake_game.process_eat()
                    if letter is not None:
                        break
                    self.snake_game.snake.process_move(self.snake_game.direction)
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print(self.hangman_game.field[self.hangman_game.conditions])
                    print(*self.hangman_game.answer)
                new_answer = self.hangman_game.check_letter(letter, self.hangman_game.secret,
                                                            self.hangman_game.answer.copy())
                if new_answer == self.hangman_game.answer:
                    self.hangman_game.conditions += 1
                self.hangman_game.answer = new_answer
                os.system('cls' if os.name == 'nt' else 'clear')
                print(self.hangman_game.field[self.hangman_game.conditions])
                if self.hangman_game.conditions == 6:
                    print('YOU LOSE')
                    break
                if self.hangman_game.answer == self.hangman_game.secret:
                    print('TUTURU')
                    break