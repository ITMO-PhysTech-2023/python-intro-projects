import pygame
import random

# Инициализация Pygame
pygame.init()

# Константы
WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Загрузка изображений виселицы
hangman_images = [pygame.image.load(f"hangman{str(i)}.png") for i in range(7)]
current_image = 0

# Слова для угадывания
words = ["pyton", "java", "class", "pygame", "snake", "hangman"]

# Выбираем случайное слово
word = random.choice(words)

# Создаем список для хранения угаданных букв
guessed_letters = []

# Инициализация окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Виселица")

# Функция для вывода текста на экран
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    surf.blit(text_surface, text_rect)

# Главный игровой цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key >= 97 and event.key <= 122:  # ASCII коды для букв 'a' до 'z'
                letter = chr(event.key)
                if letter not in guessed_letters:
                    guessed_letters.append(letter)
                    if letter not in word:
                        current_image += 1

    # Очистка экрана
    screen.fill(WHITE)

    # Рисуем виселицу
    if current_image < 7:
        screen.blit(hangman_images[current_image], (100, 100))

    # Выводим угаданные буквы
    display_word = ""
    for letter in word:
        if letter in guessed_letters:
            display_word += letter
        else:
            display_word += "_ "
    draw_text(screen, display_word, 36, WIDTH // 2, 400)

    # Проверка на победу или проигрыш
    if current_image == 6:
        draw_text(screen, "Вы проиграли! Правильное слово: " + word, 46, WIDTH // 2, 300)
    elif "_" not in display_word:
        draw_text(screen, "Вы победили!", 46, WIDTH // 2, 300)

    pygame.display.flip()

# Завершение игры
pygame.quit()
