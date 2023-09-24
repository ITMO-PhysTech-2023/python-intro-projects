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


def move(snake, apple):
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


    if x == apple.coords[0] and y == apple.coords[1]:
        canvas.delete("apple")
        apple = Apple()
    else:
        del snake.coords[-1]
        canvas.delete(snake.parts[-1])
        del snake.parts[-1]

    window.after(GAME_SPEED, move, snake,apple)

def change_direction(new_direction):
    global direction
    match new_direction:
        case 'left':
            direction = 'left'
        case 'right':
            direction = 'right'
        case 'up':
            direction = 'up'
        case 'down':
            direction = 'down'

def random_position():
    return randint(0, HEIGHT - 1), randint(0, WIDTH - 1)


window = Tk()
window.title('Sneik')

canvas = Canvas(window, bg="black", height=HEIGHT, width=WIDTH)
canvas.pack()

snake = Snake()
apple = Apple()


window.geometry(f"{700}x{700}+{400}+{100}")

move(snake, apple)

window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))
window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))

window.mainloop()