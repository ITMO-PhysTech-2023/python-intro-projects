import threading
from threading import Thread
import sys
sys.path.insert(1, 'C:/Users/LIZA/PycharmProjects/python-intro-projects/hang-snake/')
from hangman.run import Hangmangame
from snake.run import Snakegame
from providers import QueueProvider
from common.multiprinter import MultiPrinter
from common.util import hide_cursor

printer = MultiPrinter(0.3, 2)
provider = QueueProvider()


lock = threading.Lock()
s_game = Snakegame(printer.create_printer(1))
h_game = Hangmangame(provider, printer.create_printer(0))


def letter_handler():
    provider.add_letter(s_game.chosen_letter)


s_game.add_object_eaten_callback(letter_handler)


h_thread = Thread(target=h_game.run, daemon=True)
s_thread = Thread(target=s_game.run, daemon=True)

if __name__ == '__main__':
    hide_cursor()
    s_thread.start()
    h_thread.start()
    printer.run()
    h_thread.join()
    s_thread.join()
