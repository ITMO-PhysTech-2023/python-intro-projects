from pynput import keyboard
from random import randint
import os
import time
import snake_config as config

def terminal_size():
    return os.get_terminal_size()


def clear_terminal():
    cmd = 'cls' if os.name == 'nt' else 'clear'
    os.system(cmd)


WIDTH, HEIGHT = config.WIDTH, config.HEIGHT
DIRECTION = (1, 0)
BASE_LENGTH = 2
MAX_APPLES = 3

body_symbol = '$'
head_symbol = 'P'
headl_symbol = '←'
headr_symbol = '→'
headu_symbol = '↑'
headd_symbol = '↓'
borderv_symbol = 'I'
borderh_symbol = '='
apple_symbol = '0'

class Snake_Field:
    def __init__(self, width = WIDTH, height = HEIGHT, apples = []):
        self.width = width
        self.height = height
        self.apples = apples


    def spawn_apple(self):
        new_apple = random_position()
        while new_apple in self.apples:
            new_apple = random_position()
        self.apples.append(new_apple)
        return self.apples[-1]

    def delete_apple(self, apple_coord):
        if apple_coord == 0:
            self.apples.pop(0)
        else:
            ind = self.apples.index(apple_coord)
            self.apples.pop(ind)



class Snake:
    def __init__(self, length = BASE_LENGTH, direction = DIRECTION, body = []):
        self.length = length
        self.direction = direction
        self.body = body
        

    def crawl(self, Snake_Field):

        head = [self.head[0] + self.direction[0], self.head[1] + self.direction[1]]                # Перемещаем голову и проверяем условия на столкновения и съедение яблока
        if (head[1] < 0 or head[1] > Snake_Field.width or head[0] < 0 or head[0] > Snake_Field.height or head in self.body) and self.direction != (0, 0):
            snake_game_over()
        else:
            self.head = head
            if head in Snake_Field.apples:
                self.body.insert(0, head)
                self.length += 1
                Snake_Field.delete_apple(head)
                return 1
            elif self.direction != (0, 0):
                self.body.insert(0, head)
                self.body.pop(-1)
                return 0

    def set_direction(self, direction):
        self.direction = direction
        
            

EXIT = False

def snake_game_over():
    global EXIT
    print('game over!')
    EXIT = True

def spawn_Snake(Snake_Field, Snake):                             # Спауним змейку в рандомное место на поле и смотрим, чтобы она не уходила за границы
    Snake.body.append(random_position())
    borders = [0, Snake_Field.width, 0, Snake_Field.height]
    head = Snake.body[0]
    if head[0] - (BASE_LENGTH - 1) >= borders[0]:
        for i in range(1, BASE_LENGTH):
            Snake.body.append([head[0] - i, head[1]])
    elif head[0] + (BASE_LENGTH - 1) <= borders[1]:
        for i in range(1, BASE_LENGTH):
            Snake.body.append([head[0] + i, head[1]])
    elif head[1] - (BASE_LENGTH - 1) <= borders[2]:
        for i in range(1, BASE_LENGTH):
            Snake.body.append([head[0], head[1] - i])
    elif head[1] + (BASE_LENGTH - 1) <= borders[3]:
        for i in range(1, BASE_LENGTH):
            Snake.body.append([head[0], head[1] + i])

    print('snake spawned:', Snake.body)

def print_Snake_Field(Snake_Field, Snake):                             # Выводим поле на печать посимвольно
    print(borderh_symbol * (Snake_Field.width + 2))
    for i in range(0, Snake_Field.height):
        print(borderv_symbol, end = '')
        for j in range(Snake_Field.width):
            cell = [i, j]
            if cell == snake.head:
                if snake.direction == (1, 0):
                    print(headd_symbol, end = '')
                elif snake.direction == (-1, 0):
                    print(headu_symbol, end = '')
                elif snake.direction == (0, 1):
                    print(headr_symbol, end = '')
                elif snake.direction == (0, -1):
                    print(headl_symbol, end = '') 
                else:
                    print(head_symbol, end = '')                   
            elif cell in Snake.body:
                print(body_symbol, end = '')
            elif cell in Snake_Field.apples:
                print(apple_symbol, end = '')
            else:
                print(' ', end = '')
        print(borderv_symbol)
    print(borderh_symbol * (Snake_Field.width + 2))

def random_position():
    return [randint(0, HEIGHT - 1), randint(0, WIDTH - 1)]


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


field = Snake_Field()
snake = Snake()
spawn_Snake(field, snake)
snake.head = snake.body[0]
snake.crawl(field)

direction = (0, 0)

#process_press
#snake.crawl(field)
field.spawn_apple()

input('Ready to play?')
# оно умеет мониторить нажатия на кнопки!

with keyboard.Listener(on_press=process_press) as listener:
    counter = 0
    while not EXIT:
        clear_terminal()
        print_Snake_Field(field, snake)
        time.sleep(0.2)
        counter += 1
        snake.set_direction(direction)
        eaten = snake.crawl(field)
        if counter % 30 == 0 or eaten:
            counter = 0
            if len(field.apples) >= MAX_APPLES:
                field.delete_apple(0)
            new_apple = field.spawn_apple()
            while new_apple in snake.body:
                if len(field.apples) >= MAX_APPLES:
                    field.delete_apple(0)
                new_apple = field.spawn_apple()
        
