# GAINT Academy MVP v1.0 Pilot Release Gate

Release candidate: v1.0.0-rc1

## Automated gates
- [ ] CI passes for the exact release commit.
- [ ] API unit/contract tests pass.
- [ ] Web production build and high-severity dependency audit pass.
- [ ] Full Alembic chain applies to a clean PostgreSQL database.

## Environment gates
- [ ] Staging/UAT uses production-like TLS, secure cookies, CORS and secret management.
- [ ] PostgreSQL, Redis and object storage are not publicly exposed.
- [ ] PAYMENT_WEBHOOK_SECRET is configured only when payment webhook testing is enabled.
- [ ] Backup and restore drill is evidenced.

## Functional pilot gates
Complete every P0 item in docs/UAT_CHECKLIST.md and attach evidence.

## Known MVP boundaries
- GAINT AI remains a SAFE_PLACEHOLDER until approved model/RAG adapters are configured.
- Payment gateway is provider-independent; a real provider adapter must be configured and validated before accepting online payments.
- Advanced hostel, library, transport/GPS, biometric, native mobile and advanced AI capabilities are outside this MVP release.
- Production rollout is not authorized solely by merging this checklist.

## Release evidence
Record release SHA, CI run, migration revision, UAT approver, environment, backup ID, smoke-test evidence, known accepted P1 issues and rollback owner.

## Decision
v1.0.0 pilot approval requires all automated gates and all P0 UAT gates to pass with no open P0 defects.
