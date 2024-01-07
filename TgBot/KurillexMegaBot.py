from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.enums import ParseMode
from aiogram import F
import requests
from bs4 import BeautifulSoup
import asyncio
import logging

TOKEN = '6795759902:AAF6EQEUhrKdKR4Z5_GolbdAMrWF3ITEsN0'

bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    kb = [
        [
            types.KeyboardButton(text=choice)
            for choice in ["🏴󠁧󠁢󠁥󠁮󠁧󠁿АПЛ", "🇪🇸ЛаЛига", "🇩🇪Бундеслига", "🇮🇹Серия А", "🇫🇷Лига 1", " 🇷🇺РПЛ"]
        ]
    ]

    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        row_width=5,  # Установите желаемую ширину строки
        input_field_placeholder="Выберите лигу"
    )
    await message.answer("Выберите лигу", reply_markup=keyboard)


def get_data(link):
    response = requests.get(link)
    html = response.text
    soup = BeautifulSoup(html, 'lxml')
    trs = soup.find('div', class_="rsport-table").find('table').find_all('tr')
    stats, points, names = [], [], []
    for tr in trs:
        club = tr.find_all('td', class_="m-min m-tac")
        for i in club:
            stats.append(i.text)
    for tr in trs:
        club = tr.find_all('td', class_="m-min m-tac m-pointstotal")
        for i in club:
            points.append(i.text)
    for tr in trs:
        club = tr.find_all('a', class_="team-item-name")
        for i in club:
            names.append(i.text)
    #print(names)
    #print(stats)
    #print(points)
    clubs = []
    for i in range(len(names)):
        clubs.append(stats[i * 7] + '. ' + names[i] + ' ' +
                     '(' + stats[i * 7 + 2] + 'W-' + stats[i * 7 + 3] + 'D-' + stats[i * 7 + 4]
                     + 'L)' + ' ' + points[i] + ' points')
    for teams in clubs:
        print(teams)
    return clubs


@dp.message(F.text == "🏴󠁧󠁢󠁥󠁮󠁧󠁿АПЛ")
async def button_apl(message: types.Message):
    LINK = "https://rsport.ria.ru/category_premier_league_england/tablitsa/"
    clubs = get_data(LINK)
    table = 'Таблица 🏴󠁧󠁢󠁥󠁮󠁧󠁿АПЛ:' + '\n'
    for team in clubs:
        table += team + '\n'
    await bot.send_message(chat_id=message.chat.id, text=table, parse_mode='HTML')


@dp.message(F.text == "🇪🇸ЛаЛига")
async def button_laliga(message: types.Message):
    LINK = "https://rsport.ria.ru/category_primera_division/tablitsa/"
    clubs = get_data(LINK)
    table = 'Таблица 🇪🇸ЛаЛиги:' + '\n'
    for team in clubs:
        table += team + '\n'
    await bot.send_message(chat_id=message.chat.id, text=table)


@dp.message(F.text == "🇩🇪Бундеслига")
async def button_bundesliga(message: types.Message):
    LINK = "https://rsport.ria.ru/category_bundesliga/tablitsa/"
    clubs = get_data(LINK)
    table = 'Таблица 🇩🇪Бундеслиги:' + '\n'
    for team in clubs:
        table += team + '\n'
    await bot.send_message(chat_id=message.chat.id, text=table)


@dp.message(F.text == "🇮🇹Серия А")
async def button_seriea(message: types.Message):
    LINK = "https://rsport.ria.ru/category_serie_a/tablitsa/"
    clubs = get_data(LINK)
    table = 'Таблица 🇮🇹Серии А:' + '\n'
    for team in clubs:
        table += team + '\n'
    await bot.send_message(chat_id=message.chat.id, text=table)


@dp.message(F.text == "🇫🇷Лига 1")
async def button_ligue1(message: types.Message):
    LINK = "https://rsport.ria.ru/category_ligue_1/tablitsa/"
    clubs = get_data(LINK)
    table = 'Таблица 🇫🇷Лиги 1:' + '\n'
    for team in clubs:
        table += team + '\n'
    await bot.send_message(chat_id=message.chat.id, text=table)


@dp.message(F.text == "🇷🇺РПЛ")
async def button_apl(message: types.Message):
    LINK = "https://rsport.ria.ru/category_premier_league_russia/tablitsa/"
    clubs = get_data(LINK)
    table = 'Таблица 🇷🇺РПЛ:'    + '\n'

    for team in clubs:
        table += team + '\n'
    await bot.send_message(chat_id=message.chat.id, text=table)


async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
