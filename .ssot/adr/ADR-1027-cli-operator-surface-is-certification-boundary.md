# ADR-1027: CLI operator surface is part of the certification boundary

> [!WARNING] Non-authoritative active document. For current release and certification truth, use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md` and the generated current-state reports.

> **Historical / non-authoritative** — This document is retained for planning, provenance, or operator guidance only.
> Do **not** use it to determine the current certification state, executable surface, or release readiness.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and `CERTIFICATION_STATUS.md` instead.

# CLI operator surface is part of the certification boundary

- Status: accepted
- Date: 2026-03-22
- Decision: the CLI operator plane is a first-class certification boundary. `serve` MUST launch runtime, `keys` is the canonical command family, and no public strict independent wording is allowed without Tier 4 promotion.
- Consequences:
  - "fully featured" package claims include runtime, CLI, lifecycle, and release surfaces, not only RFC/OIDC protocol behavior;
  - plan-only `serve` behavior must be documented as incomplete until runtime launch is implemented;
  - catalog-only or list/show-only admin families remain partial and MUST stay below full-featured claims;
  - `key` is removed from the certified public operator surface in favor of the canonical `keys` command family;
  - public "independent" wording requires Tier 4 preserved peer evidence and manifest-backed promotion.
