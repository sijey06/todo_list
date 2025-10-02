from aiogram_dialog import Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Button, Calendar, Row, Select
from aiogram_dialog.widgets.text import Const, Format

from handlers.create import (category_chosen, get_categories,
                             handle_date_selection, handle_task_description,
                             handle_task_title, save_task_handler)
from states.main import MainSG

# Окно ввода названия задачи
create_window = Window(
    Const("🎯 Введите название задачи:"),
    TextInput(id="task_title", on_success=handle_task_title),
    Row(Button(Const("Отмена"), id="cancel_task",
               on_click=lambda c, b, m: m.switch_to(MainSG.main))),
    state=MainSG.enter_title,
)

# Окно ввода описания задачи
description_window = Window(
    Const("✍️ Введите описание задачи:"),
    TextInput(id="task_description",
              on_success=handle_task_description),
    Row(Button(Const("Отмена"), id="cancel_task",
               on_click=lambda c, b, m: m.switch_to(MainSG.main))),
    state=MainSG.enter_description,
)

# Окно выбора категории
select_category_window = Window(
    Const("Выберите категорию для задачи:"),
    Select(
        Format("{item[title]}"),
        items="categories",
        item_id_getter=lambda x: x["id"],
        on_click=category_chosen,
        id="cat_select"
    ),
    state=MainSG.select_category,
    getter=get_categories
)

# Окно выбора даты
choose_date_window = Window(
    Const("Выберите дату выполнения задачи:"),
    Calendar(id="task_deadline", on_click=handle_date_selection),
    state=MainSG.choose_date
)

# Окно сохранения задачи
finish_window = Window(
    Const("Сохранить новую задачу?"),
    Row(Button(Const("Сохранить"), id="save_task",
               on_click=save_task_handler)),
    Row(Button(Const("Отмена"), id="cancel_task",
               on_click=lambda c, b, m: m.switch_to(MainSG.main))),
    state=MainSG.create,
)
