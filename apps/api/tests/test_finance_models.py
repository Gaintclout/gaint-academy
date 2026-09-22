from app.models.finance import FeePlan,Invoice,Payment
def test_finance_tables_are_tenant_owned():
 for model in [FeePlan,Invoice,Payment]:assert "tenant_id" in model.__table__.columns
def test_money_uses_fixed_precision():
 assert str(FeePlan.__table__.columns["amount"].type)=="NUMERIC(12, 2)"
def test_payment_reference_is_required():
 assert Payment.__table__.columns["reference"].nullable is False
