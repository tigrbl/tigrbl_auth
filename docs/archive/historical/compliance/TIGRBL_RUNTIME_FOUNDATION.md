<!-- NON_AUTHORITATIVE_HISTORICAL -->

> [!WARNING]
> Historical checkpoint / planning note — non-authoritative for the current release.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and `CERTIFICATION_STATUS.md` for current release truth.

> [!WARNING] Historical / non-authoritative document. This file is retained for provenance or implementation context only. Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md` and the generated current-state reports for current release truth.

> **Historical / non-authoritative** — This document is retained for planning or provenance only.
> Do **not** use it to determine the current certification state, executable surface, or release readiness.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and `CERTIFICATION_STATUS.md` instead.

# runtime-foundation checkpoint — Tigrbl-only Runtime Foundation

This checkpoint completes the runtime-foundation checkpoint runtime-foundation tasks requested for
the migration program.

Completed in this checkpoint:
- removed release-path framework fallbacks from active runtime entry paths
- rewrote `tigrbl_auth/framework.py` to a Tigrbl-only import surface
- replaced private/non-public Tigrbl imports used in active runtime files
- corrected auth context constant import to `tigrbl.config.constants`
- finalized `plugin.py` and `gateway.py` as explicit Tigrbl composition roots
- removed `hasattr(...)` release-path fallback checks from app/plugin/lifecycle
- extended no-FastAPI/Starlette verification to runtime package, tests,
  scripts, and packaging metadata
- added `tigrbl-auth verify --scope runtime-foundation`
- generated updated runtime foundation and no-FastAPI/Starlette reports

Honest status:
- this checkpoint completes the runtime-foundation checkpoint foundation work listed above
- the repository is still **not yet certifiably fully RFC compliant**
- wrapper replacement, contract generation, full CLI, evidence, interop,
  and peer certification work remain open for later s
