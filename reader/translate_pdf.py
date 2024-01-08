import PyPDF2
from translate import Translator
import tkinter as tk
from tkinter import filedialog
from tkinter import scrolledtext

def extract_text_from_pdf(file_path):
    """
    Функция для извлечения текста из PDF-файла.
    Принимает путь к файлу в качестве входного аргумента.
    Возвращает извлеченный текст.
    """
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)  # Создание объекта PdfReader для чтения PDF-файла
        text = ''
        for page in pdf_reader.pages:  # Итерация по страницам PDF-файла
            text += page.extract_text()  # Извлечение текста со страницы и добавление его к общему тексту
        return text

def translate_text():
    """
    Функция для перевода текста из PDF-файла.
    Запрашивает у пользователя путь к файлу с помощью диалогового окна.
    Извлекает текст из PDF-файла и переводит его на русский язык.
    Выводит переведенный текст в текстовое поле.
    """
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])  # Открытие диалогового окна для выбора файла
    if file_path:
        text = extract_text_from_pdf(file_path)  # Извлечение текста из PDF-файла
        translator = Translator(to_lang='ru')  # Создание объекта Translator для перевода текста на русский язык
        translation = translator.translate(text)  # Перевод текста
        translated_text.delete('1.0', tk.END)  # Очистка текстового поля
        translated_text.insert(tk.END, translation)  # Вставка переведенного текста в текстовое поле

root = tk.Tk()  # Создание главного окна приложения
root.title("PDF Translator")  # Установка заголовка окна

select_pdf_button = tk.Button(root, text="Выбрать PDF", command=translate_text)  # Создание кнопки "Выбрать PDF" с привязкой к функции translate_text
select_pdf_button.pack()  # Размещение кнопки на главном окне

scrollbar = tk.Scrollbar(root)  # Создание полосы прокрутки
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)  # Размещение полосы прокрутки на правой стороне окна и заполнение ею вертикально

translated_text = scrolledtext.ScrolledText(root, yscrollcommand=scrollbar.set)  # Создание текстового поля с возможностью прокрутки
translated_text.pack()  # Размещение текстового поля на главном окне

scrollbar.config(command=translated_text.yview)  # Привязка полосы прокрутки к текстовому полю

root.mainloop()