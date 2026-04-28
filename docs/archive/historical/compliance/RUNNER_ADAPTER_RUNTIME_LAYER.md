<!-- NON_AUTHORITATIVE_HISTORICAL -->

> [!WARNING]
> Historical checkpoint / planning note — non-authoritative for the current release.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and `CERTIFICATION_STATUS.md` for current release truth.

> [!WARNING] Historical / non-authoritative document. This file is retained for provenance or implementation context only. Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md` and the generated current-state reports for current release truth.

> **Historical / non-authoritative** — This document is retained for planning or provenance only.
> Do **not** use it to determine the current certification state, executable surface, or release readiness.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and `CERTIFICATION_STATUS.md` instead.

# persistence-domain checkpoint — Runner-Adapter Runtime Layer

## Objective

Separate the ASGI application from any single server process and introduce a common runtime contract for Uvicorn, Hypercorn, and Tigrcorn runner profiles.

## Completed in this checkpoint

- added a dedicated runtime package:
  - `tigrbl_auth/runtime/__init__.py`
  - `tigrbl_auth/runtime/types.py`
  - `tigrbl_auth/runtime/base.py`
  - `tigrbl_auth/runtime/plan.py`
  - `tigrbl_auth/runtime/registry.py`
  - `tigrbl_auth/runtime/uvicorn.py`
  - `tigrbl_auth/runtime/hypercorn.py`
  - `tigrbl_auth/runtime/tigrcorn.py`
- introduced a `RunnerAdapter` abstraction with:
  - adapter-declared capabilities
  - adapter-declared flag metadata
  - adapter-level validation and diagnostics
  - availability detection without forcing a runner import at package import time
- introduced `RuntimePlan` and runtime-plan manifests with separate:
  - application manifest
  - runtime manifest
  - application hash
  - runtime hash
- added runtime-plan hashing so the application hash is runner-invariant while runtime hashes remain runner-qualified
- refactored `tigrbl_auth/api/app.py` so the exported ASGI object is lazy and server-agnostic at import time
- refactored `tigrbl_auth/app.py` to re-export the lazy package app and runtime-plan helpers
- refactored `tigrbl_auth/plugin.py` to remove top-level Tigrbl coupling and keep deployment/app installation lazy
- refactored `tigrbl_auth/gateway.py` to expose a lazy gateway app and runtime-plan helper
- updated the CLI metadata and handlers so `serve` now produces a runner-qualified runtime plan rather than a runner-agnostic plan payload
- updated the doctor and state reports to include runner registry and runtime-application-hash invariance data
- added unit coverage for the runtime adapter layer and CLI parser integration
- updated runtime target manifests, module mappings, test mappings, and public operator surface manifests for the new runtime layer

## Direct validation completed in this checkpoint

- imported the lazy API, package, and gateway ASGI app exports without requiring a server process launch
- generated runtime plans for `uvicorn`, `hypercorn`, and `tigrcorn`
- verified that application hashes remain invariant across registered runners
- verified that runtime hashes remain runner-qualified
- verified that the CLI parser now accepts `serve --server {uvicorn,hypercorn,tigrcorn}`
- regenerated CLI docs, certification scope, effective manifests, state reports, release bundle artifacts, and release signatures

## Truthful status after persistence-domain checkpoint

This checkpoint establishes the executable substrate needed for real runtime launch and runner-profile certification.

It does **not** yet make the package certifiably fully featured or certifiably fully RFC/spec compliant.

Remaining blockers still include:

- `serve` still does **not** launch runtime; it now emits a runner-qualified runtime plan through the adapter layer, but launch behavior remains a later - the Tigrcorn runner profile is implemented at the adapter-contract layer, but the install profile remains metadata-only in packaging and Tigrcorn was not installed in this container
- operator families remain incomplete and are not yet lifecycle-complete
- full Tier 3 closure across the retained boundary is still incomplete
- Tier 4 independent peer bundles are still absent

## Validation still blocked in this container

- full `pytest` execution remains blocked because the container does not have the published dependency set installed; test collection still fails early on `import tigrbl`
- end-to-end runtime launch was not certified in this because `serve` is not yet a launcher and the runtime profiles are not yet part of a Tier 3 preserved evidence path

## Boundary note

The new `tigrbl_auth/runtime/**` package is mapped into the certified core boundary in this checkpoint so the runtime adapter layer is treated as an in-scope certified implementation substrate rather than an orphaned implementation path.
