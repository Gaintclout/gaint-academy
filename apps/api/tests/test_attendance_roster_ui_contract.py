from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read_api(p):return (ROOT/"app"/p).read_text(encoding="utf-8")
def read_web(p):return (ROOT.parent/"web"/p).read_text(encoding="utf-8")

def test_attendance_sections_and_roster_are_tenant_scoped():
 s=read_api("api/v1/attendance.py")
 assert '@router.get("/attendance/sections")' in s
 assert '@router.get("/attendance/roster")' in s
 assert "Section.tenant_id==u.tenant_id" in s
 assert "Enrollment.tenant_id==u.tenant_id" in s
 assert "Student.tenant_id==u.tenant_id" in s
 assert "require_teacher_section(db,u,section_id)" in s

def test_attendance_ui_supports_full_roster_marking():
 s=read_web("app/attendance/page.tsx")
 for phrase in [
  "/attendance/sections",
  "/attendance/roster?section_id=",
  'method:"PUT"',
  "Save roster",
  "Submit attendance",
  "PRESENT",
  "ABSENT",
  "LATE",
  "EXCUSED",
 ]:
  assert phrase in s
