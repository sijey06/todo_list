from aiogram.fsm.state import State, StatesGroup


class ViewSG(StatesGroup):
    tasks = State()                  # Просмотр задач
