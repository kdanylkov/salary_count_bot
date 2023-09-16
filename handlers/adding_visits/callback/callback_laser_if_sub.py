from loader import bot, states
from data.objects import Visit

from telebot.types import CallbackQuery, Message


@bot.callback_query_handler(func=lambda c: c.data.startswith("laser_sub"))
def callback_laser_if_sub(call: CallbackQuery):
    id = call.message.chat.id
    bot.delete_message(id, call.message.id)

    if call.message:
        if call.data.endswith("yes"):
            bot.set_state(id, states.sub_gross)
            bot.send_message(id, "Введи стоимость абонимента")

            with bot.retrieve_data(id) as data:
                visit: Visit = data["visit"]
                visit.procedures.add(**data)
                data["visit"] = visit

        elif call.data.endswith("no"):
            bot.set_state(id, states.choose_gross)
            bot.send_message(id, "Сколько заплатил клиент?")

        elif call.data.endswith("manual"):
            bot.add_data(id, manual_input=True)
            bot.set_state(id, states.manual_input)

            bot.send_message(id, "Введи свой заработок с процедуры")


@bot.message_handler(state=states.if_subscr, content_types=["text"])
def laser_if_subscr_keyboard_input(message: Message):
    t = 'Нажми на одну из кнопок⬆️\
(или выбери пункт меню "Отменить текущую операцию")'
    bot.send_message(message.chat.id, t)
