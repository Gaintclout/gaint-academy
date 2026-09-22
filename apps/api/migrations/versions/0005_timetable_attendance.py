"""timetable attendance"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
revision="0005_timetable_attendance";down_revision="0004_guardians_staff";branch_labels=None;depends_on=None
def upgrade():
 op.create_table("timetable_slots",sa.Column("id",postgresql.UUID(as_uuid=True),primary_key=True),sa.Column("tenant_id",postgresql.UUID(as_uuid=True),sa.ForeignKey("tenants.id"),nullable=False),sa.Column("section_id",postgresql.UUID(as_uuid=True),sa.ForeignKey("sections.id"),nullable=False),sa.Column("staff_id",postgresql.UUID(as_uuid=True),sa.ForeignKey("staff.id")),sa.Column("subject_name",sa.String(120),nullable=False),sa.Column("weekday",sa.String(12),nullable=False),sa.Column("start_time",sa.Time(),nullable=False),sa.Column("end_time",sa.Time(),nullable=False),sa.UniqueConstraint("tenant_id","section_id","weekday","start_time"))
 op.create_table("attendance_sessions",sa.Column("id",postgresql.UUID(as_uuid=True),primary_key=True),sa.Column("tenant_id",postgresql.UUID(as_uuid=True),sa.ForeignKey("tenants.id"),nullable=False),sa.Column("section_id",postgresql.UUID(as_uuid=True),sa.ForeignKey("sections.id"),nullable=False),sa.Column("attendance_date",sa.Date(),nullable=False),sa.Column("status",sa.String(30),nullable=False),sa.Column("created_by",postgresql.UUID(as_uuid=True),sa.ForeignKey("users.id"),nullable=False),sa.Column("created_at",sa.DateTime(timezone=True),nullable=False),sa.UniqueConstraint("tenant_id","section_id","attendance_date"))
 op.create_table("attendance_records",sa.Column("id",postgresql.UUID(as_uuid=True),primary_key=True),sa.Column("tenant_id",postgresql.UUID(as_uuid=True),sa.ForeignKey("tenants.id"),nullable=False),sa.Column("session_id",postgresql.UUID(as_uuid=True),sa.ForeignKey("attendance_sessions.id"),nullable=False),sa.Column("student_id",postgresql.UUID(as_uuid=True),sa.ForeignKey("students.id"),nullable=False),sa.Column("status",sa.String(20),nullable=False),sa.Column("remark",sa.String(240)),sa.UniqueConstraint("tenant_id","session_id","student_id"))
def downgrade():
 for t in ["attendance_records","attendance_sessions","timetable_slots"]:op.drop_table(t)
