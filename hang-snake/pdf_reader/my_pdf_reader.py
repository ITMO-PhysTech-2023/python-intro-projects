import tkinter as tk
from tkinter import scrolledtext
import os
from googletrans import Translator
import fitz


def read_and_display_pdf(file_path):
    try:
        pdf_document = fitz.open(file_path)
        pdf_text = ""
        for page in pdf_document:
            pdf_text += page.get_text()
        pdf_document.close()
        return pdf_text
    except FileNotFoundError:
        return f"Файл '{file_path}' не найден."
    except Exception as e:
        return f"Произошла ошибка при чтении файла: {e}"


def translate_selected_text():
    selected_text = text_area.get("sel.first", "sel.last")
    translated_text = translate_text(selected_text)
    translated_text_area.delete(1.0, tk.END)
    translated_text_area.insert(tk.INSERT, translated_text)


def display_text_in_window(text):
    root = tk.Tk()
    root.title("Отображение текста из файла")
    global text_area
    text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=20)
    text_area.insert(tk.INSERT, text)
    text_area.pack(expand=True, fill="both")
    translate_button = tk.Button(root, text="Перевести выделенный текст", command=translate_selected_text)
    translate_button.pack()
    global translated_text_area
    translated_text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=5)
    translated_text_area.pack(expand=True, fill="both")
    root.mainloop()


def translate_text(text, target_language='en'):
    translator = Translator()
    translated = translator.translate(text, dest=target_language)
    return translated.text


file_name = input('Введите название файла с расширением .pdf (Пример: my_file.pdf): ')
file_path = os.path.abspath(file_name)
file_content = read_and_display_pdf(file_path)
display_text_in_window(file_content)
