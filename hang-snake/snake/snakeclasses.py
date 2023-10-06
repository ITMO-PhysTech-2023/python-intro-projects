import os
import time
from pynput import keyboard
from random import randint

WIDTH, HEIGHT = 10, 10
# можно приделать конфиг-файл с параметрами
direction = (1, 0)


def random_position():
    a, b = randint(0, HEIGHT - 1), randint(0, WIDTH - 1)
    return a, b


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


class Field:
    def __init__(self):
        self.FIELD = [['.' for i in range(WIDTH)] for i in range(HEIGHT)]
        self.apple = random_position()
        self.snake = [[randint(0, HEIGHT - 1), randint(0, WIDTH - 1)]]
        self.snake_tail = 0

    def The_Field(self):
        self.FIELD = [['.' for i in range(WIDTH)] for _ in range(HEIGHT)]

    def Zapolnenie_Apple(self):
        self.FIELD[self.apple[0]][self.apple[1]] = 'a'

    def Vyvod_Polya(self):
        for row in self.FIELD:
            print(''.join(row))
            
    def Zapolnenie_Snake(self):
        for elem in self.snake:  # обновляем змею
            if self.snake_tail > 0:
                self.FIELD[elem[0] % WIDTH][elem[1] % HEIGHT] = 'o'
                self.FIELD[self.snake[0][0] % WIDTH][self.snake[0][1] % HEIGHT] = 's'
            else:
                self.FIELD[self.snake[0][0]][self.snake[0][1]] = 's'

    def Move(self):
        if self.snake_tail > 0:
            for i in range(self.snake_tail, 0, -1):
                self.snake[i][0] = self.snake[i - 1][0]
                self.snake[i][1] = self.snake[i - 1][1]
        self.snake[0][0] = (self.snake[0][0] + direction[0]) % WIDTH
        self.snake[0][1] = (self.snake[0][1] + direction[1]) % HEIGHT

    def Snake_Eat_Apple(self):
        if self.snake[0][0] == self.apple[0] and self.snake[0][1] == self.apple[1]:
            self.apple = random_position()
            self.snake_tail += 1
            self.snake.insert(0, [self.snake[0][0] + direction[0], self.snake[0][1] + direction[1]])


class GameSnake:
    def __init__(self):
        self.Field = Field()

    def Run(self):
        with keyboard.Listener(on_press=process_press) as listener:
            while True:
                os.system('cls')
                self.Field.The_Field()
                self.Field.Zapolnenie_Snake()
                self.Field.Zapolnenie_Apple()
                self.Field.Vyvod_Polya()
                self.Field.Move()
                self.Field.Snake_Eat_Apple()
                time.sleep(0.5)



'''          
import os
import time
from pynput import keyboard
from random import randint

WIDTH, HEIGHT = 10, 10
# можно приделать конфиг-файл с параметрами
direction = (1, 0)


def random_position():
    a, b = randint(0, HEIGHT - 1), randint(0, WIDTH - 1)
    return a, b


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


class Field:
    def __init__(self):
        self.FIELD = [['.' for i in range(WIDTH)] for i in range(HEIGHT)]
        self.apple = random_position()

    def The_Field(self):
        self.FIELD = [['.' for i in range(WIDTH)] for i in range(HEIGHT)]

    def Zapolnenie_Apple(self):
        self.FIELD[self.apple[0]][self.apple[1]] = 'a'

    def Vyvod_Polya(self):
        for row in self.FIELD:
            print(''.join(row))


class Snake:
    def __init__(self):
        self.snake = [[randint(0, HEIGHT - 1), randint(0, WIDTH - 1)]]
        self.snake_tail = 0
        self.Field = Field()

    def Zapolnenie_Snake(self):
        for elem in self.snake:  # обновляем змею
            if self.snake_tail > 0:
                self.Field.FIELD[elem[0] % WIDTH][elem[1] % HEIGHT] = 'o'
                self.Field.FIELD[self.snake[0][0] % WIDTH][self.snake[0][1] % HEIGHT] = 's'
            else:
                self.Field.FIELD[self.snake[0][0]][self.snake[0][1]] = 's'

    def Move(self):
        if self.snake_tail > 0:
            for i in range(self.snake_tail, 0, -1):
                self.snake[i][0] = self.snake[i - 1][0]
                self.snake[i][1] = self.snake[i - 1][1]
        self.snake[0][0] = (self.snake[0][0] + direction[0]) % WIDTH
        self.snake[0][1] = (self.snake[0][1] + direction[1]) % HEIGHT

    def Snake_Eat_Apple(self):
        if self.snake[0][0] == self.Field.apple[0] and self.snake[0][1] == self.Field.apple[1]:
            self.Field.apple = random_position()
            self.snake_tail += 1
            self.snake.insert(0, [self.snake[0][0] + direction[0], self.snake[0][1] + direction[1]])


class GameSnake:
    def __init__(self):
        self.Field = Field()
        self.Snake = Snake()

    def Run(self):
        with keyboard.Listener(on_press=process_press) as listener:
            while True:
                os.system('cls')
                self.Field.The_Field()
                self.Snake.Zapolnenie_Snake()
                self.Field.Zapolnenie_Apple()
                self.Field.Vyvod_Polya()
                self.Snake.Move()
                self.Snake.Snake_Eat_Apple()
                time.sleep(0.5)
    '''