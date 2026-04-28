<!-- NON_AUTHORITATIVE_HISTORICAL -->

> [!WARNING]
> Historical checkpoint / planning note — non-authoritative for the current release.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and `CERTIFICATION_STATUS.md` for current release truth.

> [!WARNING] Historical / non-authoritative document. This file is retained for provenance or implementation context only. Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md` and the generated current-state reports for current release truth.

> **Historical / non-authoritative** — This document is retained for planning or provenance only.
> Do **not** use it to determine the current certification state, executable surface, or release readiness.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and `CERTIFICATION_STATUS.md` instead.

# runtime-hardening checkpoint Runtime Validation Report

## Executed checks in this checkpoint

- `python -m compileall tigrbl_auth scripts tests`
- `python scripts/generate_openapi_contract.py`
- `python scripts/generate_openrpc_contract.py`
- `python scripts/generate_effective_release_manifests.py`
- `python scripts/generate_certification_scope.py`
- `python scripts/generate_state_reports.py`
- `python scripts/run_release_gates.py`

## Direct runtime-hardening checkpoint smoke checks executed

The following runtime-hardening checkpoint test functions were executed directly in-process and passed:

- `test_hardening_profile_rejects_password_grant`
- `test_hardening_profile_rejects_implicit_flow`
- `test_hardening_profile_requires_par_when_enabled`
- `test_hardening_discovery_metadata_matches_runtime_policy`
- `test_peer_claim_discovery_metadata_matches_runtime_policy`
- `test_hardening_openapi_contract_reflects_runtime_constraints`

## Result

This checkpoint passes the repository release gates and demonstrates executable runtime-hardening checkpoint behavior for the core hardening/runtime paths. It does not, by itself, establish final certification across the entire declared boundary.
