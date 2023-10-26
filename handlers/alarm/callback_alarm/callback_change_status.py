from loader import bot, alarm_states
from database.actions.user import switch_alarm_status
from utils.handler import cancel_action
from exceptions.handlers import UnknownCallbackError

from telebot.types import CallbackQuery, Message


@bot.callback_query_handler(func=lambda c: c.data.startswith('alarm'))
def callback_alarm_switch_status(call: CallbackQuery):
    if call.message:
        id = call.message.chat.id
        bot.delete_message(id, call.message.id)

        if call.data.endswith('switch'):
            try:
                alarm_on = int(call.data[-8])
            except ValueError:
                raise UnknownCallbackError(call.data)
            switch_alarm_status(id)
            alarm_status = 'отключены' if alarm_on else 'включены'
            text = f'Уведомления {alarm_status}.'
            bot.send_message(id, text)
        elif call.data.endswith('cancel'):
            cancel_action(id, bot)
        else:
            raise UnknownCallbackError(call.data)


@bot.message_handler(state=alarm_states.alarm_action)
def alarm_action_keyboard_input(message: Message):
    t = 'Нажми на одну из кнопок⬆️\
(или выбери пункт меню "Отменить текущую операцию")'
    bot.send_message(message.chat.id, t)
