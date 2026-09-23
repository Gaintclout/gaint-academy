from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy import func,select
from sqlalchemy.orm import Session
from app.core.auth import current_user,permission_codes,has_role,linked_student_ids,scoped_student_id,teacher_section_ids
from app.db.session import get_db
from app.models.identity import User,AuditEvent
from app.models.academics import Student,Enrollment
from app.models.people import Staff
from app.models.attendance import AttendanceRecord,AttendanceSession
from app.models.finance import Invoice
router=APIRouter(prefix="/reports",tags=["reports"])
def req(db,u):
 if "reports.summary.view" not in permission_codes(db,u):raise HTTPException(403,"Permission denied")
@router.get("/summary")
def summary(u:User=Depends(current_user),db:Session=Depends(get_db)):
 req(db,u);tid=u.tenant_id
 if has_role(db,u,"PARENT"):
  ids=linked_student_ids(db,u)
  students=len(ids);staff=0
  enrollments=0 if not ids else db.scalar(select(func.count()).select_from(Enrollment).where(Enrollment.tenant_id==tid,Enrollment.student_id.in_(ids),Enrollment.status=="ACTIVE")) or 0
  absent=0 if not ids else db.scalar(select(func.count()).select_from(AttendanceRecord).join(AttendanceSession,AttendanceSession.id==AttendanceRecord.session_id).where(AttendanceRecord.tenant_id==tid,AttendanceRecord.student_id.in_(ids),AttendanceRecord.status=="ABSENT",AttendanceSession.tenant_id==tid,AttendanceSession.status=="SUBMITTED")) or 0
  billed=0 if not ids else db.scalar(select(func.coalesce(func.sum(Invoice.amount),0)).where(Invoice.tenant_id==tid,Invoice.student_id.in_(ids)))
  paid=0 if not ids else db.scalar(select(func.coalesce(func.sum(Invoice.paid_amount),0)).where(Invoice.tenant_id==tid,Invoice.student_id.in_(ids)))
 elif has_role(db,u,"STUDENT"):
  own=scoped_student_id(db,u); ids=set() if not own else {own}
  students=len(ids);staff=0
  enrollments=0 if not ids else db.scalar(select(func.count()).select_from(Enrollment).where(Enrollment.tenant_id==tid,Enrollment.student_id.in_(ids),Enrollment.status=="ACTIVE")) or 0
  absent=0 if not ids else db.scalar(select(func.count()).select_from(AttendanceRecord).join(AttendanceSession,AttendanceSession.id==AttendanceRecord.session_id).where(AttendanceRecord.tenant_id==tid,AttendanceRecord.student_id.in_(ids),AttendanceRecord.status=="ABSENT",AttendanceSession.tenant_id==tid,AttendanceSession.status=="SUBMITTED")) or 0
  billed=0 if not ids else db.scalar(select(func.coalesce(func.sum(Invoice.amount),0)).where(Invoice.tenant_id==tid,Invoice.student_id.in_(ids)))
  paid=0 if not ids else db.scalar(select(func.coalesce(func.sum(Invoice.paid_amount),0)).where(Invoice.tenant_id==tid,Invoice.student_id.in_(ids)))
 elif has_role(db,u,"TEACHER"):
  sections=teacher_section_ids(db,u)
  students=0 if not sections else db.scalar(select(func.count(func.distinct(Enrollment.student_id))).where(Enrollment.tenant_id==tid,Enrollment.section_id.in_(sections),Enrollment.status=="ACTIVE")) or 0
  staff=1;enrollments=students
  absent=0 if not sections else db.scalar(select(func.count()).select_from(AttendanceRecord).join(AttendanceSession,AttendanceSession.id==AttendanceRecord.session_id).where(AttendanceRecord.tenant_id==tid,AttendanceRecord.status=="ABSENT",AttendanceSession.tenant_id==tid,AttendanceSession.section_id.in_(sections),AttendanceSession.status=="SUBMITTED")) or 0
  billed=0;paid=0
 else:
  students=db.scalar(select(func.count()).select_from(Student).where(Student.tenant_id==tid)) or 0
  staff=db.scalar(select(func.count()).select_from(Staff).where(Staff.tenant_id==tid)) or 0
  enrollments=db.scalar(select(func.count()).select_from(Enrollment).where(Enrollment.tenant_id==tid,Enrollment.status=="ACTIVE")) or 0
  absent=db.scalar(select(func.count()).select_from(AttendanceRecord).where(AttendanceRecord.tenant_id==tid,AttendanceRecord.status=="ABSENT")) or 0
  billed=db.scalar(select(func.coalesce(func.sum(Invoice.amount),0)).where(Invoice.tenant_id==tid))
  paid=db.scalar(select(func.coalesce(func.sum(Invoice.paid_amount),0)).where(Invoice.tenant_id==tid))
 return {"data":{"students":students,"staff":staff,"active_enrollments":enrollments,"absence_records":absent,"finance":{"billed":str(billed),"paid":str(paid),"outstanding":str(billed-paid)}}}


@router.get("/audit-events")
def audit_events(limit:int=100,u:User=Depends(current_user),db:Session=Depends(get_db)):
 if "audit.event.view" not in permission_codes(db,u):raise HTTPException(403,"Permission denied")
 limit=max(1,min(limit,200))
 rows=db.scalars(select(AuditEvent).where(AuditEvent.tenant_id==u.tenant_id).order_by(AuditEvent.created_at.desc()).limit(limit)).all()
 return {"data":[{"id":str(x.id),"action":x.action,"resource_type":x.resource_type,"resource_id":x.resource_id,"user_id":None if not x.user_id else str(x.user_id),"request_id":x.request_id,"created_at":x.created_at.isoformat()} for x in rows]}
