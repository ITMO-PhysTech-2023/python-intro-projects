import time
from threading import Lock

from common.util import clear_terminal, terminal_size
from common.printer import FieldType, Printer


class MultiPrinter:
    def __init__(self, sleep_delta: float, game_count: int):
        self.sleep_delta = sleep_delta
        self.game_count = game_count
        self.fields = [[[]] for _ in range(game_count)]
        self.lock = Lock()

    def update_field(self, game_id: int, new_field: FieldType):
        self.lock.acquire()
        self.fields[game_id] = new_field
        self.lock.release()

    def print_fields(self):
        sep = '\n' + '=' * terminal_size()[0] + '\n'
        matrix = sep.join([
            '\n'.join([
                ''.join(row) for row in field
            ])
            for field in self.fields
        ])
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
