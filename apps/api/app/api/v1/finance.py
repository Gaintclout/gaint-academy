from decimal import Decimal
from uuid import UUID
from fastapi import APIRouter,Depends,HTTPException
from pydantic import BaseModel,Field
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.core.auth import current_user,permission_codes
from app.db.session import get_db
from app.models.identity import User
from app.models.academics import Student
from app.models.finance import FeePlan,Invoice,Payment
router=APIRouter(prefix="/finance",tags=["finance"])
def req(db,u,p):
 if p not in permission_codes(db,u):raise HTTPException(403,"Permission denied")
class FeePlanIn(BaseModel):name:str;amount:Decimal=Field(gt=0)
@router.post("/fee-plans",status_code=201)
def plan(p:FeePlanIn,u:User=Depends(current_user),db:Session=Depends(get_db)):
 req(db,u,"finance.plan.manage");x=FeePlan(tenant_id=u.tenant_id,**p.model_dump());db.add(x);db.commit();db.refresh(x);return {"data":{"id":str(x.id),"name":x.name,"amount":str(x.amount)}}
@router.get("/fee-plans")
def plans(u:User=Depends(current_user),db:Session=Depends(get_db)):
 req(db,u,"finance.plan.view");rows=db.scalars(select(FeePlan).where(FeePlan.tenant_id==u.tenant_id)).all();return {"data":[{"id":str(x.id),"name":x.name,"amount":str(x.amount),"status":x.status} for x in rows]}
class InvoiceIn(BaseModel):student_id:UUID;fee_plan_id:UUID;invoice_no:str
@router.post("/invoices",status_code=201)
def invoice(p:InvoiceIn,u:User=Depends(current_user),db:Session=Depends(get_db)):
 req(db,u,"finance.invoice.create");student=db.scalar(select(Student).where(Student.id==p.student_id,Student.tenant_id==u.tenant_id));plan=db.scalar(select(FeePlan).where(FeePlan.id==p.fee_plan_id,FeePlan.tenant_id==u.tenant_id,FeePlan.status=="ACTIVE"))
 if not student or not plan:raise HTTPException(404,"Invoice resource not found")
 x=Invoice(tenant_id=u.tenant_id,student_id=student.id,fee_plan_id=plan.id,invoice_no=p.invoice_no,amount=plan.amount);db.add(x);db.commit();db.refresh(x);return {"data":{"id":str(x.id),"invoice_no":x.invoice_no,"amount":str(x.amount),"status":x.status}}
class PaymentIn(BaseModel):invoice_id:UUID;reference:str;amount:Decimal=Field(gt=0);method:str
@router.post("/payments",status_code=201)
def payment(p:PaymentIn,u:User=Depends(current_user),db:Session=Depends(get_db)):
 req(db,u,"finance.payment.record");inv=db.scalar(select(Invoice).where(Invoice.id==p.invoice_id,Invoice.tenant_id==u.tenant_id))
 if not inv:raise HTTPException(404,"Invoice not found")
 due=inv.amount-inv.paid_amount
 if p.amount>due:raise HTTPException(422,"Payment exceeds invoice balance")
 x=Payment(tenant_id=u.tenant_id,**p.model_dump(),status="CONFIRMED");db.add(x);inv.paid_amount+=p.amount;inv.status="PAID" if inv.paid_amount==inv.amount else "PARTIALLY_PAID";db.commit();db.refresh(x);return {"data":{"id":str(x.id),"status":x.status,"invoice_status":inv.status,"balance":str(inv.amount-inv.paid_amount)}}
