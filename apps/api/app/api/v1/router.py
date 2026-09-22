from fastapi import APIRouter
from app.api.v1.auth import router as auth_router
from app.api.v1.dashboard import router as dashboard_router
router=APIRouter(prefix="/api/v1")
router.include_router(auth_router)
router.include_router(dashboard_router)
@router.get("")
def root(): return {"name":"GAINT Academy","version":"v1"}
