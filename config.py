from os import getenv
from dotenv import load_dotenv, find_dotenv
from pytz import timezone

from telebot.types import BotCommand


if find_dotenv():
    load_dotenv()
    BOT_TOKEN = getenv("TELEGRAM_API_TOKEN")
    print("The token has been succussfully loaded")
else:
    exit(1)

COMMANDS = (
    BotCommand("start", "Запустить бота"),
    BotCommand("help", "Помощь"),
    BotCommand("cancel", "Отменить текущюю операцию"),
    BotCommand("add_visit", "Добавить посещение"),
    BotCommand("show_date", "Показать посещения за дату"),
    BotCommand("report", "Отчет за период"),
)

TIMEZONE = timezone("Europe/Moscow")

PROCEDURE_PARAMS = [
    "type",
    "gross",
    "sub",
    "first",
    "sub_visits",
    "prime_cost",
    "duration",
    "manual_input",
    "manual_value",
]

SQLALCHEMY_URL = "sqlite:///./db.sqlite3"
SQLALCHEMY_ECHO = True
