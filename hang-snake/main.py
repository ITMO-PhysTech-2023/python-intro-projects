from threading import Thread

from common.util import hide_cursor
from connection.multiprinter import MultiPrinter
from hangman.provider import QueueProvider
from hangman.run import HangmanGame
from snake.run import AppleObject, EatableObject, SnakeGame

ALPHA = map(chr, range(ord('a'), ord('z') + 1))

printer = MultiPrinter(0.04, 2)
provider = QueueProvider()


class LetterObject(EatableObject):
    UNUSED_LETTERS = set(ALPHA)
    ALL_OBJECTS = []

    def __init__(self, position: tuple[int, int]):
        letter = LetterObject.UNUSED_LETTERS.pop()
        super().__init__(position, letter)
        self.eaten = False
        LetterObject.ALL_OBJECTS.append(self)

    def regenerate(self, position: tuple[int, int]):
        self.eaten = True
        if len(LetterObject.UNUSED_LETTERS) == 0:
            return None
        if h_game.is_won():
            return None
        return LetterObject(position)

    def change_letter(self):
        if len(LetterObject.UNUSED_LETTERS) == 0:
            return
        old_letter = self.display
        self.display = LetterObject.UNUSED_LETTERS.pop()
        LetterObject.UNUSED_LETTERS.add(old_letter)


class ReloadObject(EatableObject):
    RELOAD_CHR = '⭯'

    def __init__(self, position: tuple[int, int]):
        super().__init__(position, ReloadObject.RELOAD_CHR)

    def regenerate(self, position: tuple[int, int]):
        return ReloadObject(position)


def letter_handler(eatable_object: EatableObject):
    if isinstance(eatable_object, LetterObject):
        provider.add_letter(eatable_object.display)
    elif isinstance(eatable_object, ReloadObject):
        for item in LetterObject.ALL_OBJECTS:
            if item.eaten:
                continue
            item.change_letter()


def speed_handler(eatable_object: EatableObject):
    if isinstance(eatable_object, AppleObject):
        s_game.step_sleep /= 1.1


h_game = HangmanGame(
    provider,
    0.5,
    printer.create_printer(0)
)
s_game = SnakeGame(
    25, 25,
    0.2,
    printer.create_printer(1),
    [
        LetterObject,
        LetterObject,
        LetterObject,
        LetterObject,
        LetterObject,
        ReloadObject
    ]
)
s_game.add_object_eaten_callback(letter_handler)
s_game.add_object_eaten_callback(speed_handler)

h_thread = Thread(target=h_game.run, daemon=True)
s_thread = Thread(target=s_game.run, daemon=True)

if __name__ == '__main__':
    hide_cursor()
    h_thread.start()
    s_thread.start()
    printer.run()

    h_thread.join()
    s_thread.join()
