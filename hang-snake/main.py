from threading import Thread
from pynput import keyboard
from snake.run import GameSnake
from hangman.run import GameHangman
from common.printer import Print, HorizontalPrint, VerticalPrint
import vars


vars.init_var()
vars.a = 0

snake_game = GameSnake(15, 15, 0.3)
hangman_game = GameHangman(vars.import_letter, None)
printer = VerticalPrint()

thread_of_snake = Thread(target=snake_game.run())
thread_of_hangman = Thread(target=hangman_game.process())
thread_of_printer = Thread(target=printer.output_to_screen(0.1))

thread_of_snake.start()
thread_of_hangman.start()
thread_of_printer.start()
