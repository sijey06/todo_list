from aiogram_dialog import Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Button, Column, Row, Select, Calendar
from aiogram_dialog.widgets.text import Const, Format

from handlers.update import (delete_task_handler, edit_task_getter,
                             get_edit_list_data, task_selected,
                             handle_edit_title, handle_edit_date,
                             handle_edit_description)
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
🎯 Редактируемая задача:
📌 Название: {task[title]}
📝 Описание: {task[description]}
📅 Срок выполнения: {task[due_date]}
"""),
    Column(
        Button(Const("💬 Изменить название"), id="edit_title",
               on_click=lambda c, b, m: m.switch_to(MainSG.edit_title)),
        Button(Const("📋 Изменить описание"), id="edit_desc",
               on_click=lambda c, b, m: m.switch_to(MainSG.edit_description)),
        Button(Const("📅 Изменить срок выполнения"), id="edit_date",
               on_click=lambda c, b, m: m.switch_to(MainSG.edit_date)),
        Button(Const("❌ Удалить задачу"), id="delete_task",
               on_click=delete_task_handler),
    ),
    Row(
        Button(Const("↩️ Вернуться в список"), id="back",
               on_click=lambda c, b, m: m.switch_to(MainSG.edit_list)),
    ),
    getter=edit_task_getter,
    state=MainSG.edit_task,
)

# Окно редактирования названия задачи
edit_title_window = Window(
    Const("🎯 Введите новое название задачи:"),
    TextInput(id="task_title", on_success=handle_edit_title),
    Row(Button(Const("Отмена"), id="cancel_task",
               on_click=lambda c, b, m: m.switch_to(MainSG.edit_task))),
    state=MainSG.edit_title,
)

# Окно редактирования описания задачи
edit_description_window = Window(
    Const("✍️ Введите новое описание задачи:"),
    TextInput(id="task_description", on_success=handle_edit_description),
    Row(Button(Const("Отмена"), id="cancel_task",
               on_click=lambda c, b, m: m.switch_to(MainSG.edit_task))),
    state=MainSG.edit_description,
)

# Окно выбора новой даты выполнения задачи
edit_date_window = Window(
    Const("📅 Выберите новую дату выполнения задачи:"),
    Calendar(id="task_deadline", on_click=handle_edit_date),
    Row(Button(Const("Назад"), id="back",
               on_click=lambda c, b, m: m.switch_to(MainSG.edit_task))),
    state=MainSG.edit_date,
)
