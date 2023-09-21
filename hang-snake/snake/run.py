import random
import time
from pynput import keyboard


WIDTH = 20
HEIGHT = 10
snake = [(4, 4)]
food = (9, 9)


dx, dy = 1, 0


def draw_board():
    print('+' + '-' * WIDTH + '+')
    for y in range(HEIGHT):
        row = '|'
        for x in range(WIDTH):
            if (x, y) in snake:
                row += 'O'
            elif (x, y) == food:
                row += 'x'
            else:
                row += ' '
        row += '|'
        print(row)
    print('+' + '-' * WIDTH + '+')


def on_key_press(key):
    global dx, dy
    try:
        if key == keyboard.Key.right and dx != -1:
            dx, dy = 1, 0
        elif key == keyboard.Key.left and dx != 1:
            dx, dy = -1, 0
        elif key == keyboard.Key.up and dy != 1:
            dx, dy = 0, -1
        elif key == keyboard.Key.down and dy != -1:
            dx, dy = 0, 1
    except AttributeError:
        pass


listener = keyboard.Listener(on_press=on_key_press)
listener.start()


while True:
    x, y = snake[-1]
    new_head = (x + dx, y + dy)
    if new_head in snake or new_head[0] < 0 or new_head[0] >= WIDTH or new_head[1] < 0 or new_head[1] >= HEIGHT:
        print('Игра окончена!')
        break
    snake.append(new_head)
    if new_head == food:
        food = (random.randint(0, WIDTH - 1), random.randint(0, HEIGHT - 1))
    else:
        snake.pop(0)
    draw_board()
    time.sleep(0.2)
