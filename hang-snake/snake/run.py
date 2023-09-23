from pynput import keyboard
from random import randint

#WIDTH, HEIGHT = 20,20
class SnakeGame:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.direction=(1,0)
        #self.snake=Snake(...)

Snake = SnakeGame(width=int(input()), height=int(input()))

# можно приделать конфиг-файл с параметрами
#direction = (1, 0)


def random_position():
    position = []
    position = [randint(0, Snake.height - 1), randint(0, Snake.width - 1)]
    return position


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



snake = random_position()
apple = random_position()
print(*snake,*apple)

# while apple[0] == snake[0]:
#     new_apple = [random_position()]
#     apple=new_apple

# # оно умеет мониторить нажатия на кнопки!
with keyboard.Listener(on_press=process_press) as listener:
    while True:
        if (int(snake[0]) == Snake.height or int(snake[0]) == -1 or int(snake[1]) == -1 or int(snake[1]) == Snake.width):
            break
        else:
            if (apple[1] == snake[1] and apple[0] == snake[0]):
                new_apple = random_position()
                apple = new_apple