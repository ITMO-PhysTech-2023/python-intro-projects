import os
from time import *
from random import *
import msvcrt as m
from threading import Thread


x = 0
y = 0
game_thread = True
apple_1_x = 1
apple_2_x = 2
apple_3_x = 3
apple_1_y = 1
apple_2_y = 2
apple_3_y = 3
button_defult = "d"
ln = 0
icon_player = "@"
tail = "o"
last2X = 0
last2Y = 0
lastX = 0
lastY = 0
elemX = [0 for i in range(100)]
elemY = [0 for i in range(100)]
dictionary = 'limit'
dict_mas = open('dictionary.txt')
a = [str(i)[:-1] for i in dict_mas.readlines()]


def start_position():
    global x, y
    x = randint(5,15)
    y = randint(5,15)
def clear():
    os.system('cls')
def create_secret():
    i = randint(0, len(a)-1)
    return a[i]
def field(x):
    if x == 1:
        print(' '*25+'           ')
        print(' '*25+'           ')
        print(' '*25+'           ')
        print(' '*25+'           ')
        print(' '*25+'           ')
        print(' '*25+'_______/|\_')
    elif x == 2:
        print(' '*25+'        +')
        print(' '*25+'        |')
        print(' '*25+'        |')
        print(' '*25+'        |')
        print(' '*25+'        |')
        print(' '*25+'_______/|\_')
    elif x == 3:
        print(' '*25+'   +----+')
        print(' '*25+'        |')
        print(' '*25+'        |')
        print(' '*25+'        |')
        print(' '*25+'        |')
        print(' '*25+'_______/|\_')
    elif x == 4:
        print(' '*25+'   +----+')
        print(' '*25+'   |    |')
        print(' '*25+'        |')
        print(' '*25+'        |')
        print(' '*25+'        |')
        print(' '*25+'_______/|\_')
    elif x == 5:
        print(' '*25+'   +----+')
        print(' '*25+'   |    |')
        print(' '*25+'   o    |')
        print(' '*25+'        |')
        print(' '*25+'        |')
        print(' '*25+'_______/|\_')
    elif x == 6:
        print(' '*25+'   +----+')
        print(' '*25+'   |    |')
        print(' '*25+'   o    |')
        print(' '*25+'  /|\   |')
        print(' '*25+'  / \   |')
        print(' '*25+'_______/|\_')
first_letter = ''
second_letter = ''
third_letter = ''
word = create_secret()
cor_letters = []
to_show = ['_']*len(word)
incor_letters = ''
tries = 6

def viselitsa(a):
    global cor_letters, incor_letters, tries, game_thread, to_show, word
    if a not in word:
        incor_letters = incor_letters + a + ' '
        tries -= 1
    if tries == 0:
        print('YOU LOSE!')
        game_thread = False
        exit()
    else:
        cor_letters.append(a)
        for i in range(len(word)):
            if word[i] == a:
                to_show[i] = a
    s = str(to_show)
    print('word:')
    print(*to_show)
    print('gallows:')
    field(6-tries)
    if to_show == list(word):
        print('YOU WON!')
        game_thread = False
        exit()
    else:
        print('Incorrect letters:')
        print(incor_letters)
def apples_letters():
    global cor_letters, word, apple_1_x, apple_2_x, apple_3_x, apple_3_y, apple_1_y, apple_2_y, first_letter, second_letter, third_letter
    word_letters = list(word)
    avail = [x for x in word_letters if x not in cor_letters]
    bad_letters = [x for x in list('qwertyuiopasdfghjlzcvbnm') if x not in word_letters and x not in list(incor_letters)]
    k = randint(0, len(avail)-1)
    u1 = 0
    u2 = 0
    while u1 == u2 or u1 == k or u2 == k:
        u1 = randint(0, len(bad_letters)-1)
        u2 = randint(0, len(bad_letters)-1)
    first_letter = avail[k]
    second_letter = bad_letters[u1]
    third_letter = bad_letters[u2]
    for i in range(3):
        apple_1_x = randint(4, 17)
        apple_2_x = randint(4, 17)
        apple_3_x = randint(4, 17)
        apple_1_y = randint(4, 17)
        apple_2_y = randint(4, 17)
        apple_3_y = randint(4, 17)

def board(width: int = 20, height: int = 20, pos_player_x: int = x, pos_player_y: int = y):
    global ln, game_thread, head, last2X, lastX, lastY, last2Y, elemY, elemX, apple_1_x, apple_2_x, apple_3_x, apple_3_y, apple_1_y, apple_2_y, first_letter, second_letter, third_letter
    clear()
    for i in range(height):
        for j in range(width):
            if (pos_player_x == apple_1_x and pos_player_y == apple_1_y):
                ln += 1
                viselitsa(first_letter)
                apples_letters()
                sleep(5)
            if (pos_player_x == apple_2_x and pos_player_y == apple_2_y):
                ln += 1
                viselitsa(second_letter)
                apples_letters()
                sleep(5)
            if (pos_player_x == apple_3_x and pos_player_y == apple_3_y):
                ln += 1
                viselitsa(third_letter)
                apples_letters()
                sleep(5)
            for el in range(ln):
                if pos_player_x == elemX[el] and pos_player_y == elemY[el]:
                    print('YOU LOSE!')
                    game_thread = False
                    exit()

            if not (x in range(width - 19)) and not (y in range(height - 1)) or not (x in range(width - 1)) and not (y in range(height - 19)):
                print('YOU LOSE!')
                game_thread = False
                exit()

            if j == 0:
                print('#', end='')
            elif i == 0:
                print('#', end='')
            elif i == height - 1:
                print('#', end='')
            elif j == width - 1:
                print('#', end='')
            elif pos_player_x == j and pos_player_y == i:
                print(head, end='')
            elif apple_1_x == j and apple_1_y == i:
                print(first_letter, end='')
            elif apple_2_x == j and apple_2_y == i:
                print(second_letter, end='')
            elif apple_3_x == j and apple_3_y == i:
                print(third_letter, end='')
            else:
                flag = True
                for ls in range(ln):
                    if elemX[ls] == j and elemY[ls] == i:
                        print(tail, end="")
                        flag = False
                if flag: print(' ', end='')

        print()
        print()
    lastX = pos_player_x
    lastY = pos_player_y
    if ln > 0:
        for el in range(ln):
            last2X = elemX[el]
            last2Y = elemY[el]
            elemX[el] = lastX
            elemY[el] = lastY
            lastX = last2X
            lastY = last2Y


def button_move():
    global button_defult
    while game_thread:
        button_defult = m.getch()[0]


def move():
    global x, y, game_thread, button_defult, head
    while game_thread:
        if button_defult in ["", " "]:
            button_defult = "d"
        elif button_defult in ["w", 119, 230, 72]:
            y -= 1
            head = "@"
        elif button_defult in ["a", 97, 228, 75]:
            x -= 1
            head = "@"
        elif button_defult in ["s", 115, 235, 80]:
            y += 1
            head = "@"
        elif button_defult in ["d", 100, 162, 77]:
            x += 1
            head = "@"
        elif button_defult in ["exit", 27]:
            print("Вы покинули игру")
            game_thread = False
            exit()

        board(pos_player_x=x, pos_player_y=y)

        sleep(.2)


def main():
    create_secret()
    start_position()
    apples_letters()
    clear()
    board()
    Thread(target=move).start()
    Thread(target=button_move).start()

main()
