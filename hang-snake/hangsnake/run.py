from pynput import keyboard
from time import sleep
from common.util import clear_terminal, HANGMAN_FIELDS
from common.hangman import Hangman
from common.words import choice_word, letter_noise
from common.snake import SnakeGame

word = choice_word()

hg = Hangman(word)
snake = SnakeGame(
        apples=list(word) + letter_noise(max(15 - len(word), 2)),
        is_apples_finite=True,
        )
snake.before_eat_apple = lambda w: hg.guess(w)
with keyboard.Listener(on_press=snake.on_key_press()) as listener:
    while True:
        fs = HANGMAN_FIELDS[hg.fails].splitlines()
        fs[0] += f" Word: {hg.get_partial_word()}"
        print("\n".join(fs))
        snake.draw_screen()
        snake.loop()
        sleep(.1) # <-- Change here to .2 to test
        clear_terminal()
        if hg.get_partial_word() == hg.word:
            print("you won!!1!")
            exit(0)

