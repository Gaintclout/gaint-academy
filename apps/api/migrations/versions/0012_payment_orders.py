"""payment order lifecycle"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
revision="0012_payment_orders";down_revision="0011_guardian_user_identity";branch_labels=None;depends_on=None
def upgrade():
 op.create_table("payment_orders",sa.Column("id",postgresql.UUID(as_uuid=True),primary_key=True),sa.Column("tenant_id",postgresql.UUID(as_uuid=True),sa.ForeignKey("tenants.id"),nullable=False),sa.Column("invoice_id",postgresql.UUID(as_uuid=True),sa.ForeignKey("invoices.id"),nullable=False),sa.Column("provider",sa.String(40),nullable=False),sa.Column("provider_order_id",sa.String(160),nullable=False),sa.Column("idempotency_key",sa.String(160),nullable=False),sa.Column("amount",sa.Numeric(12,2),nullable=False),sa.Column("status",sa.String(30),nullable=False),sa.Column("created_at",sa.DateTime(timezone=True),nullable=False),sa.UniqueConstraint("tenant_id","idempotency_key"),sa.UniqueConstraint("tenant_id","provider_order_id"))
def downgrade():op.drop_table("payment_orders")
