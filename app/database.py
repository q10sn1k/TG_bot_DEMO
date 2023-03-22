from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config.settings import DATABASE_URL

# Создаем экземпляр класса Engine, который отвечает за установление соединения с БД
engine = create_engine(DATABASE_URL)

# Создаем фабрику сессий, которая будет использоваться для работы с БД
Session = sessionmaker(bind=engine)
