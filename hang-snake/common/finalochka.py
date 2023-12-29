from snake.testovayazmeya import score
self_count=score
print('Your self count:',self_count)
import pygame
import random
SIZE=800
pygame.init()
sc = pygame.display.set_mode([SIZE, SIZE])
start_field=pygame.image.load('1.png')
field1=pygame.image.load('2.png')
field2=pygame.image.load('3.png')
field3=pygame.image.load('4.png')
field4=pygame.image.load('5.png')
field5=pygame.image.load('6.png')
field6=pygame.image.load('7.png')
human_parts = 0
sc.fill(pygame.Color(255,255,255))
sc.blit(start_field,(30,50))
class Screen:
    def __init__(self):
        self.parts=human_parts
        self.score=self_count
        self.sc=sc
    def print_text(self,message, x, y, font_color=('Black'), font_type='Arial.ttf', font_size=50):
        font_type = pygame.font.Font(font_type, font_size)
        text = font_type.render(message, True, font_color, None)
        self.sc.blit(text, (x, y))
    #pygame.display.flip()
    def add_human_part(self,x:int):
        if x == 0:
            self.sc.blit(start_field, (30, 50))
        if x == 1:
            self.sc.blit(field1, (30, 50))
        if x == 2:
            self.sc.blit(field2, (30, 50))
        if x == 3:
            self.sc.blit(field3, (30, 50))
        if x == 4:
            self.sc.blit(field4, (30, 50))
        if x == 5:
            self.sc.blit(field5, (30, 50))
        if x == 6:
            self.sc.blit(field6, (30, 50))
    #
    def get_word(self):
        word_list = ['itmo','football','sneakers','capybara']
        return random.choice(word_list)

    def input_letter(self):
        flag=False
        while not flag:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    flag=True
                    #pygame.quit()
                    #quit()
                if event.type == pygame.KEYDOWN:
                    if event.unicode.isalpha():
                        return event.unicode.lower()

clock = pygame.time.Clock()
pygame.display.flip()
class Game:
    def __init__(self):#,count:int):
        self.screen=Screen
        self.count=self_count
        self.word = self.screen.get_word(self)
        self.guessed = []
        self.human_parts = 0
        self.sc = sc
    def has_won(self,word, guessed):
        for letter in word:
            if letter not in guessed:
                return False
        return True
    def counter(self,count):
        if count != 0:
            count -= 1
        return count
    def check_letter(self,letter, word, guessed, human_parts, count):
        if letter not in word:
            if self.counter(count) >= 0:
                return False
            else:
                self.screen.add_human_part(self,human_parts)
                return False
        guessed.append(letter)
        return True
    # Основной код игры
    def display_word(self, word, guessed, score, parts):
        display = ''
        for letter in word:
            if letter in guessed:
                display += letter
            else:
                display += '_'
            display += ' '
        self.sc.fill(pygame.Color(255, 255, 255))
        self.screen.add_human_part(self,parts)
        if score > 0:
            self.screen.print_text(self,'SELF COUNT:' + str(score), 50, 50, ('Black'), 'Arial.ttf', 30)
        else:
            self.screen.print_text(self,'SELF COUNT:0', 50, 50, ('Black'), 'Arial.ttf', 30)
        text = pygame.font.SysFont(None, 35).render(display, True, (0, 0, 0))
        self.sc.blit(text, (SIZE / 6, 600))
        pygame.display.flip()
    def game(self,count):
        game_over = False
        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            self.display_word(self.word, self.guessed, count, self.human_parts)
            letter = self.screen.input_letter(self)
            if not self.check_letter(letter, self.word, self.guessed, self.human_parts, count):
                if self.human_parts == 6:
                    print('YOU LOSE')
                    game_over = True
                if count <= 0:
                    self.human_parts += 1
                count -= 1
            elif self.has_won(self.word, self.guessed):
                print('YOU WON')
                game_over = True
            pygame.display.update()
        self.sc.fill(pygame.Color(255, 255, 255))
        # print_text('Good Job)' + str(score), 50, 50, ('Black'), 'Arial.ttf', 80)
        #print('GOOD JOB)')
        pygame.quit()
        quit()
gm=Game()
gm.game(self_count)