from PyPDF2 import PdfReader
import tkinter as tk
from tkinter import ttk
from translate import Translator

translator = Translator(to_lang="ru")

def get():
    extension = ".pdf"
    filename = name.get() + extension
    reader = PdfReader(filename)
    number_of_pages = len(reader.pages)
    page = reader.pages[0]
    text = page.extract_text()
    #translator = Translator(to_lang="ru")
    #translation = translator.translate(text)
    #print(text)
    label.delete(1.0)
    label.insert(1.0, text)
def textout():
    editor.delete("1.0",tk.END)
    editor.insert(tk.END, translator.translate(label.selection_get()))

root = tk.Tk()  # создаем корневой объект - окно
root.title("Original")  # устанавливаем заголовок окна
root.geometry("300x250")  # устанавливаем размеры окна

root1 = tk.Tk()  # создаем корневой объект - окно
root1.title("Translate")  # устанавливаем заголовок окна
root1.geometry("300x250+300+250")  # устанавливаем размеры окна


name = tk.StringVar()

entry = ttk.Entry(textvariable=name)
entry.pack(anchor=tk.NW, padx=8, pady=8)

open_button = ttk.Button(text="Click", command=get)
open_button.pack(anchor=tk.NW, padx=6, pady=6)

tmp_button = ttk.Button(text="Selection", command=lambda: textout())
tmp_button.pack(anchor=tk.NW, padx=6, pady=6)

label = tk.Text(root)
label.pack(anchor=tk.NW, padx=6, pady=6)

editor = tk.Text(root1)
editor.pack()

root.mainloop()
root1.mainloop()
