from pynput import keyboard
from random import randint
from common.util import clear_terminal
import time

WIDTH, HEIGHT = 25, 25

default_output = ('#' + ' '*WIDTH + '#\n')*HEIGHT
output = default_output
# можно приделать конфиг-файл с параметрами
direction = (1, 0)

def random_position():
    return randint(0, HEIGHT - 1), randint(0, WIDTH - 1)


def process_press(key):
    # обработчик нажатия на клавиши (можно сделать и поаккуратнее)
    global direction
    if key == keyboard.Key.left and direction != (-1, 0):
        direction = (-1, 0)
    elif key == keyboard.Key.up and direction != (0, -1):
        direction = (0, -1)
    elif key == keyboard.Key.right and direction != (1, 0):
        direction = (1, 0)
    elif key == keyboard.Key.down and direction != (0, 1):
        direction = (0, 1)


N = 1

init_pos = (WIDTH // 2, HEIGHT // 2)
next_pos = (init_pos[0]+direction[0], init_pos[1]+direction[1])
body = [next_pos, init_pos]

apple = random_position()


with keyboard.Listener(on_press=process_press) as listener:
    while True:
        game_over = False
        if body[1] == apple:
            apple = random_position()
            body.append(body[N])
            N+=1
        for i in range(N, 0, -1):
            body[i] = body[i-1]
        if body[1][0] < 0 or body[1][0] >= WIDTH \
            or body[1][1] < 0 or body[1][1] >= HEIGHT:
            game_over = True
        for i in range(2, N+1):
            if body[i][0] == body[1][0] and body[i][1] == body[1][1]:
                game_over = True
                break
        if game_over:
            clear_terminal()
            print('you lost!')
            break

        body[0] = (body[1][0]+direction[0], body[1][1]+direction[1])

        for i in range(1, N+1):
            output = output[:body[i][1] * (WIDTH + 3) + body[i][0] + 1] + \
                     '#' + output[body[i][1] * (WIDTH + 3) + body[i][0] + 2:]
        output = output[:apple[1] * (WIDTH + 3) + apple[0] + 1] + \
                 '#' + output[apple[1] * (WIDTH + 3) + apple[0] + 2:]
        print('#'*(WIDTH+2))
        print(output + '#' * (WIDTH+2))
        output = default_output
        time.sleep(0.3)
        clear_terminal()

