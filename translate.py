from PyPDF2 import PdfReader
import tkinter as tk
from tkinter import ttk
from tkinter import *
from googletrans import Translator,constants
from pprint import pprint

def get():
    extension = ".pdf"
    filename = name.get() + extension
    reader = PdfReader(filename)
    number_of_pages = len(reader.pages)
    text=''
    for page in reader.pages:
        text += page.extract_text()
    label.delete(1.0,END)
    label.insert(1.0, text)

root = tk.Tk()  # создаем корневой объект - окно
root.title("Tkinter")  # устанавливаем заголовок окна
root.geometry("700x500")  # устанавливаем размеры окна

name = tk.StringVar()

entry = ttk.Entry(textvariable=name)
entry.pack(anchor=tk.NW, padx=8, pady=8)

open_button = ttk.Button(text="Click", command=get)
open_button.pack(anchor=tk.NW, padx=6, pady=6)

translator = Translator()
def translate_selected_text():
    # Получаем выделенный текст
    selected_text = label.get(tk.SEL_FIRST, tk.SEL_LAST)
    # Переводим текст с английского на русский
    translated_text = translator.translate(selected_text, dest='ru')
    label_2.delete(0.1, END)
    label_2.insert(0.1 ,f'{translated_text.text}')

tmp_button = ttk.Button(text="Translate", command=translate_selected_text)
tmp_button.pack(anchor=tk.NW, padx=6, pady=6)
label = tk.Text(root)
label.pack(anchor=tk.NW, padx=6, pady=6)


root_2 = tk.Tk()
root_2.title("Translated_text")
root_2.geometry("700x500")
name_2 = tk.StringVar()

entry_2 = ttk.Entry(textvariable=name_2)
entry_2.pack(anchor=tk.NW, padx=8, pady=8)

label_2 = tk.Text(root_2)
label_2.pack(anchor=tk.NW, padx=6, pady=6)


root.mainloop()
root_2.mainloop()