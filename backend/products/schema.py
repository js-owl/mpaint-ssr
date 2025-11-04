from sqlalchemy import Column, Integer, String, Numeric
from database import Base

# Модель таблицы продуктов (соответствует структуре из main.py)
class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String, nullable=False)
    product = Column(String, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)

