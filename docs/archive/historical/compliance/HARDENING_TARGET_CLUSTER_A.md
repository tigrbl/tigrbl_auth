<!-- NON_AUTHORITATIVE_HISTORICAL -->

> [!WARNING]
> Historical checkpoint / planning note — non-authoritative for the current release.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and `CERTIFICATION_STATUS.md` for current release truth.

> [!WARNING] Historical / non-authoritative document. This file is retained for provenance or implementation context only. Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md` and the generated current-state reports for current release truth.

> **Historical / non-authoritative** — This document is retained for planning or provenance only.
> Do **not** use it to determine the current certification state, executable surface, or release readiness.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and `CERTIFICATION_STATUS.md` instead.

# capability-wiring checkpoint — hardening target cluster A completion checkpoint

## Scope completed in this checkpoint

This checkpoint closes the requested hardening cluster A targets:

- `RFC 7592`
- `RFC 8628`
- `RFC 8693`
- `RFC 8707`

The closure work was applied against the provided RFC-family runtime checkpoint checkpoint zip and then revalidated in this checkpoint environment.

## What changed

### RFC 7592

- promoted the repository claim for `RFC 7592` from Tier 2 to Tier 3
- updated the canonical owner module status to `-8-persistence-backed-management-runtime`
- extended admin/RPC parity with `client.registration.delete`
- preserved Tier 3 evidence for bearer-authenticated management semantics and shared operator-surface behavior

### RFC 8628

- promoted the repository claim for `RFC 8628` from Tier 2 to Tier 3
- extended the canonical device-code table state with polling, denial, and replay-observable fields
- preserved runtime semantics for `authorization_pending`, `slow_down`, `access_denied`, and `expired_token`
- exported `DEVICE_CODE_GRANT_TYPE` from the canonical owner module so token/runtime code and evidence tooling share one authoritative constant

### RFC 8693

- promoted the repository claim for `RFC 8693` from Tier 2 to Tier 3
- implemented bounded requested-token-type enforcement on the standards-tree token-exchange endpoint
- preserved actor-token delegation semantics and audit-observable lineage details
- extended admin/RPC parity with `token.exchange`
- added a dependency-light `describe()` surface for evidence/report generation

### RFC 8707

- promoted the repository claim for `RFC 8707` from Tier 2 to Tier 3
- replaced the prior “first value wins” behavior with a bounded single-effective-target profile
- requests with multiple distinct `resource` values now fail closed with `invalid_target`
- requests with conflicting `audience` and `resource` values now fail closed with `invalid_target`
- conflict-aware handling is preserved across `/token`, `/device_authorization`, `/token/exchange`, and `/par`

## Additional fixes discovered during validation

These fixes were necessary to make the checkpoint honest and testable:

- fixed `resource_indicators._coerce_resources()` so list input no longer raises `TypeError`
- added a dependency-light OIDC ID-token fallback in `ops/token.py` so targeted capability-wiring checkpoint evidence can execute without the full Tigrbl/SQLAlchemy stack
- refreshed module/test mappings so Tier 3 claims point at the current closure modules and the new dependency-light capability-wiring checkpoint test plane
- replaced the placeholder Tier 3 evidence directories for the four closed targets with preserved evidence bundles

## Files materially updated

Primary implementation surfaces:

- `tigrbl_auth/standards/oauth2/client_registration_management.py`
- `tigrbl_auth/standards/oauth2/device_authorization.py`
- `tigrbl_auth/standards/oauth2/token_exchange.py`
- `tigrbl_auth/standards/oauth2/resource_indicators.py`
- `tigrbl_auth/ops/token.py`
- `tigrbl_auth/ops/device_authorization.py`
- `tigrbl_auth/ops/par.py`
- `tigrbl_auth/api/rpc/methods/client_registration.py`
- `tigrbl_auth/api/rpc/schemas/client_registration.py`
- `tigrbl_auth/api/rpc/methods/token.py`
- `tigrbl_auth/api/rpc/schemas/token.py`
- `tigrbl_auth/tables/device_code.py`
- `tests/unit/test_8_hardening_cluster_a.py`

Claims / mappings / evidence:

- `compliance/claims/declared-target-claims.yaml`
- `compliance/mappings/target-to-module.yaml`
- `compliance/mappings/target-to-test.yaml`
- `compliance/mappings/test_classification.yaml`
- `compliance/mappings/test-classification.yaml`
- `compliance/evidence/tier3/client-registration-management/**`
- `compliance/evidence/tier3/device-flow/**`
- `compliance/evidence/tier3/token-exchange/**`
- `compliance/evidence/tier3/resource-indicators/**`

## Validation performed in this environment

Targeted dependency-light capability-wiring checkpoint test execution:

```text
python -m pytest --noconftest -q \
  tests/unit/test_8_hardening_cluster_a.py \
  tests/conformance/hardening/test_rfc7592_client_registration_management.py \
  tests/conformance/hardening/test_rfc8628_device_authorization.py \
  tests/conformance/hardening/test_rfc8693_token_exchange.py \
  tests/conformance/hardening/test_rfc8707_resource_indicators.py
```

Result:

- `16 passed`

Governance / release automation rerun in this checkpoint:

- `python scripts/claims_lint.py`
- `python scripts/generate_effective_release_manifests.py`
- `python scripts/generate_certification_scope.py`
- `python scripts/generate_openapi_contract.py`
- `python scripts/generate_openrpc_contract.py`
- `python scripts/generate_discovery_snapshots.py`
- `python scripts/generate_state_reports.py`
- `python scripts/run_release_gates.py`
- `python scripts/build_release_bundle.py`
- `python scripts/sign_release_bundle.py`
- `python scripts/verify_release_signing.py`
- `python scripts/run_recertification.py`

Measured outcome:

- release gates: `20/20 passing`
- declared targets: `48`
- Tier 3 targets: `30`
- Tier 4 targets: `0`

## Honest current status

This checkpoint **does not** make the package certifiably fully featured and **does not** make the package certifiably fully RFC/spec compliant across the full retained boundary.

The capability-wiring checkpoint work closes the requested hardening cluster A targets and preserves Tier 3 evidence for them, but the repository still has open gaps in:

- the remaining hardening targets
- the runtime/operator certification targets
- the Tier 4 independent claim boundary
- end-to-end runner validation in this environment
