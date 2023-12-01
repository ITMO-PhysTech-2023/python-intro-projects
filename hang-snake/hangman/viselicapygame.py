import pygame
import random
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
def print_text(message, x, y, font_color=('White'), font_type='Arial.ttf', font_size=50):
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(message, True, font_color, None)
    sc.blit(text, (x, y))
clock = pygame.time.Clock()

sc.fill(pygame.Color(255,255,255))
sc.blit(start_field,(30,50))
pygame.display.flip()
def add_human_part(x):
    if x==0:
        sc.blit(field1,(30,50))
    if x==1:
        sc.blit(field2,(30,50))
    if x==2:
        sc.blit(field3,(30,50))
    if x==3:
        sc.blit(field4,(30,50))
    if x==4:
        sc.blit(field5,(30,50))
    if x==5:
        sc.blit(field6,(30,50))
def check_guess(self, letter: str):
        if letter in self.secret:
            for i in range(len(self.secret)):
                if self.secret[i] == letter:
                    self.guessed[i] = letter
            print_text(self.guessed,(50,50))
        else:
            add_human_part(human_parts)
def input_letter():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.unicode.isalpha():
                    return event.unicode.lower()

def if_won(self) -> bool:
    return '_' not in self.guessed
def if_lose(self) -> bool:
    if sc==field6:
        return True
def game():
    while True:
        input_letter()
        if if_won():
            print_text('YOU WON',(50,30))
            pygame.quit()
        if if_lose():
            print_text('YOU LOSE', (50, 30))
            pygame.quit()



