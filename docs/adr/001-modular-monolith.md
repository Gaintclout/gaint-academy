# ADR-001: Modular Monolith for V1

Status: Accepted

GAINT Academy V1 uses a modular monolith with explicit domain boundaries. Domain modules must not bypass service/repository authorization boundaries. Extraction into independent services is deferred until operational evidence justifies it.
