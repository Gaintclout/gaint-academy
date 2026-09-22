"""secure sessions"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
revision="0002_sessions"; down_revision="0001_identity_foundation"; branch_labels=None; depends_on=None
def upgrade():
    op.create_table("sessions",
      sa.Column("id",postgresql.UUID(as_uuid=True),primary_key=True),
      sa.Column("tenant_id",postgresql.UUID(as_uuid=True),sa.ForeignKey("tenants.id"),nullable=False),
      sa.Column("user_id",postgresql.UUID(as_uuid=True),sa.ForeignKey("users.id"),nullable=False),
      sa.Column("token_hash",sa.String(64),nullable=False,unique=True),
      sa.Column("expires_at",sa.DateTime(timezone=True),nullable=False),
      sa.Column("revoked_at",sa.DateTime(timezone=True)),
      sa.Column("created_at",sa.DateTime(timezone=True),nullable=False))
    op.create_index("ix_sessions_user_id","sessions",["user_id"])
    op.create_index("ix_sessions_tenant_id","sessions",["tenant_id"])
def downgrade(): op.drop_table("sessions")
