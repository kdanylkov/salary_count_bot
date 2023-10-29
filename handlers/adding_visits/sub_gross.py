from loader import bot, states
from data.objects import Visit, Laser
from keyboards.inline.subcr_laser import if_another_subscr

from telebot.types import Message


@bot.message_handler(state=states.sub_gross, is_positive_digit=True)
def sub_gross_handler(message: Message):
    id = message.chat.id
    sub_gross = int(message.text)

    data = bot.retrieve_data(id).data

    visit: Visit = data["visit"]

    visit.procedures.add_laser_sub(sub_gross)

    bot.add_data(id, visit=visit)

    bot.set_state(id, states.if_add_subscr)
    bot.send_message(id, "Добавить еще абонемент?", reply_markup=if_another_subscr())


@bot.message_handler(state=states.sub_gross, is_positive_digit=False)
def sub_gross_handler_incorrect(message: Message):
    bot.send_message(message.chat.id, "Нужно ввести число больше нуля.")
