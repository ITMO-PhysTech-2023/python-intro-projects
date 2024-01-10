from aiogram import Bot, Dispatcher, types, F
import os, signal, asyncio, logging, requests
from aiogram.filters.command import Command, CommandStart
from aiogram.enums import ParseMode
from bs4 import BeautifulSoup

TOKEN = '6795759902:AAFQyQfcAPa5E70mcqaxcTVFoT8v6uyXAGM'

bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    keyboard = Change_league()
    await message.answer("Выберите лигу", reply_markup=keyboard)


@dp.message(Command("stop"))
async def stop_bot(message: types.Message):
    # Здесь можно добавить проверку на админа или другие условия
    await message.reply("Выключаю бот.")
    await os.kill(os.getpid(), signal.SIGINT)


def Change_league():
    kb = [
        [
            types.KeyboardButton(text=choice)
            for choice in ["🏴󠁧󠁢󠁥󠁮󠁧󠁿АПЛ", "🇪🇸ЛаЛига", "🇩🇪Бундеслига", "🇮🇹Серия А", "🇫🇷Лига 1", "🇷🇺РПЛ"]
        ]
    ]

    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        row_width=5,  # Установите желаемую ширину строки
        input_field_placeholder="Выберите лигу"
    )
    return keyboard


def get_data_tables(link):
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


def get_data_goals(link):
    response = requests.get(link)
    html = response.text
    soup = BeautifulSoup(html, 'lxml')
    trs = soup.find('div', class_="rsport-table").find('table').find_all('tr')
    surname, team, goals = [], [], []
    for tr in trs:
        player = tr.find_all(class_="person-item-name")
        for i in player:
            surname.append(i.text)
    for tr in trs:
        player = tr.find_all(class_="team-item-name")
        for i in player:
            team.append(i.text)
    for tr in trs:
        player = tr.find_all(class_="m-min m-br m-tac m-nowr")
        for i in player:
            goals.append(i.text[:2])
    players = []
    for i in range(len(goals)):
        players.append(str(i + 1) + '. ' + surname[i] + '(' + team[i] + ')  ' + goals[i])
    for pl in players:
        print(pl)
    return players


async def handle_league(message: types.Message, league_name, tablelink, goalslink):
    kb = [
        [
            types.KeyboardButton(text=choice)
            for choice in ["Таблица", "Бомбардиры"]
        ]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        row_width=5,  # Установите желаемую ширину строки
        input_field_placeholder="Выберите тип"
    )
    await bot.send_message(chat_id=message.chat.id, text="Выбери тип", reply_markup=keyboard)

    @dp.message(F.text == "Таблица")
    async def button_table(message1: types.Message):
        clubs = get_data_tables(tablelink)
        table = f'Таблица {league_name}:\n'
        for team in clubs:
            table += team + '\n'
        await bot.send_message(chat_id=message1.chat.id, text=table, parse_mode='HTML')

    @dp.message(F.text == "Бомбардиры")
    async def button_goals(message2: types.Message):
        names = get_data_goals(goalslink)
        table = f'Бомбардиры {league_name}:' + '\n'
        for team in names:
            table += team + '\n'
        await bot.send_message(chat_id=message2.chat.id, text=table, parse_mode='HTML')


@dp.message(F.text == "🇩🇪Бундеслига")
async def button_bundesliga(message: types.Message):
    await handle_league(message, "🇩🇪Бундеслиги", "https://rsport.ria.ru/category_bundesliga/tablitsa/",
                        "https://rsport.ria.ru/category_bundesliga/statistika/")


@dp.message(F.text == "🏴󠁧󠁢󠁥󠁮󠁧󠁿АПЛ")
async def button_bundesliga(message: types.Message):
    await handle_league(message, "🏴󠁧󠁢󠁥󠁮󠁧󠁿АПЛ", "https://rsport.ria.ru/category_premier_league_england/tablitsa/",
                        "https://rsport.ria.ru/category_premier_league_england/statistika/")


@dp.message(F.text == "🇪🇸ЛаЛига")
async def button_laliga(message: types.Message):
    await handle_league(message, "🇪🇸ЛаЛига", "https://rsport.ria.ru/category_primera_division/tablitsa/",
                        "https://rsport.ria.ru/category_primera_division/statistika/")


@dp.message(F.text == "🇮🇹Серия А")
async def button_seriea(message: types.Message):
    await handle_league(message, "🇮🇹Серия А", "https://rsport.ria.ru/category_serie_a/tablitsa/",
                        "https://rsport.ria.ru/category_serie_a/statistika/")


@dp.message(F.text == "🇫🇷Лига 1")
async def button_ligue1(message: types.Message):
    LINK = "https://rsport.ria.ru/category_ligue_1/tablitsa/"
    await handle_league(message, "🇫🇷Лига 1", "https://rsport.ria.ru/category_ligue_1/tablitsa/",
                        "https://rsport.ria.ru/category_ligue_1/statistika/")


@dp.message(F.text == "🇷🇺РПЛ")
async def button_apl(message: types.Message):
    LINK = "https://rsport.ria.ru/category_premier_league_russia/tablitsa/"
    await handle_league(message, "🇷🇺РПЛ", "https://rsport.ria.ru/category_premier_league_russia/tablitsa/",
                        "https://rsport.ria.ru/category_premier_league_russia/statistika/")


async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
