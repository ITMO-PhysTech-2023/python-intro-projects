from random import randint
from tkinter import *

WIDTH = 700
HEIGHT = 700
OBJ_SIDE = 35
GAME_SPEED = 50
direction = 'right'
score = 0

class Snake:
    def __init__(self):
        self.coords = []
        self.parts = []

        self.coords.append([OBJ_SIDE, OBJ_SIDE])

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
    global score
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
        score = score + 1
        label.config(text="Score: {}".format(score))
        apple = Apple()
    else:
        del snake.coords[-1]
        canvas.delete(snake.parts[-1])
        del snake.parts[-1]

    if check_collisions():
        game_over()
    else:
        window.after(GAME_SPEED, move, snake,apple)


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


def random_position():
    return randint(0, HEIGHT - 1), randint(0, WIDTH - 1)


def check_collisions():
    x, y = snake.coords[0]

    if x < 0 or x >= 700:
        return True
    if y < 0 or y >= 700:
        return True
    for body_part in snake.coords[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True
    return False


def game_over():
    canvas.delete(ALL)
    canvas.create_text(350, 300,
                       text="Game over!",
                       justify=CENTER, font="Verdana 20", fill="white")
    canvas.create_text(350, 330,
                       text="Score: {}".format(score),
                       justify=CENTER, font="Verdana 20", fill="white")


window = Tk()
window.title('Sneik')

canvas = Canvas(window, bg="black", height=HEIGHT, width=WIDTH)
canvas.pack()

label = Label(window, text="Score: {}".format(score),
                        font=("Verdana", 16))
label.pack()

snake = Snake()
apple = Apple()


window.geometry(f"{700}x{740}+{400}+{100}")

move(snake, apple)

window.bind('<w>', lambda event: change_direction('up'))
window.bind('<s>', lambda event: change_direction('down'))
window.bind('<a>', lambda event: change_direction('left'))
window.bind('<d>', lambda event: change_direction('right'))

window.mainloop()