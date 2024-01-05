import telebot
import requests
from pdf.printer.Translator import Translator

bot = telebot.TeleBot('6831422514:AAHii6u7ELVhfPh_XE-o7Gc76qhtAnhEhLQ')
translator = Translator()
@bot.message_handler(content_types=['text'])
def get_text_messages(message):

    if message.text == "Привет":
        bot.send_message(message.from_user.id, "Привет, чем я могу тебе помочь?")
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Напиши привет")

    else:
        translator.translate(str(message.text),"ru")
        bot.send_message(message.from_user.id, translator.translate(str(message.text),"ru"))


bot.polling(none_stop=True, interval=0)