import telebot
import requests

bot = telebot.TeleBot('6831422514:AAHii6u7ELVhfPh_XE-o7Gc76qhtAnhEhLQ')
r = requests.get("https://sky.pro/media/kak-sozdat-telegram-bota-na-python/")
print(r.headers['content-type'])
@bot.message_handler(content_types=['text'])
def get_text_messages(message):

    if message.text == "Привет":
        bot.send_message(message.from_user.id, "Привет, чем я могу тебе помочь?")
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Напиши привет")

    else:
        r1 = requests.get(message.text)
        bot.send_message(message.from_user.id, str(r1.status_code))


bot.polling(none_stop=True, interval=0)