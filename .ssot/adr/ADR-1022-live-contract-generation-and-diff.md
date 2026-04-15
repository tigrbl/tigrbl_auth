# ADR-1022: Live contract generation and diff

> [!WARNING] Non-authoritative active document. For current release and certification truth, use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md` and the generated current-state reports.

> **Historical / non-authoritative** — This document is retained for planning, provenance, or operator guidance only.
> Do **not** use it to determine the current certification state, executable surface, or release readiness.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and `CERTIFICATION_STATUS.md` instead.

# Live contract generation and diff

- Status: accepted
- Decision: OpenAPI and OpenRPC SHALL be generated from live deployment metadata and validated/diffed in CI.
- Consequences: placeholder or drifting contracts fail release gates.
