from aiogram.filters.state import StatesGroup, State


class UserState(StatesGroup):
    menu = State()
    add_food = State()
    edit_food = State()


class AdminState(StatesGroup):
    are_you_sure = State()
    ask_ad_content = State()
