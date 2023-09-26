import copy
import time
from pynput import keyboard
from random import randint

WIDTH, HEIGHT = 20, 10
SCREEN = list()
SCREEN.append(WIDTH * ['_'])
for i in range(HEIGHT - 2):
    SCREEN.append(['|'] + (WIDTH - 2) * [' '] + ['|'])
SCREEN.append(WIDTH * ['_'])

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
snake = [random_position()]
apple = random_position()
while apple in snake:
    apple = random_position()

# оно умеет мониторить нажатия на кнопки!
with keyboard.Listener(on_press=process_press) as listener:
    while True:
        screen = copy.deepcopy(SCREEN)
        screen[apple[0]][apple[1]] = 'a'
        screen[snake[0][0]][snake[0][1]] = 'S'
        if apple in snake:
            apple = random_position()
            counter += 1
        snake[0][0] += direction[0]
        snake[0][1] += direction[1]
        for i in screen:
            print(''.join(i))
        if (snake[0][0] not in range(len(screen))) or (snake[0][1] not in range(len(screen[1]))):
            print('Game over!\n Your score: ', counter)
            break
        time.sleep(0.25)
        pass
