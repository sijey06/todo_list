from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const

from states.main import MainSG

# Главное окно (меню)
main_window = Window(
    Const("Начальное меню с кнопками"),
    Button(Const("Список задач"), id="get_tasks",
           on_click=lambda c, b, m: m.switch_to(MainSG.tasks)),
    Button(Const("Новая задача"), id="create_task",
           on_click=lambda c, b, m: m.switch_to(MainSG.enter_title)),
    state=MainSG.main,
)
