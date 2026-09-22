from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from pydantic import BaseModel, EmailStr
from sqlalchemy import select
from sqlalchemy.orm import Session as DbSession
from app.db.session import get_db
from app.models.identity import User, Session, AuditEvent, Tenant, now
from app.core.security import verify_password
from app.core.auth import SESSION_COOKIE, current_user, new_session_token, permission_codes, token_hash
from app.core.config import settings

router=APIRouter(prefix="/auth",tags=["auth"])
class LoginIn(BaseModel):
    institution_code: str
    email: EmailStr
    password: str

@router.post("/login")
def login(payload:LoginIn,request:Request,response:Response,db:DbSession=Depends(get_db)):
    tenant=db.scalar(select(Tenant).where(Tenant.code==payload.institution_code.strip().upper(),Tenant.status=="ACTIVE"))
    user=None if not tenant else db.scalar(select(User).where(User.tenant_id==tenant.id,User.email==payload.email.lower(),User.is_active.is_(True)))
    if not user or not verify_password(payload.password,user.password_hash):
        raise HTTPException(status_code=401,detail="Invalid credentials")
    raw,digest=new_session_token()
    db.add(Session(tenant_id=user.tenant_id,user_id=user.id,token_hash=digest,expires_at=now()+timedelta(hours=settings.session_hours)))
    db.add(AuditEvent(tenant_id=user.tenant_id,user_id=user.id,action="auth.login",resource_type="user",resource_id=str(user.id),request_id=request.state.request_id))
    db.commit()
    response.set_cookie(SESSION_COOKIE,raw,httponly=True,secure=settings.cookie_secure,samesite="lax",max_age=settings.session_hours*3600,path="/")
    return {"data":{"user_id":str(user.id),"tenant_id":str(user.tenant_id),"email":user.email},"request_id":request.state.request_id}

@router.get("/me")
def me(request:Request,user:User=Depends(current_user),db:DbSession=Depends(get_db)):
    return {"data":{"user_id":str(user.id),"tenant_id":str(user.tenant_id),"email":user.email,"permissions":permission_codes(db,user)},"request_id":request.state.request_id}

@router.post("/logout")
def logout(request:Request,response:Response,session_token:str|None=None,user:User=Depends(current_user),db:DbSession=Depends(get_db)):
    raw=request.cookies.get(SESSION_COOKIE)
    if raw:
        session=db.scalar(select(Session).where(Session.token_hash==token_hash(raw),Session.user_id==user.id,Session.revoked_at.is_(None)))
        if session: session.revoked_at=now()
    db.add(AuditEvent(tenant_id=user.tenant_id,user_id=user.id,action="auth.logout",resource_type="user",resource_id=str(user.id),request_id=request.state.request_id))
    db.commit(); response.delete_cookie(SESSION_COOKIE,path="/")
    return {"data":{"logged_out":True},"request_id":request.state.request_id}
