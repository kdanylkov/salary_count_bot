from telebot.custom_filters import SimpleCustomFilter
from telebot.types import Message

import re


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


class IsValidTimeFilter(SimpleCustomFilter):
    key = "is_valid_time"

    def check(self, message: Message) -> bool:

        pattern = r"^(0[9-9]|1[0-9]|2[0-2])([0-5][0-9])$"
        match = re.match(pattern, message.text)
        return bool(match)

