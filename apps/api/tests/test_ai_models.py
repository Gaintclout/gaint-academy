from app.models.ai import AIConversation,AIMessage,AIActionProposal
def test_ai_tables_are_tenant_owned():
 for model in [AIConversation,AIMessage,AIActionProposal]:assert "tenant_id" in model.__table__.columns
def test_ai_action_requires_explicit_state():assert "status" in AIActionProposal.__table__.columns
