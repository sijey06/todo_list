from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Back, Button, Column
from aiogram_dialog.widgets.text import Const, Format

from handlers.view import get_data
from states.main import MainSG

# Окно просмотра задач
tasks_window = Window(
    Format("{tasks}"),
    Column(
        Button(Const("📋 Редактировать список"), id="edit_list",
               on_click=lambda c, b, m: m.switch_to(MainSG.edit_list)),
        Back(Const("↩️ Назад"))),
    getter=get_data,
    state=MainSG.tasks,
)
