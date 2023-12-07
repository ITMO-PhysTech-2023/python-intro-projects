import random
from hangman.hangmanclasses import *
from snake.snakeclasses import *

connection_field = []
alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]

for i in range(max(len(FINAL_FIELD), HEIGHT)):
    if i < len(FINAL_FIELD):
        connection_field.append(WIDTH * '.' + 5 * ' ' + FINAL_FIELD[i])
    else:
        connection_field.append(WIDTH * '.')


class ConnnectionField:
    def __init__(self):
        self.field = [list(row) for row in connection_field]
        self.secret_word = [elem for elem in create_secret()]
        for cell in HUMAN:
            self.field[cell[0]][cell[1] + 15] = ' '

    def PrintField(self):
        for row in self.field:
            print(''.join(row))

    def RandPos(self):
        return [randint(0, HEIGHT), randint(0, WIDTH)]

    def RandLet(self):
        return random.choice(alphabet)

    def RandLetPos(self):
        for _ in range(6):
            a, b = self.RandPos()
            while connection_field[a][b] != ' ':
                a, b = self.RandPos()
            self.field[a][b] = self.RandLet()

class Snake:
    def __init__(self):
        self.snake = [[randint(0, HEIGHT - 1), randint(0, WIDTH - 1)]]
        self.snake_tail = 0



