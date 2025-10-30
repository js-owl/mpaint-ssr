from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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


@app.get("/")
async def read_root():
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
        item = {
            "id": i,
            "category": random.choice(categories),
            "product": random.choice(products),
            "price": round(random.uniform(5.0, 250.0), 2),
        }
        items.append(item)

    return items


