from pynput import keyboard
from random import randint
from time import sleep
import os

def reductHF():
    global MAX
    if len(hangman[tries-1])>HEIGHT:
        FIELD.append('#'*WIDTH+'')
        for i in range(len(hangman[tries-1])-HEIGHT-1):
            FIELD.append(' '*WIDTH+'')
        MAX = len(hangman[tries-1]) 
    else:
        for i in range(HEIGHT-len(hangman[tries-1])):
            hangman[tries-1].append(" "*len(hangman[tries-1][0]))
        MAX = HEIGHT
def SCENE():
    print('############################################################')
    Sc=[]
    if tries==0:
        for i in range(MAX-1):
            Sc.append(FIELD[i]+'   '+hangman[len(hangman)-tries-1][i])
            print(Sc[i])
    else:
        for i in range(MAX-1):
            Sc.append(FIELD[i]+'   '+hangman[len(hangman)-tries][i])
            print(Sc[i])
    print('############################################################')    
def random_position():
    return randint(0, HEIGHT - 1), randint(0, WIDTH - 1)


def clear():
    os.system('cls')

def size_color():
    cmd = 'mode 70,18'
    os.system(cmd)
    cmcl = 'color 8E'     
    os.system(cmcl)
    
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

def snakepr():
    global y
    global x
    global R
    global k
    global G
    global word_X
    global direction
    global tries

    FIELD[snake[0][1]] = FIELD[snake[0][1]][:snake[0][0]]+' '+FIELD[snake[0][1]][1+snake[0][0]:]
    check_direction()
    if not(y>=HEIGHT-1 or y<0):
        y+=direction[0]
        x+=direction[1]
    if FIELD[y][x]=='*' and (not(y==snake[len(snake)-1][1] and x==snake[len(snake)-1][0])):
        G=1
    snake.append([x,y,direction[0],direction[1]])
    if [x,y] in applels: 
        R=1
        for i in range(3):
            if [x,y] == applels[i]:
                k=i
                symb_X=FIELD[y][x]
                if symb_X in word:
                    for j in range(len(word)):
                        if symb_X == word[j]:
                            word_X=word_X[:j] + symb_X +word_X[j+1:]
                            for t in range(len(hangman)):
                                hangman[t][7]=word_X
                else:
                    tries-=1
                    if tries >=0:
                        for t in range(len(hangman)):
                            hangman[t][8]='У Вас осталось попыток:'+str(tries)
    else:
        R=0
        snake.pop(0)
    if not(lose()):
        FIELD[snake[len(snake)-1][1]] = FIELD[snake[len(snake)-1][1]][:snake[len(snake)-1][0]]+'*'+FIELD[snake[len(snake)-1][1]][1+snake[len(snake)-1][0]:]
        
applels=[[0]*2]*3
symbsLIST =['0']*3

def SymbProvider(massive):
    str=chr(randint(ord('a'),ord('z')))
    while not(str in massive):
        if  len(massive)>1:
            str=chr(randint(ord('a'),ord('z')))
        elif len(massive)==1:
            str=massive[0]
        else:
            break
    return(str)

def check_direction():
    global x
    global y
    global direction
    if [x+direction[1],y+direction[0],-direction[0],-direction[1]] in snake:
        direction = (direction[0]*(-1),direction[1]*(-1))
        
def apple(k):
    global xa
    global ya
    global unused_symb
    global unused_symbW
    if k==0:
        symb = SymbProvider(unused_symbW)
        unused_symbW=unused_symbW.replace(symb,'')
    else:
        symb = SymbProvider(unused_symb)
    unused_symb=unused_symb.replace(symb,'')
    while True:
        xa=randint(0,WIDTH-2)
        ya=randint(0,HEIGHT-2)
        if FIELD[ya][xa]==' ': 
            FIELD[ya] = FIELD[ya][:xa]+symb+FIELD[ya][1+xa:]
            applels[k]=[xa,ya]
            symbsLIST[k]=symb
            break

def lose():
    L=0
    G=0
    global x
    global y
    if y>=HEIGHT-1:
        L=1
    if y<0:
        L=1
    if x<0:
        L=1
    if x>WIDTH-1:
        L=1
    return L

with open('dict.txt') as file:
    dictionary = file.readlines()

size_color()

while True:
    word = dictionary[randint(0,len(dictionary)-1)]
    word_X = '_'*(len(word)-1)
    tries = 6
    
    hangman=[['         ','         ','         ','         ','         ','           ', \
              '- - - - - - - -',word_X,'У Вас осталось попыток:'+str(tries)], \
             ['         ','         ','         ','         ','         ','__███__/|\_', \
              '- - - - - - - -',word_X,'У Вас осталось попыток:'+str(tries)], \
             ['         ','        |','        |','        |','        |','__███__/|\_', \
              '- - - - - - - -',word_X,'У Вас осталось попыток:'+str(tries)], \
             ['   +----+','        |','        |','        |','        |','__███__/|\_', \
              '- - - - - - - -',word_X,'У Вас осталось попыток:'+str(tries)], \
             ['   +----+','   |    |','   o    |','  /|\   |','  / \   |','__███__/|\_', \
              '- - - - - - - -',word_X,'У Вас осталось попыток:'+str(tries)], \
             ['   +----+','   |    |','   o    |','  /|\   |','  / \   |','_______/|\_', \
              '- - - - - - - -',word_X,'У Вас осталось попыток:'+str(tries)]]
    
    tries = len(hangman)
    unused_symb = '  qazxswedcvfrtgbnhyujmikolp'
    for i in word:
        unused_symb=unused_symb.replace(i,'')
    symb=''
    unused_symbW ="  " + word
    WIDTH, HEIGHT = 25, 10
    R=1
    ya=''
    xa=''
    x=10
    y=3
    k=2
    G=0
    direction = (1, 0)
    FIELD = [' '*WIDTH+'#']*(HEIGHT)
    snake=[]
    snake.append([x,y,direction[0],direction[1]])
    snake.append([x,y-1,direction[0],direction[1]])
    snake.append([x,y-1,direction[0],direction[1]])
    
    apple(0)
    apple(1)
    apple(2)
    reductHF()
    sleep(1)
    with keyboard.Listener(on_press=process_press) as listener:
        while True:
     
            SCENE()
    
            snakepr()
    
            if lose() or G or tries==0:
                break
            if not('_' in word_X):
                break
            
            
            if R:
                apple(k)
    
            sleep(0.1)
            
            clear()
    
            pass
    clear()
    SCENE()
    if lose() or G or tries==0:
        return_game = input('тЫ ЧеВо НАдЕЛаЛ, исправлять ситуацию будешь? ("+" - да, "-" - нет): ')
    else:
        return_game = input('Это как это! Выграл! Ещё будешь? ("+" - да, "-" - нет): ')
    if return_game == '+':
        continue
    else:
        break
