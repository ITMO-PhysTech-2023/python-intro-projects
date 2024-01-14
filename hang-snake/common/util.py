import shutil


def terminal_size():
    return os.get_terminal_size()


def clear_terminal():
    h = shutil.get_terminal_size()[0]
    print(f'\033[{h}A\033[3J')


def hide_cursor():
    print("\033[?25l")