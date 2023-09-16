from loader import bot, states
from keyboards.inline.add_another import if_add_another
from data.objects import Visit


def add_procedure(id):
    with bot.retrieve_data(id) as data:
        visit: Visit = data["visit"]
        visit.procedures.add(**data)
        data["visit"] = visit

    bot.set_state(id, states.if_add_another)
    bot.send_message(id, "Добавить еще процедуру?", reply_markup=if_add_another())
