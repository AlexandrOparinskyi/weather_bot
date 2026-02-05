from aiogram.fsm.state import StatesGroup, State


class StartState(StatesGroup):
    start = State()
    info_setting = State()
    skip_setting = State()


class SettingsState(StatesGroup):
    home = State()
    notification_setting = State()
    time_setting = State()
    time_day_setting = State()
    time_full_setting = State()
    location_setting = State()


class AdminState(StatesGroup):
    enter_message = State()
    confirm_message = State()
