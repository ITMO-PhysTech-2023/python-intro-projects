import time
from abc import abstractmethod
import vars
from common.util import clear_terminal


class Print:
    @abstractmethod
    def output_to_screen(self, flicker, height_field, width_field):
        pass


class HorizontalPrint(Print):
    def output_to_screen(self, flicker, height_field, width_field):
        if height_field >= 9:
            while True:
                clear_terminal()
                for i in range(height_field):
                    if i <= 6:
                        print(''.join(vars.field_snake[i]), '  |  ', ''.join(vars.field_hangman[i]))
                    elif i == 7 or i == 8:
                        print(''.join(vars.field_snake[i]))
                    else:
                        print(''.join(vars.field_snake[i]))
                print()
                print()
                for row in vars.field_enter_p:
                    print(''.join(row))
                time.sleep(flicker)
        elif height_field == 7 or height_field == 8:
            while True:
                clear_terminal()
                for i in range(height_field):
                    if i <= 6:
                        print(''.join(vars.field_snake[i]), '  |  ', ''.join(vars.field_hangman[i]))
                    else:
                        print(' ' for row in range(width_field)), '  |  ', ''.join(vars.field_snake[i])
                print()
                print()
                for row in vars.field_enter_p:
                    print(''.join(row))
                time.sleep(flicker)
        else:
            while True:
                clear_terminal()
                for i in range(height_field):
                    if i <= 6:
                        print(''.join(vars.field_snake[i]), '  |  ', ''.join(vars.field_hangman[i]))
                    else:
                        print((' ' for row in range(width_field)), '  |  ', ''.join(vars.field_hangman[i]))
                print()
                print()
                for row in vars.field_enter_p:
                    print(''.join(row))
                time.sleep(flicker)


class VerticalPrint(Print):
    def output_to_screen(self, flicker, height_field, width_field):
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
