import PyPDF2
from translate import Translator
import tkinter as tk
from tkinter import filedialog
from tkinter import scrolledtext

def extract_text_from_pdf(file_path):

    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ''
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text

def translate_text():
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if file_path:
        text = extract_text_from_pdf(file_path)
        translator = Translator(to_lang='ru')
        translation = translator.translate(text)
        translated_text.delete('1.0', tk.END)
        translated_text.insert(tk.END, translation)

root = tk.Tk()
root.title("PDF Translator")

select_pdf_button = tk.Button(root, text="Выбрать PDF", command=translate_text)
select_pdf_button.pack()

scrollbar = tk.Scrollbar(root)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

translated_text = scrolledtext.ScrolledText(root, yscrollcommand=scrollbar.set)
translated_text.pack()

scrollbar.config(command=translated_text.yview)  # Привязка полосы прокрутки к текстовому полю

root.mainloop()