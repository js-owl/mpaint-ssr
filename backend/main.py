from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


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
    return {"message": "Hello, world"}


@app.get("/api/health")
async def health_check():
    return {"status": "ok"}


