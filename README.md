# GAINT Academy

AI-powered unified education and campus management platform.

## Stage 0 Foundation

Architecture v1.0 baseline:
- Next.js + TypeScript frontend
- FastAPI + Python backend
- PostgreSQL
- Redis
- MinIO / S3-compatible object storage
- Alembic migrations
- Docker Compose
- Tenant-aware RBAC and audit foundation

Development OS: Windows

Seed administrator email: `gaintclout@gmail.com`

> The development administrator password must be supplied through environment configuration and must never be committed to Git.

## Development sequence

Stage 0 Foundation → Vertical Slice 1 → Vertical Slice 2 → Domain Modules → QA/UAT → Pilot → Production.
