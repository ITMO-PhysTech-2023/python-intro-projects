import random
import string
from random import randint
from tkinter import *
from MyPage.MyGame import window
import win32api


gamestatus = 3
WIDTH = 700
HEIGHT = 420
SIDE = 29
SPEED = 200
direction = 'right'
err = 0
def create_secret():
    words = ['capybara', 'dog', 'cat', 'rat', 'night', 'flash', 'wolverine']
    return random.choice(words)



SECRET = create_secret()
n = len(SECRET)
pole = ' _ ' * n

class Snake:
    def __init__(self):
        self.coords = []
        self.parts = []
        self.coords.append([SIDE, SIDE])
        for x1, y1 in self.coords:
            part = canvas.create_rectangle(x1, y1, x1 + SIDE, y1 + SIDE, fill="green")
            self.parts.append(part)


class Apple:
    def __init__(self):
        self.x = randint(0, 19) * SIDE
        self.y = randint(0, 11) * SIDE
        self.coords = [self.x, self.y]


        self.letter = random.choice(string.ascii_lowercase)
        canvas.create_oval(self.x, self.y, self.x + SIDE, self.y + SIDE, fill="red", tags="apple")
        canvas.create_text(self.x + SIDE/2, self.y + SIDE/2, text=self.letter,
                               justify=CENTER, font="Verdana 14", fill="black", tags="appletext")


    @staticmethod
    def move(snake, apples, refresher):
        eaten = False
        Hangsnakegame.hang()
        x, y = snake.coords[0]
        if direction == 'left':
            x = x - SIDE
        elif direction == 'right':
            x = x + SIDE
        elif direction == 'up':
            y = y - SIDE
        elif direction == 'down':
            y = y + SIDE
        snake.coords.insert(0, (x, y))
        part = canvas.create_rectangle(x, y, x + SIDE, y + SIDE, fill="green")
        snake.parts.insert(0, part)
        for apple in apples:
            if x == apple.coords[0] and y == apple.coords[1]:
                apples.remove(apple)
                Hangsnakegame.hangmanmove(apple.letter)
                apple = Apple()
                while [apple.x, apple.y] in snake.coords:
                    apple = Apple()
                apples.append(apple)
                eaten = True
        if x == refresher.coords[0] and y == refresher.coords[1]:
            apples.clear()

            while len(apples) != 3:
                apple = Apple()
                print(snake.coords, apple.x, apple.y, apple.coords)
                while [apple.x, apple.y] in snake.coords:
                    apple = Apple()
                apples.append(apple)

            canvas.delete("refresher")
            canvas.delete("ref")
            refresher = Refresher()
            while [refresher.x, refresher.y] in snake.coords:
                refresher = Refresher()
            eaten = True
        if not eaten:
            del snake.coords[-1]
            canvas.delete(snake.parts[-1])
            del snake.parts[-1]
        canvas.delete("apple")
        canvas.delete("appletext")
        for apple in apples:
            canvas.create_rectangle(apple.x, apple.y, apple.x + SIDE, apple.y + SIDE, fill="red", tags="apple")
            canvas.create_text(apple.x + SIDE / 2, apple.y + SIDE / 2, text=apple.letter,
                               justify=CENTER, font="Verdana 14", fill="black", tags="appletext")

        if Hangsnakegame.check_collisions():
            Hangsnakegame.game_over()
        else:
            window.after(SPEED, Hangsnakegame.move, snake, apples, refresher)


class Refresher:
    def __init__(self):
        gen = False
        while not gen:
            self.x = randint(0, 19) * SIDE
            self.y = randint(0, 11) * SIDE
            gen = True
            for apple in apples:
                if self.x == apple.x and self.y == apple.y:
                    gen = False
        self.coords = [self.x, self.y]
        canvas.create_rectangle(self.x, self.y, self.x + SIDE, self.y + SIDE, fill="yellow", tags="refresher")
        canvas.create_text(self.x + SIDE / 2, self.y + SIDE / 2, text='↻',
                           justify=CENTER, font="Verdana 20", fill="black", tags="ref")



