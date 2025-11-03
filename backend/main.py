from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import init_db, get_db, Product
import random


app = FastAPI(title="mpaint API", version="0.1.0")

# Allow CORS for local/dev usage; adjust origins for production as needed
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_event():
    # Создаем таблицы при запуске приложения
    init_db()
    # Заполняем базу данных начальными данными, если она пуста
    db_gen = get_db()
    db = next(db_gen)
    try:
        count = db.query(Product).count()
        if count == 0:
            categories = [
                "Electronics",
                "Books",
                "Home",
                "Toys",
                "Clothing",
                "Sports",
                "Garden",
            ]

            products = [
                "Wireless Mouse",
                "USB-C Charger",
                "LED Desk Lamp",
                "Stainless Water Bottle",
                "Bluetooth Speaker",
                "Yoga Mat",
                "Novel Paperback",
                "Coffee Mug",
                "Backpack",
                "Board Game",
            ]

            items = []
            for i in range(1, 6):
                item = Product(
                    id=i,
                    category=random.choice(categories),
                    product=random.choice(products),
                    price=round(random.uniform(5.0, 250.0), 2),
                )
                items.append(item)

            db.add_all(items)
            db.commit()
    except Exception as e:
        db.rollback()
        print(f"Ошибка при инициализации базы данных: {e}")
    finally:
        db.close()


@app.get("/")
def read_root(db: Session = Depends(get_db)):
    # Получаем все продукты из базы данных
    products = db.query(Product).all()
    
    # Преобразуем в список словарей
    items = []
    for product in products:
        item = {
            "id": product.id,
            "category": product.category,
            "product": product.product,
            "price": float(product.price),
        }
        items.append(item)
    
    return items


@app.post("/")
def create_product(db: Session = Depends(get_db)):
    # Создаем и сохраняем случайный продукт
    categories = [
        "Electronics",
        "Books",
        "Home",
        "Toys",
        "Clothing",
        "Sports",
        "Garden",
    ]

    products = [
        "Wireless Mouse",
        "USB-C Charger",
        "LED Desk Lamp",
        "Stainless Water Bottle",
        "Bluetooth Speaker",
        "Yoga Mat",
        "Novel Paperback",
        "Coffee Mug",
        "Backpack",
        "Board Game",
    ]

    new_product = Product(
        category=random.choice(categories),
        product=random.choice(products),
        price=round(random.uniform(5.0, 250.0), 2),
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return {
        "id": new_product.id,
        "category": new_product.category,
        "product": new_product.product,
        "price": float(new_product.price),
    }

