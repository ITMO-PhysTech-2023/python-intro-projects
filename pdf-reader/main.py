import json5

from reader.component import ButtonComponent, DropdownComponent, TextComponent
from reader.reader import HookType, Reader
from translate.translator import Translator

with open('config.json5', 'r') as config_file:
    config = json5.load(config_file)

reader = Reader('resources/example.pdf')
reader.hook_store(HookType.ON_SELECT, 'selected_text')
# TODO сделать стиль "прозрачное и с фиксированной позицией
translated_text = TextComponent(reader, None, style={'?': '?'})


def translate():
    translator = Translator(api_dropdown.selected_id)
    text = reader.selected_text
    if text is None:
        translated_text.hide()
    else:
        translated_text.text = translator.translate(text)
        translated_text.show()


api_dropdown = DropdownComponent(reader, config['api'], display=lambda option: option['name'])
translate_button = ButtonComponent(reader, translate)

reader.run()
