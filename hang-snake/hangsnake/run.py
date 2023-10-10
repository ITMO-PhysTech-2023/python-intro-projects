import random
import string
from random import randint
from tkinter import *
from windowout.run import window, gamestatus

WIDTH = 700
HEIGHT = 420
OBJ_SIDE = 35
GAME_SPEED = 100
direction = 'right'
mistakes = 0

words = ['programming', 'python', 'laptop', 'coffee', 'computer', 'informatics',
         'keyboard', 'monitor', 'development']  # Список слов

def create_secret():
    return random.choice(words)  # Выбор случайного слова из списка


SECRET = create_secret()
n = len(SECRET)
guess_field = '_' * n  # Создание слова и поля для ответа

class Snake:
    def __init__(self):
        self.coords = []
        self.parts = []
        self.coords.append([OBJ_SIDE, OBJ_SIDE])
        for x, y in self.coords:
            part = canvas.create_rectangle(x, y, x + OBJ_SIDE, y + OBJ_SIDE, fill="green")
            self.parts.append(part)


class Apple:
    def __init__(self):
        self.x = randint(0, 19) * OBJ_SIDE
        self.y = randint(0, 11) * OBJ_SIDE
        self.coords = [self.x, self.y]
        self.letter = random.choice(string.ascii_lowercase)
        canvas.create_rectangle(self.x, self.y, self.x + OBJ_SIDE, self.y + OBJ_SIDE, fill="red", tags="apple")
        canvas.create_text(self.x + OBJ_SIDE/2, self.y + OBJ_SIDE/2, text=self.letter,
                               justify=CENTER, font="Verdana 14", fill="black", tags="appletext")


