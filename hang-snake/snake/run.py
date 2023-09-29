from pynput import keyboard
import time
import os
from random import randint


'''
class Snake:
    def __init__(self):
        pass

    def move(self, direction: tuple[int, int]):
        pass
'''




def random_position(self):
    row = randint(1, HEIGHT - 2)
    col = randint(1, WIDTH - 2)
    while (col, row) in snake:  # проверяем не в змею ли сгенерировалось
        row = randint(1, HEIGHT - 2)
        col = randint(1, WIDTH - 2)
    return (col, row)


def print_field(self):
    for cell in CELLS:
        if cell in snake:
            print('s', end='')
        elif cell[0] in (0, WIDTH - 1):
            print('|', end='')
        elif cell[1] in (0, HEIGHT - 1):
            print('_', end='')
        elif cell == apple:
            print('a', end='')
        else:
            print(' ', end='')
        if cell[0] == WIDTH - 1:
            print('')


def snake_move(self):
    global eat
    head_snake = snake[0][0] + direction[0], snake[0][1] + direction[1]
    # делаем змейке новую голову, чтобы она ползла вперед
    snake.insert(0, head_snake)
    if not eat:  # если змея не съела яблоко то удаляем хвост
        snake.pop()
    else:
        eat = False


def apple_random(self):
    global apple, eat
    if apple == snake[0]:
        apple = random_position()
        eat = True


def process_press(key):
    # обработчик нажатия на клавиши (можно сделать и поаккуратнее)
    global direction, flag
    match key:
        case keyboard.Key.left:
            direction = (-1, 0)
        case keyboard.Key.up:
            direction = (0, -1)
        case keyboard.Key.right:
            direction = (1, 0)
        case keyboard.Key.down:
            direction = (0, 1)
        case keyboard.Key.esc:
            flag = True

# генерируем позицию яблока
def random_position():
    row = randint(1, HEIGHT - 2)
    col = randint(1, WIDTH - 2)
    while (col, row) in snake:  # проверяем не в змею ли сгенерировалось
        row = randint(1, HEIGHT - 2)
        col = randint(1, WIDTH - 2)
    return(col, row)


# наше поле
def print_field():
    for cell in CELLS:
        if cell in snake:
            print('s', end = '')
        elif cell[0] in (0, WIDTH - 1):
            print('|', end = '')
        elif cell[1] in (0, HEIGHT - 1):
            print('_', end = '')
        elif cell == apple:
            print('a', end = '')
        else:
            print(' ', end = '')

        if cell[0] == WIDTH -1:
            print('')


# змейка ползает
def snake_move():
    global eat
    head_snake = snake[0][0] + direction[0], snake[0][1] + direction[1]
    # делаем змейке новую голову, чтобы она ползла вперед
    snake.insert(0, head_snake)
    if not eat: # если змея не съела яблоко то удаляем хвост
        snake.pop()
    else:
        eat = False


# механизм поедания яблока
def apple_random():
    global apple, eat
    if apple == snake[0]:
        apple = random_position()
        eat = True

WIDTH, HEIGHT = 30, 15  # параметры поля
CELLS = [(col, row) for row in range(HEIGHT) for col in range(WIDTH)]

snake = [(5, HEIGHT // 2), (4, HEIGHT // 2), (3, HEIGHT // 2)]  # генерируем змею на поле
apple = random_position()  # генерируем яблоко на поле
eat = False  # проверка съедено ли яблоко
flag = False  # завели отдельную метку для того, чтобы выключать змейку


# управление
def process_press(key):
    # обработчик нажатия на клавиши (можно сделать и поаккуратнее)
    global direction, flag
    match key:
        case keyboard.Key.left:
            direction = (-1, 0)
        case keyboard.Key.up:
            direction = (0, -1)
        case keyboard.Key.right:
            direction = (1, 0)
        case keyboard.Key.down:
            direction = (0, 1)
        case keyboard.Key.esc:
            flag = True


direction = (1, 0)

WIDTH = 30
HEIGHT = 15
snake = [(5, HEIGHT // 2), (4, HEIGHT // 2), (3, HEIGHT // 2)]
direction = (1, 0)
apple = random_position()
eat = False
Flag = False
CELLS = [(col, row) for row in range(HEIGHT) for col in range(WIDTH)]



# делаем больше одного хода
with keyboard.Listener(on_press=process_press) as listener:
    while True:
        os.system('cls')
        print_field()
        apple_random()
        snake_move()

        # проверяем не врезалась ли змейка в границы и в себя
        if snake[0][0] in (0, WIDTH) or\
            snake[0][1] in (0, HEIGHT) or\
            snake[0] in snake[1:] or\
            flag:  # оно умеет выключаться при нажатии Esc
            os.system('cls')
            print('Game Over')
            break

        time.sleep(0.3)
