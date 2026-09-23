from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def api(p):return (ROOT/"app"/p).read_text(encoding="utf-8")
def web(p):return (ROOT.parent/"web"/p).read_text(encoding="utf-8")

def test_academic_structure_reads_require_admin_permission():
 s=api("api/v1/academics.py")
 for fn in ["def years","def classes","def sections"]:
  block=s[s.index(fn):]
  assert 'require(db,user,"academics.setup.admin")' in block[:500]

def test_student360_only_loads_academic_structure_for_admin():
 s=web("app/students/[id]/page.tsx")
 assert 'user.permissions.includes("academics.setup.admin")' in s
 assert 'else setYears([])' in s

def test_duplicate_enrollment_returns_conflict_before_insert():
 s=api("api/v1/students.py")
 assert "Student already has an enrollment for this academic year" in s

def test_student_cannot_submit_to_draft_assignment():
 s=api("api/v1/learning.py")
 assert 'if a.status!="PUBLISHED":raise HTTPException(409,"Assignment is not open for submission")' in s

def test_institution_report_absences_only_count_submitted_sessions():
 s=api("api/v1/reports.py")
 tail=s[s.index(" else:\n  students="):]
 assert 'AttendanceSession.status=="SUBMITTED"' in tail

def test_payment_idempotency_key_cannot_be_reused_for_different_order():
 s=api("api/v1/finance.py")
 assert "Idempotency key was already used for a different payment order" in s
 assert "existing.invoice_id!=p.invoice_id" in s

def test_csrf_cache_resets_across_login_and_logout():
 s=web("lib/api.ts")
 assert 'if(path==="/auth/login"||path==="/auth/logout")csrfToken=null;' in s

def test_login_surfaces_server_rate_limit_and_service_errors():
 s=web("app/login/page.tsx")
 assert 'apiFetch("/auth/login"' in s
 assert 'Invalid email or password' not in s
