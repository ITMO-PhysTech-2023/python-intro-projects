# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from pynput import keyboard
from random import randint
import time

# WIDTH, HEIGHT = 20,20

direc = 2
x = 0
y = 0


class SnakeGame:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.direction = (1, 0)
        # self.snake=Snake(...)


Snake = SnakeGame(width=int(input()), height=int(input()))


# можно приделать конфиг-файл с параметрами
# direction = (1, 0)


def random_position():
    position = []
    position = [randint(0, Snake.height - 1), randint(0, Snake.width - 1)]
    return position


def process_press(key):
    # обработчик нажатия на клавиши (можно сделать и поаккуратнее)
    global direction
    global direc
    match key:
        case keyboard.Key.left:
            direction = (0, -1)
            direc = 4
        case keyboard.Key.up:
            direction = (-1, 0)
            direc = 3
        case keyboard.Key.right:
            direction = (0, 1)
            direc = 2
        case keyboard.Key.down:
            direction = (1, 0)
            direc = 1


snake = random_position()
apple = random_position()
print(*snake, *apple)

MAP = ['_'] * 20
for ii in range(0, 20):
    MAP[ii] = ['_'] * 20

VOID = [''] * 20
for iii in range(0, 20):
    VOID[iii] = [''] * 20
# while apple[0] == snake[0]:
#     new_apple = [random_position()]
#     apple=new_apple
for i in range(0, len(MAP)):
    for j in range(0, len(MAP)):
        print(MAP[i][j], end='')
    print()

# # оно умеет мониторить нажатия на кнопки!
with keyboard.Listener(on_press=process_press) as listener:
    while True:
        if (int(snake[0]) == Snake.height or int(snake[0]) == -1 or int(snake[1]) == -1 or int(
                snake[1]) == Snake.width):
            break
        else:
            if (apple[1] == snake[1] and apple[0] == snake[0]):
                new_apple = random_position()
                apple = new_apple
        MAP[apple[0]][apple[1]] = '$'
        MAP[x][y] = '_'
        if (direc == 1):
            x = x + 1
            y = y
        if (direc == 2):
            x = x
            y = y + 1
        if (direc == 3):
            x = x - 1
            y = y
        if (direc == 4):
            x = x
            y = y - 1
        time.sleep(0.3)
        MAP[x][y] = '*'
        for i in range(0, len(MAP)):
            for j in range(0, len(MAP)):
                print(VOID[i][j], end='')
            print()
        for i in range(0, len(MAP)):
            for j in range(0, len(MAP)):
                print(MAP[i][j], end='')
            print()

        pass
