import random
import time
from abc import ABC, abstractmethod
from threading import Lock
from typing import Callable

from pynput import keyboard

from common.printer import DefaultPrinter, Printer
from common.util import clear_terminal


def opposite_directions(d1: tuple[int, int], d2: tuple[int, int]):
    return d1[0] == -d2[0] and d1[1] == -d2[1]


class Snake:
    SNAKE_CHR = '■'

    def __init__(self, initial_cell: tuple[int, int]):
        self.cells = [initial_cell]

    def __len__(self):
        return len(self.cells)

    def grow(self, direction: tuple[int, int]):
        head_row, head_col = self.cells[0]
        new_head = (head_row + direction[0], head_col + direction[1])
        self.cells.insert(0, new_head)

    def fix_to_bounds(self, height: int, width: int):
        row, col = self.cells[0]
        self.cells[0] = (row % height, col % width)

    def cut_tail(self):
        self.cells.pop()

    def draw_on(self, matrix: list[list[str]]):
        for row, col in self.cells:
            matrix[row][col] = Snake.SNAKE_CHR

    def has_collision(self):
        return self.cells[0] in self.cells[1:]


class EatableObject(ABC):
    def __init__(self, position: tuple[int, int], display: str):
        self.position = position
        self.display = display

    @abstractmethod
    def regenerate(self, position: tuple[int, int]):
        pass


EatableObjectFactory = Callable[[tuple[int, int]], EatableObject]


class AppleObject(EatableObject):
    APPLE_CHR = '●'

    def __init__(self, position: tuple[int, int]):
        super().__init__(position, AppleObject.APPLE_CHR)

    def regenerate(self, position: tuple[int, int]):
        return AppleObject(position)


class Field:
    NEUTRAL = '·'

    def __init__(self, height: int, width: int, initial_objects: list[EatableObjectFactory]):
        self.height = height
        self.width = width
        self.snake = Snake(self.random_position())
        self.objects = [AppleObject(self.random_object_position())]
        for item_factory in initial_objects:
            self.objects.append(item_factory(self.random_object_position()))

    def random_position(self) -> tuple[int, int]:
        return (random.randint(0, self.height - 1),
                random.randint(0, self.width - 1))

    def random_object_position(self) -> tuple[int, int]:
        item_positions = (
            {item.position for item in self.objects if item is not None}
            if hasattr(self, 'objects')
            else {}
        )
        position = self.random_position()
        if position in self.snake.cells or position in item_positions:
            position = self.random_position()
        return position

    def move_snake(self, direction: tuple[int, int]) -> EatableObject | None:
        self.snake.grow(direction)
        self.snake.fix_to_bounds(self.height, self.width)
        food_eaten = None
        snake_head = self.snake.cells[0]
        for i, item in enumerate(self.objects):
            if item is None:
                continue
            if item.position == snake_head:
                food_eaten = item
                self.objects[i] = item.regenerate(self.random_object_position())
                break
        if not isinstance(food_eaten, AppleObject):
            self.snake.cut_tail()
        return food_eaten

    def is_filled(self):
        return self.height * self.width == len(self.snake)

    def build_matrix(self):
        matrix = [
            [Field.NEUTRAL for _ in range(self.width)]
            for _2 in range(self.height)
        ]
        self.snake.draw_on(matrix)
        for item in self.objects:
            if item is None:
                continue
            row, col = item.position
            matrix[row][col] = item.display
        return matrix


class SnakeGame:
    def __init__(
            self, height: int, width: int,
            step_sleep: float,
            printer: Printer,
            initial_items: list[EatableObjectFactory]
    ):
        self.field = Field(height, width, initial_items)
        self.direction = (1, 0)
        self.direction_lock = Lock()
        self.direction_change_wait = False
        self.step_sleep = step_sleep
        self.printer = printer
        self.callbacks = []

    def add_object_eaten_callback(self, callback: Callable[[EatableObject], ...]):
        self.callbacks.append(callback)

    @staticmethod
    def opposite_directions(d1: tuple[int, int], d2: tuple[int, int]):
        return d1[0] == -d2[0] and d1[1] == -d2[1]

    def process_press(self, key):
        mapping = {
            keyboard.Key.left: (0, -1),
            keyboard.Key.up: (-1, 0),
            keyboard.Key.down: (1, 0),
            keyboard.Key.right: (0, 1)
        }
        new_direction = mapping.get(key, None)
        with self.direction_lock:
            if new_direction is None or opposite_directions(self.direction, new_direction):
                return
            if self.direction_change_wait:
                return
            self.direction = new_direction
            self.direction_change_wait = True

    def step(self):
        object_eaten = self.field.move_snake(self.direction)
        if object_eaten is not None:
            for callback in self.callbacks:
                callback(object_eaten)
        self.direction_change_wait = False
        time.sleep(self.step_sleep)

    def status(self):
        if self.field.snake.has_collision():
            return 'Snake died :('
        if self.field.is_filled():
            return 'You won!'

    def print(self):
        extra_lines = []
        if (status := self.status()) is not None:
            extra_lines.append(status)
        matrix = self.field.build_matrix()
        for line in extra_lines:
            matrix += [list(line)]
        self.printer.print_field(matrix)

    def run(self):
        with keyboard.Listener(on_press=self.process_press):
            while True:
                clear_terminal()
                self.step()
                self.print()
                if self.status() is not None:
                    self.print()
                    break


if __name__ == '__main__':
    # width, height = terminal_size()
    width, height = 10, 10
    printer = DefaultPrinter()
    game = SnakeGame(height, width, 0.1, printer, [])
    game.run()
