import schedule
import time

from database.actions.user import get_users_ids_with_alarm_on


def send_alarm():
    from loader import bot
    ids: list[int] = get_users_ids_with_alarm_on()
    for id in ids:
        bot.send_message(id, 'Не забудь внести новые записи!')


def start_alarm_polling():
    print('WORKS')
    schedule.every().day.at("21:00", "Europe/Moscow").do(send_alarm)

    while True:
        schedule.run_pending()
        time.sleep(1)
