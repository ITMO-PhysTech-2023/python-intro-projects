from pynput import keyboard
from random import randint
from time import sleep
from common.util import clear_terminal
import ctypes

WIDTH, HEIGHT = 15, 15

# TODO: ?
class List2(list):
    pass

def random_position():
    return [randint(0, HEIGHT - 1), randint(0, WIDTH - 1)]

def draw_screen(is_snake, is_apple, is_tail):
    def get_pos_char(x, y):
        o = [x, y]
        if is_snake(o): return "@"
        if (a := is_apple(o)) is not None: return a
        if is_tail(o):  return "+"
        return ' '
    print('#'*WIDTH + '##')
    for y in range(HEIGHT):
        print(end='#')
        #x = 0
        for x in range(WIDTH):
            print(get_pos_char(x, y), end='')
        #while x < WIDTH:
        #    near_x, _, ty = near_pos(x, y)
        #    if ty is None: break # TODO: or write lines...
        #    print(' ' * (near_x - x), end=ty)
        #    x = near_x + 1
        print('#')
    print('#'*WIDTH + '##')

# (saturated add)
def sadd(a, b, max_, min_ = 0):
    c = a + b
    if min_ <= c < max_: return c
    elif max_ <= c: return max_
    elif min_ > c: return min_

def find_idx(predict, lst):
    for i, item in enumerate(lst):
        if predict(item):
            return i
    return -1

def on_key_press(key, ptr):
    # SAFETY: this function does not reallocates or frees value of pointer
    # caller must verify that `ptr` is valid pointer to py_object
    drfn = ctypes.cast(ptr, ctypes.py_object).value
    match key:
        case keyboard.Key.left:
            drfn[0] = -1
            drfn[1] = 0
        case keyboard.Key.up:
            drfn[0] = 0
            drfn[1] = -1
        case keyboard.Key.right:
            drfn[0] = 1
            drfn[1] = 0
        case keyboard.Key.down:
            drfn[0] = 0
            drfn[1] = 1

class SnakeGame:
    """
    If True apples will be removed from map after taking it.
    Otherwise (False) it just changes position.
    """ # english b1 moment
    is_apples_finite: bool = False

    """
    Function, that called before apple was eaten.
    Takes snake game and apple char as arguments and returns nothing.
    """
    before_eat_apple = lambda _,apple: 0

    # NOTE: random_position() isn't random for every instance, lol
    snake: list[int] = random_position()
    apples: list[list[list[int]]] = [] # type: list[tupleAsList[tupleAsList[int, int], str]]
    tail: list[list[int]] = []
    direction = (1, 0)

    def __init__(self, apples: list[str] = ['*']*5, is_apples_finite = False):
        #self.apples = list(map(lambda x: [random_position(), x], apples))
        self.apples = []
        self.append_apples(apples)
        self.is_apples_finite = is_apples_finite
        self.direction = List2([1, 0])
    
    def append_apples(self, apples: list[str]):
        for a in apples:
            t = random_position()
            while find_idx(lambda x: x[0] == t, self.apples) != -1:
                t = random_position()
            self.apples.append([t, a])

    def on_key_press(self):
        return lambda o: on_key_press(o, id(self.direction))

    def draw_screen(self):
        def is_apple(o):
            i = find_idx(lambda x: x[0] == o, self.apples)
            return self.apples[i][1] if i != -1 else None
        draw_screen(
                is_snake=lambda o: o == self.snake,
                is_apple=is_apple,
                is_tail=lambda o: o in self.tail,
                )

    def loop(self):
        # move
        self.tail.insert(0, [self.snake[0], self.snake[1]])
        self.tail.pop()
        self.snake[0] = sadd(self.snake[0], self.direction[0], WIDTH - 1)
        self.snake[1] = sadd(self.snake[1], self.direction[1], HEIGHT - 1)
        # check tail
        if self.snake in self.tail:
            print("\nyou lose")
            exit(1)
        # check apples
        idx = find_idx(lambda x: x[0] == self.snake, self.apples)
        if idx != -1:
            self.before_eat_apple(self.apples[idx][1])
            self.tail.insert(0, [self.snake[0], self.snake[1]])
            if self.is_apples_finite:
                self.apples.pop(idx)
            else:
                self.apples[idx][0] = random_position()

    def run(self, timer: float = .1):
        # NOTE: python clones all objects in new thread (imagine a thread safety)
        # so just forward isn't works
        # SAFETY: current thread should not reallocate/free `self.direction`
        # TODO: rewrite without raw pointers
        with keyboard.Listener(on_press=self.on_key_press()) as listener:
            while True:
                print("Score:", len(self.tail))
                self.draw_screen()
                self.loop()
                sleep(timer)
                clear_terminal()
