from copy import deepcopy
from random import randint
from pynput import keyboard
from os import system
from time import sleep
from rules import rus_rules, eng_rules


def create_secret(a: list):
    return a[randint(0, len(a) - 1)]


class MainGame:
    hang_russian_words = ['капибара', 'аллигатор', 'черепаха', 'жираф', 'муравей', 'антилопа', 'медведь',
                          'обезьяна', 'ягуар', 'анаконда', 'выхухоль']
    hang_english_words = ['capybara', 'elephant', 'giraffe', 'chimpanzee', 'horse', 'monkey', 'scorpion',
                          'chicken', 'jaguar', 'chameleon', 'crocodile']
    HANG_FIELDS = [
        r'''
           +----+
                |
                |
                |
                |
        _______/|\_
        ''',
        r'''
           +----+
           |    |
                |
                |
                |
        _______/|\_
        ''',
        r'''
           +----+
           |    |
           o    |
                |
                |
        _______/|\_
        ''',
        r'''
           +----+
           |    |
           o    |
           |    |
                |
        _______/|\_
        ''',
        r'''
           +----+
           |    |
           o    |
           |\   |
                |
        _______/|\_
        ''',
        r'''
           +----+
           |    |
           o    |
          /|\   |
                |
        _______/|\_
        ''',
        r'''
           +----+
           |    |
           o    |
          /|\   |
          /     |
        _______/|\_
        ''',
        r'''
           +----+
           |    |
           o    |
          /|\   |
          / \   |
        _______/|\_
        '''
    ]

    def __init__(self, width: int, height: int, number_of_letters: int):
        self.SNAKE_WIDTH = width
        self.SNAKE_HEIGHT = height
        self.number_of_letters = number_of_letters
        self.SNAKE_SCREEN = list()
        self.snake_direction = (-1, 0)
        self.snake_pause = False
        self.snake_counter = 0
        self.snake_head = [int(self.SNAKE_HEIGHT / 2), int(self.SNAKE_HEIGHT / 2)]
        self.snake = [deepcopy(self.snake_head)]
        self.snake_apple = self.snake_random_position()
        self.HANG_SECRET = ''
        self.hang_letter_choosing = ''
        self.hang_invalid_letter = ''
        self.hang_wrong_letter = ''
        self.losing1 = ''
        self.losing2 = ''
        self.winning1 = ''
        self.winning2 = ''
        self.hang_secret_letters = []
        self.hang_turn_number = 0
        self.hang_trying_letters = []
        self.hang_letter = ''
        self.language = ''
        self.game_continue = ''
        self.snake_won = ''
        self.exit = ''
        self.rules = ''
        self.tried_letters = ''
        self.you_collected_letters = ''
        self.letters_on_field = []
        self.letters_positions = []
        self.letter_for_turn = ''

# обработка нажатия клавиш для змейки DONE
    def process_press(self, key):
        match key:
            case keyboard.Key.left:
                self.snake_direction = (0, -1)
            case keyboard.Key.up:
                self.snake_direction = (-1, 0)
            case keyboard.Key.right:
                self.snake_direction = (0, 1)
            case keyboard.Key.down:
                self.snake_direction = (1, 0)
            case keyboard.Key.esc:
                if self.snake_pause:
                    self.snake_pause = False
                else:
                    self.snake_pause = True

# выбор языка для всей игры DONE
    def choosing_language(self):
        while True:
            self.language = input('Select language/Выберите язык (Eng/Рус): ')
            if self.language == 'Eng':
                self.HANG_SECRET = create_secret(self.hang_english_words)
                self.hang_letter_choosing = 'Enter your letter: '
                self.hang_invalid_letter = "You didn't collect this letter! Try again"
                self.hang_wrong_letter = "This letter isn't in the word"
                self.losing1 = f'GAME OVER! \nYour score: '
                self.losing2 = f'\n' \
                               f'Your word was {self.HANG_SECRET.lower()}'
                self.winning1 = f'You won! Congratulations!\nYour score: '
                self.winning2 = '\n' \
                                f'Your word is {self.HANG_SECRET.upper()}'
                self.you_collected_letters = 'Your collected letters: '
                self.game_continue = 'Press Enter to continue'
                self.snake_won = 'Wow! \nYou finished snake...\nSo, you win)'
                self.exit = 'Press Enter to exit'
                self.tried_letters = 'You tried '
                self.rules = eng_rules
                break
            elif self.language == 'Рус':
                self.HANG_SECRET = create_secret(self.hang_russian_words)
                self.hang_letter_choosing = 'Введите букву: '
                self.hang_invalid_letter = 'Некорректный ввод. Попробуйте еще раз'
                self.hang_wrong_letter = 'Этой буквы нет в слове'
                self.losing1 = f'ПОТРАЧЕНО. \nВы набрали '
                self.losing2 = ' очков\n' \
                               f'Было загадано слово {self.HANG_SECRET.lower()}'
                self.winning1 = f'Победа!\n' \
                                f'{self.HANG_SECRET.upper()}' \
                                f'\nВаш счет: '
                self.winning2 = ''
                self.you_collected_letters = 'Собранные буквы: '
                self.game_continue = 'Чтобы продолжить, нажминет Enter'
                self.snake_won = 'ВОУ! \nТы победил в змейке, а значит, победил и во всей игре)'
                self.exit = 'Для выхода нажмите Enter'
                self.tried_letters = 'Вы уже пробовали буквы '
                self.rules = rus_rules
                break
            else:
                print('Invalid input! Try again/Некорректный ввод. Попробуйте еще раз')

# возвращает рандомную букву нужного языка DONE
    def random_letter(self):
        if self.language == 'Eng':
            return str(chr(randint(ord('a'), ord('z'))))
        elif self.language == 'Рус':
            return str(chr(randint(ord('а'), ord('я'))))

