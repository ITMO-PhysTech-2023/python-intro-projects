from database import *
import telebot
import types

bot = telebot.TeleBot('6421595548:AAEuHFF4IeILd8BTNL69H0N8hO_Fte3RvYc')

def send_message(message):
    global user_db, message_db

    message_id = message_db.add_message(sender_username = message.sender, receiver_username = message.receiver, text = message.text, header = message.header)

    user_db.push_received_message(message.receiver, message_id)
    user_db.push_sent_message(message.sender, message_id)


user_db = User_Database()
message_db = Message_Database()


@bot.message_handler(content_types=['text'])
def start(message):
    if message.text == "/start":
        bot.send_message(message.from_user.id, 'Введите логин')
        bot.register_next_step_handler(message, login_request)
    else:
        bot.send_message(message.from_user.id, 'Чтобы начать работать, напишите /start')

def login_request(login):
    login_registered = False
    if user_db.find_username(login.text):
        login_registered = True
    
    if login_registered:
        bot.send_message(login.from_user.id, 'Ваш логин - ' + login.text + '. Введите пароль.')
        global username
        username = login.text
        bot.register_next_step_handler(login, password_request, user_db.find_username(login.text)[5])
    else:
        bot.send_message(login.from_user.id, 'Вы не зареганы. Введите новый логин.')
        bot.register_next_step_handler(login, register_login)

def password_request(password, *p):
    if password.text == p[0]:
        bot.send_message(password.from_user.id, 'Поздравляю! Вы вошли в свой аккаунт. Для перехода в главное меню напишите любое сообщение.')
        bot.register_next_step_handler(password, main_menu)
        
    else:
        bot.send_message(password.from_user.id, 'Пароль неверный.')

def register_login(login):
    bot.send_message(login.from_user.id, 'Введите новый пароль.')
    bot.register_next_step_handler(login, register_password, login.text)

def register_password(password, *login):
    user_db.add_user(username = login[0], password = password.text)
    bot.send_message(password.from_user.id, 'Окей. Пароль установлен.')

def main_menu(message):

 
    keyboard = telebot.types.InlineKeyboardMarkup() #наша клавиатура
    key_received = telebot.types.InlineKeyboardButton(text='Посмотреть входящие', callback_data='received') #кнопка «Да»
    keyboard.add(key_received) #добавляем кнопку в клавиатуру
    key_sent = telebot.types.InlineKeyboardButton(text='Посмотреть исходящие', callback_data='sent')
    keyboard.add(key_sent)
    key_new = telebot.types.InlineKeyboardButton(text='Написать письмо', callback_data='new')
    keyboard.add(key_new)
    global pass_message
    pass_message = message

    bot.send_message(message.from_user.id, text='Главное меню. Что будем делать?', reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    global username, pass_message
    if call.data == "received": #call.data это callback_data, которую мы указали при объявлении кнопки
        bot.send_message(call.message.chat.id, str(user_db.view_received_messages(username = username, message_db_filename = 'messages.db')))
    elif call.data == "sent": #call.data это callback_data, которую мы указали при объявлении кнопки
        bot.send_message(call.message.chat.id, str(user_db.view_sent_messages(username = username, message_db_filename = 'messages.db')))

    elif call.data == "new": #call.data это callback_data, которую мы указали при объявлении кнопки
        bot.send_message(call.message.chat.id, 'Кому отправляем письмо?')
        bot.register_next_step_handler(message = pass_message, callback = receiver_input)

def receiver_input(usrname):
    #bot.send_message(usrname.from_user.id, 'Кому отправляем письмо?')
    if user_db.find_username(usrname.text):
        bot.register_next_step_handler(usrname, header_input, usrname.text)
        bot.send_message(usrname.from_user.id, 'Введите заголовок.')
    else:
        bot.send_message(usrname.from_user.id, 'Нет такого пользователя!')
        bot.register_next_step_handler(usrname, receiver_input)

def header_input(header, *h):
    #bot.send_message(header.from_user.id, 'Введите заголовок, будьте добры.')
    bot.register_next_step_handler(header, text_input, h[0], header.text)
    bot.send_message(header.from_user.id, 'Введите текст письма.')

def text_input(text, *t):
    
    send_message(Message(text = text.text, sender = username, receiver = t[0], header = t[1]))
    bot.register_next_step_handler(text, main_menu)


bot.polling(none_stop=True, interval=0)

