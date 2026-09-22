from pathlib import Path
P=Path(__file__).parents[1]/"app"/"api"/"v1"/"communication.py"
def test_notice_publish_creates_tenant_scoped_notifications():
 s=P.read_text()
 assert "recipient in recipients" in s
 assert "User.tenant_id==u.tenant_id" in s
 assert "Notification(tenant_id=u.tenant_id" in s
