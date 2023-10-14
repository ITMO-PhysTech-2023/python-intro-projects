import threading
from threading import Thread
from hangman.run import Hangmangame
from providers import RandomLetterProvider, SecretLetterProvider, QueueProvider
from snake.run import Snakegame

lock = threading.Lock()
s_game = Snakegame(RandomLetterProvider(), SecretLetterProvider())
h_game = Hangmangame(QueueProvider())
provider = QueueProvider()


def letter_handler():
    provider.add_letter(s_game.chosen_letter)


s_game.add_object_eaten_callback(letter_handler)

h_thread = Thread(target=h_game.run, daemon=True)
s_thread = Thread(target=s_game.run, daemon=True)

h_thread.start()
s_thread.start()
h_thread.join()
s_thread.join()
