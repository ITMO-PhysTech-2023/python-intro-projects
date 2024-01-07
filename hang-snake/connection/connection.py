import time
import os
import random
from random import randint
from pynput import keyboard
import subprocess


def Difficulty():
    print("Choose the difficulty:\n| 1 | 2 | 3 |")
    level = int(input())
    return {1: 0.7, 2: 0.5, 3: 0.3}.get(level)


TIME = Difficulty()
WIDTH, HEIGHT = 10, 10
direction = (1, 0)


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


def random_position():
    a, b = randint(0, HEIGHT - 1), randint(0, WIDTH - 1)
    return a, b


eaten = 0
alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
            'v', 'w', 'x', 'y', 'z']


def create_secret():
    words = ['embrace', 'capybara', 'haircut', 'charismatic', 'stress', 'construct', 'bike', 'mile', 'justify',
             'clinic', 'colon', 'tooth']
    return random.choice(words)


human_parts = 0
SECRET = [elem for elem in create_secret()]
HUMAN = [(3, 3), (4, 3), (4, 2), (4, 4), (5, 2), (5, 4)]
FINAL_FIELD = r'''
   +----+
   |    |
   o    |
  /|\   |
  / \   |
_______/|\____
'''.split('\n')


class SnakeField:
    def __init__(self):
        self.FIELD = [['.' for i in range(WIDTH)] for i in range(HEIGHT)]
        self.apple = random_position()
        self.snake = [[5, 5]]
        self.snake_tail = 0
        self.letters = []
        self.onelet = ''
        self.pos_let = []
        self.eaten_letters = []

    def The_Field(self):
        self.FIELD = [['.' for i in range(WIDTH)] for _ in range(HEIGHT)]

    def Vyvod_Polya(self):
        for row in self.FIELD:
            print(''.join(row))

    def Zapolnenie_Snake(self):
        for elem in self.snake:  # обновляем змею
            if self.snake_tail > 0:
                self.FIELD[elem[0] % WIDTH][elem[1] % HEIGHT] = '❄'
            else:
                self.FIELD[self.snake[0][0]][self.snake[0][1]] = '❄'

    def RandLet(self):
        for z in range(3):
            x = random.choice(alphabet)
            while (x in self.letters) or (x in self.eaten_letters):
                x = random.choice(alphabet)
            self.letters.append(x)
        for a in self.letters:
            x = [randint(0, WIDTH - 1), randint(0, HEIGHT - 1)]
            while x in self.pos_let:
                x = [randint(0, WIDTH - 1), randint(0, HEIGHT - 1)]
            self.pos_let.append(x)

    def Zapolnenie_Letters(self):
        for y in range(len(self.pos_let)):
            self.FIELD[self.pos_let[y][0]][self.pos_let[y][1]] = self.letters[y]

    def Move(self):
        if self.snake_tail > 0:
            for i in range(self.snake_tail, 0, -1):
                self.snake[i][0] = self.snake[i - 1][0]
                self.snake[i][1] = self.snake[i - 1][1]
        self.snake[0][0] = (self.snake[0][0] + direction[0])
        self.snake[0][1] = (self.snake[0][1] + direction[1])

    def Check_On_Lose(self):
        if not (0 <= self.snake[0][0] < WIDTH) or not (0 <= self.snake[0][1] < HEIGHT):
            return 0

    def Check_On_Self_Eat(self):
        if self.snake[0] in self.snake[1:]:
            return 0

    def Check_On_Eat(self):
        if self.snake[0] in self.pos_let:
            return 1

    def Eat(self):
        temp = self.snake[0]
        self.snake[0] = [self.snake[0][0] + direction[0], self.snake[0][1] + direction[1]]
        self.snake.insert(1, temp)
        self.snake_tail += 1
        self.onelet = self.letters[self.pos_let.index(temp)]
        self.eaten_letters.append(self.letters[self.pos_let.index(temp)])
        self.pos_let.clear()
        self.letters.clear()
        self.RandLet()


