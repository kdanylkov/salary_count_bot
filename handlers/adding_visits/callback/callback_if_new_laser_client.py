from loader import bot, states
from keyboards.inline.subcr_laser import if_subscr_laser
from exceptions.handlers import UnknownCallbackError

from telebot.types import Message, CallbackQuery
from telebot.util import quick_markup


@bot.callback_query_handler(func=lambda c: c.data.startswith('laser_new_client'))
def callback_if_new_laser_client(call: CallbackQuery):
    id = call.message.chat.id
    bot.delete_message(id, call.message.id)

    state = None
    if call.data.endswith('no'):
        from data.objects import Visit
        visit: Visit = bot.retrieve_data(id).data.get('visit')
        visit.laser_conversion_status = 'NOT_NEW'
        bot.add_data(id, visit=visit)

        state = states.if_subscr_laser
        bot.send_message(
            id,
            "Выбери вид посещения (либо введи вручную свой доход)",
            reply_markup=if_subscr_laser(),
        )
    elif call.data.endswith('yes'):
        state = states.if_bought_sub
        bot.send_message(id, 'Клиент купил абонемент?',
                         reply_markup=_if_bought_sub_markup())
    else:
        raise UnknownCallbackError(call.data)

    bot.set_state(id, state)


def _if_bought_sub_markup():
    return quick_markup(
            {
                'Да': {'callback_data': 'if_bought_sub_yes'},
                'Нет': {'callback_data': 'if_bought_sub_no'},
                }
            )
