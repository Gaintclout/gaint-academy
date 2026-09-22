"""ai governance"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
revision="0010_ai_governance";down_revision="0009_campus_integrations";branch_labels=None;depends_on=None
def upgrade():
 op.create_table("ai_conversations",sa.Column("id",postgresql.UUID(as_uuid=True),primary_key=True),sa.Column("tenant_id",postgresql.UUID(as_uuid=True),sa.ForeignKey("tenants.id"),nullable=False),sa.Column("user_id",postgresql.UUID(as_uuid=True),sa.ForeignKey("users.id"),nullable=False),sa.Column("title",sa.String(180),nullable=False),sa.Column("created_at",sa.DateTime(timezone=True),nullable=False))
 op.create_table("ai_messages",sa.Column("id",postgresql.UUID(as_uuid=True),primary_key=True),sa.Column("tenant_id",postgresql.UUID(as_uuid=True),sa.ForeignKey("tenants.id"),nullable=False),sa.Column("conversation_id",postgresql.UUID(as_uuid=True),sa.ForeignKey("ai_conversations.id"),nullable=False),sa.Column("role",sa.String(20),nullable=False),sa.Column("content",sa.Text(),nullable=False),sa.Column("sources_json",sa.Text()),sa.Column("created_at",sa.DateTime(timezone=True),nullable=False))
 op.create_table("ai_action_proposals",sa.Column("id",postgresql.UUID(as_uuid=True),primary_key=True),sa.Column("tenant_id",postgresql.UUID(as_uuid=True),sa.ForeignKey("tenants.id"),nullable=False),sa.Column("user_id",postgresql.UUID(as_uuid=True),sa.ForeignKey("users.id"),nullable=False),sa.Column("action_type",sa.String(100),nullable=False),sa.Column("payload_json",sa.Text(),nullable=False),sa.Column("status",sa.String(30),nullable=False),sa.Column("created_at",sa.DateTime(timezone=True),nullable=False))
def downgrade():
 op.drop_table("ai_action_proposals");op.drop_table("ai_messages");op.drop_table("ai_conversations")
