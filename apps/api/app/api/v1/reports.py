from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy import func,select
from sqlalchemy.orm import Session
from app.core.auth import current_user,permission_codes
from app.db.session import get_db
from app.models.identity import User
from app.models.academics import Student,Enrollment
from app.models.people import Staff
from app.models.attendance import AttendanceRecord
from app.models.finance import Invoice
router=APIRouter(prefix="/reports",tags=["reports"])
def req(db,u):
 if "reports.summary.view" not in permission_codes(db,u):raise HTTPException(403,"Permission denied")
@router.get("/summary")
def summary(u:User=Depends(current_user),db:Session=Depends(get_db)):
 req(db,u);tid=u.tenant_id
 students=db.scalar(select(func.count()).select_from(Student).where(Student.tenant_id==tid)) or 0
 staff=db.scalar(select(func.count()).select_from(Staff).where(Staff.tenant_id==tid)) or 0
 enrollments=db.scalar(select(func.count()).select_from(Enrollment).where(Enrollment.tenant_id==tid,Enrollment.status=="ACTIVE")) or 0
 absent=db.scalar(select(func.count()).select_from(AttendanceRecord).where(AttendanceRecord.tenant_id==tid,AttendanceRecord.status=="ABSENT")) or 0
 billed=db.scalar(select(func.coalesce(func.sum(Invoice.amount),0)).where(Invoice.tenant_id==tid))
 paid=db.scalar(select(func.coalesce(func.sum(Invoice.paid_amount),0)).where(Invoice.tenant_id==tid))
 return {"data":{"students":students,"staff":staff,"active_enrollments":enrollments,"absence_records":absent,"finance":{"billed":str(billed),"paid":str(paid),"outstanding":str(billed-paid)}}}
