import remi.gui as gui
from remi import start, App
import PyPDF2
import pyautogui as pya
import pyperclip  # handy cross-platform clipboard text handler
import time
from translate import Translator
import random


def file_select():
    paths = ['./pdf_files/kolobok.pdf', './pdf_files/red_hat.pdf']
    return random.choice(paths)

path = file_select()

def copy_clipboard():
    pya.hotkey('ctrl', 'c')
    time.sleep(1)  # ctrl-c is usually very fast but your program may execute faster
    return pyperclip.paste()


def extract_text_from_pdf(file_path):
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)

        text = ''

        for page_number in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_number]
            page_text = page.extract_text()
            text += page_text
        return text


class untitled(App):
    def __init__(self, *args, **kwargs):
        # DON'T MAKE CHANGES HERE, THIS METHOD GETS OVERWRITTEN WHEN SAVING IN THE EDITOR
        if not 'editing_mode' in kwargs.keys():
            super(untitled, self).__init__(*args, static_file_path={'my_res': './res/'})
    def idle(self):
        # idle function called every update cycle
        pass
    def main(self):
        # returning the root widge
        return untitled.construct_ui(self)

    def on_button_pressed(self, widget):
        translator = Translator(from_lang="ru", to_lang="en")
        text = translator.translate(copy_clipboard())
        if len(text) > 500:
            self.label1.set_text("Выделите текст. Менее 500 символов")
        else:
            self.label1.set_text(text)






    @staticmethod
    def construct_ui(self):
        # DON'T MAKE CHANGES HERE, THIS METHOD GETS OVERWRITTEN WHEN SAVING IN THE EDITOR
        self.container0 = gui.Container()
        self.container0.attr_class = "Container"
        self.container0.attr_editor_newclass = False
        self.container0.css_height = "100%"
        self.container0.css_left = "0px"
        self.container0.css_position = "absolute"
        self.container0.css_top = "0px"
        self.container0.css_width = "100%"
        self.container0.variable_name = "container0"
        self.label0 = gui.Label()
        self.label0.attr_class = "Label"
        self.label0.attr_editor_newclass = False
        self.label0.css_height = "90%"
        self.label0.css_left = "10.0px"
        self.label0.css_position = "absolute"
        self.label0.css_top = "15.0px"
        self.label0.css_width = "40%"
        self.label0.text = "label"
        self.label0.variable_name = "label0"
        self.container0.append(self.label0, 'label0')
        self.label1 = gui.Label()
        self.label1.attr_class = "Label"
        self.label1.attr_editor_newclass = False
        self.label1.css_height = "90 %"
        self.label1.css_left = "45%"
        self.label1.css_position = "absolute"
        self.label1.css_top = "15.0px"
        self.label1.css_width = "40%"
        self.label1.text = ""
        self.label1.variable_name = "label1"
        self.container0.append(self.label1, 'label1')
        self.button0 = gui.Button()
        self.button0.attr_class = "Button"
        self.button0.attr_editor_newclass = False
        self.button0.css_height = "30px"
        self.button0.css_left = "45%"
        self.button0.css_position = "absolute"
        self.button0.css_top = "92%"
        self.button0.css_width = "100px"
        self.button0.text = "Translate"
        self.button0.variable_name = "button0"
        self.container0.append(self.button0, 'button0')

        self.container0 = self.container0
        self.label0.set_text(extract_text_from_pdf(path))
        self.button0.onclick.do(self.on_button_pressed)
        return self.container0




configuration = {'config_project_name': 'untitled', 'config_address': '0.0.0.0', 'config_port': 8081, 'config_multiple_instance': True, 'config_enable_file_cache': True, 'config_start_browser': True, 'config_resourcepath': './res/'}

if __name__ == "__main__":
    start(untitled,address='127.0.0.1', port=8081, multiple_instance=False,enable_file_cache=True, update_interval=0.1, start_browser=True)