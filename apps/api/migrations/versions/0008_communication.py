"""communication notifications"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
revision="0008_communication";down_revision="0007_finance";branch_labels=None;depends_on=None
def upgrade():
 op.create_table("notices",sa.Column("id",postgresql.UUID(as_uuid=True),primary_key=True),sa.Column("tenant_id",postgresql.UUID(as_uuid=True),sa.ForeignKey("tenants.id"),nullable=False),sa.Column("title",sa.String(180),nullable=False),sa.Column("body",sa.Text(),nullable=False),sa.Column("audience",sa.String(60),nullable=False),sa.Column("status",sa.String(30),nullable=False),sa.Column("created_by",postgresql.UUID(as_uuid=True),sa.ForeignKey("users.id"),nullable=False),sa.Column("created_at",sa.DateTime(timezone=True),nullable=False),sa.Column("published_at",sa.DateTime(timezone=True)))
 op.create_table("notifications",sa.Column("id",postgresql.UUID(as_uuid=True),primary_key=True),sa.Column("tenant_id",postgresql.UUID(as_uuid=True),sa.ForeignKey("tenants.id"),nullable=False),sa.Column("user_id",postgresql.UUID(as_uuid=True),sa.ForeignKey("users.id"),nullable=False),sa.Column("title",sa.String(180),nullable=False),sa.Column("body",sa.Text(),nullable=False),sa.Column("status",sa.String(30),nullable=False),sa.Column("created_at",sa.DateTime(timezone=True),nullable=False))
def downgrade():
 op.drop_table("notifications");op.drop_table("notices")
