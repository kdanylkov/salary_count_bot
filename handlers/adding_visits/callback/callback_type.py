from loader import bot
from data.types import TreatemtTypes, TYPES_LIST
from loader import states
from keyboards.inline.first_proc import if_first
from keyboards.inline.subcr_laser import if_subscr_laser

from telebot.types import CallbackQuery, Message
from telebot.util import quick_markup


@bot.callback_query_handler(func=lambda c: c.data in TYPES_LIST)
def type_callback(call: CallbackQuery):
    mes = call.message

    try:
        type_chosen = TreatemtTypes[call.data]
    except KeyError as err:
        warning_text = "Что-то пошло не так... Обратись в службу поддержки!"
        bot.send_message(mes.chat.id, warning_text)

        print(
            "Critical Error! Callback data from type choice \
                doesn't correspond to any treatment type!"
        )
        print(f"Error message: {err}")
    else:
        bot.answer_callback_query(call.id, f"Ты выбрала: {type_chosen.value}")
        bot.add_data(mes.chat.id, type=type_chosen.name)

        _proceed_to_next_step_from_type(type_chosen, call.message.chat.id)
    finally:
        bot.delete_message(mes.chat.id, call.message.message_id)


@bot.message_handler(state=states.choose_type, content_types=["text"])
def type_choice_keyboard_input(message: Message):
    text = "Нужно нажать одну из кнопок!⬆️"
    bot.send_message(message.chat.id, text=text)


def _proceed_to_next_step_from_type(type: TreatemtTypes, id: str | int):
    state = None
    match type.name:
        case "CLASSIC_COSMETOLOGY" | "COSMETICS":
            state = states.choose_gross
            bot.send_message(id, "Сколько заплатил клиент?")
        case "ROLLER_MASSAGE" | "APPARATUS_COSMETOLOGY":
            state = states.if_first
            bot.send_message(id, "Это первая процедура?",
                             reply_markup=if_first())
        case "INJECTIONS":
            state = states.prime_cost
            bot.send_message(id, "Введи себестоимость материалов")
        case "LASER":
            from data.objects import Visit
            visit: Visit = bot.retrieve_data(id).data.get('visit')
            if visit.laser_conversion_status == 'UNKNOWN':
                state = states.if_laser_new
                bot.send_message(id, 'Это новый клиент?',
                                 reply_markup=_if_new_client_markup())
            else:
                state = states.if_subscr_laser
                bot.send_message(
                    id,
                    "Выбери вид посещения (либо введи вручную свой доход)",
                    reply_markup=if_subscr_laser(),
                )

    bot.set_state(id, state)


def _if_new_client_markup():
    return quick_markup(
        {
            'Да': {'callback_data': 'laser_new_client_yes'},
            'Нет': {'callback_data': 'laser_new_client_no'},
        },
        row_width=2
    )
