from loader import bot, states
from keyboards.inline.add_another import if_add_another

from telebot.types import CallbackQuery, Message


@bot.callback_query_handler(func=lambda c: c.data.startswith("plus_subscr"))
def if_add_another_subscr_callback(call: CallbackQuery):
    if call.message:
        id = call.message.chat.id
        bot.delete_message(id, call.message.id)

        if call.data.endswith("yes"):
            bot.set_state(id, states.sub_gross)
            bot.send_message(id, "Введи стоимость абонимента")
        elif call.data.endswith("no"):
            bot.set_state(id, states.if_add_another)
            bot.send_message(
                id, "Добавить еще процедуру?", reply_markup=if_add_another()
            )


@bot.message_handler(state=states.if_add_subscr)
def if_add_another_subscr_keyboard_input(message: Message):
    t = 'Нажми на одну из кнопок⬆️\
(или выбери пункт меню "Отменить текущую операцию")'
    bot.send_message(message.chat.id, t)
