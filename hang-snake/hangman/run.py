import random

words = ['capybara', 'dog', 'hehehe', 'program', 'yes-sir']

def get_random_word(words):
    return random.choice(words)


def display_word(word, guessed_letters):
    for letter in word:
        if letter in guessed_letters:
            print(letter, end=' ')
        else:
            print('_', end=' ')
    print()


def is_word_guessed(word, guessed_letters):
    for letter in word:
        if letter not in guessed_letters:
            return False
    return True


def play_game():
    word = get_random_word(words)
    guessed_letters = []
    lives = 6

    while lives > 0:
        display_word(word, guessed_letters)
        print('Lives left:', lives)

        guessed_letter = input('Guess a letter: ').lower()

        if guessed_letter in guessed_letters:
            print('You already guessed that letter!')
        elif guessed_letter in word:
            guessed_letters.append(guessed_letter)
            if is_word_guessed(word, guessed_letters):
                print('Congratulations! You guessed the word:', word)
                return
        else:
            lives -= 1
            if lives == 5:
                print(''''




                                            _______ / |\_
                                                        ''')
            if lives == 4:
                print(''''

                                                      |
                                                      |
                                                      |
                                            _______ / |\_
                                                        ''')
            if lives == 3:
                print(''''
                                                +----+
                                                      |
                                                      |
                                                      |
                                            _______ / |\_
                                                        ''')
            if lives == 2:
                print(''''
                                +----+
                                0     |
                                      |
                                      |
                            _______ / |\_
                                        ''')
            if lives == 1:
                print(''''
                            +----+
                            0     |
                          / | \   |
                                  |
                        _______ / |\_
                        ''')

            if lives == 0:
                print(''''
               +----+
               0
              /|\   |
              / \   |
            _______/|\_
            ''')
                print('You lost! Hehehe :)')

    print('Game over! The word was:', word)


play_game()
