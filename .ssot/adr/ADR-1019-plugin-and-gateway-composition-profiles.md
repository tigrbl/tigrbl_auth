# ADR-1019: ADR-0020: Plugin and Gateway Composition Profiles

> [!WARNING] Non-authoritative active document. For current release and certification truth, use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md` and the generated current-state reports.

> **Historical / non-authoritative** — This document is retained for planning, provenance, or operator guidance only.
> Do **not** use it to determine the current certification state, executable surface, or release readiness.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and `CERTIFICATION_STATUS.md` instead.

# ADR-0020: Plugin and Gateway Composition Profiles

## Status
Accepted

## Decision
`tigrbl_auth` shall support both plugin installation into an existing Tigrbl
application and standalone gateway assembly. Both composition styles must
respect the same profile, surface, slice, and boundary rules.

## Consequences
- Plugin and gateway code paths must share the same deployment resolver.
- Downstream consumers may adopt only the public surface, only admin/rpc,
  diagnostics-only, or mixed deployments.
