from threading import Lock
import time
from abc import abstractmethod

import vars
from common.util import clear_terminal
from vars import field_hangman, field_snake, field_enter_p


class Print:
    @abstractmethod
    def output_to_screen(self, flicker):
        pass


class HorizontalPrint(Print):
    def output_to_screen(self, flicker):
        while True:
            clear_terminal()
            time.sleep(flicker)


class VerticalPrint(Print):
    def output_to_screen(self, flicker):
        while True:
            clear_terminal()
            for row in vars.field_hangman:
                print(''.join(row))
            print()
            print()
            for row in vars.field_enter_p:
                print(''.join(row))
            print()
            print()
            for row in vars.field_snake:
                print(''.join(row))
            time.sleep(flicker)
