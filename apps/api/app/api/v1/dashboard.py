from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.core.auth import current_user, permission_codes
from app.db.session import get_db
from app.models.identity import User

router=APIRouter(prefix="/dashboard",tags=["dashboard"])

@router.get("/summary")
def summary(request:Request,user:User=Depends(current_user),db:Session=Depends(get_db)):
    permissions=permission_codes(db,user)
    return {"data":{
        "tenant_id":str(user.tenant_id),
        "email":user.email,
        "platform":"ONLINE",
        "tenant_isolation":"ENABLED",
        "rbac":"ENABLED" if permissions else "NO_PERMISSIONS",
        "audit":"ENABLED"
    },"request_id":request.state.request_id}
