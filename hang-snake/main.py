from threading import Thread
from snake.run import GameSnake
from hangman.run import GameHangman
from common.printer import HorizontalPrint, VerticalPrint
import vars


vars.init_var()
vars.a = 0

height_snake_field = 15
width_snake_field = 15

snake_game = GameSnake(height_snake_field, width_snake_field, 0.3)
hangman_game = GameHangman(vars.import_letter, None)
printer = HorizontalPrint()

thread_of_snake = Thread(target=snake_game.run())
thread_of_hangman = Thread(target=hangman_game.process())
thread_of_printer = Thread(target=printer.output_to_screen(1, height_snake_field, width_snake_field))

thread_of_snake.start()
thread_of_hangman.start()
thread_of_printer.start()
