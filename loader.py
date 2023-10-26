import config
from states.user_states import (
    AddVisitStates, ShowDateStates, PeriodReportStates, AlarmStates
)
from utils.set_filters import set_filters
from database.actions.core import init_db
from database.models import Base

from telebot import TeleBot

from telebot_calendar import Calendar, RUSSIAN_LANGUAGE, CallbackData
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Set up bot instance
bot = TeleBot(config.BOT_TOKEN, parse_mode="html")
bot.set_my_commands(config.COMMANDS)
set_filters(bot)

# States
states = AddVisitStates()
show_date_states = ShowDateStates()
period_states = PeriodReportStates()
alarm_states = AlarmStates()

# Set up calendar and calendar callbacks
calendar = Calendar(language=RUSSIAN_LANGUAGE)
calendar_1_callback = CallbackData(
    "calendar_1", "action", "year", "month", "day")
calendar_2_callback = CallbackData(
    "calendar_2", "action", "year", "month", "day")
calendar_3_callback = CallbackData(
    "calendar_3", "action", "year", "month", "day")
calendar_4_callback = CallbackData(
    "calendar_4", "action", "year", "month", "day")

# DB initialization and session instance creation
engine = create_engine(config.SQLALCHEMY_URL, echo=config.SQLALCHEMY_ECHO)
Session = sessionmaker(engine)
init_db(Base, engine)
