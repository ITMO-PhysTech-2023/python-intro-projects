from pynput import keyboard
from common.util import clear_terminal
import random
import time

def create_apple(WIDTH,HEIGH):
    return (random.randint(0,WIDTH-1), random.randint(0,HEIGH-1))

def field():
    clear_terminal()
    print('-' + '-' * WIDTH + '-')
    for y in range(HEIGH):
        place = '|'
        for x in range(WIDTH):
            if (x, y) in snake:
                place += '$'
            elif (x, y) == apple:
                place += 'x'
            else:
                place += ' '
        place += '|'
        print(place)
    print('-' + '-' * WIDTH + '-')


def keyboard_check(press):
    global move1, move2
    try:
        if press == keyboard.Key.right and move1 != -1:
            move1, move2 = 1, 0
        elif press == keyboard.Key.left and move1 != 1:
            move1, move2 = -1, 0
        elif press == keyboard.Key.up and move2 != 1:
            move1, move2 = 0, -1
        elif press == keyboard.Key.down and move2 != -1:
            move1, move2 = 0, 1
    except AttributeError:
        pass

flag = False
while flag == False:
    try:
        WIDTH = int(input("Введите ширину поля: "))
        flag = True
    except ValueError:
        print("Введите целое число!")
        flag = False

while flag:
    try:
        HEIGH = int(input("Введите высоту поля: "))
        flag = False
    except ValueError:
        print("Введите целое число!")
        flag = True


snake = [(1, 1)]
apple = create_apple(WIDTH, HEIGH)


move1, move2 = 1, 0

listener = keyboard.Listener(on_press=keyboard_check)
listener.start()


while True:
    x, y = snake[-1]
    snake_head = (x + move1, y + move2)
    if snake_head in snake or snake_head[0] >= WIDTH or snake_head[1] >= HEIGH or snake_head[0] < 0 or snake_head[1] < 0:
        print('You lose!')
        break
    snake.append(snake_head)
    if snake_head == apple:
        apple = create_apple(WIDTH,WIDTH)
    else:
        snake.pop(0)
    field()
    time.sleep(0.2)
