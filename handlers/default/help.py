from loader import bot

from telebot.types import Message


@bot.message_handler(commands=["help"])
def handle_help(message: Message):
    message_to_user = """
Список команд:
    - /start: Запуск бота, приветственное сообщение.
    - /cancel: Отменить любую текущую операцию.
    - /show_date: Посмотреть информацию за конкретный день.
    - /report: Создать отчет за период (можно также скачать файл в формате .pdf)
    - /alarm: Включить/отключить напоминания о внесении новых записей.
    """
    bot.delete_state(message.from_user.id, message.chat.id)
    bot.send_message(message.chat.id, message_to_user)
