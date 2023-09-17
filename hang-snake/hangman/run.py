from common.util import clear_terminal
from random import shuffle
ALP = "абвгдеёжзийклмнопрстуфхццчшщъыьэюя"
FILENAME = "words.txt"
want = True
y = 0
n = 0
START_FIELD = r'''





'''

SEC_FIELD = r'''





_______/|\_'''

TH_FIELD = r'''
        +
        |
        |
        |
        |
_______/|\_'''

FOUR_FIELD = r'''
   +----+
        |
        |
        |
        |
_______/|\_'''

FIF_FIELD = r'''
   +----+
   |    |
   o    |
        |
        |
_______/|\_'''

SIX_FIELD = r'''
   +----+
   |    |
   o    |
  /|\   |
        |
_______/|\_'''

FINAL_FIELD = r'''
   +----+
   |    |
   o    |
  /|\   |
  / \   |
_______/|\_'''

words = []
file = open(FILENAME, encoding="utf-8")
for line in file:
    words.append(line.strip())
file.close()
shuffle(words)

while want:
    if len(words) == 0:
        print("В игре больше нет слов")
        want = False
    else:
        word = words.pop()
        curword = "_" * (len(word))
        print(f"Загаданно слово состоит из {(len(word))} букв.")
        tries = 0

        used = ""

        while not(word == curword or tries > 5):
            if tries == 0:
                FIELD = START_FIELD
            elif tries == 1:
                FIELD = SEC_FIELD
            elif tries == 2:
                FIELD = TH_FIELD
            elif tries == 3:
                FIELD = FOUR_FIELD
            elif tries == 4:
                FIELD = FIF_FIELD
            elif tries == 5:
                FIELD = SIX_FIELD

            print()
            print(FIELD)
            print()
            print(f"Слово: {curword}")
            print(f"Количество ошибок: {tries} из 6")
            if len(used) == 0:
                print("Вы еще не назвали ни одной буквы")
            else:
                print("Названные буквы: ", end='')
                print(*used)
            guess = input("Введите букву: ").lower()
            while guess not in ALP and len(guess) != 1:
                guess = input("Введите одну букву из русского алфавита: ").lower()
            lett = False
            for i in range(len(word)):
                if guess == word[i]:
                    curword = curword[0:i] + guess + curword[i+1:]
                    lett = True
            if not lett:
                tries += 1
            if guess not in used:
                used += guess
        print()
        print(f"Слово: {curword}")
        print("Количество ошибок: ", tries, " из 6")
        print("Названные буквы: ", end='')
        print(*used)

        print()
        if word == curword:
            print("Вы отгадали слово!")
            y += 1
        else:
            print("Вы не смогли отгадать слово")
            print(FINAL_FIELD)
            n += 1
        print(f"Загаданное слово: \"{word}\".")

        again = input("Новое слово? (Д/Н) ").lower()
        while not(again == "д" or again == "н"):
            print("Пожалуйста, введите \"Д\", если вы хотите продолжить или \"Н\" для завершения игры.")
        if again == "н":
            want = False

print()
print(f"Вы отгадали {y} слов из {y+n}.")
print("До свидания!")
input("Нажмите ENTER для выхода из игры.")