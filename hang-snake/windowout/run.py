from tkinter import *

WIDTH = 700
HEIGHT = 700
gamestatus = 0


def playsnake():
    global gamestatus
    gamestatus = 1
    canvas.destroy()


def playhangman():
    global gamestatus
    gamestatus = 2
    canvas.destroy()


def playcombo():
    pass


window = Tk()
window.title('Snake + Hangman')
window.geometry(f"{700}x{740}+{400}+{100}")  #Создание окна для приложения

canvas = Canvas(window, bg="white", height=HEIGHT, width=WIDTH)
canvas.create_line(233, 0, 233, 710)
canvas.create_rectangle(0, 0, 233, 710, fill="black")
canvas.create_rectangle(71, 271, 100, 300, fill="green")
canvas.create_rectangle(71, 301, 100, 330, fill="green")
canvas.create_rectangle(101, 301, 130, 330, fill="green")
canvas.create_rectangle(131, 301, 160, 330, fill="green")
canvas.create_rectangle(71, 211, 100, 240, fill="red")
canvas.create_line(466, 0, 466, 710)
canvas.create_line(300, 350, 350, 350, width=3)
canvas.create_line(325, 350, 325, 200, width=3)
canvas.create_line(325, 200, 375, 200, width=3)
canvas.create_line(375, 200, 375, 250, width=1)  #Немножко UI
buttonsnake = Button(text='Играть в змейку',
                           command=playsnake)
canvas.create_window(116, 620, window=buttonsnake, tags="buttonsnake")
buttonhangman = Button(text='Играть в виселицу',
                           command=playhangman)
canvas.create_window(350, 620, window=buttonhangman, tags="buttonhangman")
buttoncombo = Button(text='Играть в змейку + виселицу',
                           command=playcombo)
canvas.create_window(584, 620, window=buttoncombo, tags="buttoncombo")
canvas.create_text(584, 300,
                   text="В разработке",
                   justify=CENTER, font="Verdana 14", tags="enter_text")
# По нажатию кнопки запускаем соответствующую игру
while gamestatus == 0:
    canvas.pack()
    window.update()
