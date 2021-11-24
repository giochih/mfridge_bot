from aiogram.dispatcher.filters.state import StatesGroup, State


class Curr (StatesGroup):
    ingrid = State()
    ingrid_confirm = State()
    date = State()
