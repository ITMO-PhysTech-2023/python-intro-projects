import random
import time

from pynput import keyboard

from common.util import clear_terminal, terminal_size


def opposite_directions(d1: tuple[int, int], d2: tuple[int, int]):
    return d1[0] == -d2[0] and d1[1] == -d2[1]


class Snake:
    SYMBOL = '■'

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
            matrix[row][col] = Snake.SYMBOL

    def has_collision(self):
        return self.cells[0] in self.cells[1:]


class EatableObject:
    def __init__(self, position: tuple[int, int], display: str):
        self.position = position
        self.display = display


class Field:
    NEUTRAL = '.'

    def __init__(self, height: int, width: int):
        self.height = height
        self.width = width
        self.snake = Snake(self.random_position())
        self.objects = {
            'apple': self.generate_object('a')
        }

    def random_position(self) -> tuple[int, int]:
        return (random.randint(0, self.height - 1),
                random.randint(0, self.width - 1))

    def generate_object(self, display: str) -> EatableObject:
        position = self.random_position()
        if position in self.snake.cells:
            position = self.random_position()
        return EatableObject(position, display)

    def move_snake(self, direction: tuple[int, int]):
        self.snake.grow(direction)
        self.snake.fix_to_bounds(self.height, self.width)
        food_eaten = False
        snake_head = self.snake.cells[0]
        for key, item in self.objects.items():
            if item.position == snake_head:
                food_eaten = True
                self.objects[key] = self.generate_object(item.display)
                break
        if not food_eaten:
            self.snake.cut_tail()

    def is_filled(self):
        return self.height * self.width == len(self.snake)

    def print(self):
        matrix = [
            [Field.NEUTRAL for _ in range(self.width)]
            for _2 in range(self.height)
        ]
        self.snake.draw_on(matrix)
        for item in self.objects.values():
            row, col = item.position
            matrix[row][col] = item.display
        for row in matrix:
            print(''.join(row))


class SnakeGame:
    def __init__(self, height: int, width: int, step_sleep: float):
        self.field = Field(height, width)
        self.direction = (1, 0)
        self.step_sleep = step_sleep

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
        if new_direction is None or opposite_directions(self.direction, new_direction):
            return
        self.direction = new_direction

    def step(self):
        self.field.move_snake(self.direction)
        time.sleep(self.step_sleep)

    def run(self):
        with keyboard.Listener(on_press=self.process_press):
            while True:
                clear_terminal()
                self.field.print()
                self.step()

                if self.field.snake.has_collision():
                    print('Snake died :(')
                    break
                if self.field.is_filled():
                    print('You won!')
                    break


# width, height = terminal_size()
width, height = 10, 10
game = SnakeGame(height, width, 0.1)
game.run()
