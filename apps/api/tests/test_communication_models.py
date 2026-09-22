from app.models.communication import Notice,Notification
def test_communication_tables_are_tenant_owned():
 for model in [Notice,Notification]:assert "tenant_id" in model.__table__.columns
def test_notification_is_user_scoped():assert "user_id" in Notification.__table__.columns
