from loader import bot


from telebot.types import CallbackQuery


@bot.callback_query_handler(func=lambda c: c.data.startswith('alarm'))
def callback_alarm_switch_status(call: CallbackQuery):
    ...
