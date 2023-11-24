from abc import ABC, abstractmethod

from common.util import clear_terminal

FieldType = list[list[str]]


class Printer(ABC):
    @abstractmethod
    def print_field(self, field: FieldType):
        pass


class DefaultPrinter(Printer):
    def print_field(self, field: FieldType):
        clear_terminal()
        for row in field:
            print(''.join(row))


class ReversePrinter(Printer):
    def print_field(self, field: FieldType):
        for row in reversed(field):
            print(''.join(row))
