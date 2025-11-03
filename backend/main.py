from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import init_db, get_db, Product
import random
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: init DB only
    init_db()

    # Yield control to application
    yield

    # Shutdown: nothing to clean up


app = FastAPI(title="mpaint API", version="0.1.0", lifespan=lifespan)

# Allow CORS for local/dev usage; adjust origins for production as needed
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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


@app.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(product)
    db.commit()

    return {"status": "deleted", "id": product_id}
