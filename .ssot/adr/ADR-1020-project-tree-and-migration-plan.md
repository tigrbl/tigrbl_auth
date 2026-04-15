# ADR-1020: ADR-0021: Project tree and migration plan are certification artifacts

> [!WARNING] Non-authoritative active document. For current release and certification truth, use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md` and the generated current-state reports.

> **Historical / non-authoritative** — This document is retained for planning, provenance, or operator guidance only.
> Do **not** use it to determine the current certification state, executable surface, or release readiness.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and `CERTIFICATION_STATUS.md` instead.

# ADR-0021: Project tree and migration plan are certification artifacts

## Decision

The repository shall carry a machine-checkable target tree layout and a
machine-checkable current-to-target move map. Legacy paths remain outside the
certified core until their replacements are complete and boundary-clean.

## Consequences

- tree layout becomes release-gated
- move-map drift becomes release-gated
- legacy paths can remain temporarily, but only as `legacy_transition`
