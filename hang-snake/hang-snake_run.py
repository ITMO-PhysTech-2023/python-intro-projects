from pynput import keyboard
from random import randint
import os
import threading
import time
import string
mutex = threading.Lock()


def fieldHang(a):
    f0 = r'''
       +----+
       |    |
       o    |
      /|\   |
      / \   |
    _______/|\_
    '''
    f1 = r'''
       +----+
       |    |
       o    |
      /|\   |
            |
    _______/|\_
    '''
    f2 = r'''
       +----+
       |    |
       o    |
            |
            |
    _______/|\_
    '''
    f3 = r'''
       +----+
       |    |
            |
            |
            |
    _______/|\_
    '''
    f4 = r'''
       +----+
            |
            |
            |
            |
    _______/|\_
    '''
    f5 = r'''
            +
            |
            |
            |
            |
    _______/|\_
    '''
    f6 = r'''





    _______/|\_
    '''
    f7 = " "
    arr = [f0, f1, f2, f3, f4, f5, f6, f7]
    return arr[a]


def create_secret():
    dict = [i for i in open("hangman/dictionary")]
    i = randint(0, len(dict))
    return dict[i]


def hangman(currentLetter):
    global TRIES
    if TRIES > 0:

        if currentLetter not in SECRET:
            TRIES -= 1
            already_named.append(currentLetter)
            global letOther
            letOther.remove(currentLetter)

        else:
            global letWord
            letWord.remove(currentLetter)
            for i in range(len(SECRET) - 1):
                if SECRET[i] == currentLetter:
                    WORD[i] = currentLetter

def spawnLetters():
    let = {}
    # 2 буквы не из слова
    for i in range(2):
        while True:
            tryLetter = random_position()
            if tryLetter not in snake and tryLetter not in let.keys():
                let[tryLetter] = letOther[randint(0, len(letOther)-1)]
                break
    # буква из слова
    while True:
        tryLetter = random_position()
        if tryLetter not in snake and tryLetter not in let.keys():
            let[tryLetter] = letWord[randint(0, len(letWord)-1)]
            break
    return let
def printField():
    os.system('cls')
    for i in range(WIDTH):
        for j in range(HEIGHT):
            if (i, j) in snake:
                print(0, end=' ')
            else:
                print(lettersField.get((i,j), '_'), end=' ')
        print()
    FIELD = fieldHang(TRIES)
    print("\n x: ", *already_named)
    print(*WORD)

    print(FIELD)

def scrawl():

    global stop
    deleteLastCoor = True
    while stop == False:
        time.sleep(0.5)

        x = snake[0][0] + direction[0]
        y = snake[0][1] + direction[1]
        snake.insert(0, (x, y))

        if deleteLastCoor == True:
            snake.pop()

        # если змейка съела букву
        global lettersField
        if snake[0] in lettersField.keys():
            print(lettersField.get(snake[0]))
            hangman(lettersField.get(snake[0]))
            deleteLastCoor = False
            if len(letWord) > 0:
                lettersField = spawnLetters()
        else:
            deleteLastCoor = True
        printField()
        if keepMoving()==False:
            print("Game over")
            print(SECRET)
            stop = True
            return 0
        if len(letWord)==0:
            print("You win")
            return 0



def keepMoving():
    if TRIES==0 or (len(snake)>1 and snake[0] in snake[1:]) or snake[0][0]==-1 or snake[0][1]==-1 or snake[0][0]==HEIGHT or snake[0][1]==WIDTH:
        return False
    return True


def random_position():
    return randint(0, HEIGHT - 1), randint(0, WIDTH - 1)


def process_press(key):
    # обработчик нажатия на клавиши
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
    if stop == True:
        listener.stop()



WIDTH, HEIGHT = 10, 10
stop = False
direction = (1, 0)
snake = [random_position()]
SECRET = create_secret()
letWord = [i for i in SECRET]
letWord.pop(len(letWord)-1)
letWord = list(set(letWord))
letOther = [i for i in string.ascii_lowercase if i not in letWord]

WORD = ['_' for i in range(len(SECRET) - 1)]
lettersField = spawnLetters()
already_named = []
TRIES = 7
printField()

run = threading.Thread(target=scrawl)
run.start()
with keyboard.Listener(on_press=process_press) as listener:
    listener.join()

run.join()

