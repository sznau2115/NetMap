# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy import text
from pathlib import Path
from app.database import Base, engine, get_db
from app import models
from app.routers import floor, device

app = FastAPI(
    title="NetMap API",
    description="Network infrastructure visualization and monitoring",
    version="0.1.0"
)
UPLOAD_DIR = Path(__file__).resolve().parent.parent / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

app.mount(
    "/uploads",
    StaticFiles(directory=str(UPLOAD_DIR)),
    name="uploads"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Tworzenie tabel podczas uruchamiania aplikacji
Base.metadata.create_all(bind=engine)

app.include_router(floor.router)
app.include_router(device.router)

@app.get("/")
def root():
    return {
        "application": "NetMap",
        "status": "running",
        "version": "0.1.0"
    }


@app.get("/api/health")
def health_check():
    return {"status": "ok"}


@app.get("/api/database/health")
def database_health():
    db = next(get_db())

    try:
        db.execute(text("SELECT 1"))
        return {"database": "connected"}
    finally:
        db.close()