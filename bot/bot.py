import telebot
from telebot import types

bot = telebot.TeleBot('6801853424:AAFFB8qf6pp0dZBRkX4e1lJY45V3rGa2RmE')
try:
    file = open("database.txt", 'r')
    x, y = map(int, file.read().split())
    file.close()
except:
    x, y = 0, 0

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    global x, y
    if message.text == "Привет":
        bot.send_message(message.from_user.id, "Привет, дорогой пользователь :D")
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Напиши 'Привет', если хочешь поздороваться, или '/questions', если хочешь пройти опрос; соблюдай регистр!")
    elif message.text == "/questions":
        keyboard = types.InlineKeyboardMarkup()
        key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')
        keyboard.add(key_yes)
        key_no= types.InlineKeyboardButton(text='Нет', callback_data='no')
        keyboard.add(key_no)
        question = 'Ты веришь в гороскопы?'
        bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)
    else:
        bot.send_message(message.from_user.id, "Напиши /help, я помогу.")

    @bot.callback_query_handler(func = lambda call: True)
    def callback_worker(call):
        global x, y
        if call.data == "yes":
            y += 1
            x += 1
            bot.send_message(call.message.chat.id, f'Ты дурачок :(\nТаких дурачков еще {100 * y // x}%')
        elif call.data == "no":
            x += 1
            bot.send_message(call.message.chat.id, f'Молодец! Так держать!\nТаких молодцов еще {100 - (100 * y) // x}%')
            file = open("database.txt", 'w')
            file.write(str(x)+" "+str(y))
            file.close()

bot.polling(none_stop=True, interval=0)
