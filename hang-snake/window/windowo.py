from tkinter import *

WIDTH = 700
HEIGHT = 700
gamestatus = 0


def playcombo():
    global gamestatus
    gamestatus = 3
    canvas.destroy()


window = Tk()
window.title('Snake + Hangman')
window.geometry(f"{700}x{740}+{400}+{100}")  #Создание окна для приложения

canvas = Canvas(window, bg="white", height=HEIGHT, width=WIDTH)

buttoncombo = Button(text='Играть',
                           command=playcombo)
canvas.create_window(350, 620, window=buttoncombo, tags="buttoncombo")
canvas.create_line(280, 350, 380, 350, width=3)
canvas.create_line(330, 350, 330, 200, width=3)
canvas.create_line(330, 200, 400, 200, width=3)
canvas.create_line(400, 200, 400, 250, width=1)
canvas.create_rectangle(390, 250, 410, 270, fill="green")
canvas.create_rectangle(390, 270, 410, 290, fill="green")
# По нажатию кнопки запускаем соответствующую игру
while gamestatus == 0:
    canvas.pack()
    window.update()