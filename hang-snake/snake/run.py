import time
import vars
from common.util import clear_terminal
from pynput import keyboard
from random import randint
from vars import repeat, proposal_repeat


def generate_position(width, height):
    return randint(0, width - 1), randint(0, height - 1)


def generate_diff_pos(width, height):
    position_for_fl = []
    for i in range(vars.hard_level - 1):
        pos = generate_position(width, height)
        while pos in position_for_fl:
            pos = generate_position(width, height)
        position_for_fl.append(pos)
    return position_for_fl


def generate_letter():
    alphabet = list('abcdefghijklmnoprstuvwxyz')
    for row in vars.secret_word:
        if row in alphabet:
            alphabet.pop(alphabet.index(row))
    return alphabet


direction = (1, 0)


def process_press(key):
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


class Letters:
    def __init__(self, width, height):
        self.right_letter = generate_position(width, height)
        self.random_letter = generate_diff_pos(width, height)
        self.symbol_tl = vars.secret_word[randint(0, len(vars.secret_word) - 1)]
        self.symbol_fl = [generate_letter()[randint(0, len(generate_letter()))] for row in
                          range(vars.hard_level - 1)]


class Snake:
    def __init__(self, width, height):
        self.snake = [generate_position(width, height)]
        self.body_snake = 0
        self.new_elem = (self.snake[0][0] + direction[0], self.snake[0][1] + direction[1])


class Field:
    def __init__(self, height_F: int, width_F: int):
        self.Letters_f = Letters(width_F, height_F)
        self.Snake_f = Snake(width_F, height_F)
        self.height = height_F
        self.width = width_F
        self.field = [['.' for i in range(width_F)] for i in range(height_F)]

    def put_true_letter(self):
        self.field[self.Letters_f.right_letter[0]][self.Letters_f.right_letter[1]] = self.Letters_f.symbol_tl

    def put_false_letter(self):
        for i in vars.hard_level-1:
            self.field[self.Letters_f.random_letter[i][0]][self.Letters_f.random_letter[i][1]] = (
                self.Letters_f.symbol_fl)[i]

    def put_snake(self):
        for i in range(self.Snake_f.body_snake + 1):
            if i == 0:
                self.field[self.Snake_f.snake[0][0]][self.Snake_f.snake[0][1]] = 'O'
            else:
                self.field[self.Snake_f.snake[i][0]][self.Snake_f.snake[i][1]] = 'o'

    def print_f(self):
        if __name__ == '__main__':
            for row in self.field:
                print(' '.join(row))
        else:
            vars.init_var()
            vars.field_snake = self.field


class GameSnake:
    def __init__(self, height_f: int, width_f: int, wait_time_repeat):
        self.Field = Field(height_f, width_f)
        self.l_width = [i for i in range(self.Field.width + 1)]
        self.l_height = [i for i in range(self.Field.height + 1)]
        self.wait_time = wait_time_repeat
        self.height_field = height_f
        self.width_field = width_f

    @property
    def Snake(self):
        return self.Field.Snake_f

    @property
    def Letter(self):
        return self.Field.Letters_f

    def check_to_eat(self):
        return self.Snake.new_elem == self.Letter.right_letter or self.Snake.new_elem in self.Letter.random_letter

    def eat_tl(self):
        return self.Snake.new_elem == self.Letter.right_letter

    @staticmethod
    def not_full_word():
        rest_of_word = str(list(vars.secret_word).pop(vars.last_letter))
        return rest_of_word

    def create_new_pos(self):
        while self.Letter.right_letter in self.Snake.snake or self.Snake.new_elem in self.Letter.random_letter:
            self.Letter.right_letter = generate_position(self.width_field, self.height_field)
            self.Letter.random_letter = generate_diff_pos(self.width_field, self.height_field)
        self.Letter.symbol_tl = self.not_full_word()[randint(0, len(self.not_full_word()) - 1)]
        self.Letter.symbol_fl = [generate_letter()[randint(0, len(generate_letter()))] for row in
                                 vars.hard_level - 1]

    def eat(self):
        self.Snake.snake.insert(0, self.Snake.new_elem)
        vars.init_var()
        if self.check_to_eat():
            self.create_new_pos()
            self.Snake.body_snake += 1
            if self.eat_tl():
                vars.import_letter = self.Letter.symbol_tl
            else:
                vars.import_letter = self.Letter.symbol_fl[self.Letter.random_letter.index(self.Snake.new_elem)]
        else:
            self.Snake.snake.pop(-1)

    def check_move(self):
        return (self.Snake.new_elem[0] not in self.l_height or self.Snake.new_elem[1] not in self.l_width or
                self.Snake.new_elem in self.Snake.snake)

    def update_var(self):
        self.Field.field = [['.' for i in range(self.width_field)] for i in range(self.height_field)]
        self.Snake.new_elem = (self.Snake.snake[0][0] + direction[0], self.Snake.snake[0][1] + direction[1])

    def do_change(self):
        if self.Snake.body_snake == 0:
            self.Field.field[self.Snake.snake[0][0]][self.Snake.snake[0][1]] = 'O'
        else:
            self.Field.put_snake()
        self.Field.put_true_letter()

    def run(self):
        vars.init_var()
        with keyboard.Listener(on_press=process_press):
            while True:
                clear_terminal()
                self.update_var()
                if self.check_move():
                    print('You lost')
                    proposal_repeat()
                    with keyboard.Listener(on_press=repeat):
                        time.sleep(3)
                        if vars.a == 'continue':
                            continue
                        else:
                            break
                self.do_change()
                self.Field.print_f()
                self.eat()
                time.sleep(self.wait_time)


if __name__ == '__main__':
    wait_time = 0.3
    width = 15
    height = 15
    game = GameSnake(height, width, wait_time)
    game.run()
