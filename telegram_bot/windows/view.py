from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Back, Row
from aiogram_dialog.widgets.text import Const, Format

from handlers.view import get_data
from states.main import MainSG

# Окно просмотра задач
tasks_window = Window(
    Format("{tasks}"),
    Row(Back(Const("Назад"))),
    getter=get_data,
    state=MainSG.tasks,
)
