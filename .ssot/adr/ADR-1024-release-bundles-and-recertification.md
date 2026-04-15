# ADR-1024: Release bundles and recertification

> [!WARNING] Non-authoritative active document. For current release and certification truth, use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md` and the generated current-state reports.

> **Historical / non-authoritative** — This document is retained for planning, provenance, or operator guidance only.
> Do **not** use it to determine the current certification state, executable surface, or release readiness.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and `CERTIFICATION_STATUS.md` instead.

# Release bundles and recertification

- Status: accepted
- Decision: release bundles SHALL contain claims, evidence, contracts, ADR index, and peer refs; recertification SHALL track standards-boundary and Tigrbl changes.
- Consequences: releases fail closed when governance inputs drift.
