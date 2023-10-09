from threading import Thread

from hangman.run import Hangmangame
from providers import RandomLetterProvider, HangmanLetterProvider, SnakeLetterProvider
from snake.run import Snakegame

h_game = Hangmangame(
     SnakeLetterProvider(Snakegame.self.choose_letter()),
     1
)
s_game = Snakegame(

    RandomLetterProvider(),
    HangmanLetterProvider()
)

h_thread = Thread(target=h_game.run)
s_thread = Thread(target=s_game.run)
h_thread.start()
s_thread.start()
