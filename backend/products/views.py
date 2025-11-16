from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from products.schema import Product
import random
from pydantic import BaseModel, Field

router = APIRouter(prefix="/products", tags=["products"])


@router.get("/")
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


class ProductCreate(BaseModel):
    category: str = Field(..., min_length=1)
    product: str = Field(..., min_length=1)
    price: float = Field(..., gt=0)


@router.post("/")
def create_product(payload: ProductCreate, db: Session = Depends(get_db)):
    new_product = Product(
        category=payload.category,
        product=payload.product,
        price=payload.price,
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


@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(product)
    db.commit()

    return {"status": "deleted", "id": product_id}

