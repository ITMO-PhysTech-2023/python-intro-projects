import telebot
from currency_converter import CurrencyConverter
from telebot import types

bot = telebot.TeleBot('6906355714:AAEJYZBpTZhd9EaR2F-FSEcSuFUWkT3EnTY')

currency = CurrencyConverter()
amount = 0
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Здравствуйте! Введите сумму для конвертации.')
    bot.register_next_step_handler(message, summa)

def summa(message):
    global amount
    try:
        amount = int(message.text.strip())
    except ValueError:
        bot.send_message(message.chat.id, 'Неверный формат. Введите число, которое хотите конвертировать.')
        bot.register_next_step_handler(message, summa) #следующие, что введет пользователь будет обработано функцией summa
        return
    if amount > 0:
        markup = types.InlineKeyboardMarkup(row_width=2)
        button1 = types.InlineKeyboardButton('USD/EUR', callback_data='usd/eur')
        button2 = types.InlineKeyboardButton('EUR/USD', callback_data='eur/usd')
        button3 = types.InlineKeyboardButton('USD/GBD', callback_data='USD/GBD')
        button4 = types.InlineKeyboardButton('GBD/USD', callback_data='GBD/USD')
        button5 = types.InlineKeyboardButton('Другая пара', callback_data='else')
        markup.add(button1, button2, button3, button4, button5)
    else:
        bot.send_message(message.chat.id, 'Неверный формат. Введите число, которое хотите конвертировать.')
        bot.register_next_step_handler(message,summa)  # следующие, что введет пользователь будет обработано функцией summa

    bot.send_message(message.chat.id, 'Выберите пару валют:', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data != 'else':
        values = call.data.upper().split('/')
        result = currency.convert(amount, values[0], values[1])
        bot.send_message(call.message.chat.id, f'Ваша сумма в {values[1]}: {round(result, 2)}. Можете вписать новую сумму.')
        bot.register_next_step_handler(call.message, summa)
    else:
        bot.send_message(call.message.chat.id, 'Введите валютную пару через слэш.')
        bot.register_next_step_handler(call.message, my_currency)

def my_currency(message):
    try:
        values = message.text.upper().split('/')
        result = currency.convert(amount, values[0], values[1])
        bot.send_message(message.chat.id, f'Ваша сумма в {values[1]}: {round(result, 2)}. Можете вписать новую сумму.')
        bot.register_next_step_handler(message, summa)
    except Exception:
        bot.send_message(message.chat.id, 'Что-то не так) Впишите валютную пару заново.')
        bot.register_next_step_handler(message, my_currency)

bot.polling(none_stop=True)