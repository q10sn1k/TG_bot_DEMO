from typing import List

from app.models import TodoTask


# Функция для создания списка задач в виде строки
def create_todo_list(tasks: List[TodoTask]) -> str:
    if not tasks:
        return 'Список задач пуст'

    todo_list = 'Список задач:\n'
    for task in tasks:
        todo_list += f'{task.id}. {task.title}\n'

    return todo_list
