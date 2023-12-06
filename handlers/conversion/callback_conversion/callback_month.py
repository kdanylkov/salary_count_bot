from loader import bot
from utils.calendar import get_first_and_last_dates
from utils.jinja import get_template
from database.actions.visit import calculate_conversion_rate, get_visits_new_clients_by_period
from config import MONTH_MAPPING_PREPOSITIONAL_CASE

from telebot.types import CallbackQuery


@bot.callback_query_handler(func=lambda c: c.data.startswith('month_of_conversion'))
def handle_callback_month_choice(call: CallbackQuery):
    id = call.message.chat.id
    bot.delete_message(id, call.message.id)
    month, year = call.data[20:].split('_')

    first_date, last_date = get_first_and_last_dates(
        int(month), int(year)
    )
    print(first_date, last_date)

    conversion_rate, total_new_clients, new_clients_bought = \
        calculate_conversion_rate(id, first_date, last_date)
    month_prepos = MONTH_MAPPING_PREPOSITIONAL_CASE[month]
    text = (
        f'Всего новых клиентов в {month_prepos}: {total_new_clients}.\n'
        f'Купили абонемент: {new_clients_bought}.\n'
        f'Конверсия: {conversion_rate}%'
    )

    visits = get_visits_new_clients_by_period(id, first_date, last_date)

    tmpt = get_template("conversion_report.j2")
    msg = tmpt.render(visits=visits)
    text = '\n'.join([text, msg])

    bot.send_message(id, text)
