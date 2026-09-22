import uuid
from datetime import datetime,timezone
from decimal import Decimal
from sqlalchemy import DateTime,ForeignKey,Numeric,String,UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped,mapped_column
from app.db.base import Base
def uid():return uuid.uuid4()
def now():return datetime.now(timezone.utc)
class FeePlan(Base):
 __tablename__="fee_plans";__table_args__=(UniqueConstraint("tenant_id","name"),)
 id:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),primary_key=True,default=uid);tenant_id:Mapped[uuid.UUID]=mapped_column(ForeignKey("tenants.id"),index=True,nullable=False);name:Mapped[str]=mapped_column(String(160),nullable=False);amount:Mapped[Decimal]=mapped_column(Numeric(12,2),nullable=False);status:Mapped[str]=mapped_column(String(30),default="ACTIVE",nullable=False)
class Invoice(Base):
 __tablename__="invoices";__table_args__=(UniqueConstraint("tenant_id","invoice_no"),)
 id:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),primary_key=True,default=uid);tenant_id:Mapped[uuid.UUID]=mapped_column(ForeignKey("tenants.id"),index=True,nullable=False);student_id:Mapped[uuid.UUID]=mapped_column(ForeignKey("students.id"),index=True,nullable=False);fee_plan_id:Mapped[uuid.UUID]=mapped_column(ForeignKey("fee_plans.id"),nullable=False);invoice_no:Mapped[str]=mapped_column(String(80),nullable=False);amount:Mapped[Decimal]=mapped_column(Numeric(12,2),nullable=False);paid_amount:Mapped[Decimal]=mapped_column(Numeric(12,2),default=0,nullable=False);status:Mapped[str]=mapped_column(String(30),default="ISSUED",nullable=False);created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now,nullable=False)
class Payment(Base):
 __tablename__="payments";__table_args__=(UniqueConstraint("tenant_id","reference"),)
 id:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),primary_key=True,default=uid);tenant_id:Mapped[uuid.UUID]=mapped_column(ForeignKey("tenants.id"),index=True,nullable=False);invoice_id:Mapped[uuid.UUID]=mapped_column(ForeignKey("invoices.id"),index=True,nullable=False);reference:Mapped[str]=mapped_column(String(120),nullable=False);amount:Mapped[Decimal]=mapped_column(Numeric(12,2),nullable=False);method:Mapped[str]=mapped_column(String(40),nullable=False);status:Mapped[str]=mapped_column(String(30),default="PENDING",nullable=False);created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now,nullable=False)
