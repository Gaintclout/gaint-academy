from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read_web(p): return (ROOT.parent/"web"/p).read_text(encoding="utf-8")
def read_api(p): return (ROOT/"app"/p).read_text(encoding="utf-8")

def test_staff_ui_supports_teacher_account_and_assignment():
 s=read_web("app/staff/page.tsx")
 for phrase in ["/teacher-account","/assignments","Create teacher account","Assign section","users.user.create","academics.setup.admin"]:
  assert phrase in s

def test_student360_gates_admin_actions_and_supports_student_login():
 s=read_web("app/students/[id]/page.tsx")
 for phrase in ["students.student.create","users.user.create","academics.setup.admin","/student-account","Create student login"]:
  assert phrase in s

def test_operational_account_provisioning_is_allowlisted():
 s=read_api("api/v1/people.py")
 assert 'OPERATIONAL_ROLE_CODES={"ACCOUNTS","HR","CAMPUS_ADMIN","AUDITOR"}' in s
 assert '@router.post("/users/operational-account"' in s
 assert 'scope_type="TENANT"' in s

def test_settings_exposes_operational_role_account_ui_to_authorized_admin():
 s=read_web("app/settings/page.tsx")
 assert "Operational role accounts" in s
 assert "/users/operational-account" in s
 assert 'me.permissions.includes("users.user.create")' in s
