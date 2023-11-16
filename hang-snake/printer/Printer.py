from random import randint
import time
import pygame
import random
import time
from common.util import clear_terminal
from hangman.provider import LetterProvider, KeyboardLetterProvider
from snake.run import SnakeGame, eatableobject
from hangman.run import HangmanGame, Field
from printer.secret import Secret

#provider = KeyboardLetterProvider()
secr = Secret()
#game1 = HangmanGame(provider, secr, 1)
game = SnakeGame(secr,width=10, height=10,headx=100,heady=100,speed=10,length=1)
game.run()