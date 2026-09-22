from fastapi import APIRouter
from app.api.v1.auth import router as auth_router
from app.api.v1.dashboard import router as dashboard_router
from app.api.v1.academics import router as academics_router
from app.api.v1.students import router as students_router
from app.api.v1.people import router as people_router
from app.api.v1.attendance import router as attendance_router
from app.api.v1.learning import router as learning_router
from app.api.v1.finance import router as finance_router
from app.api.v1.communication import router as communication_router
from app.api.v1.reports import router as reports_router
from app.api.v1.campus import router as campus_router
router=APIRouter(prefix="/api/v1")
router.include_router(auth_router)
router.include_router(dashboard_router)
router.include_router(academics_router)
router.include_router(students_router)
router.include_router(people_router)
router.include_router(attendance_router)
router.include_router(learning_router)
router.include_router(finance_router)
router.include_router(communication_router)
router.include_router(reports_router)
router.include_router(campus_router)
@router.get("")
def root(): return {"name":"GAINT Academy","version":"v1"}
