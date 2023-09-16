from loader import bot, states
from exceptions.handlers import UnknownCallbackError

from telebot.types import Message, CallbackQuery


@bot.callback_query_handler(func=lambda c: c.data.startswith("visits_count"))
def visits_count_callback(call: CallbackQuery):
    id = call.message.chat.id
    bot.delete_message(id, call.message.id)
    if call.message:
        try:
            sub_visits = int(call.data[-1])
        except ValueError:
            raise UnknownCallbackError(call.data)

        if sub_visits not in range(1, 7):
            raise UnknownCallbackError(call.data)

        bot.add_data(id, sub_visits=sub_visits)
        bot.set_state(id, states.choose_gross)
        bot.send_message(id, "Сколько клиент заплатил за абонимент?")


@bot.message_handler(state=states.visits_in_subscr, content_types=["text"])
def visits_count_keyboard_input(message: Message):
    t = 'Нажми на одну из кнопок⬆️\
(или выбери пункт меню "Отменить текущую операцию")'
    bot.send_message(message.chat.id, t)
