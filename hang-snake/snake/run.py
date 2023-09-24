from pynput import keyboard
from random import randint
from tkinter import *

WIDTH = 700
HEIGHT = 700
OBJ_SIDE = 35
GAME_SPEED = 100
direction = 'right'


class Snake:
    def __init__(self):
        self.coords = []
        self.parts = []

        self.coords.append([35,35])

        for x,y in self.coords:
            part = canvas.create_rectangle(x, y, x + OBJ_SIDE, y + OBJ_SIDE, fill="green")
            self.parts.append(part)


class Apple:
    def __init__(self):
        self.x = randint(0, 19)*OBJ_SIDE
        self.y = randint(0, 19)*OBJ_SIDE
        self.coords = [self.x, self.y]
        canvas.create_rectangle(self.x, self.y, self.x + OBJ_SIDE, self.y + OBJ_SIDE, fill="red", tags="apple")


def random_position():
    return randint(0, HEIGHT - 1), randint(0, WIDTH - 1)


window = Tk()
window.title('Sneik')

canvas = Canvas(window, bg="black", height=HEIGHT, width=WIDTH)
canvas.pack()

snake = Snake()
apple = Apple()


window.geometry(f"{700}x{700}+{400}+{100}")
window.mainloop()