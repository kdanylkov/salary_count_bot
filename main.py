from threading import Thread
from handlers import bot
from services.scheduler import start_alarm_polling
import logging


def main():
    logging.basicConfig(level=logging.INFO)

    start_bot = Thread(target=bot.infinity_polling)
    start_scheduler = Thread(target=start_alarm_polling)

    start_bot.start()
    start_scheduler.start()


if __name__ == "__main__":
    main()
