import telebot
import requests

bot = telebot.TeleBot('6791056471:AAF-nUg1TZUuBvxi7g7vjhJ25KNQ2w8BYR0')

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет! Я бот, который может поддерживать сценарий-диалога и узнавать погоду влюбом городе или селе. Напиши мне что-нибудь.')

@bot.message_handler(func=lambda message: True)
def dialog_message(message):
    if message.text == 'Привет':
        bot.send_message(message.chat.id, 'Привет! Как тебя зовут?')
    elif message.text.startswith('Меня зовут'):
        bot.send_message(message.chat.id, 'Приятно познакомиться,'+ message.text.split()[-1] +',сколько тебе лет?')
    elif not(message.text.startswith('Я') or message.text.startswith('Город') or message.text.startswith('Да') or message.text.startswith('Нет') or message.text.startswith ('Село')):
            if int(message.text)<40:
                bot.send_message(message.chat.id, 'Да ты еще совсем молодой, у тебя вся жизнь впереди. Ты хочешь узнать погоду в своем городе (селе), где ты живешь? Если да, то смело пиши мне :"Я живу в городе(селе) ...". Если тебе не интересна погода в своем городе(селе) сейчас, то напиши название любого другого населенного пункта таким образом:" Город(село) ...". Я представлю тебе подробное описание и ты смело сможешь идти гулять, ведь будешь готов к любым погодным условиям! Гулять надо часто в любом возрасте, ведь это полезно для здоровья!')
                city = message.text.split()[-1]
            else:
                bot.send_message(message.chat.id, 'Да ты уже опытный человек и много повидал за свою жизнь! Ты хочешь узнать погоду в своем городе(селе), где ты живешь? Если да, то смело пиши мне :"Я живу в городе(селе) ...". Если тебе не интересна погода в своем городе(селе) сейчас, то напиши название любого другого населенного пункта таким образом:" Город(село) ...". Я представлю тебе подробное описание и ты смело сможешь идти гулять, ведь будешь готов к любым погодным условиям! Гулять надо часто в любом возрасте, ведь это полезно для здоровья!')
    elif message.text.startswith ('Я живу в городе') or message.text.startswith ('Город') or message.text.startswith ('Я живу в селе') or message.text.startswith ('Село'):
        city = message.text.split()[-1]
            # формируем запрос
        url = 'https://api.openweathermap.org/data/2.5/weather?q=' + city + '&units=metric&lang=ru&appid=99ec11f1bb95491c60a9262a8c927fb9'
            # отправляем запрос на сервер и сразу получаем результат
        weather_data = requests.get(url).json()
            # получаем данные о температуре и о том, как она ощущается
        temperature = round (weather_data['main']['temp'])
        temperature_feels = round(weather_data['main']['feels_like'])
        humidity = round(weather_data["main"]["humidity"])
        pressure = round(weather_data["main"]["pressure"])
        wind = round(weather_data["wind"]["speed"])
            # формируем ответы
        w_now = 'Сейчас в городе(селе) ' + city + ' ' + str(temperature) + ' °C'
        w_feels = 'Ощущается как ' + str(temperature_feels) + ' °C'
        w_humidity ='Влажность в городе(селе) '+city+' '+str(humidity)+' %'
        w_pressure ='Давление ' + str(pressure/1.333)+' мм.рт.ст.'
        w_wind ='Скорость ветра в городе(селе) '+ str(wind)+' м/с'
        w_dalee= 'Хотите ли вы узнать погоду в каком-либо еще городе(селе)?'
            # отправляем значения пользователю
        bot.send_message(message.chat.id, w_now)
        bot.send_message(message.chat.id, w_feels)
        bot.send_message(message.chat.id, w_humidity)
        bot.send_message(message.chat.id, w_pressure)
        bot.send_message(message.chat.id, w_wind)
        if wind < 5:
            bot.send_message(message.from_user.id, '✅ Погода хорошая, ветра почти нет')
        elif wind < 10:
            bot.send_message(message.from_user.id, '🤔 На улице ветрено, оденьтесь чуть теплее')
        elif wind < 20:
            bot.send_message(message.from_user.id, '❗️ Ветер очень сильный, будьте осторожны, выходя из дома')
        else:
            bot.send_message(message.from_user.id, '❌ На улице шторм, на улицу лучше не выходить')
        bot.send_message(message.chat.id, w_dalee)


    elif message.text == 'Да':
        bot.send_message(message.chat.id, 'Какой город(село) тебя интересует?')
    elif message.text == 'Нет':
        bot.send_message(message.chat.id, 'Хорошо, если захочешь узнать что-то еще, то пиши мне. До новых встреч!')

bot.polling()