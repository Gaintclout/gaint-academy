from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def api(p):return (ROOT/"app"/p).read_text(encoding="utf-8")
def web(p):return (ROOT.parent/"web"/p).read_text(encoding="utf-8")

def test_payment_order_checks_family_and_student_scope():
 s=api("api/v1/finance.py")
 block=s[s.index('@router.post("/payment-orders"'):s.index('class WebhookIn')]
 assert "require_linked_student(db,u,inv.student_id)" in block
 assert "require_self_student(db,u,inv.student_id)" in block

def test_finance_ui_covers_invoice_record_and_initiation_flows():
 s=web("app/finance/page.tsx")
 for phrase in ["Create invoice","Record confirmed payment","Initiate payment","/finance/billable-students","/finance/payment-orders"]:
  assert phrase in s

def test_notice_publish_and_notification_ui_are_complete():
 api_src=api("api/v1/communication.py")
 web_src=web("app/communication/page.tsx")
 assert '@router.get("/notices/drafts")' in api_src
 for phrase in ["/notices/drafts","Notice published.","Mark read","My notifications"]:
  assert phrase in web_src
