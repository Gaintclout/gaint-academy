from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
def read(path):return (ROOT/path).read_text(encoding="utf-8")

def test_final_uat_execution_assets_exist_and_are_linked():
 readme=read("README.md")
 assert "docs/V1_1_UAT_EXECUTION.md" in readme
 assert "scripts/uat_smoke.ps1" in readme
 read("docs/V1_1_UAT_EXECUTION.md")
 read("scripts/uat_smoke.ps1")

def test_smoke_runner_checks_health_invalid_login_and_optional_auth():
 s=read("scripts/uat_smoke.ps1")
 for phrase in [
  "/health/live",
  "/health/ready",
  "/api/v1/auth/login",
  "Invalid login rejected",
  "GAINT_UAT_ADMIN_EMAIL",
  "GAINT_UAT_ADMIN_PASSWORD",
  "/api/v1/auth/csrf",
  "/api/v1/auth/logout",
 ]:
  assert phrase in s

def test_uat_guide_covers_all_core_roles_and_responsive_checks():
 s=read("docs/V1_1_UAT_EXECUTION.md")
 for phrase in [
  "Institution Admin",
  "Teacher",
  "Student",
  "Parent",
  "Accounts",
  "HR",
  "Campus Admin",
  "Auditor",
  "390px",
  "backup/restore rehearsal",
 ]:
  assert phrase in s
