import fitz  # PyMuPDF
import tkinter as tk
from tkinter import filedialog
from googletrans import Translator

def translate_selected_word():
    selection = text_widget.selection_get()
    translator = Translator()
    translated_text = translator.translate(selection, src='en', dest='ru').text
    translation_label.config(text="Translation: " + translated_text)

def open_pdf_file():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if file_path:
        doc = fitz.open(file_path)
        text = ""
        for page_num in range(doc.page_count):
            page = doc.load_page(page_num)
            text += page.get_text("text")
        text_widget.insert(tk.END, text)


root = tk.Tk()
root.title("PDF Reader and Translator")

text_widget = tk.Text(root)
text_widget.pack()

translate_button = tk.Button(root, text="Translate", command=translate_selected_word, bg="lightblue", fg="black", relief=tk.RAISED)
translate_button.pack(pady=10)

translation_label = tk.Label(root, text="")
translation_label.pack()

open_file_button = tk.Button(root, text="Open PDF File", command=open_pdf_file, bg="lightgreen", fg="black", relief=tk.RAISED)
open_file_button.pack(pady=10)

root.mainloop()
