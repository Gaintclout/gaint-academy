# GAINT Academy v1.1 Final UAT Execution Guide

This guide is the final runtime validation layer for the v1.1 release candidate. CI verifies builds, migrations, contract tests, tenant/IDOR integration tests and dependency audit; it does not replace browser UAT.

## 1. Update local canonical branch

Use the canonical upstream repository only:

```powershell
git fetch upstream
git pull upstream main
```

Do not use or modify unrelated Docker projects.

## 2. Rebuild GAINT Academy only

```powershell
docker compose up -d --build
docker compose ps
```

Expected GAINT Academy services: web, api, postgres, redis and minio.

## 3. Automated local smoke

The script never stores credentials in the repository.

Optional authenticated checks use temporary PowerShell environment variables:

```powershell
$env:GAINT_UAT_ADMIN_EMAIL="<admin-email>"
$env:GAINT_UAT_ADMIN_PASSWORD="<admin-password>"
powershell -ExecutionPolicy Bypass -File scripts/uat_smoke.ps1
```

Without those variables the script still checks API live/ready, Web login and invalid-login rejection.

## 4. Role-by-role runtime matrix

| Role | Required runtime checks |
| --- | --- |
| Institution Admin | Academics setup; Student 360; guardian/parent account; student account; staff/teacher account; operational accounts |
| Teacher | Only assigned sections; attendance roster; courses; assignments; assessments; marks; no finance administration |
| Student | Own Student 360 only; submitted attendance; enrolled courses; published assignments/results; own invoices |
| Parent | Linked children only; submitted attendance; linked-child learning/results; linked-child invoices; notices |
| Accounts | Finance workspace only as granted; create invoice; record confirmed payment; no academic administration |
| HR | Staff workspace only as granted; no finance or academic administration |
| Campus Admin | Integrations, assets and grievance queue; no finance KPI/workflow |
| Auditor | Reports and audit events read-only; no mutation controls |

## 5. Security runtime checks

Verify:
- wrong-tenant login fails;
- five repeated failed logins trigger rate limiting;
- successful login clears the failed-login counter;
- mutation without CSRF fails;
- logout revokes the session and clears cookies;
- Parent cannot open an unlinked Student ID;
- Student cannot open another Student ID;
- Teacher cannot access an unassigned section;
- payment initiation cannot target another family's invoice;
- Auditor has no write controls.

## 6. Responsive/browser checks

Run the major pages at approximately 1440px, 1024px, 768px and 390px widths:
login, dashboard, academics, students, Student 360, staff, attendance, learning, finance, communication, campus, reports and settings.

Record any overflow, clipped controls, unreadable tables, inaccessible buttons or broken navigation as defects.

## 7. Release evidence

For every P0 item in `docs/UAT_CHECKLIST.md`, record tester, date/time, role, tenant, expected result, actual result, PASS/FAIL and screenshot/log reference.

Do not mark v1.1 pilot-ready until all P0 items pass, backup/restore rehearsal is complete, and the release-candidate CI is green.
