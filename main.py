from handlers import bot
import logging


def main():
    logging.basicConfig(level=logging.INFO)
    bot.infinity_polling()


if __name__ == "__main__":
    main()