class HangmanField:
    def __init__(self):
        self.FIELD = [
            list(row)
            for row in FINAL_FIELD
        ]
        self.chasti_cheloveka = 0
        for cell in HUMAN:
            self.FIELD[cell[0]][cell[1]] = ' '
        self.letter = ''
        self.secret_word = SECRET
        self.guessed = ['_' for _ in self.secret_word]

    def Vyvod_Polya(self):
        for row in self.FIELD:
            print(''.join(row))

    def Dorisovka_Polya(self):
        self.FIELD[HUMAN[self.chasti_cheloveka][0]][HUMAN[self.chasti_cheloveka][1]] = \
        FINAL_FIELD[HUMAN[self.chasti_cheloveka][0]][
            HUMAN[self.chasti_cheloveka][1]]

    def Proverka_Na_Lose(self):
        if self.chasti_cheloveka == 6:
            return 0

    def Proverka_na_Pobedu(self):
        if '_' not in self.guessed:
            return 0

    def Vyvod_Ugadannyh_Bukv(self):
        print(''.join(self.guessed), len(self.secret_word))

    def Proverka_Na_Nalichie(self):
        if self.letter not in self.secret_word:
            self.Dorisovka_Polya()
            self.chasti_cheloveka += 1
        else:
            for i in range(len(self.secret_word)):
                if self.letter == self.secret_word[i]:
                    self.guessed[i] = self.letter


class GameSnakeHangman:
    def __init__(self):
        self.SnakeField = SnakeField()
        self.HangmanField = HangmanField()

    def Run(self):
        global eaten
        with keyboard.Listener(on_press=process_press) as listener:
            self.SnakeField.RandLet()
            while True:
                os.system('cls' if os.name == 'nt' else 'clear')
                if self.SnakeField.Check_On_Lose() == 0:  # проверка на стенки
                    print("You lost!")
                    print('Слово было:', ''.join(SECRET))
                    break
                if self.SnakeField.Check_On_Self_Eat() == 0:  # проверка на съедание себя
                    print("You lost!")
                    print('Слово было:', ''.join(SECRET))
                    break

                if self.HangmanField.Proverka_Na_Lose() == 0:
                    print("You lost!")
                    print('Слово было:', ''.join(SECRET))
                    break
                if self.HangmanField.Proverka_na_Pobedu() == 0:
                    print('You won!')
                    break

                self.SnakeField.The_Field()
                self.SnakeField.Zapolnenie_Letters()
                self.SnakeField.Zapolnenie_Snake()
                self.SnakeField.Vyvod_Polya()

                print('\n\n\n')

                self.HangmanField.Vyvod_Polya()
                self.HangmanField.Vyvod_Ugadannyh_Bukv()
                print(self.SnakeField.eaten_letters)
                if self.SnakeField.snake[0] == [0, 0]:
                    self.SnakeField.pos_let.clear()
                    self.SnakeField.letters.clear()
                    self.SnakeField.RandLet()

                if self.SnakeField.Check_On_Eat() == 1:
                    self.SnakeField.Eat()
                    self.HangmanField.letter = self.SnakeField.eaten_letters[eaten]
                    eaten += 1
                    self.HangmanField.Proverka_Na_Nalichie()
                else:
                    self.SnakeField.Move()
                time.sleep(TIME)


game = GameSnakeHangman()
game.Run()

'''def Snake_Eat_Apple(self):
    if self.snake[0][0] + direction[0]== self.apple[0] and self.snake[0][1] + direction[1] == self.apple[1]:
        self.apple = random_position()
        return 1

    def Zapolnenie_Apple(self):
        self.FIELD[self.apple[0]][self.apple[1]] = 'a'

    if self.Field.Snake_Eat_Apple() == 1:
                    temp = self.Field.snake[0]
                    self.Field.snake[0] = [self.Field.snake[0][0] + direction[0], self.Field.snake[0][1] + direction[1]]
                    self.Field.snake.insert(1, temp)
                    self.Field.snake_tail += 1
                    attempts += 1
                else:
                    self.Field.Move()
    '''
