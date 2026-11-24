from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.database import get_db, Base, engine
from app import models

app = FastAPI(
    title="NetMap API",
    description="API for NetMap application",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables
Base.metadata.create_all(bind=engine)


@app.get("/")
async def root():
    return {
        "application": "NetMap",
        "status": "running",
        "version": "0.1.0"
    }


@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}


@app.get("/api/database/health")
def database_health():
    db = next(get_db())

    try:
        db.execute(text("SELECT 1"))
        return {"database": "connected"}
    finally:
        db.close()