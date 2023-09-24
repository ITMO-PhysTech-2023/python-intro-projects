from pynput import keyboard
from random import randint
from tkinter import *

WIDTH = 700
HEIGHT = 700
OBJ_SIDE = 35
GAME_SPEED = 100
direction = 'right'



def random_position():
    return randint(0, HEIGHT - 1), randint(0, WIDTH - 1)


snake = [random_position()]
apple = random_position()
while apple in snake:
    apple = random_position()

window = Tk()
window.title('Sneik')

canvas = Canvas(window, bg="black", height=HEIGHT, width=WIDTH)
canvas.pack()

window.geometry(f"{700}x{700}+{400}+{100}")
window.mainloop()