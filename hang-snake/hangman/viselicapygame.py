import pygame
import random
self_count=5
SIZE=800
pygame.init()
def create_secret():
    return 'capybara'
SECRET = create_secret()
n = len(SECRET)
GUESSED = ['_' for _ in range(n)]
sc = pygame.display.set_mode([SIZE, SIZE])
start_field=pygame.image.load('1.png')
field1=pygame.image.load('2.png')
field2=pygame.image.load('3.png')
field3=pygame.image.load('4.png')
field4=pygame.image.load('5.png')
field5=pygame.image.load('6.png')
field6=pygame.image.load('7.png')
human_parts = 0
clock = pygame.time.Clock()
sc.fill(pygame.Color(255,255,255))
sc.blit(start_field,(30,50))
pygame.display.flip()
class Field:
    def __int__(self,hp:int):
        self.hp=human_parts
    def print_text(message, x, y, font_color=('Black'), font_type='Arial.ttf', font_size=50):
        font_type = pygame.font.Font(font_type, font_size)
        text = font_type.render(message, True, font_color, None)
        sc.blit(text, (x, y))
    def add_human_part(self,x:int):
        self.x=x
        if x == 0:
            sc.blit(start_field, (30, 50))
        if x == 1:
            sc.blit(field1, (30, 50))
        if x == 2:
            sc.blit(field2, (30, 50))
        if x == 3:
            sc.blit(field3, (30, 50))
        if x == 4:
            sc.blit(field4, (30, 50))
        if x == 5:
            sc.blit(field5, (30, 50))
        if x == 6:
            sc.blit(field6, (30, 50))
    def get_word(self):
        word_list = ['capybara']
        return random.choice(word_list)
#
class HangmanGame:
    def __int__(self,count:int):
        self.count=count
        self.parts=human_parts
        self.field=Field
    def display_word(self,word:str, guessed:str, score:int,parts:int):
        display = ''
        for letter in word:
            if letter in guessed:
                display += letter
            else:
                display += '_'
            display += ' '
        sc.fill(pygame.Color(255, 255, 255))
        self.field.add_human_part(parts)
        if score > 0:
            self.field.print_text('SELF COUNT:' + str(score), 50, 50, ('Black'), 'Arial.ttf', 30)
        else:
            self.field.print_text('SELF COUNT:0', 50, 50, ('Black'), 'Arial.ttf', 30)
        text = pygame.font.SysFont(None, 35).render(display, True, (0, 0, 0))
        sc.blit(text, (SIZE / 6, 600))
    def input_letter(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.unicode.isalpha():
                        return event.unicode.lower()
    def counter(self,count):
        if count != 0:
            count -= 1
        return count
    def check_letter(self,letter, word, guessed, human_parts, count):
        if letter not in word:
            if self.counter(count) >= 0:
                return False
            else:
                self.field.add_human_part(human_parts)
                return False
        guessed.append(letter)
        return True

    def has_won(word, guessed):
        for letter in word:
            if letter not in guessed:
                return False
        return True



    # Основной код игры
class Game():
    def __int__(self,count):
        self.count=count
        game_over = False
        word=self.field.get_word()
        guessed = []
        human_parts = 0
        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            self.display_word(word, guessed, self.count, human_parts)
            letter = self.input_letter()
            if not self.check_letter(letter, word, guessed, human_parts, self.count):
                if human_parts == 6:
                    game_over = True
                if self.count <= 0:
                    human_parts += 1
                self.count -= 1
            elif self.has_won(word, guessed):
                game_over = True
            pygame.display.update()
        sc.fill(pygame.Color(255, 255, 255))
        # print_text('Good Job)' + str(score), 50, 50, ('Black'), 'Arial.ttf', 80)
        print('GOOD JOB)')
        pygame.quit()
        quit()
game=Game.__int__(2,2)

