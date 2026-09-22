from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, EmailStr
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.identity import User
from app.core.security import verify_password
router=APIRouter(prefix="/auth",tags=["auth"])
class LoginIn(BaseModel):
    email: EmailStr
    password: str
@router.post("/login")
def login(payload:LoginIn,request:Request,db:Session=Depends(get_db)):
    user=db.scalar(select(User).where(User.email==payload.email.lower(),User.is_active.is_(True)))
    if not user or not verify_password(payload.password,user.password_hash):
        raise HTTPException(status_code=401,detail="Invalid credentials")
    return {"data":{"user_id":str(user.id),"tenant_id":str(user.tenant_id),"email":user.email},"request_id":request.state.request_id}
