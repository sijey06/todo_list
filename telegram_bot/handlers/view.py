from datetime import datetime

import aiohttp
from aiogram_dialog import DialogManager

from config.settings import API_URL


async def fetch_tasks(session, telegram_user_id=None):
    """Загрузка задач из RestAPI, фильтруя по telegram_user_id."""
    params = {}
    if telegram_user_id is not None:
        params["telegram_user_id"] = telegram_user_id
    async with session.get(f"{API_URL}/tasks", params=params) as response:
        return await response.json()


async def get_data(dialog_manager: DialogManager, **kwargs):
    """Получение и форматирование списка задач для пользователя."""
    event = dialog_manager.event
    telegram_user_id = getattr(event.from_user, 'id', None)
    if telegram_user_id is None:
        return {"tasks": []}
    async with aiohttp.ClientSession() as session:
        tasks = await fetch_tasks(session, telegram_user_id=telegram_user_id)
        formatted_list = await format_tasks(tasks)
        return {"tasks": formatted_list}


async def format_tasks(tasks):
    """Формирование строки списка задач."""
    if not tasks:
        return "Нет активных задач!"

    formatted_tasks = ["🎯 Список задач:"]
    for index, task in enumerate(tasks, start=1):
        created_at = datetime.fromisoformat(
            task['created_at']).strftime('%H:%M %d.%m.%Y')
        due_date = datetime.fromisoformat(
            task['due_date']).strftime('%H:%M %d.%m.%Y')
        formatted_task = (
            f"\n{index}. 📌 {task['title']}\n"
            f"📝 Описание: {task['description']}\n"
            f"🔖 Категория: {', '.join(cat[
                'title'] for cat in task['category']) or '-'} \n"
            f"📅 Дата создания: {created_at}\n"
            f"📆 Срок выполнения: {due_date}"
        )
        formatted_tasks.append(formatted_task)
    return '\n'.join(formatted_tasks)
