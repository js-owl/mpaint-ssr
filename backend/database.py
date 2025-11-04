from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Получаем URL базы данных из переменной окружения
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://mpaint_user:mpaint_pass@localhost:5432/mpaint_db"
)

# Создаем движок SQLAlchemy
engine = create_engine(DATABASE_URL, echo=False)

# Создаем фабрику сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для моделей
Base = declarative_base()


# Функция для создания таблиц
def init_db():
    Base.metadata.create_all(bind=engine)


# Функция для получения сессии БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

