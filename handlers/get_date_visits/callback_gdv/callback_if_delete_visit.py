from loader import bot
from database.actions.visit import delete_visit

from telebot.types import CallbackQuery


@bot.callback_query_handler(func=lambda c: c.data.startswith("if_delete_visit"))
def callback_if_delete_visit(call: CallbackQuery):
    id = call.message.chat.id
    bot.delete_message(id, call.message.id)
    if call.data.endswith("yes"):
        visit = bot.retrieve_data(id).data["workday_visit"]
        deleted = delete_visit(visit.db_id)

        if deleted:
            bot.send_message(id, "Посещение удалено!")
        else:
            bot.send_message(id, "Что-то пошло не так... Обратись в службу поддержки.")
    else:
        bot.send_message(id, "Операция отменена.")

    bot.delete_state(id)
