<!-- NON_AUTHORITATIVE_HISTORICAL -->

> [!WARNING]
> Historical checkpoint / planning note — non-authoritative for the current release.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and `CERTIFICATION_STATUS.md` for current release truth.

> [!WARNING] Historical / non-authoritative document. This file is retained for provenance or implementation context only. Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md` and the generated current-state reports for current release truth.

> **Historical / non-authoritative** — This document is retained for planning or provenance only.
> Do **not** use it to determine the current certification state, executable surface, or release readiness.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and `CERTIFICATION_STATUS.md` instead.

# operator-service checkpoint — operator service layer and admin/RPC parity checkpoint

## Scope completed in this checkpoint

This checkpoint implements the requested operator-service checkpoint work to move the operator plane away from handler-local ad hoc state and into shared services.

## Implemented service layer

Added or completed the following service modules:

- `tigrbl_auth/services/_operator_store.py`
- `tigrbl_auth/services/operator_service.py`
- `tigrbl_auth/services/audit_service.py`
- `tigrbl_auth/services/client_service.py`
- `tigrbl_auth/services/identity_service.py`
- `tigrbl_auth/services/session_service.py`
- `tigrbl_auth/services/discovery_service.py`
- `tigrbl_auth/services/import_export_service.py`
- `tigrbl_auth/services/key_management.py` (lazy runtime imports + operator wrappers)
- `tigrbl_auth/services/token_service.py` (lazy runtime imports + operator wrappers)

## CLI/operator changes

- `tigrbl_auth/cli/handlers.py` now routes resource lifecycle verbs through the shared service layer.
- tenant/client/identity/flow/session/token/keys/discovery/import/export handlers now use service-backed semantics.
- operator transactions and audit rows are written under `dist/operator-state/`.
- key lifecycle and JWKS publication use the shared key/operator services.

## RPC changes

Updated RPC method modules to use the same operator services rather than separate ad hoc/durable-path logic:

- `tigrbl_auth/api/rpc/methods/client_registration.py`
- `tigrbl_auth/api/rpc/methods/session.py`
- `tigrbl_auth/api/rpc/methods/token.py`
- `tigrbl_auth/api/rpc/methods/keys.py`
- `tigrbl_auth/api/rpc/methods/governance.py` (discovery)

## REST surface observation hooks

Updated routers to emit operator/audit observations:

- `tigrbl_auth/api/rest/routers/register.py`
- `tigrbl_auth/api/rest/routers/logout.py`
- `tigrbl_auth/api/rest/routers/token.py`
- `tigrbl_auth/api/rest/routers/par.py`
- `tigrbl_auth/api/rest/routers/device_authorization.py`

These hooks record checkpoint-grade parity artifacts for token issuance, logout, PAR, device authorization, and registration workflows.

## Repository truthfulness and import safety

- `tigrbl_auth/services/__init__.py` was reduced to a non-eager package stub so lightweight operator modules can import without forcing the full runtime dependency set.
- `key_management.py` and `token_service.py` now defer runtime-only framework imports until those runtime paths are actually used.

## Test and mapping updates

- added `tests/unit/test_5_operator_service_layer.py`
- updated `compliance/mappings/target-to-module.yaml`
- updated `compliance/mappings/target-to-test.yaml`
- updated canonical test classification mappings

## Validation completed in this environment

- modified Python modules compile successfully
- RPC registry loads successfully with the operator-service checkpoint service-layer changes
- contracts were regenerated and brought back into sync
- state reports were regenerated
- release gates pass: `20/20`
- release bundle signing verifies in this checkpoint environment

## Honest current state

This checkpoint **does not** make the package certifiably fully featured or certifiably fully RFC/spec compliant.

The main remaining blockers are unchanged in principle:

- the retained production and hardening RFC/OIDC targets are still not fully promoted to Tier 3
- Tier 4 independent claims are still absent
- the operator service layer is checkpoint-grade parity, not final production-grade persistence parity across the full runtime plane
- this container still lacks parts of the published runtime dependency set needed for full runtime execution and full pytest collection
