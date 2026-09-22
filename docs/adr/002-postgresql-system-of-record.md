# ADR-002: PostgreSQL as System of Record

Status: Accepted

PostgreSQL is the authoritative transactional data store. Redis is supporting infrastructure and object storage holds private files; neither replaces PostgreSQL for business state.
