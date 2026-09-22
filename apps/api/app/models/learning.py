import uuid
from datetime import datetime,timezone
from sqlalchemy import DateTime,ForeignKey,Integer,String,Text,UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped,mapped_column
from app.db.base import Base
def uid():return uuid.uuid4()
def now():return datetime.now(timezone.utc)
class Course(Base):
 __tablename__="courses";__table_args__=(UniqueConstraint("tenant_id","section_id","name"),)
 id:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),primary_key=True,default=uid);tenant_id:Mapped[uuid.UUID]=mapped_column(ForeignKey("tenants.id"),index=True,nullable=False);section_id:Mapped[uuid.UUID]=mapped_column(ForeignKey("sections.id"),index=True,nullable=False);teacher_id:Mapped[uuid.UUID|None]=mapped_column(ForeignKey("staff.id"));name:Mapped[str]=mapped_column(String(160),nullable=False);status:Mapped[str]=mapped_column(String(30),default="ACTIVE",nullable=False)
class Assignment(Base):
 __tablename__="assignments"
 id:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),primary_key=True,default=uid);tenant_id:Mapped[uuid.UUID]=mapped_column(ForeignKey("tenants.id"),index=True,nullable=False);course_id:Mapped[uuid.UUID]=mapped_column(ForeignKey("courses.id"),index=True,nullable=False);title:Mapped[str]=mapped_column(String(180),nullable=False);instructions:Mapped[str|None]=mapped_column(Text);max_marks:Mapped[int]=mapped_column(Integer,default=100,nullable=False);due_at:Mapped[datetime|None]=mapped_column(DateTime(timezone=True));status:Mapped[str]=mapped_column(String(30),default="DRAFT",nullable=False);created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now,nullable=False)
class Submission(Base):
 __tablename__="submissions";__table_args__=(UniqueConstraint("tenant_id","assignment_id","student_id"),)
 id:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),primary_key=True,default=uid);tenant_id:Mapped[uuid.UUID]=mapped_column(ForeignKey("tenants.id"),index=True,nullable=False);assignment_id:Mapped[uuid.UUID]=mapped_column(ForeignKey("assignments.id"),index=True,nullable=False);student_id:Mapped[uuid.UUID]=mapped_column(ForeignKey("students.id"),index=True,nullable=False);content:Mapped[str|None]=mapped_column(Text);status:Mapped[str]=mapped_column(String(30),default="SUBMITTED",nullable=False);submitted_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now,nullable=False)
class Assessment(Base):
 __tablename__="assessments"
 id:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),primary_key=True,default=uid);tenant_id:Mapped[uuid.UUID]=mapped_column(ForeignKey("tenants.id"),index=True,nullable=False);course_id:Mapped[uuid.UUID]=mapped_column(ForeignKey("courses.id"),index=True,nullable=False);name:Mapped[str]=mapped_column(String(180),nullable=False);max_marks:Mapped[int]=mapped_column(Integer,default=100,nullable=False);status:Mapped[str]=mapped_column(String(30),default="DRAFT",nullable=False)
class AssessmentMark(Base):
 __tablename__="assessment_marks";__table_args__=(UniqueConstraint("tenant_id","assessment_id","student_id"),)
 id:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),primary_key=True,default=uid);tenant_id:Mapped[uuid.UUID]=mapped_column(ForeignKey("tenants.id"),index=True,nullable=False);assessment_id:Mapped[uuid.UUID]=mapped_column(ForeignKey("assessments.id"),index=True,nullable=False);student_id:Mapped[uuid.UUID]=mapped_column(ForeignKey("students.id"),index=True,nullable=False);marks:Mapped[int]=mapped_column(Integer,nullable=False);status:Mapped[str]=mapped_column(String(30),default="DRAFT",nullable=False)
