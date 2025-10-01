import asyncio

import aiohttp
from aiogram import Bot, Dispatcher
from aiogram.filters.command import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram_dialog import Dialog, setup_dialogs
from redis.asyncio import Redis

from config.settings import TELEGRAM_TOKEN
from handlers.main import start_command
from handlers.view import fetch_tasks
from windows.create import (choose_date_window, create_window,
                            description_window, finish_window,
                            select_category_window)
from windows.main import main_window
from windows.view import tasks_window


async def main():
    """Запуск бота."""
    bot = Bot(TELEGRAM_TOKEN)
    storage = MemoryStorage()
    dialog = Dialog(main_window, tasks_window, create_window,
                    description_window, select_category_window,
                    choose_date_window, finish_window)

    dp = Dispatcher(storage=storage)
    dp.include_router(dialog)
    setup_dialogs(dp)

    dp.message.register(start_command, Command('start'))
    redis_client = Redis(host="redis", port=6379, decode_responses=True)
    task = asyncio.create_task(process_redis_messages(bot, redis_client))

    try:
        await dp.start_polling(bot,
                               allowed_updates=dp.resolve_used_update_types())
    finally:
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass
        await redis_client.close()
        await bot.session.close()


async def process_redis_messages(bot: Bot, redis_client: Redis):
    """Напоминание о задаче."""
    while True:
        keys = await redis_client.keys(":1:reminder_*")
        for key in keys:
            raw_value = await redis_client.get(key)
            parts = key.split("_")[2:]
            task_id = parts[0]
            user_id = int(raw_value.strip('"'))
            async with aiohttp.ClientSession() as session:
                tasks = await fetch_tasks(session)
            task = next(
                (item for item in tasks if item['id'] == task_id), None)
            if task:
                task_title = task.get('title', 'Без названия')
                await bot.send_message(user_id,
                                       f"Пора выполнить задачу: {task_title}")
            await bot.send_message(user_id, "Не выполнено")
            await redis_client.delete(key)
        await asyncio.sleep(5)


if __name__ == "__main__":
    asyncio.run(main())
