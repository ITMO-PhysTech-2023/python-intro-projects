from pynput import keyboard
import random
from common.util import clear_terminal
import time
import threading
import hangman.states
from playsound import playsound

WIDTH, HEIGHT = 25, 25
APPLES_COUNT = 5

LETTER_A = ord('a')
LETTER_Z = ord('z')

SPACE = '      '
def random_position():
    return random.randint(0, HEIGHT - 1), random.randint(0, WIDTH - 1)


IS_PLAYING_SOUND = False
def nomnom():
    IS_PLAYING_SOUND = True
    playsound('pudge.mp3')
    IS_PLAYING_SOUND = False

def create_secret():
    global SECRET
    global OUTPUTSTR
    global wrdlen
    global not_guessed
    r = random.randint(0, 49)
    SECRET = open('secrets').readlines()[r]
    wrdlen = len(SECRET) - 1
    not_guessed = wrdlen
    OUTPUTSTR = '_'*wrdlen

def make_guess(letter):
    global SECRET
    global OUTPUTSTR
    global wrdlen
    global GUESSED
    has_changes = False
    if not (letter in OUTPUTSTR):
        if not (letter in SECRET):
            return has_changes
        GUESSED+=letter
        i = SECRET.index(letter)
        for i in range(wrdlen):
            if SECRET[i] == letter:
                has_changes = True
                OUTPUTSTR = OUTPUTSTR[:i] + letter + OUTPUTSTR[i+1:]
    return has_changes


def form_hangman_field(rem_tries, outputwrd_field):
    HNGMN_FIELD = hangman.states.STATES[7-rem_tries]
    HNGMN_FIELD += '\n' + outputwrd_field
    return HNGMN_FIELD

def process_press(key):
    # обработчик нажатия на клавиши (можно сделать и поаккуратнее)
    global direction
    if key == keyboard.Key.left and direction != (-1, 0) and direction != (1,0):
        direction = (-1, 0)
    elif key == keyboard.Key.up and direction != (0, -1) and direction != (0,1):
        direction = (0, -1)
    elif key == keyboard.Key.right and direction != (1, 0) and direction != (-1,0):
        direction = (1, 0)
    elif key == keyboard.Key.down and direction != (0, 1) and direction != (0,-1):
        direction = (0, 1)


def generete_apples(body):
    global apples
    global letters
    global APPLES_COUNT
    global GUESSED
    global SECRET
    letters.clear()
    apples.clear()
    while True:
        char = SECRET[random.randint(0, len(SECRET) - 2)]
        if not (char in GUESSED):
            letters.append(char)
            break
    while True:
        rand_pos = random_position()
        if not (rand_pos in body[1:]):
            apples.append(rand_pos)
            break
    for i in range(1, APPLES_COUNT):
        while True:
            rand_pos, rand_letter = random_position(), chr(random.randint(LETTER_A, LETTER_Z))
            if not ((rand_pos in apples) and (rand_pos in body[1:]) and (rand_letter in GUESSED)):
                apples.append(rand_pos)
                letters.append(rand_letter)
                break

N = 1
direction = (1, 0)
init_pos = (WIDTH // 2, HEIGHT // 2)
next_pos = (init_pos[0]+direction[0], init_pos[1]+direction[1])
body = [next_pos, init_pos]

apples = list()
letters = list()

SECRET = str()
OUTPUTSTR = str()
GUESSED = str()
points = 0
rem_tries = 7

can_process_key = True
def thr_f():
    global apples
    global letters
    global N            # body len
    global output
    global default_output
    global can_process_key
    global rem_tries
    global points
    global GUESSED
    snd_thr = threading.Thread(target=nomnom)
    while True:
        game_over = False
        guessed = False
        if body[1] in apples:
            if not IS_PLAYING_SOUND:
                snd_thr.start()
                snd_thr = threading.Thread(target=nomnom)
            index = apples.index(body[1])
            delta = 0
            if make_guess(letters[index]):
                delta = 1
                guessed = True
            else:
                delta = 3
                rem_tries -= 1
            for i in range(delta):
                body.append(body[N])
            apples.pop(index)
            letters.pop(index)
            N += delta
        for i in range(N, 0, -1):
            body[i] = body[i - 1]
        if body[1][0] < 0 or body[1][0] >= WIDTH \
                or body[1][1] < 0 or body[1][1] >= HEIGHT:
            game_over = True
        if not rem_tries:
            game_over = True
        for i in range(2, N + 1):
            if body[i][0] == body[1][0] and body[i][1] == body[1][1]:
                game_over = True
                break
        if game_over:
            clear_terminal()
            print('you lost!')
            playsound('sound3.mp3')
            print('you scored ' + str(points))
            break

        body[0] = (body[1][0] + direction[0], body[1][1] + direction[1])

        if OUTPUTSTR == SECRET[:-1]:
            points += 1
            for i in range(len(SECRET) - 1):
                body.pop(N)
                N -= 1
            clear_terminal()
            print('You guessed the word!\nYour current score: ' + str(points))
            playsound('pudgers.mp3')
            clear_terminal()
            create_secret()
            generete_apples(body)
            GUESSED = ''
            continue

        if guessed:
            generete_apples(body)

        hangman_field_lines = list()          # stores lines of hangman field lines
        temp = form_hangman_field(rem_tries, OUTPUTSTR)
        while '\n' in temp:
            hangman_field_lines.append(temp[:temp.index('\n')])
            temp = temp[temp.index('\n')+1:]
        hangman_field_lines.append(temp)
        hangman_field_lines.reverse()
        for i in range(1, N + 1):
            output = output[:body[i][1] * (WIDTH + 2) + body[i][0] + 1] + \
                     '#' + output[body[i][1] * (WIDTH + 2) + body[i][0] + 2:]
        for i in range(len(letters)):
            output = output[:apples[i][1] * (WIDTH + 2) + apples[i][0] + 1] + \
                 letters[i] + output[apples[i][1] * (WIDTH + 2) + apples[i][0] + 2:]

        print('#' * (WIDTH + 2))
        hangman_field_lines_count = len(hangman_field_lines)
        for i in range(HEIGHT):
            output_line = output[i*(WIDTH+2):(i+1)*(WIDTH+2)]
            if i < hangman_field_lines_count:
                output_line += SPACE[:-1] + hangman_field_lines.pop()
            print(output_line)
        print('#'*(WIDTH+2))
        output = default_output
        time.sleep(0.3)
        clear_terminal()


default_output = ('#' + ' '*WIDTH + '#')*HEIGHT + '#'*(WIDTH+2)
output = default_output
create_secret()
generete_apples(body)
# можно приделать конфиг-файл с параметрами


print('WELCOME TO HANGSNAKE SIMULATOR 2023!!!')
playsound('sound1.mp3')
print('DO YOU WANT TO PLAY???')
while(input('Y/N')[0] != 'y'):
    pass
print('SURE MY FRIEND')
playsound('sound2.mp3')
with keyboard.Listener(on_press=process_press) as listener:
    thread = threading.Thread(target=thr_f)
    thread.start()
    thread.join()