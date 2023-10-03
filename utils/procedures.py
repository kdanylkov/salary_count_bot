from loader import bot, states, show_date_states
from exceptions.objects import ProcedureNotDeleted
from keyboards.inline.add_another import if_add_another
from keyboards.inline.choose_date_action import choose_action
from data.objects import Visit
from database.actions.procedures import (delete_procedure_from_db,
                                         create_procedure_in_db)
from utils.visit import clean_state
from database.actions.workday import get_workday_with_visits_from_db


def add_procedure(id):
    with bot.retrieve_data(id) as data:
        visit: Visit = data.get('visit')
        visit.procedures.add(**data)
        data["visit"] = visit

        edit_visit = data.get('edit_visit')
        for_deletion = data.get('for_deletion')

    if edit_visit:
        edit_proc_in_visit(id, visit, for_deletion)
    else:
        bot.set_state(id, states.if_add_another)
        bot.send_message(id, "Добавить еще процедуру?",
                         reply_markup=if_add_another())


def delete_procedure(chat_id: int | str, proc_id: int):
    with bot.retrieve_data(chat_id) as data:
        visit = data.get('visit')
        workday = data.get('workday')

    deleted_from_db = delete_procedure_from_db(proc_id)
    deleted_from_obj = visit.delete_procedure(proc_id)

    if not deleted_from_db and not deleted_from_obj:
        raise ProcedureNotDeleted(deleted_from_db, deleted_from_obj)

    workday.update_visit(visit)
    bot.add_data(chat_id, workday=workday, visit=visit)


def edit_proc_in_visit(id, visit: Visit, for_deletion) -> None:
    proc_to_add = visit.procedures.last()

    if for_deletion:
        try:
            delete_procedure(id, for_deletion.db_id)
        except ProcedureNotDeleted:
            raise

    create_procedure_in_db(visit.db_id, proc_to_add.to_dict())

    workday = get_workday_with_visits_from_db(id, visit.date)
    visit = workday.get_visit_by_id(visit.db_id)

    bot.add_data(id, workday=workday, visit=visit)

    text = 'Посещение успешно изменено.\n' + workday.workday_report()
    bot.send_message(id, text, reply_markup=choose_action(workday.visits))
    bot.set_state(id, show_date_states.choose_action)

    clean_state(bot, id)
