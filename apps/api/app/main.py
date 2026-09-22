from fastapi import FastAPI
from app.core.config import settings

app = FastAPI(title=settings.app_name, version="0.1.0")

@app.get("/health/live", tags=["health"])
def live():
    return {"status": "ok", "service": "api"}

@app.get("/health/ready", tags=["health"])
def ready():
    return {"status": "ready", "service": "api"}

@app.get("/api/v1", tags=["root"])
def api_root():
    return {"name": settings.app_name, "version": "v1", "environment": settings.app_env}
