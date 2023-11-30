
import remi.gui as gui
from remi import start, App
from threading import Timer
from Reader import Reader
from pynput import mouse, keyboard

import pyautogui as pya
import pyperclip  # handy cross-platform clipboard text handler
import time
from api_requests import translate, paraphraze, summarize



clipboard = ''

class MyApp(App):

    def copy_clipboard(self, *args):

        pyperclip.copy("") # <- This prevents last copy replacing current copy of null.
        pya.hotkey('ctrl', 'c')
        #time.sleep(.01)  # ctrl-c is usually very fast but your program may execute faster
        self.clipboard = pyperclip.paste()
        return pyperclip.paste()

    
    def print_translate(self, *args):
        self.full_text = self.clipboard
        #self.output.set_text(self.clipboard)
        self.output.set_text(translate(self.clipboard, 'en', 'ru'))

    def print_summarize(self, *args):
        self.full_text = self.clipboard
        #self.output.set_text(self.clipboard)
        self.output.set_text(summarize(self.clipboard))

    def print_paraphraze(self, *args):
        self.full_text = self.clipboard
        #self.output.set_text(self.clipboard)
        self.output.set_text(paraphraze(self.clipboard))

    def update_position(self, *args):
        if self.button_flag == 'True':
            self.button_flag = False
            self.bt_paraphraze.style['display']='none'
        else:
            self.bt_paraphraze.style['display']='block'
            self.button_flag = True #НЕ робит!!!!!!!!!

    def button_append(self, *args):
        self.main_container.append(self.bt)

    def __init__(self, *args):
        super(MyApp, self).__init__(*args)


    def on_scroll(self, x, y, dx, dy):
        pass
    
    def main(self):
        # the margin 0px auto centers the main container
        self.button_flag = True

        pdf_text = 'No PDF selected'
        self.full_text = ''
        verticalContainer = gui.Container(width=1040, margin='0px auto', style={'display': 'block', 'overflow': 'hidden'})

        self.horizontalContainer = gui.Container(width='100%', layout_orientation=gui.Container.LAYOUT_HORIZONTAL, margin='0px', style={'display': 'block', 'overflow': 'auto'})
        
        self.subContainerLeft = gui.Container(width=500, style={'display': 'block', 'overflow': 'auto', 'text-align': 'center'})

        # the arguments are	width - height - layoutOrientationOrizontal
        subContainerRight = gui.Container(style={'width': '500px', 'display': 'block', 'overflow': 'auto', 'text-align': 'center'})

        self.lbl = gui.Label(pdf_text, width=200, height=30, margin='10px')

        self.bt = gui.Button('Press me!', width=200, height=30, margin='10px')
        # setting the listener for the onclick event of the button
        self.bt.onclick.do(self.on_button_pressed)

        self.txt = gui.TextInput(width=450, height=500, margin='20px')
        self.txt.set_text('PDF text will be displayed here. Чтобы прочитать пдф файл, надо нажать на синюю кнопку ниже и выбрать файлик. Чтобы выбрать текст для обработки, нужно выделить его и отпустить мышку внутри этого текстового окна. Далее нажимаем одну из кнопок сверху и выводится обработанный текст.')
        self.main_container = gui.VBox(width = 1000, height = 100, style = {'display': 'block', 'overflow': 'auto'})
        #self.main_container.append(self.txt)
        self.bt = gui.Button("paraphraze", style={'margin': '3px', 'background-color': 'orange'})
        #self.txt.oncontextmenu.do(self.button_append)
        self.txt.onmouseup.do(self.copy_clipboard)


        self.btFileDiag = gui.Button('Select PDF file', width=200, height=30, margin='10px')
        self.btFileDiag.onclick.do(self.open_fileselection_dialog)

        self.btUploadFile = gui.FileUploader('./', width=200, height=30, margin='10px')
        self.btUploadFile.onsuccess.do(self.fileupload_on_success)
        self.btUploadFile.onfailed.do(self.fileupload_on_failed)


        self.bt_translate = gui.Button("translate", style={'margin': '3px'})
        
        self.bt_summarize = gui.Button("summarize", style={'margin': '3px'})
        
        self.bt_paraphraze = gui.Button("paraphraze", style={'margin': '3px'})

        self.main_container.append(self.bt_translate)
        self.main_container.append(self.bt_paraphraze)
        self.main_container.append(self.bt_summarize)

        #self.subContainerLeft.append([])


        self.bt_translate.onclick.do(self.print_translate)
        self.bt_paraphraze.onclick.do(self.print_paraphraze)
        self.bt_summarize.onclick.do(self.print_summarize)


        self.output = gui.TextInput(width=450, height=500, margin='20px')
        self.output.set_text('Processed text will be displayed here.')


        self.link = gui.Link("http://localhost:8081", "A link to here", width=200, height=30, margin='10px')

        self.dropDown = gui.DropDown.new_from_list(('DropDownItem 0', 'DropDownItem 1'),
                                                   width=200, height=20, margin='10px')
        self.dropDown.onchange.do(self.drop_down_changed)
        self.dropDown.select_by_value('DropDownItem 0')

        self.slider = gui.Slider(10, 0, 100, 5, width=200, height=20, margin='10px')
        self.slider.onchange.do(self.slider_changed)

        self.colorPicker = gui.ColorPicker('#ffbb00', width=200, height=20, margin='10px')
        self.colorPicker.onchange.do(self.color_picker_changed)

        self.date = gui.Date('2015-04-13', width=200, height=20, margin='10px')
        self.date.onchange.do(self.date_changed)


        # appending a widget to another, the first argument is a string key

        add_container = gui.Container(style={'width': '500px', 'display': 'block', 'overflow': 'auto', 'text-align': 'center'})

        add_container.append([self.output])

        subContainerRight.append([self.txt])
        
        down_container = gui.Container(style={'width': '1000px', 'display': 'block', 'overflow': 'auto', 'text-align': 'center'})

        down_container.append([self.btFileDiag])

        # use a defined key as we replace this widget later
        fdownloader = gui.FileDownloader('download test', '../remi/res/logo.png', width=200, height=30, margin='10px')
        #subContainerRight.append(fdownloader, key='file_downloader')
        #subContainerRight.append([self.btUploadFile])
        self.subContainerRight = subContainerRight

        #subContainerLeft.append([self.img, self.table, self.listView, self.link, self.video])

        self.horizontalContainer.append([ self.main_container, subContainerRight, add_container])

        menu = gui.Menu(width='100%', height='30px')
        m1 = gui.MenuItem('File', width=100, height=30)
        m2 = gui.MenuItem('View', width=100, height=30)
        m2.onclick.do(self.menu_view_clicked)
        m11 = gui.MenuItem('Save', width=100, height=30)
        m12 = gui.MenuItem('Open', width=100, height=30)
        m12.onclick.do(self.menu_open_clicked)
        m111 = gui.MenuItem('Save', width=100, height=30)
        m111.onclick.do(self.menu_save_clicked)
        m112 = gui.MenuItem('Save as', width=100, height=30)
        m112.onclick.do(self.menu_saveas_clicked)
        m3 = gui.MenuItem('Dialog', width=100, height=30)
        m3.onclick.do(self.menu_dialog_clicked)

        menu.append([m1, m2, m3])
        m1.append([m11, m12])
        m11.append([m111, m112])

        menubar = gui.MenuBar(width='100%', height='30px')
        menubar.append(menu)

        verticalContainer.append([self.horizontalContainer, self.lbl, down_container])

        #this flag will be used to stop the display_counter Timer
        self.stop_flag = False 

        # returning the root widget               
        return verticalContainer

    

    def menu_dialog_clicked(self, widget):
        self.dialog = gui.GenericDialog(title='Dialog Box', message='Click Ok to transfer content to main page', width='500px')
        self.dtextinput = gui.TextInput(width=200, height=30)
        self.dtextinput.set_value('Initial Text')
        self.dialog.add_field_with_label('dtextinput', 'Text Input', self.dtextinput)

        self.dcheck = gui.CheckBox(False, width=200, height=30)
        self.dialog.add_field_with_label('dcheck', 'Label Checkbox', self.dcheck)
        values = ('Danny Young', 'Christine Holand', 'Lars Gordon', 'Roberto Robitaille')
        self.dlistView = gui.ListView.new_from_list(values, width=200, height=120)
        self.dialog.add_field_with_label('dlistView', 'Listview', self.dlistView)

        self.ddropdown = gui.DropDown.new_from_list(('DropDownItem 0', 'DropDownItem 1'),
                                                    width=200, height=20)
        self.dialog.add_field_with_label('ddropdown', 'Dropdown', self.ddropdown)

        self.dspinbox = gui.SpinBox(min=0, max=5000, width=200, height=20)
        self.dspinbox.set_value(50)
        self.dialog.add_field_with_label('dspinbox', 'Spinbox', self.dspinbox)

        self.dslider = gui.Slider(10, 0, 100, 5, width=200, height=20)

        self.dialog.add_field_with_label('dslider', 'Slider', self.dslider)


        self.dialog.confirm_dialog.do(self.dialog_confirm)
        self.dialog.show(self)

    def dialog_confirm(self, widget):
        result = self.dialog.get_field('dtextinput').get_value()
        self.txt.set_value(result)

        result = self.dialog.get_field('dcheck').get_value()
        self.check.set_value(result)

        result = self.dialog.get_field('ddropdown').get_value()
        self.dropDown.select_by_value(result)

        result = self.dialog.get_field('dspinbox').get_value()
        self.spin.set_value(result)

        result = self.dialog.get_field('dslider').get_value()
        self.slider.set_value(result)

        result = self.dialog.get_field('dcolor').get_value()
        self.colorPicker.set_value(result)

        result = self.dialog.get_field('ddate').get_value()
        self.date.set_value(result)

        result = self.dialog.get_field('dlistView').get_value()
        self.listView.select_by_value(result)



    def on_button_pressed(self, widget):
        self.lbl.set_text('Button pressed! ')
        self.bt.set_text('Hi!')

    def on_text_area_change(self, widget, newValue):
        self.lbl.set_text('Text Area value changed!')

    def on_spin_change(self, widget, newValue):
        self.lbl.set_text('SpinBox changed, new value: ' + str(newValue))

    def on_check_change(self, widget, newValue):
        self.lbl.set_text('CheckBox changed, new value: ' + str(newValue))

    def open_input_dialog(self, widget):
        self.inputDialog = gui.InputDialog('Input Dialog', 'Your name?',
                                           initial_value='type here', 
                                           width=500)
        self.inputDialog.confirm_value.do(
            self.on_input_dialog_confirm)

        # here is returned the Input Dialog widget, and it will be shown
        self.inputDialog.show(self)

    def on_input_dialog_confirm(self, widget, value):
        self.lbl.set_text('Hello ' + value)

    def open_fileselection_dialog(self, widget):
        self.fileselectionDialog = gui.FileSelectionDialog('File Selection Dialog', 'Select files and folders', False,
                                                           '.')
        self.fileselectionDialog.confirm_value.do(
            self.on_fileselection_dialog_confirm)

        # here is returned the Input Dialog widget, and it will be shown
        self.fileselectionDialog.show(self)

    def on_fileselection_dialog_confirm(self, widget, filelist):
        # a list() of filenames and folders is returned
        self.lbl.set_text('Current PDF: %s' % ','.join(filelist))
        if len(filelist):
            f = filelist[0]
            # replace the last download link
            fdownloader = gui.FileDownloader("download selected", f, width=200, height=30)
            self.subContainerRight.append(fdownloader, key='file_downloader')
            self.full_text = Reader(filelist[0]).return_pdf_text()
            self.txt.set_text(self.full_text)

            #self.lbl = gui.Label('current PDF: ' + str(f), width=200, height=30, margin='10px')

    def list_view_on_selected(self, widget, selected_item_key):
        """ The selection event of the listView, returns a key of the clicked event.
            You can retrieve the item rapidly
        """
        self.lbl.set_text('List selection: ' + self.listView.children[selected_item_key].get_text())

    def drop_down_changed(self, widget, value):
        self.lbl.set_text('New Combo value: ' + value)

    def slider_changed(self, widget, value):
        self.lbl.set_text('New slider value: ' + str(value))

    def color_picker_changed(self, widget, value):
        self.lbl.set_text('New color value: ' + value)

    def date_changed(self, widget, value):
        self.lbl.set_text('New date value: ' + value)

    def menu_save_clicked(self, widget):
        self.lbl.set_text('Menu clicked: Save')

    def menu_saveas_clicked(self, widget):
        self.lbl.set_text('Menu clicked: Save As')

    def menu_open_clicked(self, widget):
        self.lbl.set_text('Menu clicked: Open')

    def menu_view_clicked(self, widget):
        #pya.doubleClick(pya.position())
        pass#self.lbl.set_text(copy_clipboard())

    def fileupload_on_success(self, widget, filename):
        self.lbl.set_text('File upload success: ' + filename)

    def fileupload_on_failed(self, widget, filename):
        self.lbl.set_text('File upload failed: ' + filename)

    def on_close(self):

        self.stop_flag = True
        super(MyApp, self).on_close()


if __name__ == "__main__":
    # starts the webserver
    # optional parameters
    # start(MyApp,address='127.0.0.1', port=8081, multiple_instance=False,enable_file_cache=True, update_interval=0.1, start_browser=True)
    start(MyApp, debug=True, address='0.0.0.0', port=8081, start_browser=True, multiple_instance=True)
