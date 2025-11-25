from aiogram.fsm.state import State,StatesGroup

class Payments(StatesGroup):
    payments = State()
    