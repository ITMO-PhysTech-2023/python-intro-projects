import telebot
from telebot import types
import requests
import json


bot = telebot.TeleBot('6847881555:AAFHK8n9RJBtqFayimaTukklAq-PL4zE_Gs')
API_key = '7bb6deab6a964b450b6d6e4fc9fa168b'

@bot.message_handler(commands=['start'])
def welcome(message):
    marka = types.ReplyKeyboardMarkup()
    button_1 = types.KeyboardButton('Москва')
    button_2 = types.KeyboardButton('Санкт-Петербург')
    marka.row(button_1,button_2)
    bot.send_message(message.chat.id, 'Вы мне название города, я Вам погоду\nМожно использовать как английские названия городов, так и русские\n \n<em><u>Ниже кнопки для жителей Москвы и СПБ</u></em>', parse_mode='html', reply_markup=marka)


@bot.message_handler(content_types=['text'])
def weather(message):
    try:
        city_name = message.text.strip().lower()
        answer = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_key}&units=metric&lang=ru')
        final_ans = json.loads(answer.text)
        bot.send_message(message.chat.id, f'''<b><u>Погода в городе {final_ans["name"]}</u></b>:
{final_ans["weather"][0]["description"].capitalize()}
    
Фактическая температура: {final_ans["main"]["temp"]}°C
Ощущается как: {final_ans["main"]["feels_like"]}°C
Максимальная температура: {final_ans["main"]["temp_max"]}°C
Минимальная температура: {final_ans["main"]["temp_min"]}°C
    
Скорость ветра: {final_ans["wind"]["speed"]}м/с
''',parse_mode='html')
    except KeyError:
        bot.send_message(message.chat.id, "Такого города не существует!")

bot.polling(none_stop=True)
