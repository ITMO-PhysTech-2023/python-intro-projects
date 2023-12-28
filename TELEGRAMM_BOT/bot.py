import telebot
from telebot import types
from currency_converter import CurrencyConverter
bot=telebot.TeleBot('6818144100:AAEz4vGQvSOoMarvNxR5tAOpDkNeAryP340')
currency=CurrencyConverter()
s=0
started_value=''
finished_value=''
@bot.message_handler(commands=['start'])
def begining(message):
    markup=types.InlineKeyboardMarkup()
    button1=types.InlineKeyboardButton('Конвертировать', callback_data='trans')
    button2=types.InlineKeyboardButton('Узнать курс валют', callback_data='currancy')
    markup.row(button1,button2)
    #bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name} {message.from_user.last_name}! Выбери из списка нужное',markup)
    bot.reply_to(message,f'Привет, {message.from_user.first_name} {message.from_user.last_name}! Выбери из списка нужное',reply_markup=markup)
@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data=='trans':
        bot.send_message(callback.message.chat.id,'Введи сумму')
        bot.register_next_step_handler(callback.message, summa)

def summa(message):
    global s
    try:
        s=int(message.text.strip())
        if s>0:
            bot.send_message(message.chat.id, 'Введи начальную валюту')
            bot.register_next_step_handler(message,st_value)
        else:
            bot.send_message(message.chat.id, 'Что-то не так, попробуй еще раз')
            bot.register_next_step_handler(message, summa)
    except Exception:
        bot.send_message(message.chat.id, 'Что-то не так, попробуй еще раз')
        bot.register_next_step_handler(message,summa)
        return
def st_value(message):
    global started_value
    try:
        started_value=message.text.upper()
        bot.send_message(message.chat.id, 'Введи конченую валюту')
        bot.register_next_step_handler(message,fin_value)
    except Exception:
        bot.send_message(message.chat.id, 'Неверная валюта, попробуй сначала')
        bot.register_next_step_handler(message,summa)
        return
def fin_value(message):
    global finished_value
    try:
        finished_value=message.text.upper()
        res = currency.convert(s, started_value,finished_value)
        bot.send_message(message.chat.id, f'{round(res, 2)}')
        bot.send_message(message.chat.id, 'Для продолжения напиши: 1')
        bot.register_next_step_handler(message,begining)
        #bot.register_next_step_handler(message,translate)
    except Exception:
        bot.send_message(message.chat.id, 'Неверные валюты, попробуй сначала. Введи сумму')
        bot.register_next_step_handler(message,summa)
        return

#def translate(message):
    #bot.send_message(message.chat.id, 'Введи')
    #values=message.text.upper().split('/')
    #res = currency.convert(s,started_value,finished_value)#currency_converter.CurrencyConverter(s,values[0],values[1])
    #bot.send_message(message.chat.id,f'{round(res,2)}')
    #bot.register_next_step_handler(message,begining)



bot.polling(none_stop=True)