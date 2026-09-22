from app.models.people import Guardian,StudentGuardian,Staff,TeacherAssignment
def test_people_tables_are_tenant_owned():
    for model in [Guardian,StudentGuardian,Staff,TeacherAssignment]: assert "tenant_id" in model.__table__.columns
def test_guardian_link_has_relationship():
    assert "relationship" in StudentGuardian.__table__.columns
def test_teacher_assignment_links_section():
    assert "section_id" in TeacherAssignment.__table__.columns
