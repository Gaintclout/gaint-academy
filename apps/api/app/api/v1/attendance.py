from datetime import date,time
from uuid import UUID
from fastapi import APIRouter,Depends,HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.core.auth import current_user,permission_codes
from app.db.session import get_db
from app.models.identity import User
from app.models.academics import Section,Enrollment,Student
from app.models.attendance import TimetableSlot,AttendanceSession,AttendanceRecord
router=APIRouter(tags=["attendance"])
def require(db,u,c):
 if c not in permission_codes(db,u): raise HTTPException(403,"Permission denied")
class SlotIn(BaseModel): section_id:UUID;staff_id:UUID|None=None;subject_name:str;weekday:str;start_time:time;end_time:time
@router.post("/timetable",status_code=201)
def slot(p:SlotIn,u:User=Depends(current_user),db:Session=Depends(get_db)):
 require(db,u,"timetable.slot.manage");sec=db.scalar(select(Section).where(Section.id==p.section_id,Section.tenant_id==u.tenant_id))
 if not sec: raise HTTPException(404,"Section not found")
 x=TimetableSlot(tenant_id=u.tenant_id,**p.model_dump());db.add(x);db.commit();db.refresh(x);return {"data":{"id":str(x.id)}}
@router.get("/timetable")
def slots(section_id:UUID,u:User=Depends(current_user),db:Session=Depends(get_db)):
 require(db,u,"timetable.slot.view")
 rows=db.scalars(select(TimetableSlot).where(TimetableSlot.tenant_id==u.tenant_id,TimetableSlot.section_id==section_id)).all()
 return {"data":[{"id":str(x.id),"subject_name":x.subject_name,"weekday":x.weekday,"start_time":str(x.start_time),"end_time":str(x.end_time)} for x in rows]}
class AttendanceIn(BaseModel): section_id:UUID;attendance_date:date
@router.post("/attendance/sessions",status_code=201)
def create_session(p:AttendanceIn,u:User=Depends(current_user),db:Session=Depends(get_db)):
 require(db,u,"attendance.session.create");sec=db.scalar(select(Section).where(Section.id==p.section_id,Section.tenant_id==u.tenant_id))
 if not sec: raise HTTPException(404,"Section not found")
 x=AttendanceSession(tenant_id=u.tenant_id,created_by=u.id,**p.model_dump());db.add(x);db.commit();db.refresh(x);return {"data":{"id":str(x.id),"status":x.status}}
class RecordIn(BaseModel): student_id:UUID;status:str;remark:str|None=None
@router.put("/attendance/sessions/{session_id}/records")
def mark(session_id:UUID,records:list[RecordIn],u:User=Depends(current_user),db:Session=Depends(get_db)):
 require(db,u,"attendance.record.mark");s=db.scalar(select(AttendanceSession).where(AttendanceSession.id==session_id,AttendanceSession.tenant_id==u.tenant_id,AttendanceSession.status=="DRAFT"))
 if not s: raise HTTPException(404,"Attendance session not found")
 valid={"PRESENT","ABSENT","LATE","EXCUSED"}
 for r in records:
  if r.status not in valid: raise HTTPException(422,"Invalid attendance status")
  enrolled=db.scalar(select(Enrollment).where(Enrollment.tenant_id==u.tenant_id,Enrollment.section_id==s.section_id,Enrollment.student_id==r.student_id,Enrollment.status=="ACTIVE"))
  if not enrolled: raise HTTPException(404,"Student enrollment not found")
  x=db.scalar(select(AttendanceRecord).where(AttendanceRecord.session_id==s.id,AttendanceRecord.student_id==r.student_id))
  if x:x.status=r.status;x.remark=r.remark
  else:db.add(AttendanceRecord(tenant_id=u.tenant_id,session_id=s.id,student_id=r.student_id,status=r.status,remark=r.remark))
 db.commit();return {"data":{"saved":len(records)}}
@router.post("/attendance/sessions/{session_id}/submit")
def submit(session_id:UUID,u:User=Depends(current_user),db:Session=Depends(get_db)):
 require(db,u,"attendance.session.submit");s=db.scalar(select(AttendanceSession).where(AttendanceSession.id==session_id,AttendanceSession.tenant_id==u.tenant_id))
 if not s:raise HTTPException(404,"Attendance session not found")
 if s.status!="DRAFT":raise HTTPException(409,"Attendance session is not in DRAFT state")
 enrolled_count=len(db.scalars(select(Enrollment).where(Enrollment.tenant_id==u.tenant_id,Enrollment.section_id==s.section_id,Enrollment.status=="ACTIVE")).all())
 marked_count=len(db.scalars(select(AttendanceRecord).where(AttendanceRecord.tenant_id==u.tenant_id,AttendanceRecord.session_id==s.id)).all())
 if marked_count!=enrolled_count:raise HTTPException(409,"Attendance is incomplete for the active section roster")
 s.status="SUBMITTED";db.commit();return {"data":{"id":str(s.id),"status":s.status}}
