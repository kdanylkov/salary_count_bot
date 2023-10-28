from loader import bot, states
from keyboards.inline.subcr_laser import if_subscr_laser
from exceptions.handlers import UnknownCallbackError

from telebot.types import Message, CallbackQuery


@bot.callback_query_handler(func=lambda c: c.data.startswith('if_bought_sub'))
def callback_if_new_laser_client(call: CallbackQuery):
    id = call.message.chat.id
    bot.delete_message(id, call.message.id)

    value = None
    if call.data.endswith('no'):
        value = 'NEW_NOT_BOUGHT'
    elif call.data.endswith('yes'):
        value = 'NEW_BOUGHT'
    else:
        raise UnknownCallbackError(call.data)

    from data.objects import Visit
    visit: Visit = bot.retrieve_data(id).data.get('visit')
    visit.laser_conversion_status = value
    bot.add_data(id, visit=visit)

    bot.send_message(
        id,
        "Выбери вид посещения (либо введи вручную свой доход)",
        reply_markup=if_subscr_laser(),
    )
    bot.set_state(id, states.if_subscr_laser)
