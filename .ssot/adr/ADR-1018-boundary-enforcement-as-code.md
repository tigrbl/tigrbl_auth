# ADR-1018: ADR-0019: Boundary Enforcement as Code

> [!WARNING] Non-authoritative active document. For current release and certification truth, use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md` and the generated current-state reports.

> **Historical / non-authoritative** — This document is retained for planning, provenance, or operator guidance only.
> Do **not** use it to determine the current certification state, executable surface, or release readiness.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and `CERTIFICATION_STATUS.md` instead.

# ADR-0019: Boundary Enforcement as Code

## Status
Accepted

## Decision
Boundary decisions shall be enforced by machine-checkable reports and release
gates. At minimum, the repository shall maintain checks for claims hygiene,
framework leakage, wrapper hygiene, contract synchronization, evidence
readiness, and peer-readiness.

## Consequences
- Wrapper modules in certified-core paths block promotion.
- Contract drift blocks release.
- Tier 3 and Tier 4 promotion require evidence-aware checks.
