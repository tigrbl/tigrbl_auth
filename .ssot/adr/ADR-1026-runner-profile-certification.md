# ADR-1026: Runner profile certification

> [!WARNING] Non-authoritative active document. For current release and certification truth, use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md` and the generated current-state reports.

> **Historical / non-authoritative** — This document is retained for planning, provenance, or operator guidance only.
> Do **not** use it to determine the current certification state, executable surface, or release readiness.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and `CERTIFICATION_STATUS.md` instead.

# Runner profile certification

- Status: accepted
- Date: 2026-03-22
- Decision: `tigrbl_auth` is certified as an **ASGI 3 application package**, not as a single bundled HTTP server. Runtime claims are made per supported runner profile.
- Consequences:
  - runner-backed serving claims MUST be profile-qualified rather than collapsed into one undifferentiated server claim;
  - `Uvicorn`, `Hypercorn`, and `Tigrcorn` are separate runtime profiles for certification and peer evidence;
  - the core package boundary remains server-agnostic and centers on the ASGI 3 app factory, deployment resolution, mounted surfaces, and contracts;
  - runtime profile claims MAY be declared before full implementation, but they MUST stay below Tier 3 until executable launch, tests, evidence, and gates exist;
  - blanket "bundled server" language is prohibited in current-state, certification, and release documents.
