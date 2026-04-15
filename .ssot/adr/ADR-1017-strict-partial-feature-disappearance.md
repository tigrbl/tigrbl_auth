# ADR-1017: ADR-0018: Strict Partial Feature Disappearance

> [!WARNING] Non-authoritative active document. For current release and certification truth, use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md` and the generated current-state reports.

> **Historical / non-authoritative** — This document is retained for planning, provenance, or operator guidance only.
> Do **not** use it to determine the current certification state, executable surface, or release readiness.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and `CERTIFICATION_STATUS.md` instead.

# ADR-0018: Strict Partial Feature Disappearance

## Status
Accepted

## Decision
When a downstream deployment disables a profile feature, protocol slice,
surface set, or quarantined extension, that feature shall disappear from the
mounted runtime surface, discovery/metadata output, generated contracts,
claim manifests, and release evidence manifests.

## Consequences
- Partial consumption is certifiable rather than ambiguous.
- Contract and evidence generation must be profile-aware.
- Runtime composition must not leave disabled endpoints mounted.
