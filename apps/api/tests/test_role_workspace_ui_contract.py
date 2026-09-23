from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read_web(p):return (ROOT.parent/"web"/p).read_text(encoding="utf-8")

def test_role_workspaces_gate_write_controls_by_permissions():
 cases={
  "app/attendance/page.tsx":["attendance.session.create","canCreate"],
  "app/learning/page.tsx":["learning.course.manage","canCourse"],
  "app/finance/page.tsx":["finance.plan.manage","canPlan"],
  "app/communication/page.tsx":["communication.notice.manage","canManage"],
 }
 for path,phrases in cases.items():
  s=read_web(path)
  for phrase in phrases: assert phrase in s

def test_family_users_get_read_only_surfaces():
 attendance=read_web("app/attendance/page.tsx")
 finance=read_web("app/finance/page.tsx")
 communication=read_web("app/communication/page.tsx")
 assert "/attendance/records" in attendance and "Attendance history" in attendance
 assert "/finance/invoices" in finance and "Invoices" in finance
 assert "/notices" in communication and "Published notices" in communication

def test_reports_do_not_redirect_non_auth_errors_to_login():
 s=read_web("app/reports/page.tsx")
 assert "isAuthError(e)" in s
 assert "Unable to load report" in s
