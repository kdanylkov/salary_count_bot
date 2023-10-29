from telebot.custom_filters import StateFilter

from filters.custom_filter import IsDigitFilter, IsDigitZeroAndAboveFilter


def set_filters(bot):
    bot.add_custom_filter(StateFilter(bot))
    bot.add_custom_filter(IsDigitFilter())
    bot.add_custom_filter(IsDigitZeroAndAboveFilter())
