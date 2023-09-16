from loader import bot, states
from keyboards.inline.subcr_laser import if_subscr_laser

from telebot.types import Message


@bot.message_handler(state=states.duration, is_positive_digit=True)
def proc_duration_handler(message: Message):
    id = message.chat.id
    duration = int(message.text)

    bot.add_data(id, duration=duration)
    bot.set_state(id, states.if_subscr_laser)

    bot.send_message(
        message.chat.id,
        "Выбери вид посещения (либо введи вручную свой доход)",
        reply_markup=if_subscr_laser(),
    )


@bot.message_handler(state=states.duration, is_positive_digit=False)
def proc_duration_handler_wrong_value(message: Message):
    bot.send_message(message.chat.id, "Вводи только цифры больше нyля!")
