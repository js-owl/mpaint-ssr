from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import init_db
from products.views import router
from products.schema import Product  # Import to register model with Base.metadata
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

app.include_router(router)
