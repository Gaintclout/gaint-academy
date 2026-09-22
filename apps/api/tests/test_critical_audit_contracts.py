from pathlib import Path
ROOT=Path(__file__).parents[1]/"app"/"api"/"v1"
def source(name):return (ROOT/name).read_text()
def test_attendance_submit_audited(): assert "attendance.submitted" in source("attendance.py")
def test_assessment_publish_audited(): assert "assessment.published" in source("learning.py")
def test_finance_payment_audited(): assert "finance.payment.confirmed" in source("finance.py")
def test_notice_publish_audited(): assert "notice.published" in source("communication.py")
def test_ai_confirmation_audited(): assert "ai.action.confirmed" in source("ai.py")
