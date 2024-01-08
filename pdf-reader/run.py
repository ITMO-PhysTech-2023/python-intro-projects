from PyPDF2 import PdfReader
from googletrans import Translator
from tkinter import *


def read_the_file():
    text = ''
    try:
        file_name = pdf_file_name_field.get()
        pdf = PdfReader(file_name).pages
        for number_page in range(len(pdf)):
            text += pdf[number_page].extract_text()
        field_for_text.delete("1.0", END)
        field_for_text.insert(END, text)
    except FileNotFoundError:
        field_translate_text.insert(END, "Файла в папке программы не существует или отсутствует .pdf в названии")


def translate_text_to_en():
    field_translate_text.delete("1.0", END)
    selected_text = field_for_text.selection_get()
    if len(selected_text) <= 5000:
        translated = translator.translate(selected_text, dest='en', src='ru')
        field_translate_text.insert(END, translated.text)
    else:
        field_translate_text.insert(END, "Не более 5000 символов!")


def translate_text_to_ru():
    field_translate_text.delete("1.0", END)
    selected_text = field_for_text.selection_get()
    if len(selected_text) <= 5000:
        translated = translator.translate(selected_text, dest='ru', src='en')
        field_translate_text.insert(END, translated.text)
    else:
        field_translate_text.insert(END, "Не более 5000 символов!")


def delete_text():
    field_for_text.delete("1.0", END)


translator = Translator()

text_window = Tk()
text_window.title = "PDF Read and Translate"
text_window.geometry("1280x720")

pdf_file_name_field = Entry(text_window, width=40)
pdf_file_name_field.pack(side=TOP)

field_for_text = Text(height=20)
field_for_text.pack(anchor=N, fill=BOTH, pady=5)
field_for_text.insert(END, 'Чтобы открыть файл, необходимо набрать его \
название и формат в узкой строке сверху (пример: bebra.pdf)\nЧтобы перевести \
выделенный текст с английского на русский или наоборот, нажмите соответствующие \
кнопки\nКнопка "Очистить" для очистки поля')

field_translate_text = Text(height=20)
field_translate_text.pack(anchor=N, fill=BOTH)

button_clear = Button(text='Очистить', command=delete_text)
button_clear.pack(side=BOTTOM)

button_translate_to_en = Button(text='Перевести на английский(не более 5000 символов)', command=translate_text_to_en)
button_translate_to_en.pack(side=BOTTOM)

button_translate_to_ru = Button(text='Перевести на русский(не более 5000 символов)', command=translate_text_to_ru)
button_translate_to_ru.pack(side=BOTTOM)

button_read = Button(text='Прочитать файл', command=read_the_file)
button_read.pack(side=BOTTOM)

text_window.mainloop()
