from loader import bot, states
from keyboards.inline.treatment_types import types_keyboard
from data.objects import Visit

from telebot.types import CallbackQuery

from utils.handler import cancel_action


@bot.callback_query_handler(func=lambda c: c.data.startswith('time'))
def callback_time_of_procedure(call: CallbackQuery):
    id = call.message.chat.id
    bot.delete_message(id, call.message.id)

    cb = call.data[5:]

    if cb == 'custom':
        bot.set_state(id, states.enter_custom_time)
        text = 'Введи своё время (4 цифры, например: 0945 или 1910), в диапазоне 9:00 - 22:59'
        bot.send_message(id, text)
    elif cb == 'cancel':
        cancel_action(id, bot)
    else:
        with bot.retrieve_data(id) as data:
            data["visit"] = Visit(data["date"], cb)

        bot.set_state(id, states.choose_type)
        bot.send_message(id, "Выбери тип процедуры", reply_markup=types_keyboard())
