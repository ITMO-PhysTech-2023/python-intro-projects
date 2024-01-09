import telebot
from pdf.printer.Translator import Translator

bot = telebot.TeleBot('6831422514:AAHii6u7ELVhfPh_XE-o7Gc76qhtAnhEhLQ')
translator = Translator()
name=''
@bot.message_handler(content_types=['text'])
def get_text_messages(message):

    if message.text == "/start":
        bot.send_message(message.from_user.id, "команда /help поможет начать")
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Напиши привет")
    elif (message.text == "привет") or (message.text == "Привет"):
        bot.send_message(message.from_user.id, "Привет. Давай познакомимся. напиши свое имя")
        bot.register_next_step_handler(message,get_name)
    else:
        bot.send_message(message.from_user.id, translator.translate(str(message.text), "ru"))
def get_name(message):
        global name
        name = str(message.text)
        bot.send_message(message.from_user.id, "Можешь перевести любой текст на русский язык. Для этого напиши его в сообщении")
bot.polling(none_stop=True, interval=0)