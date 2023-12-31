import pygame
import random

# Инициализация Pygame
pygame.init()

# Размеры окна
WIDTH = 800
HEIGHT = 600

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Класс змейки
class Snake:
    def __init__(self, surface):
        self.size = 1
        self.segments = [(WIDTH // 2, HEIGHT // 2)]
        self.direction = random.choice(['left', 'right', 'up', 'down'])
        self.surface = surface
        self.is_hanged = False
        self.attempt = 0
        self.FIELDS = [
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
           /|    |
                 |
         _______/|\_
         ''',

            r'''
            +----+
            |    |
            o    |
           /|\   |
                 |
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

    def move(self):
        x, y = self.segments[0]
        if self.direction == 'left':
            x -= 10
        elif self.direction == 'right':
            x += 10
        elif self.direction == 'up':
            y -= 10
        elif self.direction == 'down':
            y += 10
        self.segments.insert(0, (x, y))
        if len(self.segments) > self.size:
            self.segments.pop()
        if x >= WIDTH or x < 0 or y >= HEIGHT or y < 0:
            Game.check_game_over(self)

    def change_direction(self, direction):
        if direction == 'left' and self.direction != 'right':
            self.direction = 'left'
        elif direction == 'right' and self.direction != 'left':
            self.direction = 'right'
        elif direction == 'up' and self.direction != 'down':
            self.direction = 'up'
        elif direction == 'down' and self.direction != 'up':
            self.direction = 'down'

    def draw(self):
        for segment in self.segments:
            pygame.draw.rect(self.surface, WHITE, (segment[0], segment[1], 10, 10))

    def check_collision(self, letters, guessed_word,beginword,attempt):
        head = self.segments[0]
        for letter in letters:
            if letter.rect.collidepoint(head):
                if letter.letter in guessed_word:
                    letter.correct = True
                    for i in range(len(guessed_word)):
                        if guessed_word[i] == letter.letter:
                            beginword[i]=letter.letter
                            print(*beginword)
                    self.size += 2

                else:
                    if self.attempt == 7:
                        print('Вы проиграли!')
                        Game.check_game_over(self)
                    else:
                        print(self.FIELDS[self.attempt])
                        self.attempt += 1
                    self.size += 2
                letters.remove(letter)

# Класс буквы
class Letter:
    def __init__(self, x, y, letter):
        self.x = x
        self.y = y
        self.letter = letter
        self.newletter=letter
        self.correct = False
        self.rect = pygame.Rect(self.x, self.y, 10, 10)

    def draw(self, surface):
        if self.correct:
            self.color = RED
        else:
            self.color = WHITE

        pygame.draw.rect(surface, self.color, (self.x, self.y, 10, 10))
        font = pygame.font.Font(None, 20)
        text = font.render(self.letter, True, BLACK)
        surface.blit(text, (self.x, self.y))


# Класс игры
class Game:
    def __init__(self, surface):

        self.snake = Snake(surface)
        self.letters = []
        self.newletters=''
        self.guessed_word = ''
        self.hanged_man = []
        self.is_hanged = False
        self.surface = surface
        self.beginword = []
        self.happid_word=[]
        self.attempt=Snake(surface)

        # Загадываем слово
        word = input("Введите слово для угадывания: ")
        self.guessed_word = word.lower()

        # Размещаем буквы
        for letter in self.guessed_word:
            x = random.randint(0, WIDTH - 10)
            y = random.randint(0, HEIGHT - 10)
            self.letters.append(Letter(x, y, letter))
            self.happid_word.append(Letter(x, y, letter))
            x += 15

        #Вводим другие буквы
        otherletters = ''
        for otherletters in 'qwertyuiopasdfghjklzxcvbnm':
            if otherletters not in self.guessed_word:
                self.newletters=self.newletters+otherletters
            if len(self.newletters)==15:
                break

        #Размещаем буквы
        for letter in self.newletters:
            x = random.randint(0, WIDTH - 10)
            y = random.randint(0, HEIGHT - 10)
            self.letters.append(Letter(x, y, letter))
            x+=15

        for i in range(len(self.guessed_word)):
            self.beginword.append('_')
        print(*self.beginword)



    def run(self):
        clock = pygame.time.Clock()
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.snake.change_direction('left')
                    elif event.key == pygame.K_RIGHT:
                        self.snake.change_direction('right')
                    elif event.key == pygame.K_UP:
                        self.snake.change_direction('up')
                    elif event.key == pygame.K_DOWN:
                        self.snake.change_direction('down')

            self.snake.move()
            self.snake.check_collision(self.letters, self.guessed_word,self.beginword,self.snake.attempt)
            if self.snake.is_hanged:
                print('Вы проиграли!')
                break
            if '_' not in self.beginword:
                print("Вы выиграли!")
                break

            self.surface.fill(BLACK)

            for letter in self.letters:
                letter.draw(self.surface)
            for newletter in self.newletters:
                letter.draw(self.surface)

            self.snake.draw()

            pygame.display.flip()

            clock.tick(10)

        pygame.quit()
    def check_game_over(self):
        self.snake.is_hanged = True


# Создаем окно игры
surface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Змейка')

# Запускаем игру
game = Game(surface)
game.run()
