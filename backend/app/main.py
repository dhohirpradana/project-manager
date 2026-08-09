from fastapi import FastAPI
from sqlalchemy import text
from app.core.database import engine
from app.api.v1 import api_router

app = FastAPI(title="Project & Task Management API", version="1.0.0")

app.include_router(api_router)


@app.get("/health", tags=["system"])
def health():
    return {"status": "ok"}


@app.get("/ready", tags=["system"])
def ready():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "ready", "database": "up"}
    except Exception:
        return {"status": "not_ready", "database": "down"}