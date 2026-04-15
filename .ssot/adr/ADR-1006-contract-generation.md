# ADR-1006: Generate OpenAPI and OpenRPC artifacts

> [!WARNING] Non-authoritative active document. For current release and certification truth, use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md` and the generated current-state reports.

> **Historical / non-authoritative** — This document is retained for planning, provenance, or operator guidance only.
> Do **not** use it to determine the current certification state, executable surface, or release readiness.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and `CERTIFICATION_STATUS.md` instead.

# Generate OpenAPI and OpenRPC artifacts

- Status: Accepted
- Date: 2026-03-19

## Context

The public HTTP contract is expressed through OpenAPI 3.1 and the internal
admin/control-plane contract through OpenRPC. Contract drift is a release
gate.

## Decision

This ADR is accepted for the current repository checkpoint.

## Consequences

- Architectural traceability is required.
- Standards claims must map to code, tests, and evidence.
