from PyPDF2 import PdfReader
from tkinter import *


def output(event):
    s = ent.get()
    reader = PdfReader(s)
    page = reader.pages[0]
    text = page.extract_text()
    with open(f'{s}.txt', 'w', encoding='utf-8') as f:
        f.write(text)
    tex.delete(1.0, END)
    tex.insert(END, text)
    return


root = Tk()
root.title('PDF Reader')
root.minsize(width=580, height=480)
open_button = Button(root, text='Открыть')
open_button.grid(row=2, column=0)
open_button.bind("<Button-1>", output)

ent = Entry(root, width=20)
ent.grid(row=0, column=0)

tex = Text(root, width=80, height=30, font="Arial.14", wrap=WORD)
tex.grid(row=1, column=0)

translate_button = Button(
    root,
    text='Translate',
    command=lambda: print(translate_button.selection_get())
)
translate_button.grid(row=3, column=0)
root.mainloop()
