from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read_api(p):return (ROOT/"app"/p).read_text(encoding="utf-8")
def read_web(p):return (ROOT.parent/"web"/p).read_text(encoding="utf-8")

def test_learning_reads_are_scope_aware_and_publish_controlled():
 s=read_api("api/v1/learning.py")
 for phrase in [
  'def _visible_course_ids',
  '@router.get("/assignments")',
  '@router.post("/assignments/{assignment_id}/publish")',
  '@router.get("/assessments")',
  '@router.get("/courses/{course_id}/roster")',
  '@router.get("/assessment-results")',
  'Assignment.status=="PUBLISHED"',
  'Assessment.status=="PUBLISHED"',
 ]:
  assert phrase in s

def test_learning_ui_covers_teacher_and_student_uat_flows():
 s=read_web("app/learning/page.tsx")
 for phrase in [
  "Create course",
  "Create assignment",
  "Publish",
  "Create assessment",
  "Save marks",
  "Assignment submitted.",
  "Published results",
  "/assessment-results",
 ]:
  assert phrase in s
