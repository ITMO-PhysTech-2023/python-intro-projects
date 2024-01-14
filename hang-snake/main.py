import pygame
import random
from hangman.run import HangmanGame
from snake.run import Snake
from random_word import RandomWords
random_generator = RandomWords()


def create_secret_word():
    return random_generator.get_random_word()


win = pygame.display.set_mode((800, 600))

secret = create_secret_word()
hangman_game = HangmanGame(0, secret)
snake_game = Snake(600, 800, 20, [(0, -1), (0, 1), (-1, 0), (1, 0)], secret)


def game():
    hangman_game.show()
    clock = pygame.time.Clock()
    all_letters = ''.join(set(secret + 'bcdejklmrstu'))
    while True:
        win.fill((0, 0, 0))
        snake_game.handle_keys()
        snake_game.move()
        if snake_game.get_head_position() == snake_game.letter.position:
            snake_game.length += 1
            snake_game.letter.randomize_position()
            eaten_letter = snake_game.letter.letter
            all_letters = all_letters.replace(eaten_letter, '')
            next_letter = random.choice(all_letters)
            snake_game.letter.draw(win, next_letter)

            hangman_game.step(eaten_letter)
            hangman_game.show()
            if hangman_game.is_won():
                print('You won!')
                break
            if hangman_game.is_lost():
                print('(((')
                break

        if snake_game.get_head_position() == snake_game.food.position:
            snake_game.length += 1
            snake_game.letter.randomize_position()
            next_letter = random.choice(all_letters)
            snake_game.letter.draw(win, next_letter)
            snake_game.food.randomize_position()
            snake_game.food.draw(win)

        snake_game.draw(win)
        snake_game.letter.draw(win, '')
        snake_game.food.draw(win)

        pygame.display.update()
        clock.tick(10)


if __name__ == '__main__':
    game()