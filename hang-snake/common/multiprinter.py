import time
from threading import Lock
from common.util import clear_terminal, terminal_size
from common.printer import FieldType, Printer
import sys


class MultiPrinter:
    def __init__(self, sleep_delta: float, game_count: int, direction='h'):
        self.sleep_delta = sleep_delta
        self.game_count = game_count
        self.fields = [[[]] for _ in range(game_count)]
        self.lock = Lock()
        self.direction = direction

    def update_field(self, game_id: int, new_field: FieldType):
        width = max([len(row) for row in new_field])
        for i, row in enumerate(new_field):
            new_field[i] += [' ' for _ in range(width - len(row))]
        self.lock.acquire()
        self.fields[game_id] = new_field
        self.lock.release()

    def print_fields(self):
        if sys.stdin.isatty():
            time.sleep(3)
        if self.direction == 'v':
            fields_strings = [
                '\n'.join([
                    ''.join(row) for row in field
                ])
                for field in self.fields
            ]
            sep = '\n' + '=' * 10 + '\n'
            matrix = sep.join(fields_strings)
        else:
            height = max([len(field) for field in self.fields])
            width = sum([len(field[0]) for field in self.fields]) + self.game_count - 1
            x = 0
            matrix = [[' ' for _ in range(width)] for _2 in range(height)]
            for field in self.fields:
                y = (height - len(field)) // 2
                for i, row in enumerate(field):
                    for j, char in enumerate(row):
                        matrix[y + i][x + j] = char
                x += len(field[0]) + 1
            matrix = '\n'.join([''.join(row) for row in matrix])
        self.lock.acquire()
        print(matrix)
        self.lock.release()

    def run(self):
        while True:
            clear_terminal()
            self.print_fields()
            time.sleep(self.sleep_delta)

    def create_printer(self, game_id: int) -> Printer:
        class PrinterProxy(Printer):
            # noinspection PyMethodParameters
            def print_field(proxy, field: FieldType):
                self.update_field(game_id, field)

        return PrinterProxy()
