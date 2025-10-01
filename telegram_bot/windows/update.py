from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Button, Column, Row, Select
from aiogram_dialog.widgets.text import Const, Format

from handlers.update import edit_task_getter, get_edit_list_data, task_selected
from states.main import MainSG

# Окно редактирования списка задач
edit_list_window = Window(
    Const("Список задач для редактирования:"),
    Column(
        Select(
            Format("{item[title]}"),
            items="tasks",
            item_id_getter=lambda x: x["id"],
            on_click=task_selected,
            id="task_select"
        )),
    Row(Button(Const("Вернуться назад"), id="back",
               on_click=lambda c, b, m: m.switch_to(MainSG.tasks))),
    state=MainSG.edit_list,
    getter=get_edit_list_data
)

# Окно редактирования конкретной задачи
edit_task_window = Window(
    Format("""
🎯 Ваша задача:
📌 Название: {task[title]}
📝 Описание: {task[description]}
📅 Срок выполнения: {task[due_date]}
"""),
    Column(
        Button(Const("💬 Изменить название"), id="edit_title",
               on_click=lambda c, b, m: m.switch_to(MainSG.enter_title)),
        Button(Const("📋 Изменить описание"), id="edit_desc",
               on_click=lambda c, b, m: m.switch_to(MainSG.enter_description)),
        Button(Const("📅 Изменить срок выполнения"), id="edit_date",
               on_click=lambda c, b, m: m.switch_to(MainSG.choose_date)),
    ),
    Row(
        Button(Const("↩️ Вернуться в список"), id="back",
               on_click=lambda c, b, m: m.switch_to(MainSG.edit_list)),
    ),
    getter=edit_task_getter,
    state=MainSG.edit_task,
)
