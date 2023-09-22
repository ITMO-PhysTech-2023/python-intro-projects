import os
from time import sleep
# from common.util import clear_terminal
from pynput import keyboard
from random import randint

WIDTH, HEIGHT = 8, 8
# можно приделать конфиг-файл с параметрами
direction = (0, 0)
FIELD = [['o' for x in range(WIDTH)] for h in range(HEIGHT)]


# STROKA=''.join([' ' for x in range(WIDTH)])
# STROKA=STROKA+'\n'
# for i in range(HEIGHT):
#     FIELD.append(STROKA)

# print('\n'.join([''.join(row) for row in FIELD]))
def random_position():
    return randint(0, HEIGHT - 1), randint(0, WIDTH - 1)


def process_press(key):
    global direction
    match key:
        case keyboard.Key.left:
            direction = (0, -1)
        case keyboard.Key.up:
            direction = (-1, 0)
        case keyboard.Key.right:
            direction = (0, 1)
        case keyboard.Key.down:
            direction = (1, 0)


snake = [random_position()]
apple = random_position()
lenght = 1
FIELD[snake[0][0]][snake[0][1]] = 's'
FIELD[apple[0]][apple[1]] = 'a'
print('\n'.join([''.join(row) for row in FIELD]))
print()
while apple in snake:
    apple = random_position()
    lenght += 1
w = 0


def clear_terminal():
    cmd = 'cls' if os.name == 'nt' else 'clear'
    os.system(cmd)


def update_field():
    for row in range(len(FIELD)):
        for column in range(len(FIELD[0])):
            FIELD[row][column] = 'o'
    for i in snake:
        FIELD[i[0]][i[1]] = 's'
    FIELD[apple[0]][apple[1]] = 'a'


with keyboard.Listener(on_press=process_press) as listener:
    while True:
        clear_terminal()
        snake[-1] = (snake[-1][0] + direction[0], snake[-1][1] + direction[1])
        update_field()
        print('\n'.join([''.join(row) for row in FIELD]))
        print()
        print(direction)
        sleep(1)
        # if apple==snake:
        #     lenght+=1
        #     FIELD[apple[0]][apple[1]]='s'
        #     snake.append(FIELD[apple[0]][apple[1]])
        # pass
