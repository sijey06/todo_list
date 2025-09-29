from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const

from states.create import CreateSG
from states.main import MainSG
from states.view import ViewSG

# Главное окно (меню)
main_window = Window(
    Const("Начальное меню с кнопками"),
    Button(Const("Список задач"), id="get_tasks",
           on_click=lambda c, b, m: m.switch_to(ViewSG.tasks)),
    Button(Const("Новая задача"), id="create_task",
           on_click=lambda c, b, m: m.switch_to(CreateSG.enter_title)),
    state=MainSG.main,
)
