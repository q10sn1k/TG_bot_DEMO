from aiogram.dispatcher.filters.state import State, StatesGroup


def state_factory(cls):
    """Декоратор, добавляющий к классу заданные State'ы."""
    attributes = {attribute_name: State() for attribute_name in dir(cls) if attribute_name.endswith('_state')}
    new_cls = type(cls.__name__, (cls, StatesGroup), attributes)
    new_cls.__qualname__ = cls.__qualname__
    new_cls.__module__ = cls.__module__
    return new_cls


class TodoHandler(StatesGroup):
    todo = State()
    add_task_name = State()
