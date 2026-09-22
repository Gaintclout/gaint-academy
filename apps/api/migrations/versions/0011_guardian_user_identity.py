"""guardian authenticated user identity"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
revision="0011_guardian_user_identity";down_revision="0010_ai_governance";branch_labels=None;depends_on=None
def upgrade():
 op.add_column("guardians",sa.Column("user_id",postgresql.UUID(as_uuid=True),sa.ForeignKey("users.id"),nullable=True))
 op.create_index("ix_guardians_user_id","guardians",["user_id"])
def downgrade():
 op.drop_index("ix_guardians_user_id",table_name="guardians");op.drop_column("guardians","user_id")
