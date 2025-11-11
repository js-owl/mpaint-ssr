from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session, joinedload

from cart.schema import CartItem
from database import get_db
from products.schema import Product
from users.schema import User


router = APIRouter(prefix="/cart", tags=["cart"])


class CartItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(default=1, gt=0)


class CartItemUpdate(BaseModel):
    quantity: int = Field(gt=0)


def _ensure_user(db: Session, user_id: int) -> None:
    exists = db.query(User.id).filter(User.id == user_id).first()
    if exists is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


def _ensure_product(db: Session, product_id: int) -> Product:
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product


def _serialize_cart_item(cart_item: CartItem) -> dict:
    product = cart_item.product
    product_payload = None
    if product is not None:
        product_payload = {
            "id": product.id,
            "category": product.category,
            "product": product.product,
            "price": float(product.price),
        }

    return {
        "id": cart_item.id,
        "user_id": cart_item.user_id,
        "product_id": cart_item.product_id,
        "quantity": cart_item.quantity,
        "product": product_payload,
    }


@router.get("/{user_id}")
def get_cart(user_id: int, db: Session = Depends(get_db)):
    _ensure_user(db, user_id)
    items = (
        db.query(CartItem)
        .options(joinedload(CartItem.product))
        .filter(CartItem.user_id == user_id)
        .all()
    )
    return [_serialize_cart_item(item) for item in items]


@router.post("/{user_id}", status_code=status.HTTP_201_CREATED)
def add_to_cart(user_id: int, payload: CartItemCreate, db: Session = Depends(get_db)):
    _ensure_user(db, user_id)
    _ensure_product(db, payload.product_id)

    cart_item = (
        db.query(CartItem)
        .filter(
            CartItem.user_id == user_id,
            CartItem.product_id == payload.product_id,
        )
        .first()
    )

    if cart_item is None:
        cart_item = CartItem(
            user_id=user_id,
            product_id=payload.product_id,
            quantity=payload.quantity,
        )
        db.add(cart_item)
    else:
        cart_item.quantity += payload.quantity

    db.commit()
    db.refresh(cart_item)

    return _serialize_cart_item(cart_item)


@router.put("/{user_id}/{item_id}")
def update_cart_item(user_id: int, item_id: int, payload: CartItemUpdate, db: Session = Depends(get_db)):
    cart_item = (
        db.query(CartItem)
        .filter(
            CartItem.id == item_id,
            CartItem.user_id == user_id,
        )
        .first()
    )

    if cart_item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart item not found")

    cart_item.quantity = payload.quantity
    db.commit()
    db.refresh(cart_item)

    return _serialize_cart_item(cart_item)


@router.delete("/{user_id}/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_cart_item(user_id: int, item_id: int, db: Session = Depends(get_db)):
    cart_item = (
        db.query(CartItem)
        .filter(
            CartItem.id == item_id,
            CartItem.user_id == user_id,
        )
        .first()
    )

    if cart_item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart item not found")

    db.delete(cart_item)
    db.commit()

    return None

