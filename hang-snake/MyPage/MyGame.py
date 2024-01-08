from tkinter import *

WIDTH = 700
HEIGHT = 700
gamestatus = 0


def start_of_the_game():
    global gamestatus
    gamestatus = 3
    canvas.destroy()


window = Tk()
window.title('Snake + Hangman')
window.geometry(f"{800}x{860}+{300}+{50}")

canvas = Canvas(window, bg="white", height=HEIGHT, width=WIDTH)

buttoncombo = Button(text='ИГРАТЬ',
                           command=start_of_the_game)
canvas.create_window(355, 480, window=buttoncombo, tags="buttoncombo")


canvas.create_line(255, 420, 455, 420, width=3)
canvas.create_line(355, 420, 355, 200, width=3)
canvas.create_line(270, 200, 355, 200, width=3)
canvas.create_line(270, 200, 270, 283, width=1)


canvas.create_oval(258, 283, 282, 307, width=3)
canvas.create_line(270, 307, 270, 357, width=3)
canvas.create_line(270, 327, 289, 357, width=3)
canvas.create_line(270, 327, 261, 357, width=3)
canvas.create_line(270, 357, 289, 387, width=3)
canvas.create_line(270, 357, 261, 387, width=3)




canvas.create_rectangle(255, 420, 275, 400, fill="green")
canvas.create_rectangle(275, 420, 295, 400, fill="green")
canvas.create_rectangle(295, 420, 315, 400, fill="green")
canvas.create_rectangle(295, 420, 315, 400, fill="green")
canvas.create_line(315, 410, 325, 410, width=3, fill="pink")
canvas.create_line(325, 410, 330, 415, width=2, fill="pink")
canvas.create_line(325, 410, 330, 405, width=2, fill="pink")
canvas.create_oval(308, 403, 312, 407, fill='black')
canvas.create_oval(308, 413, 312, 417, fill='black')

canvas.create_rectangle(355, 420, 375, 400, fill="red")

# По нажатию кнопки запускаем соответствующую игру
while gamestatus == 0:
    canvas.pack()
    window.update()