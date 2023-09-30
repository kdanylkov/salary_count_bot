from loader import bot, states
from exceptions.objects import ProcedureNotDeleted
from keyboards.inline.add_another import if_add_another
from data.objects import Visit
from database.actions.procedures import delete_procedure_from_db


def add_procedure(id):
    with bot.retrieve_data(id) as data:
        visit: Visit = data["visit"]
        visit.procedures.add(**data)
        data["visit"] = visit

    bot.set_state(id, states.if_add_another)
    bot.send_message(id, "Добавить еще процедуру?", reply_markup=if_add_another())


def delete_procedure(bot, chat_id: int | str, proc_id: int):
    with bot.retrieve_data(chat_id) as data:
        visit = data.get('workday_visit')
        workday = data.get('workday')

    deleted_from_db = delete_procedure_from_db(proc_id)
    deleted_from_obj = visit.delete_procedure(proc_id)

    if not deleted_from_db and not deleted_from_obj:
        raise ProcedureNotDeleted(deleted_from_db, deleted_from_obj)

    workday.update_visit(visit)
    bot.add_data(chat_id, workday=workday, workday_visit=visit)
