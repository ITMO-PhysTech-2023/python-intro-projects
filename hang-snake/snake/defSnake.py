import os


def terminal_size():
    return os.get_terminal_size()


def clear_terminal():
    cmd = 'clear'
    os.system(cmd)