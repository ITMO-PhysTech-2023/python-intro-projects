from PyPDF2 import PdfReader
from tkinter import *
from googletrans import Translator


def output(event):
    name = ent.get()
    reader = PdfReader(name)
    for page in reader.pages:
        text = page.extract_text()
        translate_text = translator.translate(text, src='en', dest='ru').text
        with open(f'{name[:-4]}.txt', 'a', encoding='utf-8') as f:
            f.write(translate_text)

        tex.insert(END, translate_text)

    return


translator = Translator()
root = Tk()
root.title('PDF Reader')
root.minsize(width=640, height=580)
open_button = Button(root, text='Открыть и перевести')
open_button.grid(row=2, column=0)
open_button.bind("<Button-1>", output)

ent = Entry(root, width=30)
ent.grid(row=0, column=0)

tex = Text(root, width=80, height=30, font="Arial.14", wrap=WORD)
tex.grid(row=1, column=0)

root.mainloop()