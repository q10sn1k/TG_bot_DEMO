from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

# Создаем базовый класс для всех моделей
Base = declarative_base()


# Описываем модель для хранения задач
class TodoTask(Base):
    __tablename__ = 'todo_tasks'

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
