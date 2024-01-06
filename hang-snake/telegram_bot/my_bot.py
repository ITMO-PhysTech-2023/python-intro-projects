from datetime import datetime
import time, threading
import requests, os
import telebot
from pycbrf import ExchangeRates
from googletrans import Translator
import schedule
from dotenv import load_dotenv


load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
API_KEY = os.getenv('API_KEY')

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2)
    itembtn1 = telebot.types.KeyboardButton('Курс валют')
    itembtn2 = telebot.types.KeyboardButton('Добавить задачу')
    itembtn3 = telebot.types.KeyboardButton('Узнать погоду')
    itembtn4 = telebot.types.KeyboardButton('Переводчик')
    markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
    bot.send_message(chat_id=message.chat.id, text='Выберите функцию:', reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == 'Курс валют')
def currency_start(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2)
    itembtn1 = telebot.types.KeyboardButton('Доллар(США)')
    itembtn2 = telebot.types.KeyboardButton('Евро')
    itembtn3 = telebot.types.KeyboardButton('Тенге(Казахстан)')
    itembtn4 = telebot.types.KeyboardButton('Иена(Япония)')
    itembtn5 = telebot.types.KeyboardButton('Фунт Ст.(Великобритания)')
    itembtn_back = telebot.types.KeyboardButton('Назад')
    markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5, itembtn_back)
    bot.send_message(chat_id=message.chat.id, text='Выберите валюту:', reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == 'Назад')
def back(message):
    start(message)


@bot.message_handler(func=lambda message: message.text == 'Добавить задачу')
def add_task(message):
    bot.send_message(chat_id=message.chat.id, text='Введите вашу заметку для задачи:')
    bot.register_next_step_handler(message, set_task)


def set_task(message):
    task_text = message.text
    bot.send_message(chat_id=message.chat.id, text='Введите время выполнения задачи в формате HH:MM (24-часовой формат):')
    bot.register_next_step_handler(message, lambda m: set_task_time(m, task_text))


def set_task_time(message, task_text):
    try:
        task_time = message.text
        schedule.every().day.at(task_time).do(send_task, message.chat.id, task_text)
        bot.send_message(chat_id=message.chat.id, text=f'Задача добавлена на выполнение в {task_time}')
    except Exception as e:
        bot.send_message(chat_id=message.chat.id, text=f'Ошибка при установке времени: {e}')


def send_task(chat_id, task_text):
    bot.send_message(chat_id=chat_id, text=f'Напоминание: {task_text}')


def scheduled_job():
    while True:
        schedule.run_pending()
        time.sleep(1)


schedule_thread = threading.Thread(target=scheduled_job)
schedule_thread.start()


def check_weather(city):
    params = {
    'city_name': city.text,
    'API_key': API_KEY,
    }
    response = (
        requests.get('https://api.openweathermap.org/data/2.5/weather?q=' + params['city_name'] + '&appid=' + params['API_key'] + '&lang=ru')
    )
    bot.send_message(chat_id=city.chat.id, text=(
        f'В городе {params["city_name"]} сейчас {response.json()["weather"][0]["description"]}\n'
        f'Температура: {round(response.json()["main"]["temp"] - 273.15, 2)} °С \n'
        f'Ощущается, как: {round(response.json()["main"]["feels_like"] - 273.15, 2)} °С\n'
        f'Скорость ветра: {round(response.json()["wind"]["speed"], 2)} м/с'
    ))


def engToRus(message):
    from googletrans import Translator
    translator = Translator()
    result = translator.translate(message.text, src='en', dest='ru')
    bot.send_message(chat_id=message.chat.id, text=f'{result.text}')


def rusToEng(message):
    text = message.text
    if text == 'Назад':
        return back(message)
    translator = Translator()
    result = translator.translate(text, src='ru', dest='en')
    bot.send_message(chat_id=message.chat.id, text=f'{result.text}')


def translator(message):
    text = message.text
    if text == 'Назад':
        return back(message)
    bot.send_message(chat_id=message.chat.id, text='Напишите текст для перевода: ')
    if text == 'ENG -> RUS':
        bot.register_next_step_handler(message, lambda m: engToRus(m))
    else:
        bot.register_next_step_handler(message, lambda m: rusToEng(m))


@bot.message_handler(func=lambda message: message.text == 'Переводчик')
def choose_translator(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=1)
    itembtn5 = telebot.types.KeyboardButton('ENG -> RUS')
    itembtn6 = telebot.types.KeyboardButton('RUS -> ENG')
    itembtn_back = telebot.types.KeyboardButton('Назад')
    markup.add(itembtn5, itembtn6,itembtn_back)
    bot.send_message(chat_id=message.chat.id, text='Выберите режим: ', reply_markup=markup)
    bot.register_next_step_handler(message, lambda m: translator(m))


@bot.message_handler(func=lambda message: message.text == 'Узнать погоду')
def weather(message):
    bot.send_message(chat_id=message.chat.id, text='Укажите город: :')
    bot.register_next_step_handler(message, lambda m: check_weather(m))


@bot.message_handler(content_types=['text'])
def handle_text(message):
    message_form = message.text.strip()
    if message_form in ['Доллар(США)', 'Евро', 'Тенге(Казахстан)', 'Иена(Япония)', 'Фунт Ст.(Великобритания)']:
        dctValues ={
            'Доллар(США)': 'usd',
            'Евро': 'eur',
            'Тенге(Казахстан)': 'kzt',
            'Иена(Япония)': 'jpy',
            'Фунт Ст.(Великобритания)': 'gbp'
        }
        message_new = dctValues[message_form]
        rates = ExchangeRates(datetime.now())
        bot.send_message(chat_id=message.chat.id, text=f' Курс {message_new.upper()} - {round(float(rates[message_new.upper()].rate), 2)} RUB')


bot.polling(non_stop=True)
