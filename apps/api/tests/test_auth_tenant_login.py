from app.api.v1.auth import LoginIn
def test_login_requires_institution_code():
 fields=LoginIn.model_fields
 assert "institution_code" in fields
 assert "email" in fields and "password" in fields
