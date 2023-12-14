from telebot.handler_backends import State, StatesGroup


class AddVisitStates(StatesGroup):
    choose_date = State()
    visit_time = State()
    choose_type = State()
    choose_gross = State()
    if_add_another = State()
    if_first = State()
    if_subscr = State()
    visits_in_subscr = State()
    prime_cost = State()
    if_subscr_laser = State()
    if_add_subscr = State()
    manual_input = State()
    if_one_more_visit = State()
    sub_gross = State()
    if_laser_new = State()
    if_bought_sub = State()


class ShowDateStates(StatesGroup):
    idle_hours = State()
    choose_date = State()
    choose_action = State()
    choose_visit = State()
    confirm_delete = State()
    if_change_delete_visit = State()
    choose_proc = State()


class PeriodReportStates(StatesGroup):
    get_start_date = State()
    get_end_date = State()
    get_full_report = State()


class AlarmStates(StatesGroup):
    alarm_action = State()


class ConversionStates(StatesGroup):
    choose_month = State()
