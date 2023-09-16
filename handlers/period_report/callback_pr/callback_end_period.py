from loader import bot, period_states, calendar, calendar_4_callback
from config import TIMEZONE
from utils.calendar import get_calendar
from data.objects import PeriodReport
from database.actions.workday import get_workdays_for_period
from keyboards.inline.full_report import if_full_report

from telebot.types import CallbackQuery, Message, ReplyKeyboardRemove
from datetime import datetime


@bot.callback_query_handler(
    func=lambda c: c.data.startswith(calendar_4_callback.prefix)
)
def date_chosen(call: CallbackQuery):
    id = call.message.chat.id
    name, action, year, month, day = call.data.split(calendar_4_callback.sep)
    date = calendar.calendar_query_handler(
        bot=bot, call=call, name=name, action=action, year=year, month=month, day=day
    )

    if action == "CANCEL":
        text = "Операция отменена."
        bot.send_message(id, text, reply_markup=ReplyKeyboardRemove())
        bot.delete_state(id)

    else:
        date = TIMEZONE.localize(date)
        now = TIMEZONE.localize(datetime.now())
        offset = bot.retrieve_data(id).data.get("start_date")
        if date > now or date <= offset:
            text = f"Ошибка ввода! Выбери дату между сегодняшним днём и {offset.strftime('%d.%m.%Y')}"
            bot.send_message(
                id, text, reply_markup=get_calendar(now, calendar_4_callback)
            )
        else:
            if action == "DAY":
                text = f'Ты выбрала дату: {date.strftime("%d.%m.%Y")}'
                bot.send_message(id, text)
                bot.set_state(id, period_states.get_full_report)

                workdays = get_workdays_for_period(id, offset, date)
                master_name = call.from_user.first_name
                period = PeriodReport(workdays, offset, date, master_name)
                text = period.get_report()

                bot.send_message(id, text=text)
                bot.add_data(id, period=period)

                text = (
                    "Можешь скачать детальный отчет, нажав на соответствующую кнопку."
                )
                bot.send_message(id, text=text, reply_markup=if_full_report())


@bot.message_handler(state=period_states.get_end_date, content_types=["text"])
def handler_period_start_date_keyboard_input(message: Message):
    t = "Нажми на одну из кнопок⬆️ "
    bot.send_message(message.chat.id, t)
