from pynput import keyboard
from random import randint

#WIDTH, HEIGHT = 20,20
class Apple:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.eaten = False
class Snake:
    def __init__(self, length):
        self.length = length
        self.x = 0
        self.y = 0

class SnakeGame:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.field = []
        for i in range( self.height ):
            self.field.append( ['#']*self.width )
        self.direction = (1,0)
        self.snake = Snake(1)
        self.apple = Apple()

    def print_field( self ):
        for i in range(self.height):
            for j in range( self.width ):
                if( i == self.snake.y and j == self.snake.x ):
                    print( '0' , end = '' )
                elif( i == self.apple.y and j == self.apple.x ):
                    print( 'A' , end = '' )
                else:
                    print( '#', end = '' )
            print()
        #print( *self.field[i] )

    def random_snake_head_position(self):
        position = []
        position = [randint(0, self.height - 1), randint(0, self.width - 1)]
        self.snake.x = position[1]
        self.snake.y = position[0]
    def random_apple_position(self):
        position = []
        position = [randint(0, self.height - 1), randint(0, self.width - 1)]
        self.apple.x = position[1]
        self.apple.y = position[0]

snakeGameA = SnakeGame(width = int(input()), height = int(input()))
snakeGameA.random_snake_head_position()
snakeGameA.random_apple_position()
snakeGameA.print_field()

#def random_position():
#    position = []
#    position = [randint(0, snakeGameA.height - 1), randint(0, snakeGameA.width - 1)]
#    return position

def process_press(key):
    global direction
    match key:
        case keyboard.Key.left:
            direction = (0, -1)
        case keyboard.Key.up:
            direction = (-1, 0)
        case keyboard.Key.right:
            direction = (0, 1)
        case keyboard.Key.down:
            direction = (1, 0)


# while apple[0] == snake[0]:
#     new_apple = [random_position()]
#     apple = new_apple

# with keyboard.Listener(on_press=process_press) as listener:
#      while True:
#         if (int(snake[0]) == snakeGameA.height or int(snake[0]) == -1 or int(snake[1]) == -1 or int(snake[1]) == snakeGameA.width):
#             break
#         else:
#             if (apple[1] == snake[1] and apple[0] == snake[0]):
#                 new_apple = random_position()
#                 apple = new_apple