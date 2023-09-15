from pynput import keyboard
from random import randint

WIDTH, HEIGHT = ..., ...
# можно приделать конфиг-файл с параметрами
direction = (1, 0)


def random_position():
    return randint(0, HEIGHT - 1), randint(0, WIDTH - 1)


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


snake = [random_position()]
apple = random_position()
while apple in snake:
    apple = random_position()

# оно умеет мониторить нажатия на кнопки!
with keyboard.Listener(on_press=process_press) as listener:
    while True:
        # let's play the game!
        pass
