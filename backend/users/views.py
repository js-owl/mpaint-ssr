from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from users.schema import User
import random


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/")
def read_users(db: Session = Depends(get_db)):
    users = db.query(User).all()

    items = []
    for user in users:
        items.append(
            {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "role": user.role,
            }
        )

    return items


@router.post("/")
def create_user(db: Session = Depends(get_db)):
    names = [
        "Alice",
        "Bob",
        "Charlie",
        "Diana",
        "Eve",
        "Frank",
        "Grace",
        "Heidi",
        "Ivan",
        "Judy",
    ]

    domains = ["example.com", "test.com", "sample.org", "mail.net"]

    roles = [
        "admin",
        "editor",
        "viewer",
        "contributor",
        "manager",
    ]

    name = random.choice(names)
    email = f"{name.lower()}_{random.randint(1000, 9999)}@{random.choice(domains)}"

    new_user = User(
        name=name,
        email=email,
        role=random.choice(roles),
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "id": new_user.id,
        "name": new_user.name,
        "email": new_user.email,
        "role": new_user.role,
    }


@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()

    return {"status": "deleted", "id": user_id}


