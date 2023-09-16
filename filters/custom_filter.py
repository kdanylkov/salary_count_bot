from telebot.custom_filters import SimpleCustomFilter
from telebot.types import Message


class IsDigitFilter(SimpleCustomFilter):
    key = "is_positive_digit"

    def check(self, message: Message):
        try:
            value = int(message.text)
        except ValueError:
            return False

        return value > 0
