"""guardians staff teacher assignments"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
revision="0004_guardians_staff"; down_revision="0003_core_academics"; branch_labels=None; depends_on=None
def upgrade():
 op.create_table("guardians",sa.Column("id",postgresql.UUID(as_uuid=True),primary_key=True),sa.Column("tenant_id",postgresql.UUID(as_uuid=True),sa.ForeignKey("tenants.id"),nullable=False),sa.Column("name",sa.String(180),nullable=False),sa.Column("phone",sa.String(30),nullable=False),sa.Column("email",sa.String(320)),sa.Column("created_at",sa.DateTime(timezone=True),nullable=False),sa.UniqueConstraint("tenant_id","phone"))
 op.create_table("student_guardians",sa.Column("id",postgresql.UUID(as_uuid=True),primary_key=True),sa.Column("tenant_id",postgresql.UUID(as_uuid=True),sa.ForeignKey("tenants.id"),nullable=False),sa.Column("student_id",postgresql.UUID(as_uuid=True),sa.ForeignKey("students.id"),nullable=False),sa.Column("guardian_id",postgresql.UUID(as_uuid=True),sa.ForeignKey("guardians.id"),nullable=False),sa.Column("relationship",sa.String(60),nullable=False),sa.Column("is_primary",sa.Boolean(),nullable=False),sa.UniqueConstraint("tenant_id","student_id","guardian_id"))
 op.create_table("staff",sa.Column("id",postgresql.UUID(as_uuid=True),primary_key=True),sa.Column("tenant_id",postgresql.UUID(as_uuid=True),sa.ForeignKey("tenants.id"),nullable=False),sa.Column("employee_no",sa.String(80),nullable=False),sa.Column("name",sa.String(180),nullable=False),sa.Column("email",sa.String(320)),sa.Column("designation",sa.String(120)),sa.Column("status",sa.String(30),nullable=False),sa.Column("created_at",sa.DateTime(timezone=True),nullable=False),sa.UniqueConstraint("tenant_id","employee_no"))
 op.create_table("teacher_assignments",sa.Column("id",postgresql.UUID(as_uuid=True),primary_key=True),sa.Column("tenant_id",postgresql.UUID(as_uuid=True),sa.ForeignKey("tenants.id"),nullable=False),sa.Column("staff_id",postgresql.UUID(as_uuid=True),sa.ForeignKey("staff.id"),nullable=False),sa.Column("section_id",postgresql.UUID(as_uuid=True),sa.ForeignKey("sections.id"),nullable=False),sa.Column("assignment_type",sa.String(40),nullable=False),sa.UniqueConstraint("tenant_id","staff_id","section_id"))
def downgrade():
 for t in ["teacher_assignments","staff","student_guardians","guardians"]: op.drop_table(t)
