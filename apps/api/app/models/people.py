import uuid
from datetime import datetime,timezone
from sqlalchemy import DateTime,ForeignKey,String,UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped,mapped_column
from app.db.base import Base
def uid(): return uuid.uuid4()
def now(): return datetime.now(timezone.utc)
class Guardian(Base):
    __tablename__="guardians"; __table_args__=(UniqueConstraint("tenant_id","phone"),)
    id:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),primary_key=True,default=uid)
    tenant_id:Mapped[uuid.UUID]=mapped_column(ForeignKey("tenants.id"),index=True,nullable=False)
    name:Mapped[str]=mapped_column(String(180),nullable=False)
    phone:Mapped[str]=mapped_column(String(30),nullable=False)
    email:Mapped[str|None]=mapped_column(String(320))
    created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now,nullable=False)
class StudentGuardian(Base):
    __tablename__="student_guardians"; __table_args__=(UniqueConstraint("tenant_id","student_id","guardian_id"),)
    id:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),primary_key=True,default=uid)
    tenant_id:Mapped[uuid.UUID]=mapped_column(ForeignKey("tenants.id"),index=True,nullable=False)
    student_id:Mapped[uuid.UUID]=mapped_column(ForeignKey("students.id"),index=True,nullable=False)
    guardian_id:Mapped[uuid.UUID]=mapped_column(ForeignKey("guardians.id"),index=True,nullable=False)
    relationship:Mapped[str]=mapped_column(String(60),nullable=False)
    is_primary:Mapped[bool]=mapped_column(default=False,nullable=False)
class Staff(Base):
    __tablename__="staff"; __table_args__=(UniqueConstraint("tenant_id","employee_no"),)
    id:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),primary_key=True,default=uid)
    tenant_id:Mapped[uuid.UUID]=mapped_column(ForeignKey("tenants.id"),index=True,nullable=False)
    employee_no:Mapped[str]=mapped_column(String(80),nullable=False)
    name:Mapped[str]=mapped_column(String(180),nullable=False)
    email:Mapped[str|None]=mapped_column(String(320))
    designation:Mapped[str|None]=mapped_column(String(120))
    status:Mapped[str]=mapped_column(String(30),default="ACTIVE",nullable=False)
    created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now,nullable=False)
class TeacherAssignment(Base):
    __tablename__="teacher_assignments"; __table_args__=(UniqueConstraint("tenant_id","staff_id","section_id"),)
    id:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),primary_key=True,default=uid)
    tenant_id:Mapped[uuid.UUID]=mapped_column(ForeignKey("tenants.id"),index=True,nullable=False)
    staff_id:Mapped[uuid.UUID]=mapped_column(ForeignKey("staff.id"),index=True,nullable=False)
    section_id:Mapped[uuid.UUID]=mapped_column(ForeignKey("sections.id"),index=True,nullable=False)
    assignment_type:Mapped[str]=mapped_column(String(40),default="CLASS_TEACHER",nullable=False)