class Hangsnakegame:  # Переписано под ООП
    def __init__(self):
        pass

    @staticmethod
    def move(snake, apples):
        eaten = False
        Hangsnakegame.hang()
        x, y = snake.coords[0]
        if direction == 'left':
            x = x - OBJ_SIDE
        elif direction == 'right':
            x = x + OBJ_SIDE
        elif direction == 'up':
            y = y - OBJ_SIDE
        elif direction == 'down':
            y = y + OBJ_SIDE
        snake.coords.insert(0, (x, y))
        part = canvas.create_rectangle(x, y, x + OBJ_SIDE, y + OBJ_SIDE, fill="green")
        snake.parts.insert(0, part)
        for apple in apples:
            if x == apple.coords[0] and y == apple.coords[1]:
                apples.remove(apple)
                Hangsnakegame.hangmanmove(apple.letter)
                apples.append(Apple())
                eaten = True
        if not eaten:
            del snake.coords[-1]
            canvas.delete(snake.parts[-1])
            del snake.parts[-1]
        canvas.delete("apple")
        canvas.delete("appletext")
        for apple in apples:
            canvas.create_rectangle(apple.x, apple.y, apple.x + OBJ_SIDE, apple.y + OBJ_SIDE, fill="red", tags="apple")
            canvas.create_text(apple.x + OBJ_SIDE / 2, apple.y + OBJ_SIDE / 2, text=apple.letter,
                               justify=CENTER, font="Verdana 14", fill="black", tags="appletext")

        if Hangsnakegame.check_collisions():
            Hangsnakegame.game_over()
        else:
            window.after(GAME_SPEED, Hangsnakegame.move, snake, apples)

    @staticmethod
    def change_direction(new_direction):
        global direction
        match new_direction:
            case 'left':
                if direction != 'right':
                    direction = 'left'
            case 'right':
                if direction != 'left':
                    direction = 'right'
            case 'up':
                if direction != 'down':
                    direction = 'up'
            case 'down':
                if direction != 'up':
                    direction = 'down'

    @staticmethod
    def check_collisions():
        x, y = snake.coords[0]
        if x < 0 or x >= WIDTH:
            return True
        if y < 0 or y >= HEIGHT:
            return True
        for body_part in snake.coords[1:]:
            if x == body_part[0] and y == body_part[1]:
                return True
        return False

    @staticmethod
    def game_over():
        canvas.delete(ALL)
        canvas.create_text(350, 210,
                           text="Game over!",
                           justify=CENTER, font="Verdana 20", fill="white")
        canvas.create_text(350, 240, text="Word: {}".format(SECRET),
                           justify=CENTER, font="Verdana 20", fill="white")

    @staticmethod
    def correct_answer(letter):  # Добавление правильной буквы в поле ответа
        new_guess_field = ''
        for i in range(n):  # Если буква правильная, "открываем" её в поле ответа
            if SECRET[i] == letter:
                new_guess_field = new_guess_field + letter
            else:
                new_guess_field = new_guess_field + guess_field[i]
        return new_guess_field

    @staticmethod
    def hangmanmove(letter):  # Ход
        global guess_field, mistakes
        if letter in SECRET:  # Если буква правильная, выполняем соответствующую функцию
            guess_field = Hangsnakegame.correct_answer(letter)  # Изменяем поле для ответа
        else:
            mistakes = mistakes + 1  # Если буква неправильная, добавляем ошибку
        Hangsnakegame.win_lose()
        window.after(1, Hangsnakegame.hang)
    @staticmethod
    def win_lose():
        global guess_field
        if SECRET == guess_field:  # Если поле для ответа совпадает с загаданным словом - победа
            canvas.delete("enter_text")
            canvas.delete("letter_window")
            canvas.delete("button")
            canvas.delete("comm")
            canvas.create_text(350, 550,
                               text="You won!",
                               justify=CENTER, font="Verdana 14")
        if mistakes == 5:  # Если 5 ошибок - проигрыш
            canvas.delete("enter_text")
            canvas.delete("letter_window")
            canvas.delete("button")
            canvas.delete("comm")
            canvas.create_text(350, 550,
                               text="You lost!",
                               justify=CENTER, font="Verdana 14")
            canvas.create_text(350, 580,
                               text=f"Answer: {SECRET}",

                               justify=CENTER, font="Verdana 14")

    @staticmethod
    def run():
        Hangsnakegame.move(snake, apples)
        canvas.pack()  # Отрисовка поверх окна
        canvashang.pack()

    window.bind('<w>', lambda event: Hangsnakegame.change_direction('up'))  # wasd строчными буквами
    window.bind('<s>', lambda event: Hangsnakegame.change_direction('down'))
    window.bind('<a>', lambda event: Hangsnakegame.change_direction('left'))
    window.bind('<d>', lambda event: Hangsnakegame.change_direction('right'))

    @staticmethod
    def hang():
        global mistakes
        canvashang.create_line(125, 250, 195, 250, width=3)
        canvashang.create_line(160, 250, 160, 50, width=3)
        canvashang.create_line(160, 50, 240, 50, width=3)
        canvashang.create_line(240, 50, 240, 100, width=1)
        match mistakes:
            case 1:
                canvashang.create_oval(220, 100, 260, 140, width=2)
            case 2:
                canvashang.create_line(240, 140, 240, 200, width=2)
            case 3:
                canvashang.create_line(240, 150, 270, 175, width=2)
                canvashang.create_line(240, 150, 210, 175, width=2)
            case 4:
                canvashang.create_line(240, 200, 270, 235, width=2)
            case 5:
                canvashang.create_line(240, 200, 210, 235, width=2)
        canvashang.delete("guess")
        canvashang.create_text(500, 200,
                           text=guess_field,
                           justify=CENTER, font="Verdana 20", tags="guess")  # Вывод поля для ответа


def random_position():
    return randint(0, HEIGHT - 1), randint(0, WIDTH - 1)


canvas = Canvas(window, bg="black", height=HEIGHT, width=WIDTH)
canvashang = Canvas(window, bg="white", height=280, width=WIDTH)
snake = Snake()
apples = [Apple(), Apple(), Apple()]
game = Hangsnakegame()

if gamestatus == 3:
    Hangsnakegame.run()
while gamestatus == 3:
    window.update()
