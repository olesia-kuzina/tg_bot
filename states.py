from aiogram.fsm.state import State, StatesGroup

class FSMForm(StatesGroup):
    enter_country = State()
    enter_city = State()
