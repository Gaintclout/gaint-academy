from pathlib import Path
ROOT=Path(__file__).parents[1]/"app"/"api"/"v1"
def text(name):return (ROOT/name).read_text()
def test_student_permissions_are_domain_specific():
 s=text("students.py");assert "students.student.view" in s and "students.student.create" in s
def test_timetable_read_requires_permission():
 assert 'require(db,u,"timetable.slot.view")' in text("attendance.py")
def test_attendance_submit_checks_completeness():
 s=text("attendance.py");assert "Attendance is incomplete" in s and 's.status!="DRAFT"' in s
def test_learning_checks_enrollment_and_supports_submission():
 s=text("learning.py");assert "learning.submission.create" in s and "actively enrolled" in s
def test_notice_publication_is_single_transition():
 s=text("communication.py");assert "communication.notice.view" in s and 'x.status!="DRAFT"' in s
