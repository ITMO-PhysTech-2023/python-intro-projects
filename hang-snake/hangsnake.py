from common.util import clear_terminal, terminal_size
from hangman.__init__ import *


from snake.snake_config import *

from pynput import keyboard
from random import randint
import os
import time
import threading

word = ''
guessed = ''
correct = ''
incorrect = ''

MAX_LETTERS = 3
tries = 6
LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

word, correct, incorrect, guessed = [], [], [], [] 

class Snake_Field:
    def __init__(self, width = WIDTH, height = HEIGHT, letters = []):
        self.width = width
        self.height = height
        self.letters = letters


    def spawn_letter(self):
        new_letter = [LETTERS[random.randint(0, len(LETTERS) - 1)], random_position()]
        while new_letter in self.letters:
            new_letter = [LETTERS[random.randint(0, len(LETTERS) - 1)], random_position()]
        self.letters.append(new_letter)
        return self.letters[-1]

    def delete_letter(self, letter_coord):
        if letter_coord == 0:
            self.letters.pop(0)
            return 0
        else:
            ind = [i[1] for i in self.letters].index(letter_coord)
            output_letter = self.letters[ind]
            self.letters.pop(ind)
            return output_letter



class Snake:
    def __init__(self, length = BASE_LENGTH, direction = DIRECTION, body = []):
        self.length = length
        self.direction = direction
        self.body = body
        

    def crawl(self, Snake_Field):
        global eaten_letter
        head = [self.head[0] + self.direction[0], self.head[1] + self.direction[1]]                # Перемещаем голову и проверяем условия на столкновения и съедение яблока
        if head == self.body[1]:
            head = [self.head[0] - self.direction[0], self.head[1] - self.direction[1]]
            self.head = head
        if (head[1] < 0 or head[1] > Snake_Field.width - 1 or head[0] < 0 or head[0] > Snake_Field.height or head in self.body) and self.direction != (0, 0):
            snake_game_over()
        else:
            self.head = head
            letter_positions = [i[1] for i in Snake_Field.letters]
            if head in letter_positions:
                self.body.insert(0, head)
                self.length += 1
                output_letter = Snake_Field.delete_letter(head)
                eaten_letter = output_letter[0]
                return output_letter
            elif self.direction != (0, 0):
                self.body.insert(0, head)
                self.body.pop(-1)
                return 0

    def set_direction(self, direction):
        self.direction = direction
        
eaten_letter = ''            

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
    Snake.head = Snake.body[0]

    print('snake spawned:', Snake.body)


def print_Snake_Field(Snake_Field, Snake):                             # Выводим поле на печать посимвольно

    strings = []

    string = str(borderh_symbol * (Snake_Field.width + 2))
    strings.append(string)
    for i in range(0, Snake_Field.height + 1):
        string = str(borderv_symbol)
        for j in range(Snake_Field.width):
            cell = [i, j]
            if cell == Snake.head:
                if Snake.direction == (1, 0):
                    string += str(headd_symbol)
                elif Snake.direction == (-1, 0):
                    string += str(headu_symbol)
                elif Snake.direction == (0, 1):
                    string += str(headr_symbol)
                elif Snake.direction == (0, -1):
                    string += str(headl_symbol) 
                else:
                    string += str(head_symbol)                   
            elif cell in Snake.body:
                string += str(body_symbol)
            elif cell in [l[1] for l in Snake_Field.letters]:
                for l in Snake_Field.letters:
                    if l[1] == cell:
                        string += str(l[0])
            else:
                string += str(' ')
        string += str(borderv_symbol)
        strings.append(string)
    string = str(borderh_symbol * (Snake_Field.width + 2))
    strings.append(string)
    return strings
    #(Snake_Field.letters)

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

FPS = 100
counter = 0
direction = (0, 0)

def check_correct(field, correct):
    global word
    s = set(word.upper())
    left = []
    for i in s:
        if i not in correct:
            left.append(i)
    flag = False
    for i in [letter[0] for letter in field.letters]:
        if i in left:
            flag = True
    return flag

def await_input():
    global direction, counter
    with keyboard.Listener(on_press=process_press) as listener:
        for i in range(int((1 / FPS) / 0.001) + 1):
            time.sleep(0.01)
    

def game_move(Snake, Snake_Field):
    global counter, eaten
    Snake.set_direction(direction)
    eaten = Snake.crawl(Snake_Field)
    clear_terminal()
    #print_Snake_Field(Snake_Field, Snake)
    if not check_correct(field, correct) or len(Snake_Field.letters) < MAX_LETTERS:
        if len(Snake_Field.letters) >= MAX_LETTERS:
            Snake_Field.delete_letter(0)
        new_letter = Snake_Field.spawn_letter()
        while new_letter[1] in Snake.body or not check_correct(field, correct):
            
            Snake_Field.delete_letter(new_letter[1])
            new_letter = Snake_Field.spawn_letter()

def hangsnake_output(field, snake, guessed, correct, incorrect, tries):
    output = []
    snake_output = print_Snake_Field(field, snake)
    hang_output = print_hang_field(guessed, correct, incorrect, tries)

    for i in range(len(snake_output)):
        if i < len(hang_output):
            output.append(snake_output[i] + '           ' + hang_output[i])
        else:
            output.append(snake_output[i])
    strings = []
    for i in output:
        string = ''
        for j in i:
            string += j
        string += '\n'
        strings.append(string)

    return strings

def osn():
    global eaten_letter, answer, incorrect, guessed, correct, tries, EXIT, snake, field
    game_move(snake, field)
    if eaten_letter != '':
        answer, correct, incorrect, guessed = user_input(eaten_letter)
        if answer == incorrect_msg or answer == gameover_msg:
            tries -= 1
        elif answer == gameover_msg:
            EXIT = True
        eaten_letter = ''
    strings = hangsnake_output(field, snake, guessed, correct, incorrect, tries)

    for string in strings:
        print(string, end = '')
    if tries <= 0:
        EXIT = True

field = Snake_Field()
for i in range(MAX_LETTERS):
    field.spawn_letter()
#print(field.letters)
snake = Snake(direction = (0, 0))
spawn_Snake(field, snake)

word, guessed = hang_init()
#print(word)
input('Ready?')
tries = 6
while not EXIT:
    
    e1 = threading.Event()
    e2 = threading.Event()

    t1 = threading.Thread(target=await_input, args=())
    t2 = threading.Thread(target=osn, args=())


    t1.start()
    t2.start()

    e1.set()


    t1.join()
    t2.join()
