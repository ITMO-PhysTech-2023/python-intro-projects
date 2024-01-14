import pygame
import random
pygame.init()

# Создание окна
win = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Змейка")


class Letter:
    def __init__(self, height: int, width: int, block_size: int, secret_word):
        self.position = (0, 0)
        self.color = (255, 255, 255)
        self.height = height
        self.width = width
        self.block_size = block_size
        self.randomize_position()
        self.secret_word = secret_word
        self.letter = random.choice(secret_word)

    def randomize_position(self):
        self.position = (random.randint(0, round(self.width / self.block_size - 1)) * self.block_size,
                         random.randint(0, round(self.height / self.block_size - 1)) * self.block_size)

    def get_letter(self):
        return random.choice(self.secret_word)

    def draw(self, surface, letter):
        if letter != '':
            self.letter = letter
        font = pygame.font.SysFont(None, 25)
        text = font.render(self.letter, True, self.color)
        surface.blit(text, self.position)


class Food:
    def __init__(self, height: int, width: int, block_size: int):
        self.position = (0, 0)
        self.color = (255, 255, 255)
        self.height = height
        self.width = width
        self.block_size = block_size
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, round(self.width / self.block_size - 1)) * self.block_size,
                         random.randint(0, round(self.height / self.block_size - 1)) * self.block_size)

    def draw(self, surface):
        r = pygame.Rect((self.position[0], self.position[1]), (self.block_size, self.block_size))
        pygame.draw.rect(surface, self.color, r)
        pygame.draw.rect(surface, self.color, r, 1)


# Класс для змейки
class Snake:
    def __init__(self, height: int, width: int,
                 block_size: int,
                 directions: list, secret_word: str):
        self.length = 1
        self.block_size = block_size
        self.width = width
        self.height = height
        self.positions = [((width / 2), (height / 2))]
        self.directions = directions
        self.direction = random.choice(directions)
        self.color = (255, 0, 0)
        self.white_color = (255, 255, 255)
        self.letter = Letter(height, width, block_size, secret_word)
        self.food = Food(height, width, block_size)

    def get_head_position(self):
        return self.positions[0]

    def turn(self, point):
        if self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return
        else:
            self.direction = point

    def move(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = (((cur[0] + (x * self.block_size)) % self.width, (cur[1] + (y * self.block_size)) % self.height))
        if len(self.positions) > 2 and new in self.positions[2:]:
            self.end_game()
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()

    def end_game(self):
        pygame.quit()
        print('oops you lost(')

    def draw(self, surface):
        for p in self.positions:
            r = pygame.Rect((p[0], p[1]), (self.block_size, self.block_size))
            pygame.draw.rect(surface, self.color, r)
            pygame.draw.rect(surface, self.white_color, r, 1)

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.turn(self.directions[0])
                elif event.key == pygame.K_DOWN:
                    self.turn(self.directions[1])
                elif event.key == pygame.K_LEFT:
                    self.turn(self.directions[2])
                elif event.key == pygame.K_RIGHT:
                    self.turn(self.directions[3])

    def run(self):
        clock = pygame.time.Clock()
        while True:
            win.fill((0, 0, 0))
            self.handle_keys()
            self.move()
            if self.get_head_position() == self.letter.position or self.get_head_position() == self.food.position:
                self.length += 1
                self.letter.randomize_position()
                self.letter.draw(win, random.choice('ghghghgh'))
                self.food.randomize_position()
                self.food.draw(win)

            self.draw(win)
            self.letter.draw(win, '')
            self.food.draw(win)

            pygame.display.update()
            clock.tick(10)


if __name__ == '__main__':
    game = Snake(600, 800, 20, [(0, -1), (0, 1), (-1, 0), (1, 0)], 'mama')
    game.run()
