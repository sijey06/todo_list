from datetime import date

import aiohttp
from aiogram.types import Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import ManagedTextInput

from config.settings import API_URL


async def handle_task_title(
        message: Message, widget: ManagedTextInput[str],
        manager: DialogManager, value: str):
    """Обработчик ввода названия задачи."""
    manager.current_context().dialog_data["task_title"] = value
    await manager.next()


async def handle_task_description(
        message: Message, widget: ManagedTextInput[str],
        manager: DialogManager, value: str):
    """Обработчик ввода описания задачи."""
    manager.current_context().dialog_data["task_description"] = value
    await manager.next()


async def fetch_categories():
    """Загрузка доступных категорий задач из RestAPI."""
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_URL}/categories") as response:
            return await response.json()


async def get_categories(dialog_manager: DialogManager, **kwargs):
    """Возвращение списка категорий задач."""
    categories = await fetch_categories()
    return {"categories": categories}


async def category_chosen(callback, select, manager: DialogManager, item_id):
    """Обработчик выбора категории для задачи."""
    categories = await fetch_categories()
    selected_category = next(
        (cat for cat in categories if cat["id"] == item_id), None)
    if selected_category:
        manager.current_context().dialog_data["selected_category"] = item_id
        manager.current_context().dialog_data[
            "selected_category_title"] = selected_category["title"]
    else:
        await callback.message.answer("Категория не найдена!")
        return
    await manager.next()


async def handle_date_selection(
        callback, widget, manager: DialogManager, selected_date: date):
    """Обработчик выбора даты выполнения задачи."""
    manager.current_context().dialog_data[
        "chosen_date"] = selected_date.isoformat()
    await manager.next()


async def save_task_handler(callback, button, manager: DialogManager):
    """Обработчик сохранения задачи."""
    task_title = manager.current_context().dialog_data.get("task_title")
    task_description = manager.current_context().dialog_data.get(
        "task_description")
    chosen_date = manager.current_context().dialog_data.get("chosen_date")
    selected_category_id = manager.current_context().dialog_data.get(
        "selected_category")
    selected_category_title = manager.current_context().dialog_data.get(
        "selected_category_title")
    telegram_user_id = callback.from_user.id
    async with aiohttp.ClientSession() as session:
        payload = {
            "telegram_user_id": telegram_user_id,
            "title": task_title,
            "description": task_description,
            "category": [selected_category_id],
            "due_date": chosen_date
        }
        async with session.post(f"{API_URL}/tasks/", json=payload) as resp:
            if resp.status == 201:
                message = f"""
📌 Задача успешно создана:
⚡️ Название: {task_title}
✅ Описание: {task_description}
🔖 Категория: {selected_category_title}
📆 Срок выполнения: {chosen_date}
"""
                await callback.message.answer(message)
            else:
                await callback.message.answer(
                    "❗ Произошла ошибка при создании задачи.")
