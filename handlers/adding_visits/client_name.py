from loader import bot, states
from data.objects import Visit

from telebot.types import Message
from keyboards.inline.treatment_types import types_keyboard


@bot.message_handler(state=states.client_name)
def client_name_handler(message: Message):
    id = message.chat.id
    print(bot.retrieve_data(id).data)

    with bot.retrieve_data(id) as data:
        data["visit"] = Visit(data["date"], message.text)

    bot.set_state(id, states.choose_type)
    bot.send_message(id, "Выбери тип процедуры", reply_markup=types_keyboard())
