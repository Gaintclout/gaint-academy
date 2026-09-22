from fastapi import FastAPI
from app.core.config import settings
from app.core.request_id import RequestIdMiddleware
from app.api.v1.router import router as v1_router

app=FastAPI(title=settings.app_name,version="0.1.0")
app.add_middleware(RequestIdMiddleware)
app.include_router(v1_router)

@app.get("/health/live",tags=["health"])
def live(): return {"status":"ok","service":"api"}
@app.get("/health/ready",tags=["health"])
def ready(): return {"status":"ready","service":"api"}
