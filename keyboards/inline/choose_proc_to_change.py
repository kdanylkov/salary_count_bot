from data.objects import Visit
from data.types import TreatemtTypes
from exceptions.keyboards import UnknownAction

from telebot.util import quick_markup


def choose_proc(visit: Visit, action: str):
    if action not in ['del', 'add', 'chg']:
        raise UnknownAction(
            f'Unknown action in inline keyboard "choose_proc": {action}'
        )

    return quick_markup(
        {
            f'{TreatemtTypes[p.type].value} ({p.earning})':
            {'callback_data': f'choose_proc:{p.db_id}{action}'}
            for p in visit.procedures
        },
        row_width=1
    )
