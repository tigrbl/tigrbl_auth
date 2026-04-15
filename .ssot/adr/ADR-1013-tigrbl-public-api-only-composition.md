# ADR-1013: Tigrbl public-API-only composition is mandatory in release paths

> [!WARNING] Non-authoritative active document. For current release and certification truth, use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md` and the generated current-state reports.

> **Historical / non-authoritative** — This document is retained for planning, provenance, or operator guidance only.
> Do **not** use it to determine the current certification state, executable surface, or release readiness.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and `CERTIFICATION_STATUS.md` instead.

# Tigrbl public-API-only composition is mandatory in release paths

- Status: Accepted
- Date: 2026-03-20

## Context

`tigrbl_auth` is intended to be a Tigrbl-native authn/z package. Release paths
must therefore compose the runtime through Tigrbl's documented public API rather
than private Tigrbl modules, alternate framework fallbacks, or ad-hoc framework
capability checks.

## Decision

Release-path composition code in `framework.py`, `plugin.py`, `gateway.py`,
`api/app.py`, `api/lifecycle.py`, and `app.py` shall:

- import Tigrbl only through public modules and documented public surfaces,
- avoid private `tigrbl._*` imports,
- avoid `tigrbl_core` imports,
- avoid release-path `hasattr(...)` framework capability fallbacks,
- remain free of direct FastAPI and Starlette imports and dependencies.

## Consequences

- package composition becomes stricter and easier to certify,
- runtime foundation verification can fail closed on private-import or
  fallback regressions,
- some compatibility behavior is intentionally removed from release paths,
- deeper persistence/runtime refactors remain allowed in later phases, but they
  may not reintroduce non-public framework composition.
