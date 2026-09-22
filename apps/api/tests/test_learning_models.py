from app.models.learning import Course,Assignment,Submission,Assessment,AssessmentMark
def test_learning_tables_are_tenant_owned():
 for model in [Course,Assignment,Submission,Assessment,AssessmentMark]:assert "tenant_id" in model.__table__.columns
def test_marks_have_student_and_assessment(): 
 assert "student_id" in AssessmentMark.__table__.columns and "assessment_id" in AssessmentMark.__table__.columns
