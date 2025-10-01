from aiogram.fsm.state import State, StatesGroup


class MainSG(StatesGroup):
    main = State()                     # Главное меню
    tasks = State()                    # Просмотр задач
    enter_title = State()              # Ввод названия задачи
    enter_description = State()        # Ввод описания задачи
    select_category = State()          # Выбор категории
    choose_date = State()              # Выбор даты
    create = State()                   # Сохранение задачи
    edit_list = State()            # Меню редактирования списка задач
    edit_task = State()            # Меню редактирования конкретной задачи
