from threading import Thread

from connection.multiprinter import MultiPrinter
from hangman.run import HangmanGame
from hangman.provider import RandomLetterProvider
from snake.run import SnakeGame

printer = MultiPrinter(0.25, 2)
h_game = HangmanGame(
    RandomLetterProvider(),
    0.5,
    printer.create_printer(0)
)
s_game = SnakeGame(
    10, 10,
    0.2,
    printer.create_printer(1)
)

h_thread = Thread(target=h_game.run)
s_thread = Thread(target=s_game.run)
h_thread.start()
s_thread.start()
printer.run()
'''
1. Parallel print -- potentially add Printer class
2. LetterProvider that gets letters from Snake
3. Add option to perform custom action on object eaten to Snake
'''

# h_thread.join()
# s_thread.join()
