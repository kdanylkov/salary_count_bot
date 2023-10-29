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


class IsDigitZeroAndAboveFilter(IsDigitFilter):
    key = "is_positive_and_zero_digit"

    def check(self, message: Message):
        try:
            value = int(message.text)
        except ValueError:
            return False

        return value >= 0
