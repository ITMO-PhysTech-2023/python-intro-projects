import pygame
import random
# Определение базовых параметров
pygame.init()
DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 200)
LIGHT_RED = (255, 0, 0)
LIGHT_GREEN = (0, 255, 0)
LIGHT_BLUE = (0, 0, 255)
gameDisplay = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
# Создание функций
def display_hangman(count):
    if count == 0:
        pygame.draw.rect(gameDisplay, BLACK, [150, 100, 100, 10])
        pygame.draw.rect(gameDisplay, BLACK, [200, 100, 10, 400])
        pygame.draw.rect(gameDisplay, BLACK, [150, 500, 100, 10])
        pygame.display.update()
def display_word(word, guessed):
    display = ''
    for letter in word:
        if letter in guessed:
            display += letter
        else:
            display += '_'
        display += ' '
    text = pygame.font.SysFont(None, 35).render(display, True, BLACK)
    gameDisplay.blit(text, (DISPLAY_WIDTH/6, 400))
def get_word():
    word_list = ['python', 'java', 'ruby', 'javascript', 'swift', 'kotlin']
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
def check_letter(letter, word, guessed):
    if letter not in word:
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
    tries = 6
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        gameDisplay.fill(WHITE)
        display_hangman(tries)
        display_word(word, guessed)
        letter = input_letter()
        if not check_letter(letter, word, guessed):
            tries -= 1
            if tries == 0:
                game_over = True
        elif has_won(word, guessed):
            game_over = True
        pygame.display.update()
    pygame.quit()
    quit()
game()