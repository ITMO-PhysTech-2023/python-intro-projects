from threading import Thread

# from hangman.FIELD import FIELD
# from hangman.run import Hangmangame
from providers import LetterProvider, RandomLetterProvider, HangmanLetterProvider
from snake.run import Snakegame

# h_game = Hangmangame(
#     RandomLetterProvider(),
#     1
# )
s_game = Snakegame(

    RandomLetterProvider(),
    HangmanLetterProvider()
)

# h_thread = Thread(target=h_game.run)
s_thread = Thread(target=s_game.run)
# h_thread.start()
s_thread.start()


'''
1. Parallel print -- potentially add Printer class
2. LetterProvider that gets letters from Snake
3. Add option to perform custom action on object eaten to Snake
'''