import random
from tkinter import *
from windowout.run import window, gamestatus

WIDTH = 700  # Размеры окна
HEIGHT = 700

words = ['programming', 'python', 'laptop', 'coffee', 'computer', 'informatics',
         'keyboard', 'monitor', 'development']  # Список слов


def create_secret():
    return random.choice(words)  # Выбор случайного слова из списка


SECRET = create_secret()
n = len(SECRET)
guess_field = '_' * n  # Создание слова и поля для ответа
mistakes = 0  # Счет количества ошибок, от которого зависит какое поле выведено на экран


class HangmanGame:
    @staticmethod
    def output():  # Вывод на экран
        global mistakes
        canvas.create_line(250, 400, 350, 400, width=5)
        canvas.create_line(300, 400, 300, 100, width=5)
        canvas.create_line(300, 100, 400, 100, width=5)
        canvas.create_line(400, 100, 400, 200, width=2)
        match mistakes:
            case 1:
                canvas.create_oval(375, 200, 425, 250, width=3)
            case 2:
                canvas.create_line(400, 250, 400, 325, width=3)
            case 3:
                canvas.create_line(400, 260, 375, 300, width=3)
                canvas.create_line(400, 260, 425, 300, width=3)
            case 4:
                canvas.create_line(400, 325, 375, 375, width=3)
            case 5:
                canvas.create_line(400, 325, 425, 375, width=3)  # Рисование виселицы и частей человека
        canvas.delete("guess")
        canvas.create_text(350, 500,
                           text=guess_field,
                           justify=CENTER, font="Verdana 20", tags="guess")  # Вывод поля для ответа

    @staticmethod
    def enterpressed(event):
        HangmanGame.move()

    @staticmethod
    def move():  # Ход
        letter = letter_window.get()
        letter_window.delete(0, END)  # Очистка окна
        global guess_field, mistakes
        if letter in SECRET:  # Если буква правильная, выполняем соответствующую функцию
            guess_field = HangmanGame.correct_answer(letter)  # Изменяем поле для ответа
        else:
            mistakes = mistakes + 1  # Если буква неправильная, добавляем ошибку
        HangmanGame.win_lose()
        window.after(1, HangmanGame.output)

    @staticmethod
    def correct_answer(letter):  # Добавление правильной буквы в поле ответа
        new_guess_field = ''
        for i in range(n):  # Если буква правильная, "открываем" её в поле ответа
            if SECRET[i] == letter:
                new_guess_field = new_guess_field + letter
            else:
                new_guess_field = new_guess_field + guess_field[i]
        return new_guess_field

    @staticmethod
    def win_lose():
        global guess_field
        if SECRET == guess_field:  # Если поле для ответа совпадает с загаданным словом - победа
            canvas.delete("enter_text")
            canvas.delete("letter_window")
            canvas.delete("button")
            canvas.delete("comm")
            canvas.create_text(350, 550,
                               text="You won!",
                               justify=CENTER, font="Verdana 14")
        if mistakes == 5:  # Если 5 ошибок - проигрыш
            canvas.delete("enter_text")
            canvas.delete("letter_window")
            canvas.delete("button")
            canvas.delete("comm")
            canvas.create_text(350, 550,
                               text="You lost!",
                               justify=CENTER, font="Verdana 14")
            canvas.create_text(350, 580,
                               text=f"Answer: {SECRET}",

                               justify=CENTER, font="Verdana 14")
            gameover = Button(text='Выйти из игры',
                              command=HangmanGame.game_exit)
            canvas.create_window(350, 610, window=gameover, tags="gameover")

    @staticmethod
    def game_exit():
        global gamestatus
        gamestatus = 4

    @staticmethod
    def run():
        canvas.pack()
        HangmanGame.output()


canvas = Canvas(window, bg="white", height=HEIGHT, width=WIDTH)
canvas.create_text(350, 550,
                   text="Enter your guess:",
                   justify=CENTER, font="Verdana 14", tags="enter_text")
letter_window = Entry(window)
canvas.create_window(350, 580, window=letter_window, tags="letter_window")
letter_window.focus()
button_widget = Button(text='GUESS',
                       command=HangmanGame.move)
canvas.create_window(350, 620, window=button_widget, tags="button")
canvas.create_text(350, 650,
                   text="(Можно делать ввод по нажатию клавиши Вверх)",
                   justify=CENTER, font="Verdana 8", tags="comm")
window.bind('<Up>', HangmanGame.enterpressed)  # Можно делать ввод по клавише "Вверх"

if gamestatus == 2:
    HangmanGame.run()
while gamestatus == 2:
    window.update()
