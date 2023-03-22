from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class TodoKeyboard:
    @staticmethod
    def get_keyboard() -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardMarkup()
        keyboard.add(
            InlineKeyboardButton('Добавить задачу', callback_data='todo_add'),
            InlineKeyboardButton('Очистить список', callback_data='todo_clear')
        )
        return keyboard
