import threading
from threading import Thread
from hangman.run import Hangmangame
from providers import RandomLetterProvider, SecretLetterProvider
from snake.run import Snakegame
import  time

s_game = Snakegame(RandomLetterProvider(), SecretLetterProvider())
h_game = Hangmangame()


def play_snake():
    if s_game.chosen_letter is None:
        s_game.run()


def play_hang():
    while s_game.chosen_letter is not None:
        s_game.Playing = False
        print(s_game.chosen_letter)


while True:
    play_snake()
    play_hang()





# lock = threading.Lock()
# value = None
# letter = None
#
#
# def run_snake_game():
#     global value, letter
#     s_game = Snakegame(RandomLetterProvider(), SecretLetterProvider())
#     s_game.run()
#     letter = s_game.chosen_letter
#     print(letter)
    # if letter is not None:
    #     lock.acquire()
    #     print(letter)
    #     time.sleep(5)
    #     value = "Value from Game 1"
    #     lock.release()  # Release the lock after setting the variables


# def run_hangman_game():
#     global value, letter
#     lock.acquire()
#     if value is not None:
#         lock.release()  # Release the lock before starting Hangmangame
#         h_game = Hangmangame(letter)
#         h_game.run()
#         letter = None
#         value = None


# s_thread = Thread(target=run_snake_game)
# h_thread = Thread(target=run_hangman_game)
# s_thread.start()
# h_thread.start()
