from snake.testovayazmeya import score
self_count=score
print(self_count)
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
def print_text(message, x, y, font_color=('Black'), font_type='Arial.ttf', font_size=50):
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
def display_word(word, guessed):
    display = ''
    for letter in word:
        if letter in guessed:
            display += letter
        else:
            display += '_'
        display += ' '
    print_text('SELF COUNT:' + str(self_count), 50, 50, ('Black'), 'Arial.ttf',30)
    text = pygame.font.SysFont(None, 35).render(display, True, (0,0,0))
    sc.blit(text, (SIZE/6, 600))

def get_word():
    word_list = ['capybara']
    return random.choice(word_list)
def input_letter():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.unicode.isalpha():
                    return event.unicode.lower()
def check_letter(letter, word, guessed,human_parts):
    if letter not in word:
        add_human_part(human_parts)
        return False
    guessed.append(letter)
    return True
def has_won(word, guessed):
    for letter in word:
        if letter not in guessed:
            return False
    return True
# Основной код игры
def game():
    game_over = False
    word = get_word()
    guessed = []
    human_parts=0
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        display_word(word, guessed)
        letter = input_letter()
        if not check_letter(letter, word, guessed,human_parts):
            if human_parts == 5:
                game_over = True
            human_parts += 1
        elif has_won(word, guessed):
            game_over = True
        pygame.display.update()
    pygame.quit()
    quit()
game()