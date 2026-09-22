# GAINT Academy v1.0.0-rc1

## Pilot scope
GAINT Academy MVP provides tenant-aware institution access, campuses/users/RBAC/audit, academic setup, students/guardians/staff, timetable and attendance, learning/assessment foundations, finance/invoicing/payment-order foundations, notices/in-app notifications, campus/integration registry foundations, reports and governed GAINT AI placeholder workflows.

## Security and reliability gates included
Institution-code tenant resolution, permission checks, critical-action audit events, tenant-safe guardian identity links, attendance completeness checks, idempotent payment orders, signed payment webhook boundary, PostgreSQL migration CI, web dependency audit and UAT/deployment runbooks.

## Important release boundaries
This candidate is for controlled pilot/UAT. It does not by itself establish production readiness. Real online payment acceptance requires an approved provider adapter/configuration and provider-specific verification testing. GAINT AI does not yet call a live model or RAG service. Advanced campus modules and native apps remain later releases.
