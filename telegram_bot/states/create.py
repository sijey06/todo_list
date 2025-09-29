from aiogram.fsm.state import State, StatesGroup


class CreateSG(StatesGroup):
    enter_title = State()            # Ввод названия задачи
    enter_description = State()      # Ввод описания задачи
    select_category = State()        # Окно выбора категории
    choose_date = State()            # Окно выбора даты
    create = State()                 # Окно сохранения задачи
