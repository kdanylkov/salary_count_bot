from json import dumps
from telebot.util import quick_markup

from data.objects import Workday


def choose_visit(workday: Workday):
    pref = "choose_visit"
    return quick_markup(
        {
            f"{v.visit_time} ({v.get_total()})": {
                "callback_data": dumps({pref: f"{v.db_id}"})
            }
            for v in workday.visits
        },
        row_width=2,
    )
