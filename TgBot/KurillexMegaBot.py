from aiogram import Bot, Dispatcher, types, F
import os, signal, asyncio, logging, requests
from aiogram.filters.command import Command, CommandStart
from aiogram.filters import StateFilter
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
from bs4 import BeautifulSoup

TOKEN = '6795759902:AAFQyQfcAPa5E70mcqaxcTVFoT8v6uyXAGM'

bot = Bot(token=TOKEN)
dp = Dispatcher()
leagues = ["🏴󠁧󠁢󠁥󠁮󠁧󠁿АПЛ", "🇪🇸ЛаЛига", "🇩🇪Бундеслига", "🇮🇹Серия А", "🇫🇷Лига 1", "🇷🇺РПЛ"]
knopki = ["Таблица", "Бомбардиры"]
links = {
    "🏴󠁧󠁢󠁥󠁮󠁧󠁿АПЛ": ["https://rsport.ria.ru/category_premier_league_england/tablitsa/", "https://rsport.ria.ru/category_premier_league_england/statistika/"],
    "🇪🇸ЛаЛига": ["https://rsport.ria.ru/category_primera_division/tablitsa/", "https://rsport.ria.ru/category_primera_division/statistika/"],
    "🇩🇪Бундеслига": ["https://rsport.ria.ru/category_bundesliga/tablitsa/", "https://rsport.ria.ru/category_bundesliga/statistika/"],
    "🇮🇹Серия А": ["https://rsport.ria.ru/category_serie_a/tablitsa/", "https://rsport.ria.ru/category_serie_a/statistika/"],
    "🇫🇷Лига 1": ["https://rsport.ria.ru/category_ligue_1/tablitsa/", "https://rsport.ria.ru/category_ligue_1/statistika/"],
    "🇷🇺РПЛ": ["https://rsport.ria.ru/category_premier_league_russia/tablitsa/", "https://rsport.ria.ru/category_premier_league_russia/statistika/"]
}


class BotMenu(StatesGroup):
    choosing_league = State()
    choosing_type = State()


@dp.message(CommandStart(), StateFilter(None))
async def cmd_start(message: types.Message, state: FSMContext):
    kb = [[types.KeyboardButton(text=choice) for choice in leagues]]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        row_width=5,  # Установите желаемую ширину строки
        input_field_placeholder="Выберите лигу"
    )
    await message.answer("Выберите лигу", reply_markup=keyboard)
    await state.set_state(BotMenu.choosing_league)


@dp.message(Command("stop"))
async def stop_bot(message: types.Message):
    await message.reply("Выключаю бот.")
    await state.finish()


@dp.message(BotMenu.choosing_league, F.text.in_(leagues))
async def button1(message: types.Message,  state: FSMContext):
    await state.update_data(chosen_league=message.text)
    kb = [[types.KeyboardButton(text=choice) for choice in knopki]]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        row_width=5,  # Установите желаемую ширину строки
        input_field_placeholder="Выберите тип"
    )
    await bot.send_message(chat_id=message.chat.id, text="Выбери тип", reply_markup=keyboard)
    await state.set_state(BotMenu.choosing_type)


@dp.message(BotMenu.choosing_type, F.text == "Таблица")
async def button_table(message1: types.Message, state: FSMContext):
    user_data = await state.get_data()
    LEAGUE = user_data['chosen_league']
    clubs = get_data_tables(links[LEAGUE][0])
    table = f'Таблица {LEAGUE}:\n'
    for team in clubs:
        table += team + '\n'
    kb = [[types.KeyboardButton(text=choice) for choice in leagues]]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        row_width=5,  # Установите желаемую ширину строки
        input_field_placeholder="Выберите лигу"
    )
    await bot.send_message(chat_id=message1.chat.id, text=table, parse_mode='HTML', reply_markup=keyboard)
    await state.clear()
    await state.set_state(BotMenu.choosing_league)


@dp.message(BotMenu.choosing_type, F.text == "Бомбардиры")
async def button_goals(message2: types.Message, state: FSMContext):
    user_data = await state.get_data()
    LEAGUE = user_data['chosen_league']
    names = get_data_goals(links[LEAGUE][1])
    table = f'Бомбардиры {LEAGUE}:' + '\n'
    for team in names:
        table += team + '\n'
    kb = [[types.KeyboardButton(text=choice) for choice in leagues]]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        row_width=5,  # Установите желаемую ширину строки
        input_field_placeholder="Выберите лигу"
    )
    await bot.send_message(chat_id=message2.chat.id, text=table, parse_mode='HTML', reply_markup=keyboard)
    await state.clear()
    await state.set_state(BotMenu.choosing_league)


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


async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
