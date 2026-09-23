from uuid import UUID
from fastapi import APIRouter,Depends,HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.core.auth import current_user,permission_codes
from app.db.session import get_db
from app.models.identity import User,AuditEvent
from app.models.campus import Integration,Grievance,Asset
router=APIRouter(tags=["campus"])
def req(db,u,p):
 if p not in permission_codes(db,u):raise HTTPException(403,"Permission denied")
class IntegrationIn(BaseModel):kind:str;provider:str;config_ref:str|None=None
@router.get("/integrations")
def integrations(u:User=Depends(current_user),db:Session=Depends(get_db)):
 req(db,u,"integrations.view");rows=db.scalars(select(Integration).where(Integration.tenant_id==u.tenant_id)).all();return {"data":[{"id":str(x.id),"kind":x.kind,"provider":x.provider,"enabled":x.enabled} for x in rows]}
@router.post("/integrations",status_code=201)
def add_integration(p:IntegrationIn,u:User=Depends(current_user),db:Session=Depends(get_db)):
 req(db,u,"integrations.manage");x=Integration(tenant_id=u.tenant_id,**p.model_dump());db.add(x);db.flush();db.add(AuditEvent(tenant_id=u.tenant_id,user_id=u.id,action="integration.created",resource_type="integration",resource_id=str(x.id)));db.commit();db.refresh(x);return {"data":{"id":str(x.id),"enabled":x.enabled}}

@router.post("/integrations/{integration_id}/toggle")
def toggle_integration(integration_id:UUID,u:User=Depends(current_user),db:Session=Depends(get_db)):
 req(db,u,"integrations.manage");x=db.scalar(select(Integration).where(Integration.id==integration_id,Integration.tenant_id==u.tenant_id))
 if not x:raise HTTPException(404,"Integration not found")
 x.enabled=not x.enabled;db.add(AuditEvent(tenant_id=u.tenant_id,user_id=u.id,action="integration.toggled",resource_type="integration",resource_id=str(x.id)));db.commit()
 return {"data":{"id":str(x.id),"enabled":x.enabled}}
class GrievanceIn(BaseModel):category:str;subject:str;description:str
@router.post("/grievances",status_code=201)
def grievance(p:GrievanceIn,u:User=Depends(current_user),db:Session=Depends(get_db)):
 x=Grievance(tenant_id=u.tenant_id,submitted_by=u.id,**p.model_dump());db.add(x);db.commit();db.refresh(x);return {"data":{"id":str(x.id),"status":x.status}}
@router.get("/grievances")
def grievances(u:User=Depends(current_user),db:Session=Depends(get_db)):
 req(db,u,"grievances.manage");rows=db.scalars(select(Grievance).where(Grievance.tenant_id==u.tenant_id).order_by(Grievance.created_at.desc())).all();return {"data":[{"id":str(x.id),"subject":x.subject,"category":x.category,"description":x.description,"status":x.status} for x in rows]}

class GrievanceStatusIn(BaseModel):status:str
@router.patch("/grievances/{grievance_id}/status")
def grievance_status(grievance_id:UUID,p:GrievanceStatusIn,u:User=Depends(current_user),db:Session=Depends(get_db)):
 req(db,u,"grievances.manage")
 status=p.status.upper()
 if status not in {"OPEN","IN_PROGRESS","RESOLVED","CLOSED"}:raise HTTPException(422,"Invalid grievance status")
 x=db.scalar(select(Grievance).where(Grievance.id==grievance_id,Grievance.tenant_id==u.tenant_id))
 if not x:raise HTTPException(404,"Grievance not found")
 x.status=status;db.add(AuditEvent(tenant_id=u.tenant_id,user_id=u.id,action="grievance.status_changed",resource_type="grievance",resource_id=str(x.id)));db.commit()
 return {"data":{"id":str(x.id),"status":x.status}}
class AssetIn(BaseModel):asset_code:str;name:str;category:str
@router.post("/assets",status_code=201)
def asset(p:AssetIn,u:User=Depends(current_user),db:Session=Depends(get_db)):
 req(db,u,"assets.manage");x=Asset(tenant_id=u.tenant_id,**p.model_dump());db.add(x);db.flush();db.add(AuditEvent(tenant_id=u.tenant_id,user_id=u.id,action="asset.created",resource_type="asset",resource_id=str(x.id)));db.commit();db.refresh(x);return {"data":{"id":str(x.id),"status":x.status}}

@router.get("/assets")
def assets(u:User=Depends(current_user),db:Session=Depends(get_db)):
 req(db,u,"assets.manage");rows=db.scalars(select(Asset).where(Asset.tenant_id==u.tenant_id).order_by(Asset.asset_code)).all()
 return {"data":[{"id":str(x.id),"asset_code":x.asset_code,"name":x.name,"category":x.category,"status":x.status} for x in rows]}

class AssetStatusIn(BaseModel):status:str
@router.patch("/assets/{asset_id}/status")
def asset_status(asset_id:UUID,p:AssetStatusIn,u:User=Depends(current_user),db:Session=Depends(get_db)):
 req(db,u,"assets.manage");status=p.status.upper()
 if status not in {"ACTIVE","INACTIVE","MAINTENANCE","RETIRED"}:raise HTTPException(422,"Invalid asset status")
 x=db.scalar(select(Asset).where(Asset.id==asset_id,Asset.tenant_id==u.tenant_id))
 if not x:raise HTTPException(404,"Asset not found")
 x.status=status;db.add(AuditEvent(tenant_id=u.tenant_id,user_id=u.id,action="asset.status_changed",resource_type="asset",resource_id=str(x.id)));db.commit()
 return {"data":{"id":str(x.id),"status":x.status}}
