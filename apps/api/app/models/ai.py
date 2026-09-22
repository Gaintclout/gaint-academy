import uuid
from datetime import datetime,timezone
from sqlalchemy import DateTime,ForeignKey,String,Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped,mapped_column
from app.db.base import Base
def uid():return uuid.uuid4()
def now():return datetime.now(timezone.utc)
class AIConversation(Base):
 __tablename__="ai_conversations"
 id:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),primary_key=True,default=uid);tenant_id:Mapped[uuid.UUID]=mapped_column(ForeignKey("tenants.id"),index=True,nullable=False);user_id:Mapped[uuid.UUID]=mapped_column(ForeignKey("users.id"),index=True,nullable=False);title:Mapped[str]=mapped_column(String(180),default="New conversation",nullable=False);created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now,nullable=False)
class AIMessage(Base):
 __tablename__="ai_messages"
 id:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),primary_key=True,default=uid);tenant_id:Mapped[uuid.UUID]=mapped_column(ForeignKey("tenants.id"),index=True,nullable=False);conversation_id:Mapped[uuid.UUID]=mapped_column(ForeignKey("ai_conversations.id"),index=True,nullable=False);role:Mapped[str]=mapped_column(String(20),nullable=False);content:Mapped[str]=mapped_column(Text,nullable=False);sources_json:Mapped[str|None]=mapped_column(Text);created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now,nullable=False)
class AIActionProposal(Base):
 __tablename__="ai_action_proposals"
 id:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),primary_key=True,default=uid);tenant_id:Mapped[uuid.UUID]=mapped_column(ForeignKey("tenants.id"),index=True,nullable=False);user_id:Mapped[uuid.UUID]=mapped_column(ForeignKey("users.id"),index=True,nullable=False);action_type:Mapped[str]=mapped_column(String(100),nullable=False);payload_json:Mapped[str]=mapped_column(Text,nullable=False);status:Mapped[str]=mapped_column(String(30),default="PROPOSED",nullable=False);created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now,nullable=False)
