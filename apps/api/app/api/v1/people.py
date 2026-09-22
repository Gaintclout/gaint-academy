from uuid import UUID
from fastapi import APIRouter,Depends,HTTPException
from pydantic import BaseModel,EmailStr
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.core.auth import current_user,permission_codes
from app.db.session import get_db
from app.models.identity import User
from app.models.academics import Student,Section
from app.models.people import Guardian,StudentGuardian,Staff,TeacherAssignment
router=APIRouter(tags=["people"])
def require(db,user,code):
    if code not in permission_codes(db,user): raise HTTPException(403,"Permission denied")
class GuardianIn(BaseModel): name:str; phone:str; email:EmailStr|None=None; relationship:str="PARENT"; is_primary:bool=True
@router.post("/students/{student_id}/guardians",status_code=201)
def add_guardian(student_id:UUID,p:GuardianIn,user:User=Depends(current_user),db:Session=Depends(get_db)):
    require(db,user,"students.student.create")
    student=db.scalar(select(Student).where(Student.id==student_id,Student.tenant_id==user.tenant_id))
    if not student: raise HTTPException(404,"Student not found")
    guardian=db.scalar(select(Guardian).where(Guardian.tenant_id==user.tenant_id,Guardian.phone==p.phone))
    if not guardian: guardian=Guardian(tenant_id=user.tenant_id,name=p.name,phone=p.phone,email=p.email);db.add(guardian);db.flush()
    link=StudentGuardian(tenant_id=user.tenant_id,student_id=student.id,guardian_id=guardian.id,relationship=p.relationship,is_primary=p.is_primary);db.add(link);db.commit()
    return {"data":{"guardian_id":str(guardian.id),"relationship":link.relationship}}
class GuardianUserLinkIn(BaseModel):user_id:UUID
@router.put("/guardians/{guardian_id}/user-link")
def link_guardian_user(guardian_id:UUID,p:GuardianUserLinkIn,user:User=Depends(current_user),db:Session=Depends(get_db)):
    require(db,user,"students.student.create");guardian=db.scalar(select(Guardian).where(Guardian.id==guardian_id,Guardian.tenant_id==user.tenant_id));target=db.scalar(select(User).where(User.id==p.user_id,User.tenant_id==user.tenant_id,User.is_active.is_(True)))
    if not guardian or not target:raise HTTPException(404,"Guardian or user not found")
    guardian.user_id=target.id;db.commit();return {"data":{"guardian_id":str(guardian.id),"user_id":str(target.id)}}
class StaffIn(BaseModel): employee_no:str; name:str; email:EmailStr|None=None; designation:str|None=None
@router.get("/staff")
def staff_list(user:User=Depends(current_user),db:Session=Depends(get_db)):
    require(db,user,"staff.staff.view"); rows=db.scalars(select(Staff).where(Staff.tenant_id==user.tenant_id)).all()
    return {"data":[{"id":str(x.id),"employee_no":x.employee_no,"name":x.name,"designation":x.designation,"status":x.status} for x in rows]}
@router.post("/staff",status_code=201)
def staff_create(p:StaffIn,user:User=Depends(current_user),db:Session=Depends(get_db)):
    require(db,user,"staff.staff.create");x=Staff(tenant_id=user.tenant_id,**p.model_dump());db.add(x);db.commit();db.refresh(x);return {"data":{"id":str(x.id),"employee_no":x.employee_no}}
class AssignIn(BaseModel): section_id:UUID; assignment_type:str="CLASS_TEACHER"
@router.post("/staff/{staff_id}/assignments",status_code=201)
def assign(staff_id:UUID,p:AssignIn,user:User=Depends(current_user),db:Session=Depends(get_db)):
    require(db,user,"academics.setup.admin")
    staff=db.scalar(select(Staff).where(Staff.id==staff_id,Staff.tenant_id==user.tenant_id));section=db.scalar(select(Section).where(Section.id==p.section_id,Section.tenant_id==user.tenant_id))
    if not staff or not section: raise HTTPException(404,"Assignment resource not found")
    x=TeacherAssignment(tenant_id=user.tenant_id,staff_id=staff.id,**p.model_dump());db.add(x);db.commit();db.refresh(x);return {"data":{"id":str(x.id)}}
