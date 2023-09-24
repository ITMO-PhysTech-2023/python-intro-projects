import random

# Список слов для угадывания
word_list = ["яблоко", "банан", "змея", "итмо", "африка", "музыка"]

# изображения виселицы
hangman_images = [
    """
        _________
       |         |
       |
       |
       |
       |
    """,
    """
        _________
       |         |
       |         O
       |
       |
       |
    """,
    """
        _________
       |         |
       |         O
       |         |
       |
       |
    """,
    """
        _________
       |         |
       |         O
       |        /|
       |
       |
    """,
    """
        _________
       |         |
       |         O
       |        /|\\
       |
       |
    """,
    """
        _________
       |         |
       |         O
       |        /|\\
       |        /
       |
    """,
    """
        _________
       |         |
       |         O
       |        /|\\
       |        / \\
       |
    """
]


# Выбор случайного слова из списка
def choose_word(word_list):
    return random.choice(word_list)


# Инициализация игры
def initialize_game():
    word_to_guess = choose_word(word_list)
    guessed_letters = set()
    incorrect_attempts = 0
    return word_to_guess, guessed_letters, incorrect_attempts


# Отображение текущего состояния слова с угаданными буквами
def display_word(word, guessed_letters):
    display = ""
    for letter in word:
        if letter in guessed_letters:
            display += letter
        else:
            display += "_"
    return display


# Отображение текущего состояния виселицы
def display_hangman(incorrect_attempts):
    return hangman_images[incorrect_attempts]


# Основная функция игры
def hangman_game():
    word_to_guess, guessed_letters, incorrect_attempts = initialize_game()
    max_attempts = len(hangman_images) - 1

    print("Добро пожаловать в игру 'Виселица'!")

    while True:
        print(display_hangman(incorrect_attempts))
        print(display_word(word_to_guess, guessed_letters))

        if "_" not in display_word(word_to_guess, guessed_letters):
            print("Поздравляем, вы угадали слово: " + word_to_guess)
            break

        if incorrect_attempts >= max_attempts:
            print("Вы проиграли. Загаданное слово было: " + word_to_guess)
            break

        guess = input("Угадайте букву: ").lower()

        if len(guess) != 1 or not guess.isalpha():
            print("Пожалуйста, введите одну букву.")
            continue

        if guess in guessed_letters:
            print("Вы уже угадали эту букву.")
        elif guess in word_to_guess:
            guessed_letters.add(guess)
        else:
            guessed_letters.add(guess)
            incorrect_attempts += 1


if __name__ == "__main__":
    hangman_game()