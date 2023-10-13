from pynput import keyboard
from random import randint
import os
import threading
import time
mutex = threading.Lock()
def spawnApple():
    while True:
        tryApple = random_position()
        if tryApple not in snake:
            return tryApple
def printField():
    os.system('cls')
    for i in range(WIDTH):
        for j in range(HEIGHT):
            if (i, j) in snake:
                print(0, end=' ')
            elif (i,j) == apple:
                print('A', end=' ')
            else:
                print('_', end=' ')
        print()

def scrawl():
    #threading.Timer(1.0, scrawl).start()
    global stop
    deleteLastCoor = True
    while stop == False:
        time.sleep(0.2)

        x = snake[0][0]+direction[0]
        y = snake[0][1] + direction[1]
        snake.insert(0,(x,y))

        if deleteLastCoor == True:
            snake.pop()
        global apple
        if snake[0] == apple:
            deleteLastCoor = False
            apple = spawnApple()
        else:
            deleteLastCoor = True
        printField()
        if keepMoving()==False:
            print("Game over")
            stop = True
            return 0
            #threading.Timer(1.0, scrawl).join()



def keepMoving():

    if (len(snake)>1 and snake[0] in snake[1:]) or snake[0][0]==-1 or snake[0][1]==-1 or snake[0][0]==HEIGHT or snake[0][1]==WIDTH:
        return False
    return True


def random_position():
    return randint(0, HEIGHT - 1), randint(0, WIDTH - 1)


def process_press(key):
    # обработчик нажатия на клавиши (можно сделать и поаккуратнее)
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
#def on_release(key):
#    if STOP==True:
        # Stop listener
#        return False

WIDTH, HEIGHT = 10, 10
stop = False
# можно приделать конфиг-файл с параметрами
direction = (1, 0)

snake = [random_position()]
apple = random_position()
printField()


'''def press():
    while True:  # making a loop
        try:  # used try so that if user pressed other than the given key error will not be shown
            if keyboard.is_pressed('q'):  # if key 'q' is pressed
                print('You Pressed A Key!')
                break  # finishing the loop
        except:
            break
t = threading.Thread(target=press())'''
run = threading.Thread(target=scrawl)
run.start()
with keyboard.Listener(on_press=process_press) as listener:
    listener.join()


run.join()

