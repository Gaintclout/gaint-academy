import uuid
from datetime import date,datetime,time,timezone
from sqlalchemy import Date,DateTime,ForeignKey,String,Time,UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped,mapped_column
from app.db.base import Base
def uid(): return uuid.uuid4()
def now(): return datetime.now(timezone.utc)
class TimetableSlot(Base):
 __tablename__="timetable_slots";__table_args__=(UniqueConstraint("tenant_id","section_id","weekday","start_time"),)
 id:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),primary_key=True,default=uid);tenant_id:Mapped[uuid.UUID]=mapped_column(ForeignKey("tenants.id"),index=True,nullable=False);section_id:Mapped[uuid.UUID]=mapped_column(ForeignKey("sections.id"),index=True,nullable=False);staff_id:Mapped[uuid.UUID|None]=mapped_column(ForeignKey("staff.id"));subject_name:Mapped[str]=mapped_column(String(120),nullable=False);weekday:Mapped[str]=mapped_column(String(12),nullable=False);start_time:Mapped[time]=mapped_column(Time,nullable=False);end_time:Mapped[time]=mapped_column(Time,nullable=False)
class AttendanceSession(Base):
 __tablename__="attendance_sessions";__table_args__=(UniqueConstraint("tenant_id","section_id","attendance_date"),)
 id:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),primary_key=True,default=uid);tenant_id:Mapped[uuid.UUID]=mapped_column(ForeignKey("tenants.id"),index=True,nullable=False);section_id:Mapped[uuid.UUID]=mapped_column(ForeignKey("sections.id"),index=True,nullable=False);attendance_date:Mapped[date]=mapped_column(Date,nullable=False);status:Mapped[str]=mapped_column(String(30),default="DRAFT",nullable=False);created_by:Mapped[uuid.UUID]=mapped_column(ForeignKey("users.id"),nullable=False);created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now,nullable=False)
class AttendanceRecord(Base):
 __tablename__="attendance_records";__table_args__=(UniqueConstraint("tenant_id","session_id","student_id"),)
 id:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),primary_key=True,default=uid);tenant_id:Mapped[uuid.UUID]=mapped_column(ForeignKey("tenants.id"),index=True,nullable=False);session_id:Mapped[uuid.UUID]=mapped_column(ForeignKey("attendance_sessions.id"),index=True,nullable=False);student_id:Mapped[uuid.UUID]=mapped_column(ForeignKey("students.id"),index=True,nullable=False);status:Mapped[str]=mapped_column(String(20),nullable=False);remark:Mapped[str|None]=mapped_column(String(240))
