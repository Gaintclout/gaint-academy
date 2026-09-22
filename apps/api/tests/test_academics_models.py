from app.models.academics import AcademicYear,AcademicClass,Section,Student,Enrollment
def test_academic_tables_are_tenant_owned():
    for model in [AcademicYear,AcademicClass,Section,Student,Enrollment]:
        assert "tenant_id" in model.__table__.columns
def test_student_admission_number_is_required():
    assert Student.__table__.columns["admission_no"].nullable is False
def test_enrollment_links_academic_structure():
    cols=Enrollment.__table__.columns
    for name in ["student_id","academic_year_id","class_id","section_id"]:
        assert name in cols
