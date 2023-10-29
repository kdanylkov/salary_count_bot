from loader import bot, states
from exceptions.handlers import UnknownCallbackError
from keyboards.inline.visits_in_sub import visits_markup

from telebot.types import CallbackQuery, Message


@bot.callback_query_handler(func=lambda c: c.data.startswith("subscription"))
def if_first_handler(call: CallbackQuery):
    id = call.message.chat.id
    bot.delete_message(id, call.message.id)

    if call.message:
        if call.data == "subscription_yes":
            sub = True
            bot.set_state(id, states.visits_in_subscr)
            bot.send_message(
                id, "Сколько посещений в абонементе?", reply_markup=visits_markup()
            )
        elif call.data == "subscription_no":
            sub = False
            bot.send_message(id, "Сколько клиент заплатил за процедуру?")
            bot.set_state(id, states.choose_gross)
        else:
            bot.send_message(id, "Ошибка! Обратись в службу поддержки.")
            raise UnknownCallbackError(call.data)

        bot.add_data(id, sub=sub)


@bot.message_handler(state=states.if_first, content_types=["text"])
def if_first_keyboard_input(message: Message):
    t = 'Нажми на одну из кнопок⬆️\
(или выбери пункт меню "Отменить текущую операцию")'
    bot.send_message(message.chat.id, t)
