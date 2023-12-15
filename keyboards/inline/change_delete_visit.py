from telebot.util import quick_markup


def edit_visit():
    return quick_markup(
        {
            "Удалить посещение": {"callback_data": "edit_visit:del_visit"},
            "Изменить время посещения": {"callback_data": "edit_visit:chg_visit_time"},
            "Изменить процедуру": {"callback_data": "edit_visit:chg_proc"},
            "Удалить процедуру": {"callback_data": "edit_visit:del_proc"},
            "Добавить процедуру": {"callback_data": "edit_visit:add_proc"},
            "Отмена": {"callback_data": "edit_visit:cancel"},
        },
        row_width=2,
    )
