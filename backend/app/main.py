from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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

@app.get("/")
async def root():
    return{
        "application": "NetMap",
        "status": "running",
        "version": "0.1.0"
    }

@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}