from app.models.campus import Integration,Grievance,Asset
def test_campus_tables_are_tenant_owned():
 for model in [Integration,Grievance,Asset]:assert "tenant_id" in model.__table__.columns
def test_integration_does_not_store_plain_credentials():
 assert "secret" not in Integration.__table__.columns and "password" not in Integration.__table__.columns
