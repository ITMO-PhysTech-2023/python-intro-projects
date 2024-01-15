import os


def terminal_size():
    return os.get_terminal_size()


def clear_terminal():
    h = os.get_terminal_size()[0]
    print(f'\033[{h}A\033[3J')