# GAINT Academy UAT Checklist

## Release gate
Do not approve pilot deployment until every P0 item passes in the target environment.

## P0 acceptance
- [ ] Institution-code login succeeds for the correct tenant and fails across tenants.
- [ ] Institution Admin can create academic year, class, section, student, guardian and staff.
- [ ] Guardian identity linking cannot cross tenant boundaries.
- [ ] Timetable read/write permissions are enforced.
- [ ] Attendance cannot submit until the active roster is complete.
- [ ] Submitted absences create notifications only for explicitly linked guardian users.
- [ ] Course, assignment, assessment and marks respect tenant/enrollment boundaries.
- [ ] Assessment publication is one-way from DRAFT and is audited.
- [ ] Fee plan and invoice creation are tenant scoped.
- [ ] Duplicate payment-order idempotency keys do not create duplicate orders.
- [ ] Invalid payment webhook signatures are rejected.
- [ ] Replayed confirmed payment references do not duplicate payments.
- [ ] Published notices create in-app notifications only inside the tenant.
- [ ] AI remains SAFE_PLACEHOLDER unless an approved provider/retrieval adapter is configured.
- [ ] AI action confirmation reports executed=false.
- [ ] Critical state changes appear in audit records.
- [ ] /health/live and /health/ready return healthy status.
- [ ] Alembic upgrade head succeeds against a clean PostgreSQL database.
- [ ] Backup and restore procedure has been tested with a disposable database.

## UAT evidence
Record tester, environment, date/time, test data IDs, expected result, actual result, PASS/FAIL, defect link and retest result for every P0 item.

## Pilot decision
Pilot approval requires zero open P0 defects. P1 defects require an owner, workaround and agreed remediation date.
