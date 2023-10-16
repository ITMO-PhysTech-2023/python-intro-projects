from random import randint
from tkinter import *
from windowout.run import window, gamestatus


WIDTH = 700
HEIGHT = 700
OBJ_SIDE = 35
GAME_SPEED = 60
direction = 'right'
score = 0


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
        self.y = randint(0, 19) * OBJ_SIDE
        self.coords = [self.x, self.y]
        canvas.create_rectangle(self.x, self.y, self.x + OBJ_SIDE, self.y + OBJ_SIDE, fill="red", tags="apple")


class SnakeGame:  #Переписано под ООП
    def __init__(self):
        pass

    @staticmethod
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
        if SnakeGame.check_collisions():
            SnakeGame.game_over()
        else:
            window.after(GAME_SPEED, SnakeGame.move, snake, apple)

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
        if x < 0 or x >= 700:
            return True
        if y < 0 or y >= 700:
            return True
        for body_part in snake.coords[1:]:
            if x == body_part[0] and y == body_part[1]:
                return True
        return False

    @staticmethod
    def game_over():
        canvas.delete(ALL)
        canvas.create_text(350, 300,
                           text="Game over!",
                           justify=CENTER, font="Verdana 20", fill="white")
        canvas.create_text(350, 330,
                           text="Score: {}".format(score),
                           justify=CENTER, font="Verdana 20", fill="white")
        gameover = Button(text='Выйти из игры',
                          command=SnakeGame.game_exit)
        canvas.create_window(350, 370, window=gameover, tags="gameover")

    @staticmethod
    def game_exit():
        global gamestatus
        gamestatus = 4

    @staticmethod
    def run():
        SnakeGame.move(snake, apple)
        canvas.pack()  #Отрисовка поверх окна
        label.pack()

    window.bind('<w>', lambda event: SnakeGame.change_direction('up'))  #wasd строчными буквами
    window.bind('<s>', lambda event: SnakeGame.change_direction('down'))
    window.bind('<a>', lambda event: SnakeGame.change_direction('left'))
    window.bind('<d>', lambda event: SnakeGame.change_direction('right'))


def random_position():
    return randint(0, HEIGHT - 1), randint(0, WIDTH - 1)


canvas = Canvas(window, bg="black", height=HEIGHT, width=WIDTH)
label = Label(window, text="Score: {}".format(score),
              font=("Verdana", 16))


snake = Snake()
apple = Apple()
game = SnakeGame()

if gamestatus == 1:
    SnakeGame.run()
while gamestatus == 1:
    window.update()




