import uuid
from datetime import date, datetime, timezone
from sqlalchemy import Date, DateTime, ForeignKey, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base
def uid(): return uuid.uuid4()
def now(): return datetime.now(timezone.utc)
class AcademicYear(Base):
    __tablename__="academic_years"; __table_args__=(UniqueConstraint("tenant_id","name"),)
    id:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),primary_key=True,default=uid)
    tenant_id:Mapped[uuid.UUID]=mapped_column(ForeignKey("tenants.id"),index=True,nullable=False)
    name:Mapped[str]=mapped_column(String(80),nullable=False)
    start_date:Mapped[date]=mapped_column(Date,nullable=False)
    end_date:Mapped[date]=mapped_column(Date,nullable=False)
    status:Mapped[str]=mapped_column(String(30),default="ACTIVE",nullable=False)
class AcademicClass(Base):
    __tablename__="academic_classes"; __table_args__=(UniqueConstraint("tenant_id","academic_year_id","name"),)
    id:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),primary_key=True,default=uid)
    tenant_id:Mapped[uuid.UUID]=mapped_column(ForeignKey("tenants.id"),index=True,nullable=False)
    academic_year_id:Mapped[uuid.UUID]=mapped_column(ForeignKey("academic_years.id"),index=True,nullable=False)
    name:Mapped[str]=mapped_column(String(100),nullable=False)
class Section(Base):
    __tablename__="sections"; __table_args__=(UniqueConstraint("tenant_id","class_id","name"),)
    id:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),primary_key=True,default=uid)
    tenant_id:Mapped[uuid.UUID]=mapped_column(ForeignKey("tenants.id"),index=True,nullable=False)
    class_id:Mapped[uuid.UUID]=mapped_column(ForeignKey("academic_classes.id"),index=True,nullable=False)
    name:Mapped[str]=mapped_column(String(80),nullable=False)
class Student(Base):
    __tablename__="students"; __table_args__=(UniqueConstraint("tenant_id","admission_no"),)
    id:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),primary_key=True,default=uid)
    tenant_id:Mapped[uuid.UUID]=mapped_column(ForeignKey("tenants.id"),index=True,nullable=False)
    admission_no:Mapped[str]=mapped_column(String(80),nullable=False)
    first_name:Mapped[str]=mapped_column(String(120),nullable=False)
    last_name:Mapped[str|None]=mapped_column(String(120))
    email:Mapped[str|None]=mapped_column(String(320))
    status:Mapped[str]=mapped_column(String(30),default="ACTIVE",nullable=False)
    created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now,nullable=False)
class Enrollment(Base):
    __tablename__="enrollments"; __table_args__=(UniqueConstraint("tenant_id","student_id","academic_year_id"),)
    id:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),primary_key=True,default=uid)
    tenant_id:Mapped[uuid.UUID]=mapped_column(ForeignKey("tenants.id"),index=True,nullable=False)
    student_id:Mapped[uuid.UUID]=mapped_column(ForeignKey("students.id"),index=True,nullable=False)
    academic_year_id:Mapped[uuid.UUID]=mapped_column(ForeignKey("academic_years.id"),index=True,nullable=False)
    class_id:Mapped[uuid.UUID]=mapped_column(ForeignKey("academic_classes.id"),index=True,nullable=False)
    section_id:Mapped[uuid.UUID]=mapped_column(ForeignKey("sections.id"),index=True,nullable=False)
    status:Mapped[str]=mapped_column(String(30),default="ACTIVE",nullable=False)
