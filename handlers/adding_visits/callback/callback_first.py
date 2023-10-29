from loader import bot, states
from exceptions.handlers import UnknownCallbackError
from keyboards.inline.subcription import if_subscription

from telebot.types import CallbackQuery, Message


@bot.callback_query_handler(func=lambda c: c.data.startswith("first"))
def if_first_handler(call: CallbackQuery):
    id = call.message.chat.id
    bot.delete_message(id, call.message.id)

    if call.message:
        if call.data == "first_yes":
            first = True
        elif call.data == "first_no":
            first = False
        else:
            bot.send_message(id, "Ошибка! Обратись в службу поддержки.")
            raise UnknownCallbackError(call.data)

        bot.add_data(id, first=first)
        bot.set_state(id, states.if_subscr)
        bot.send_message(id, "Процедура по абонементу?", reply_markup=if_subscription())


@bot.message_handler(state=states.if_first, content_types=["text"])
def if_first_keyboard_input(message: Message):
    t = 'Нажми на одну из кнопок⬆️\
(или выбери пункт меню "Отменить текущую операцию")'
    bot.send_message(message.chat.id, t)
