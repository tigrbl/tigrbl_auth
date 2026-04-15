# ADR-1021: CLI metadata as the single source

> [!WARNING] Non-authoritative active document. For current release and certification truth, use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md` and the generated current-state reports.

> **Historical / non-authoritative** — This document is retained for planning, provenance, or operator guidance only.
> Do **not** use it to determine the current certification state, executable surface, or release readiness.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and `CERTIFICATION_STATUS.md` instead.

# CLI metadata as the single source

- Status: accepted
- Decision: argparse help text and generated CLI documentation SHALL both derive from `tigrbl_auth.cli.metadata`.
- Consequences: flag drift is caught by regeneration and contract/report automation.
