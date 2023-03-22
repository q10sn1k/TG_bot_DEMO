import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ParseMode
from aiogram.utils import executor

from app.config.settings import TOKEN
from app.handlers.todo_handler import setup_todo_handler

# Настраиваем логирование
logging.basicConfig(level=logging.INFO)

# Создаем бота и диспетчер
bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())

# Регистрируем обработчики команд
setup_todo_handler(dp)

# Запускаем бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
