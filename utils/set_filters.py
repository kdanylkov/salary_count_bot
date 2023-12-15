from telebot.custom_filters import StateFilter

from filters.custom_filter import IsDigitFilter, IsDigitZeroAndAboveFilter, IsValidTimeFilter


def set_filters(bot):
    bot.add_custom_filter(StateFilter(bot))
    bot.add_custom_filter(IsDigitFilter())
    bot.add_custom_filter(IsDigitZeroAndAboveFilter())
    bot.add_custom_filter(IsValidTimeFilter())