# возвращает список из трех рандомных букв DONE
    def field_letters_generation(self):
        self.letters_on_field = [self.random_letter()] * self.number_of_letters
        for i in range(len(self.letters_on_field)):
            while self.letters_on_field.count(self.letters_on_field[i]) > 1:
                self.letters_on_field[i] = self.random_letter()

# генерация рандомного положения объекта на поле змейки DONE
    def snake_random_position(self):
        return [randint(1, self.SNAKE_HEIGHT - 2), randint(1, self.SNAKE_WIDTH - 2)]

# возвращает список из трех позиций букв на поле DONE
    def letters_positions_generation(self):
        self.letters_positions = [self.snake_random_position()] * self.number_of_letters
        for i in range(len(self.letters_positions)):
            while self.letters_positions[i] == self.snake_apple or self.letters_positions[i] in self.snake or \
                    self.letters_positions.count(self.letters_positions[i]) > 1:
                self.letters_positions[i] = self.snake_random_position()

# создание поля змейки DONE
    def snake_make_field(self):
        for i in range(self.SNAKE_HEIGHT - 1):
            self.SNAKE_SCREEN.append(self.SNAKE_WIDTH * ['.'])

# генерация яблока для змейки DONE
    def apple_generation(self):
        while self.snake_apple in self.snake:
            self.snake_apple = self.snake_random_position()

# движение змейки и ее рост DONE
    def snake_move(self):
        if self.snake_apple in self.snake:
            self.snake_counter += 1
            self.letters_positions_generation()
            self.field_letters_generation()
            self.apple_generation()
            self.snake.insert(0, deepcopy(self.snake_head))
        else:
            self.snake.insert(0, deepcopy(self.snake_head))
            self.snake.pop()
        for i in range(len(self.letters_positions)):
            if self.letters_positions[i] in self.snake:
                if self.letters_on_field[i] != '.':
                    self.letter_for_turn = self.letters_on_field[i]
                self.letters_on_field[i] = '.'
                self.letters_positions_generation()
                self.field_letters_generation()
        self.snake_head[0] += self.snake_direction[0]
        self.snake_head[1] += self.snake_direction[1]

# проверка смерти змейки DONE
    def snake_is_lost(self) -> bool:
        return (self.snake_head[0] not in range(len(self.SNAKE_SCREEN))) or \
                (self.snake_head[1] not in range(len(self.SNAKE_SCREEN[1]))) or \
                (self.snake_head in self.snake)

# печатает поле для змейки DONE
    def snake_print_everything(self):
        field = ''
        screen = deepcopy(self.SNAKE_SCREEN)
        screen[self.snake_apple[0]][self.snake_apple[1]] = 'A'
        for j in range(len(self.letters_positions)):
            screen[self.letters_positions[j][0]][self.letters_positions[j][1]] = self.letters_on_field[j]
        for i in self.snake:
            screen[i[0]][i[1]] = 'o'
        screen[self.snake_head[0]][self.snake_head[1]] = 'S'
        for k in screen:
            field += ('  '.join(k) + '\n')
        print('\n' * 5)
        print(''.join(self.hang_secret_letters))
        print(', '.join(set(self.hang_trying_letters)))
        print(field)

# чекает правильность хода в висилице DONE
    def hang_chek_true(self):
        if self.hang_letter in self.HANG_SECRET:
            for i in range(len(self.HANG_SECRET)):
                if self.HANG_SECRET[i] == self.hang_letter:
                    self.hang_secret_letters[i] = self.hang_letter
            print(''.join(self.hang_secret_letters))
        else:
            self.hang_trying_letters.append(self.hang_letter)
            print(self.hang_wrong_letter, '(' + self.letter_for_turn + ')')
            self.hang_turn_number += 1

# чекает поражение в висилице DONE
    def hang_is_lost(self) -> bool:
        return self.hang_turn_number == len(self.HANG_FIELDS) - 1

# чекает поражение в любой из игр DONE
    def check_lost(self) -> bool:
        return self.hang_is_lost() or self.snake_is_lost()

# поражение DONE
    def lost(self):
        system('cls')
        print(self.losing1 + str(self.snake_counter) + self.losing2)
        input(self.exit)

# чекает победу DONE
    def check_won(self) -> bool:
        return ''.join(self.hang_secret_letters) == self.HANG_SECRET

# победа E
    def won(self):
        system('cls')
        print(self.winning1 + str(self.snake_counter) + self.winning2)
        input(self.exit)

# печатает всякое для виселицы
    def hang_print_everything(self):
        print(''.join(self.hang_secret_letters))
        print(self.HANG_FIELDS[self.hang_turn_number])
        print(self.tried_letters + ', '.join(set(self.hang_trying_letters)))

# запуск игры
    def run(self):
        system('cls')
        self.choosing_language()
        input(self.rules)
        self.field_letters_generation()
        self.snake_make_field()
        self.hang_secret_letters = ['_'] * len(self.HANG_SECRET)
        with keyboard.Listener(on_press=self.process_press):
            while True:
                if self.snake_pause:
                    continue
                self.snake_move()
                if self.check_lost():
                    self.lost()
                    break
                self.snake_print_everything()
                if self.letter_for_turn != '':
                    system('cls')
                    self.hang_print_everything()
                    self.hang_letter = self.letter_for_turn
                    self.hang_chek_true()
                    self.letter_for_turn = ''
                    input(self.game_continue)
                if self.check_won():
                    self.won()
                    break
                if len(self.snake) <= 55:
                    sleep(0.25 - (len(self.snake) * 0.003))
                else:
                    sleep(0.25 - 55 * 0.003)


if __name__ == '__main__':
    game = MainGame(25, 25, 5)
    game.run()

