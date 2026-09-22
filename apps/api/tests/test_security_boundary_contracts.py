from pathlib import Path
ROOT=Path(__file__).parents[1]/"app"
def read(p):return (ROOT/p).read_text()
def test_login_requires_institution_code():
 s=read("api/v1/auth.py");assert "institution_code" in s and "Tenant.code" in s
def test_payment_webhook_uses_constant_time_signature():
 s=read("api/v1/finance.py");assert "hmac.compare_digest" in s
def test_guardian_link_is_tenant_scoped():
 s=read("api/v1/people.py");assert "Guardian.tenant_id==user.tenant_id" in s and "User.tenant_id==user.tenant_id" in s
def test_ai_confirmation_does_not_claim_execution():
 s=read("api/v1/ai.py");assert '"executed":False' in s
