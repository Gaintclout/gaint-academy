# GAINT Academy Deployment Runbook

## Pre-deployment
1. Use an isolated staging/UAT environment and production-grade secrets.
2. Set APP_ENV, DATABASE_URL, REDIS_URL, COOKIE_SECURE=true, CORS_ORIGINS, object-storage credentials and PAYMENT_WEBHOOK_SECRET through the deployment secret store.
3. Never use the example seed password in production. Do not expose PostgreSQL, Redis or object-storage administration ports publicly.
4. Back up PostgreSQL and verify the backup artifact before migration.
5. Run the same application revision through UAT before production.

## Database
Run `alembic upgrade head` as an explicit release step. Record the previous revision and the new revision. Do not depend on multiple application replicas racing to migrate the database.

## Application
Deploy API, then verify `/health/live` and `/health/ready`; deploy Web after API readiness. Terminate TLS at the approved reverse proxy/load balancer and forward only required headers.

## Smoke test
Verify tenant login, dashboard, student read, attendance, notices/notifications and a non-monetary payment-webhook signature rejection test. Do not run a real charge as a generic smoke test.

## Rollback
1. Stop new traffic or return the release to maintenance mode.
2. Roll application images back to the previous known-good revision.
3. Database downgrade is not automatic. Use a tested migration-specific downgrade only when data compatibility has been reviewed.
4. Restore the pre-deployment database backup when a destructive migration/data incident requires it.
5. Re-run health and tenant-isolation smoke tests.

## Evidence
Retain release SHA, image digests, migration revision, UAT approval, backup identifier, deployment timestamps, smoke-test result, rollback decision and operator identity.
