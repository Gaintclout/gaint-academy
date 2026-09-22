from pathlib import Path
ROOT=Path(__file__).parents[1]/"app"
def test_payment_order_has_tenant_idempotency():
 s=(ROOT/"models"/"finance.py").read_text();assert '"tenant_id","idempotency_key"' in s and '"tenant_id","provider_order_id"' in s
def test_payment_order_api_is_tenant_scoped_and_audited():
 s=(ROOT/"api"/"v1"/"finance.py").read_text();assert "PaymentOrder.tenant_id==u.tenant_id" in s and "finance.payment_order.created" in s and "idempotent_replay" in s
