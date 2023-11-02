from pynput import keyboard

hard_level = int(input('enter level of hard: '))
secret_word = input('enter secret word: ').lower()
a = 0
import_letter = None
last_letter = []
to_stop = None
field_snake = None
field_hangman = None
field_enter_p = None


def repeat(key):
    global a
    if key == keyboard.Key.space:
        a = 'continue'
    else:
        a = 'break'


def proposal_repeat():
    print()
    print('If you want to try again press to space. If you want to stop press other')


def init_var():
    global a, import_letter, last_letter, to_stop, field_hangman, field_snake


def init_input_var():
    global hard_level, secret_word
