import telebot
import time
from telebot import types
from date_parser import DateParser
from date_parser import check_date
from team_parser import TeamParser
from team_parser import check_team

TOKEN = "5800711742:AAETdUzLGyLoZKo2MS-uqTY2eNnEj9kJ5tQ"

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    markup_start_choice = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)  # задали формат кнопок
    search_by_date_button = types.KeyboardButton("Поиск по дате")
    search_by_team_button = types.KeyboardButton("Поиск по команде")
    help = types.KeyboardButton("Помощь")
    markup_start_choice.add(search_by_date_button, search_by_team_button, help)  # добавили кнопки
    bot.send_message(
        message.chat.id,
        "Привет! \nЭто бот для поиска футбольных матчей. \nНажми кнопку чтобы начать...",
        reply_markup=markup_start_choice)


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(
        message.chat.id,
        "Чтобы начать использование бота введите команду '/start';"
        "\nЕсли возникли проблемы — перезапустите бота и нажмите '/start';"
        "\nЧтобы посмотреть все возможности бота введите '/all_commands'.",
    )


@bot.message_handler(commands=['all_commands'])
def all_commands(message):
    bot.send_message(
        message.chat.id,
        "Перечень всех команд: "
        "\n/start — перезапуск бота; "
        "\n/help — инструкция использования; "
        "\n/all_commands — перечень возможных команд; "
        "\n/search_by_date — поиск матчей по дате;"
        "\n/search_by_team — поиск информации по команде;"
    )


@bot.message_handler(commands=['search_by_date'])
def search_by_date_com(message):
    bot.send_message(
        message.chat.id,
        "Введите дату в формате: дд.мм.гггг")
    bot.register_next_step_handler(message, send_matches_by_date)


def send_matches_by_date(message):
    msg = message.text
    msg = msg.split('.')
    print(msg, check_date(msg))
    if not check_date(msg):
        bot.send_message(
            message.chat.id,
            "Некорректный ввод. Начните поиск заново"
        )
        return
    msg.reverse()
    date = '-'.join(msg)
    parser = DateParser(date)
    if not parser.leagues:
        bot.send_message(
            message.chat.id,
            "Матчей на эту дату нет. Начните поиск заново"
        )
    else:
        for i in parser.messages:
            bot.send_message(
                message.chat.id,
                i,
                parse_mode="Markdown"
            )
            time.sleep(0.1)


@bot.message_handler(commands=['search_by_team'])
def search_by_team_com(message):
    bot.send_message(
        message.chat.id,
        "Введите название футбольной команды:")
    bot.register_next_step_handler(message, search_by_team)


def search_by_team(message):
    msg = message.text
    if not check_team(msg):
        bot.send_message(
            message.chat.id,
            text="Такой команды нет. Начните поиск заново"
        )
        return
    parser = TeamParser(msg)
    for match in parser.calendar:
        bot.send_message(
            message.chat.id,
            text=match
        )
    for stat in parser.stats:
        bot.send_message(
            message.chat.id,
            text=stat
        )
    for news in parser.news:
        bot.send_message(
            message.chat.id,
            text=news
        )


@bot.message_handler(content_types=['text'])
def get_text(message):
    print(message)
    if message.text == "Поиск по дате":
        search_by_date_com(message)
    elif message.text == "Поиск по команде":
        search_by_team_com(message)
    elif message.text == "Помощь":
        help(message)


bot.polling(none_stop=True)

