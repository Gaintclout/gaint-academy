import uuid
from datetime import datetime,timezone
from sqlalchemy import DateTime,ForeignKey,String,Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped,mapped_column
from app.db.base import Base
def uid():return uuid.uuid4()
def now():return datetime.now(timezone.utc)
class Notice(Base):
 __tablename__="notices"
 id:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),primary_key=True,default=uid);tenant_id:Mapped[uuid.UUID]=mapped_column(ForeignKey("tenants.id"),index=True,nullable=False);title:Mapped[str]=mapped_column(String(180),nullable=False);body:Mapped[str]=mapped_column(Text,nullable=False);audience:Mapped[str]=mapped_column(String(60),nullable=False);status:Mapped[str]=mapped_column(String(30),default="DRAFT",nullable=False);created_by:Mapped[uuid.UUID]=mapped_column(ForeignKey("users.id"),nullable=False);created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now,nullable=False);published_at:Mapped[datetime|None]=mapped_column(DateTime(timezone=True))
class Notification(Base):
 __tablename__="notifications"
 id:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),primary_key=True,default=uid);tenant_id:Mapped[uuid.UUID]=mapped_column(ForeignKey("tenants.id"),index=True,nullable=False);user_id:Mapped[uuid.UUID]=mapped_column(ForeignKey("users.id"),index=True,nullable=False);title:Mapped[str]=mapped_column(String(180),nullable=False);body:Mapped[str]=mapped_column(Text,nullable=False);status:Mapped[str]=mapped_column(String(30),default="UNREAD",nullable=False);created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now,nullable=False)
