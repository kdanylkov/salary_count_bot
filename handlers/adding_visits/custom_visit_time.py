from keyboards.inline.treatment_types import types_keyboard
from loader import bot, states
from data.objects import Visit

from telebot.types import Message

from utils.visit import change_visit_time


@bot.message_handler(
    state=states.enter_custom_time, content_types=["text"], is_valid_time=True
)
def custom_time_handler(message: Message):
    id = message.chat.id
    time = message.text
    time = ':'.join([time[:2], time[2:]])
    bot.send_message(id, f'Ты выбрала время: {time}')

    visit_to_change_time_id = bot.retrieve_data(id).data.get('visit_to_change_time_id')
    if visit_to_change_time_id:
        change_visit_time(bot, id, visit_to_change_time_id, time)
    else:
        with bot.retrieve_data(id) as data:
            data["visit"] = Visit(data["date"], time)

        bot.set_state(id, states.choose_type)
        bot.send_message(id, "Выбери тип процедуры", reply_markup=types_keyboard())


@bot.message_handler(
    state=states.enter_custom_time, content_types=["text"], is_valid_time=False
)
def custom_time_handler_incorrect(message: Message):
    text = ("Время введено в неправильном формате (либо неправильный диапазон времени). \nПравильный формат: `ЧЧММ`, "
            "например: `1400`, или `0943`.\nДиапазон времени: 09:00 - 22:59")
    bot.send_message(message.chat.id, text)

