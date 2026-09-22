"""finance foundation"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
revision="0007_finance";down_revision="0006_learning_assessment";branch_labels=None;depends_on=None
def upgrade():
 op.create_table("fee_plans",sa.Column("id",postgresql.UUID(as_uuid=True),primary_key=True),sa.Column("tenant_id",postgresql.UUID(as_uuid=True),sa.ForeignKey("tenants.id"),nullable=False),sa.Column("name",sa.String(160),nullable=False),sa.Column("amount",sa.Numeric(12,2),nullable=False),sa.Column("status",sa.String(30),nullable=False),sa.UniqueConstraint("tenant_id","name"))
 op.create_table("invoices",sa.Column("id",postgresql.UUID(as_uuid=True),primary_key=True),sa.Column("tenant_id",postgresql.UUID(as_uuid=True),sa.ForeignKey("tenants.id"),nullable=False),sa.Column("student_id",postgresql.UUID(as_uuid=True),sa.ForeignKey("students.id"),nullable=False),sa.Column("fee_plan_id",postgresql.UUID(as_uuid=True),sa.ForeignKey("fee_plans.id"),nullable=False),sa.Column("invoice_no",sa.String(80),nullable=False),sa.Column("amount",sa.Numeric(12,2),nullable=False),sa.Column("paid_amount",sa.Numeric(12,2),nullable=False),sa.Column("status",sa.String(30),nullable=False),sa.Column("created_at",sa.DateTime(timezone=True),nullable=False),sa.UniqueConstraint("tenant_id","invoice_no"))
 op.create_table("payments",sa.Column("id",postgresql.UUID(as_uuid=True),primary_key=True),sa.Column("tenant_id",postgresql.UUID(as_uuid=True),sa.ForeignKey("tenants.id"),nullable=False),sa.Column("invoice_id",postgresql.UUID(as_uuid=True),sa.ForeignKey("invoices.id"),nullable=False),sa.Column("reference",sa.String(120),nullable=False),sa.Column("amount",sa.Numeric(12,2),nullable=False),sa.Column("method",sa.String(40),nullable=False),sa.Column("status",sa.String(30),nullable=False),sa.Column("created_at",sa.DateTime(timezone=True),nullable=False),sa.UniqueConstraint("tenant_id","reference"))
def downgrade():
 for t in ["payments","invoices","fee_plans"]:op.drop_table(t)
