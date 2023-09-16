from telebot.custom_filters import StateFilter

from filters.custom_filter import IsDigitFilter


def set_filters(bot):
    bot.add_custom_filter(StateFilter(bot))
    bot.add_custom_filter(IsDigitFilter())
