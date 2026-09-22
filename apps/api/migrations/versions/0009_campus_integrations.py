"""campus integrations"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
revision="0009_campus_integrations";down_revision="0008_communication";branch_labels=None;depends_on=None
def upgrade():
 op.create_table("integrations",sa.Column("id",postgresql.UUID(as_uuid=True),primary_key=True),sa.Column("tenant_id",postgresql.UUID(as_uuid=True),sa.ForeignKey("tenants.id"),nullable=False),sa.Column("kind",sa.String(50),nullable=False),sa.Column("provider",sa.String(80),nullable=False),sa.Column("enabled",sa.Boolean(),nullable=False),sa.Column("config_ref",sa.String(255)),sa.Column("created_at",sa.DateTime(timezone=True),nullable=False),sa.UniqueConstraint("tenant_id","provider","kind"))
 op.create_table("grievances",sa.Column("id",postgresql.UUID(as_uuid=True),primary_key=True),sa.Column("tenant_id",postgresql.UUID(as_uuid=True),sa.ForeignKey("tenants.id"),nullable=False),sa.Column("submitted_by",postgresql.UUID(as_uuid=True),sa.ForeignKey("users.id"),nullable=False),sa.Column("category",sa.String(80),nullable=False),sa.Column("subject",sa.String(180),nullable=False),sa.Column("description",sa.Text(),nullable=False),sa.Column("status",sa.String(30),nullable=False),sa.Column("created_at",sa.DateTime(timezone=True),nullable=False))
 op.create_table("assets",sa.Column("id",postgresql.UUID(as_uuid=True),primary_key=True),sa.Column("tenant_id",postgresql.UUID(as_uuid=True),sa.ForeignKey("tenants.id"),nullable=False),sa.Column("asset_code",sa.String(80),nullable=False),sa.Column("name",sa.String(160),nullable=False),sa.Column("category",sa.String(80),nullable=False),sa.Column("status",sa.String(30),nullable=False),sa.UniqueConstraint("tenant_id","asset_code"))
def downgrade():
 op.drop_table("assets");op.drop_table("grievances");op.drop_table("integrations")