class Hangsnakegame:  # Переписано под ООП
    def __init__(self):
        pass

    @staticmethod
    def move(snake, apples, refresher):
        global err, pole, SECRET
        eaten = False
        Hangsnakegame.hang()
        x, y = snake.coords[0]
        if direction == 'left':
            x = x - SIDE
        elif direction == 'right':
            x = x + SIDE
        elif direction == 'up':
            y = y - SIDE
        elif direction == 'down':
            y = y + SIDE
        snake.coords.insert(0, (x, y))
        part = canvas.create_rectangle(x, y, x + SIDE, y + SIDE, fill="green")
        snake.parts.insert(0, part)
        for apple in apples:
            if x == apple.coords[0] and y == apple.coords[1]:
                apples.remove(apple)
                Hangsnakegame.hangmanmove(apple.letter)
                apple = Apple()
                while [apple.x, apple.y] in snake.coords:
                    apple = Apple()
                apples.append(apple)
                eaten = True
        if x == refresher.coords[0] and y == refresher.coords[1]:
            apples.clear()
            while len(apples) != 3:
                apple = Apple()
                while [apple.x, apple.y] in snake.coords:
                    apple = Apple()
                apples.append(apple)

            canvas.delete("refresher")
            canvas.delete("ref")
            refresher = Refresher()
            while [refresher.x, refresher.y] in snake.coords:
                refresher = Refresher()
            eaten = True
        if not eaten:
            del snake.coords[-1]
            canvas.delete(snake.parts[-1])
            del snake.parts[-1]
        canvas.delete("apple")
        canvas.delete("appletext")
        for apple in apples:
            canvas.create_rectangle(apple.x, apple.y, apple.x + SIDE, apple.y + SIDE, fill="red", tags="apple")
            canvas.create_text(apple.x + SIDE / 2, apple.y + SIDE / 2, text=apple.letter,
                               justify=CENTER, font="Verdana 14", fill="black", tags="appletext")

        if Hangsnakegame.check_collisions():
            Hangsnakegame.game_over()
        elif err == 5:
            Hangsnakegame.game_over()
        elif SECRET == pole:
            Hangsnakegame.win()
        else:
            window.after(SPEED, Hangsnakegame.move, snake, apples, refresher)

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
        gameover = Button(text='Выйти из игры',
                               command = Hangsnakegame.game_exit)
        canvas.create_window(350, 280, window=gameover, tags="gameover")

    @staticmethod
    def correct_answer(letter):
        new_pole = ''
        for i in range(n):
            if SECRET[i] == letter:
                new_pole = new_pole + letter
            else:
                new_pole = new_pole + pole[i]
        return new_pole

    @staticmethod
    def hangmanmove(letter):
        global pole, err
        if letter in SECRET:
            pole = Hangsnakegame.correct_answer(letter)
        else:
            err = err + 1
        window.after(1, Hangsnakegame.hang)


    @staticmethod
    def win():
        global pole, err, gamestatus

        canvas.delete(ALL)

        canvas.create_text(350, 210,
                            text="You won!",
                            justify=CENTER, font="Verdana 20", fill="white")
        gameover = Button(text='Выйти из игры',
                          command=Hangsnakegame.game_exit)
        canvas.create_window(350, 280, window=gameover, tags="gameover")


    @staticmethod
    def game_exit():
        global gamestatus
        gamestatus = 4



    @staticmethod
    def run():
        Hangsnakegame.move(snake, apples, refresher)
        canvas.pack()
        canvashang.pack()

    @staticmethod
    def get_keyboard_layout():
        layout_id = win32api.GetKeyboardLayout()
        return hex(layout_id)

    layout = get_keyboard_layout()



    if layout == '0x4190419':
        window.bind('<Up>', lambda event: Hangsnakegame.change_direction('up'))
        window.bind('<Down>', lambda event: Hangsnakegame.change_direction('down'))
        window.bind('<Left>', lambda event: Hangsnakegame.change_direction('left'))
        window.bind('<Right>', lambda event: Hangsnakegame.change_direction('right'))

    elif layout == '0x4090409':
        window.bind('<w>', lambda event: Hangsnakegame.change_direction('up'))
        window.bind('<s>', lambda event: Hangsnakegame.change_direction('down'))
        window.bind('<a>', lambda event: Hangsnakegame.change_direction('left'))
        window.bind('<d>', lambda event: Hangsnakegame.change_direction('right'))






    @staticmethod
    def hang():
        global err
        canvashang.create_line(125, 250, 195, 250, width=3)
        canvashang.create_line(160, 250, 160, 50, width=3)
        canvashang.create_line(160, 50, 240, 50, width=3)
        canvashang.create_line(240, 50, 240, 100, width=1)

        match err:
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
                           text=pole,
                           justify=CENTER, font="Verdana 20", tags="guess")


def random_position():
    return randint(0, HEIGHT - 1), randint(0, WIDTH - 1)


canvas = Canvas(window, bg="black", height=HEIGHT, width=WIDTH)
canvashang = Canvas(window, bg="white", height=280, width=WIDTH)
snake = Snake()
apples = [Apple(), Apple(), Apple()]
refresher = Refresher()
game = Hangsnakegame()

if gamestatus == 3:
    Hangsnakegame.run()
while gamestatus == 3:
    window.update()

