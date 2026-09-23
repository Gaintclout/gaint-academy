from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def api(p):return (ROOT/"app"/p).read_text(encoding="utf-8")
def web(p):return (ROOT.parent/"web"/p).read_text(encoding="utf-8")

def test_campus_admin_workflows_are_tenant_scoped_and_audited():
 s=api("api/v1/campus.py")
 for phrase in [
  '@router.post("/integrations/{integration_id}/toggle")',
  '@router.patch("/grievances/{grievance_id}/status")',
  '@router.get("/assets")',
  '@router.patch("/assets/{asset_id}/status")',
  "Integration.tenant_id==u.tenant_id",
  "Grievance.tenant_id==u.tenant_id",
  "Asset.tenant_id==u.tenant_id",
  "AuditEvent",
 ]:
  assert phrase in s

def test_auditor_feed_is_read_only_and_tenant_scoped():
 s=api("api/v1/reports.py")
 assert '@router.get("/audit-events")' in s
 assert '"audit.event.view"' in s
 assert "AuditEvent.tenant_id==u.tenant_id" in s
 assert ".limit(limit)" in s

def test_campus_and_auditor_ui_cover_uat_paths():
 campus=web("app/campus/page.tsx")
 reports=web("app/reports/page.tsx")
 for phrase in ["Add integration","Integrations","Add asset","Grievance queue","/assets/","/grievances/"]:
  assert phrase in campus
 for phrase in ["Audit events","/reports/audit-events","Read-only tenant audit trail"]:
  assert phrase in reports
