from uuid import UUID
from fastapi import APIRouter,Depends,HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.core.auth import current_user,permission_codes
from app.db.session import get_db
from app.models.identity import User
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
 req(db,u,"integrations.manage");x=Integration(tenant_id=u.tenant_id,**p.model_dump());db.add(x);db.commit();db.refresh(x);return {"data":{"id":str(x.id),"enabled":x.enabled}}
class GrievanceIn(BaseModel):category:str;subject:str;description:str
@router.post("/grievances",status_code=201)
def grievance(p:GrievanceIn,u:User=Depends(current_user),db:Session=Depends(get_db)):
 x=Grievance(tenant_id=u.tenant_id,submitted_by=u.id,**p.model_dump());db.add(x);db.commit();db.refresh(x);return {"data":{"id":str(x.id),"status":x.status}}
@router.get("/grievances")
def grievances(u:User=Depends(current_user),db:Session=Depends(get_db)):
 req(db,u,"grievances.manage");rows=db.scalars(select(Grievance).where(Grievance.tenant_id==u.tenant_id)).all();return {"data":[{"id":str(x.id),"subject":x.subject,"category":x.category,"status":x.status} for x in rows]}
class AssetIn(BaseModel):asset_code:str;name:str;category:str
@router.post("/assets",status_code=201)
def asset(p:AssetIn,u:User=Depends(current_user),db:Session=Depends(get_db)):
 req(db,u,"assets.manage");x=Asset(tenant_id=u.tenant_id,**p.model_dump());db.add(x);db.commit();db.refresh(x);return {"data":{"id":str(x.id),"status":x.status}}
