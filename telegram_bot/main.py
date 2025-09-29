import asyncio

from aiogram import Bot, Dispatcher
from aiogram.filters.command import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram_dialog import Dialog, setup_dialogs

from config.settings import TELEGRAM_TOKEN
from handlers.main import start_command
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

    try:
        await dp.start_polling(bot,
                               allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
