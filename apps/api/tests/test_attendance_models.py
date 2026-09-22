from app.models.attendance import TimetableSlot,AttendanceSession,AttendanceRecord
def test_attendance_tables_are_tenant_owned():
 for model in [TimetableSlot,AttendanceSession,AttendanceRecord]: assert "tenant_id" in model.__table__.columns
def test_attendance_session_state_exists(): assert "status" in AttendanceSession.__table__.columns
def test_attendance_record_is_student_scoped(): assert "student_id" in AttendanceRecord.__table__.columns
