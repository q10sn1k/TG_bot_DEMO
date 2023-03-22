from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, state
from aiogram.types import Message, CallbackQuery
from app.keyboards.todo_keyboard import TodoKeyboard
from app.database import Session, engine
from app.models import TodoTask, Base
from app.utils import create_todo_list
from app.states import TodoHandler
from aiogram.dispatcher.filters.state import State, StatesGroup


class TodoHandler(StatesGroup):
    todo = State()
    add_task_name = State()

    @staticmethod
    async def start_handler(message: Message):
        # Создаем таблицу в базе данных, если ее нет
        Base.metadata.create_all(bind=engine)

        # Создаем клавиатуру для списка задач
        keyboard = TodoKeyboard().get_keyboard()

        # Отображаем список задач
        session = Session(bind=engine)
        tasks = session.query(TodoTask).all()
        todo_list = create_todo_list(tasks)
        await message.answer(todo_list, reply_markup=keyboard)

        # Переходим на обработку команды todo
        await state.update_data(prev_state=None)
        await TodoHandler.todo.set()


    @staticmethod
    async def add_task_handler(callback_query: CallbackQuery):
        await callback_query.message.answer('Введите название задачи')

        # Переходим на обработку ввода названия задачи
        await TodoHandler.add_task_name.set()

    @classmethod
    async def save_task_name(cls, message: Message, state: FSMContext):
        task_name = message.text

        session = Session(bind=engine)
        task = TodoTask(title=task_name)
        session.add(task)
        session.commit()

        tasks = session.query(TodoTask).all()
        todo_list = create_todo_list(tasks)
        keyboard = TodoKeyboard().get_keyboard()
        await message.answer(todo_list, reply_markup=keyboard)

        await state.finish()

    @staticmethod
    async def clear_tasks_handler(callback_query: CallbackQuery):
        session = Session(bind=engine)
        session.query(TodoTask).delete()
        session.commit()

        await callback_query.message.answer('Список задач очищен')

    @staticmethod
    async def cancel_handler(message: Message, state: FSMContext):
        await state.finish()

        # Создаем клавиатуру для списка задач
        keyboard = TodoKeyboard().get_keyboard()

        # Отображаем список задач
        session = Session(bind=engine)
        tasks = session.query(TodoTask).all()
        todo_list = create_todo_list(tasks)
        await message.answer(todo_list, reply_markup=keyboard)

        # Переходим на обработку команды todo
        await TodoHandler.todo.set()


def setup_todo_handler(dp):
    dp.register_message_handler(TodoHandler.start_handler, Command('start'), state='*')
    dp.register_callback_query_handler(TodoHandler.add_task_handler,
                                       lambda callback_query: callback_query.data == 'todo_add')
    dp.register_message_handler(TodoHandler.save_task_name, state=TodoHandler.add_task_name)
    dp.register_callback_query_handler(TodoHandler.clear_tasks_handler,
                                       lambda callback_query: callback_query.data == 'todo_clear')
    dp.register_message_handler(TodoHandler.cancel_handler, state=TodoHandler.add_task_name)
