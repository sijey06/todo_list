from datetime import date
from typing import Any

import aiohttp
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import ManagedTextInput

from config.settings import API_URL
from handlers.view import fetch_task_by_id, fetch_tasks
from states.main import MainSG


async def update_task(session: aiohttp.ClientSession,
                      task_id, **fields_to_update):
    """Обновляет задачу с указанным ID через API."""
    patch_url = f"{API_URL}/tasks/{task_id}/"
    async with session.patch(patch_url, json=fields_to_update) as response:
        if response.status == 200:
            return True
        else:
            return False


async def delete_task(session: aiohttp.ClientSession, task_id):
    """Удаление задачи с заданым ID через API."""
    async with session.delete(f"{API_URL}/tasks/{task_id}/") as response:
        return response.status == 200


def switch_to_edit_task(c, b, m, task_id):
    """обработчик перехода к окну редактирования задачи."""
    data = {'task_id': task_id}
    m.switch_to(MainSG.edit_task, data=data)


async def task_selected(callback, select, manager: DialogManager, task_id):
    """обработчик выбора задачи для редактирования."""
    manager.current_context().dialog_data["task_id"] = task_id
    await manager.switch_to(MainSG.edit_task)


async def get_edit_list_data(dialog_manager: DialogManager, **kwargs):
    """Обработчик получения задачи для редактирования."""
    event = dialog_manager.event
    user = event.from_user if hasattr(event, 'from_user') else None
    if user is None or user.id is None:
        return {"tasks": []}
    async with aiohttp.ClientSession() as session:
        tasks = await fetch_tasks(session, telegram_user_id=user.id)
        formatted_tasks = [
            {
                "id": task["id"],
                "title": task["title"]
            }
            for task in tasks
        ]
    return {"tasks": formatted_tasks}


async def edit_task_getter(*args, **kwargs):
    """Обработчик редактирования задачи."""
    dialog_manager = kwargs.pop('dialog_manager', None)
    if dialog_manager is None:
        raise ValueError("Менеджер диалога не найден.")
    task_id = dialog_manager.current_context().dialog_data.get("task_id")
    if task_id:
        async with aiohttp.ClientSession() as session:
            task = await fetch_task_by_id(session, task_id)
            if task:
                return {"task": task}
    return {}


async def handle_edit_title(
        message: Message, widget: ManagedTextInput[str],
        manager: DialogManager, value: str):
    """Обработчик редактирования названия задачи."""
    task_id = manager.current_context().dialog_data.get("task_id")
    if not task_id:
        await message.answer(
            "Ошибка: невозможно определить задачу для редактирования.")
        return
    async with aiohttp.ClientSession() as session:
        success = await update_task(session, task_id, title=value)
        if success:
            await message.answer(
                f"Название задачи успешно изменено на '{value}'.")
        else:
            await message.answer("Ошибка при изменении названия задачи.")
    await manager.switch_to(MainSG.edit_task)


async def handle_edit_description(
        message: Message, widget: ManagedTextInput[str],
        manager: DialogManager, value: str):
    """Обработчик редактирования описания задачи."""
    task_id = manager.current_context().dialog_data.get("task_id")
    if not task_id:
        await message.answer(
            "Ошибка: невозможно определить задачу для редактирования.")
        return
    async with aiohttp.ClientSession() as session:
        success = await update_task(session, task_id, description=value)
        if success:
            await message.answer(
                f"Описание задачи успешно изменено на '{value}'.")
        else:
            await message.answer("Ошибка при изменении описания задачи.")
    await manager.switch_to(MainSG.edit_task)


async def handle_edit_date(
        callback, widget, manager: DialogManager, selected_date: date):
    """Обработчик редактирования даты задачи."""
    task_id = manager.current_context().dialog_data.get("task_id")
    if not task_id:
        await callback.message.answer(
            "Ошибка: невозможно определить задачу для редактирования.")
        return
    formatted_due_date = selected_date.strftime("%Y-%m-%dT%H:%M:%S+00:00")
    async with aiohttp.ClientSession() as session:
        success = await update_task(session, task_id,
                                    due_date=formatted_due_date)
        if success:
            await callback.message.answer("Дата задачи успешно изменена.")
        else:
            await callback.message.answer("Ошибка при изменении даты задачи.")
    await manager.switch_to(MainSG.edit_task)


async def delete_task_handler(callback_query: CallbackQuery, button: Any,
                              manager: DialogManager):
    """Обработчик удаления задачи."""
    task_id = manager.current_context().dialog_data.get("task_id")
    if task_id:
        async with aiohttp.ClientSession() as session:
            await delete_task(session, task_id)
            await callback_query.message.answer("Задача успешно удалена.")
            await manager.switch_to(MainSG.edit_list)
    else:
        await callback_query.answer(
            "Не удалось определить задачу для удаления.")
