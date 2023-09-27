import copy
import time
from pynput import keyboard
from random import randint
import os

WIDTH, HEIGHT = 20, 20
SCREEN = list()
for i in range(HEIGHT - 1):
    SCREEN.append(WIDTH * ['.'])

direction = (-1, 0)


def process_press(key):
    # обработчик нажатия на клавиши (можно сделать и поаккуратнее)
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


def random_position():
    return [randint(1, HEIGHT - 2), randint(1, WIDTH - 2)]


counter = 0
snake_head = random_position()
snake = [copy.deepcopy(snake_head)]
apple = random_position()


def apple_generation():
    global apple
    while apple in snake:
        apple = random_position()
    return apple


# оно умеет мониторить нажатия на кнопки!
with keyboard.Listener(on_press=process_press) as listener:
    while True:
        field = ''
        screen = copy.deepcopy(SCREEN)
        screen[apple[0]][apple[1]] = 'a'
        for j in snake:
            screen[j[0]][j[1]] = 'o'
        screen[snake_head[0]][snake_head[1]] = 'S'
        if apple in snake:
            apple_generation()
            snake.insert(0, copy.deepcopy(snake_head))
            counter += 1
        else:
            snake.insert(0, copy.deepcopy(snake_head))
            snake.pop()
        snake_head[0] += direction[0]
        snake_head[1] += direction[1]
        for i in screen:
            field += ('  '.join(i) + '\n')
        print('\n' * 5)
        print(field)
        if (snake_head[0] not in range(len(screen))) or (snake_head[1] not in range(len(screen[1]))) or (snake_head in snake):
            print('Game over!\n Your score: ', counter)
            break
        time.sleep(0.25)
        pass
