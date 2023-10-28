from os import getenv
from dotenv import load_dotenv, find_dotenv
from sqlalchemy.engine import URL

from telebot.types import BotCommand


if find_dotenv():
    load_dotenv()

    BOT_TOKEN = getenv("TELEGRAM_API_TOKEN")
    PG_DB = getenv('POSTGRES_DB')
    PG_USER = getenv('POSTGRES_USER')
    PG_PASSWORD = getenv('POSTGRES_PASSWORD')

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
    BotCommand("alarm", "Напоминания")
)

PROCEDURE_PARAMS = [
    "id",
    "type",
    "gross",
    "sub",
    "first",
    "sub_visits",
    "prime_cost",
    "manual_input",
    "manual_value",
]

SQLALCHEMY_URL = URL.create(
    drivername='postgresql+psycopg2',
    username=PG_USER,
    password=PG_PASSWORD,
    database=PG_DB,
    host='bot_db',
).render_as_string(hide_password=False)
SQLALCHEMY_ECHO = True

LASER_CONVERSION_STATUSES = [
    'UNKNOWN',
    'NOT_NEW',
    'NEW_BOUGHT',
    'NEW_NOT_BOUGHT',
]
