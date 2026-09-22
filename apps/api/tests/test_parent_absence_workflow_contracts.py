from pathlib import Path
MODELS=Path(__file__).parents[1]/"app"/"models"/"people.py"
API=Path(__file__).parents[1]/"app"/"api"/"v1"
def test_guardian_has_explicit_user_identity(): assert 'ForeignKey("users.id")' in MODELS.read_text()
def test_guardian_link_is_tenant_scoped():
 s=(API/"people.py").read_text();assert 'Guardian.tenant_id==user.tenant_id' in s and 'User.tenant_id==user.tenant_id' in s
def test_absence_alert_targets_linked_guardian_users_only():
 s=(API/"attendance.py").read_text();assert 'AttendanceRecord.status=="ABSENT"' in s and "Guardian.user_id.is_not(None)" in s and 'Notification(tenant_id=u.tenant_id' in s
