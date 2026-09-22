import uuid
from datetime import datetime,timezone
from sqlalchemy import Boolean,DateTime,ForeignKey,String,Text,UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped,mapped_column
from app.db.base import Base
def uid():return uuid.uuid4()
def now():return datetime.now(timezone.utc)
class Integration(Base):
 __tablename__="integrations";__table_args__=(UniqueConstraint("tenant_id","provider","kind"),)
 id:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),primary_key=True,default=uid);tenant_id:Mapped[uuid.UUID]=mapped_column(ForeignKey("tenants.id"),index=True,nullable=False);kind:Mapped[str]=mapped_column(String(50),nullable=False);provider:Mapped[str]=mapped_column(String(80),nullable=False);enabled:Mapped[bool]=mapped_column(Boolean,default=False,nullable=False);config_ref:Mapped[str|None]=mapped_column(String(255));created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now,nullable=False)
class Grievance(Base):
 __tablename__="grievances"
 id:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),primary_key=True,default=uid);tenant_id:Mapped[uuid.UUID]=mapped_column(ForeignKey("tenants.id"),index=True,nullable=False);submitted_by:Mapped[uuid.UUID]=mapped_column(ForeignKey("users.id"),index=True,nullable=False);category:Mapped[str]=mapped_column(String(80),nullable=False);subject:Mapped[str]=mapped_column(String(180),nullable=False);description:Mapped[str]=mapped_column(Text,nullable=False);status:Mapped[str]=mapped_column(String(30),default="OPEN",nullable=False);created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now,nullable=False)
class Asset(Base):
 __tablename__="assets";__table_args__=(UniqueConstraint("tenant_id","asset_code"),)
 id:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),primary_key=True,default=uid);tenant_id:Mapped[uuid.UUID]=mapped_column(ForeignKey("tenants.id"),index=True,nullable=False);asset_code:Mapped[str]=mapped_column(String(80),nullable=False);name:Mapped[str]=mapped_column(String(160),nullable=False);category:Mapped[str]=mapped_column(String(80),nullable=False);status:Mapped[str]=mapped_column(String(30),default="ACTIVE",nullable=False)
