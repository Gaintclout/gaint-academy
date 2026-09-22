from uuid import UUID
from fastapi import APIRouter,Depends,HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.core.auth import current_user,permission_codes
from app.db.session import get_db
from app.models.identity import User
from app.models.ai import AIConversation,AIMessage,AIActionProposal
router=APIRouter(prefix="/ai",tags=["ai"])
def req(db,u,p):
 if p not in permission_codes(db,u):raise HTTPException(403,"Permission denied")
class AskIn(BaseModel):conversation_id:UUID|None=None;message:str
@router.post("/ask")
def ask(p:AskIn,u:User=Depends(current_user),db:Session=Depends(get_db)):
 req(db,u,"ai.use")
 if not p.message.strip():raise HTTPException(422,"Message is required")
 c=None
 if p.conversation_id:c=db.scalar(select(AIConversation).where(AIConversation.id==p.conversation_id,AIConversation.tenant_id==u.tenant_id,AIConversation.user_id==u.id))
 if p.conversation_id and not c:raise HTTPException(404,"Conversation not found")
 if not c:c=AIConversation(tenant_id=u.tenant_id,user_id=u.id,title=p.message[:80]);db.add(c);db.flush()
 db.add(AIMessage(tenant_id=u.tenant_id,conversation_id=c.id,role="user",content=p.message))
 answer="GAINT AI gateway is active. Model-provider and permission-scoped retrieval adapters are not configured yet."
 db.add(AIMessage(tenant_id=u.tenant_id,conversation_id=c.id,role="assistant",content=answer,sources_json="[]"));db.commit()
 return {"data":{"conversation_id":str(c.id),"answer":answer,"sources":[],"mode":"SAFE_PLACEHOLDER"}}
class ProposalIn(BaseModel):action_type:str;payload_json:str
@router.post("/actions/propose",status_code=201)
def propose(p:ProposalIn,u:User=Depends(current_user),db:Session=Depends(get_db)):
 req(db,u,"ai.action.propose");x=AIActionProposal(tenant_id=u.tenant_id,user_id=u.id,**p.model_dump());db.add(x);db.commit();db.refresh(x);return {"data":{"id":str(x.id),"status":x.status}}
@router.post("/actions/{proposal_id}/confirm")
def confirm(proposal_id:UUID,u:User=Depends(current_user),db:Session=Depends(get_db)):
 req(db,u,"ai.action.confirm");x=db.scalar(select(AIActionProposal).where(AIActionProposal.id==proposal_id,AIActionProposal.tenant_id==u.tenant_id,AIActionProposal.user_id==u.id))
 if not x:raise HTTPException(404,"Proposal not found")
 if x.status!="PROPOSED":raise HTTPException(409,"Proposal is not confirmable")
 x.status="CONFIRMED";db.commit();return {"data":{"id":str(x.id),"status":x.status,"executed":False}}
