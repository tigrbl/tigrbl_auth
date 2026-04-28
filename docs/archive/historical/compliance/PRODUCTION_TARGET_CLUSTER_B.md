<!-- NON_AUTHORITATIVE_HISTORICAL -->

> [!WARNING]
> Historical checkpoint / planning note — non-authoritative for the current release.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and `CERTIFICATION_STATUS.md` for current release truth.

> [!WARNING] Historical / non-authoritative document. This file is retained for provenance or implementation context only. Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md` and the generated current-state reports for current release truth.

> **Historical / non-authoritative** — This document is retained for planning or provenance only.
> Do **not** use it to determine the current certification state, executable surface, or release readiness.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and `CERTIFICATION_STATUS.md` instead.

# RFC-family runtime checkpoint — production target cluster B checkpoint

## Scope completed in this checkpoint

This checkpoint implements the requested RFC-family runtime checkpoint work for the remaining production browser/session/logout targets in cluster B:

- `OIDC Session Management`
- `OIDC RP-Initiated Logout`

The checkpoint closes the helper-only and policy-partial gaps for those two targets at the standards/runtime/contract/evidence plane and promotes them to Tier 3 in the repository claim manifests.

## Implemented browser session/runtime work

### OIDC Session Management

Completed work:

- updated `tigrbl_auth/standards/oidc/session_mgmt.py` so the module is dependency-light importable in this checkpoint environment
- added explicit session-state parsing and validation helpers:
  - `parse_session_state(...)`
  - `validate_session_state(...)`
  - `validate_session_state_for_client(...)`
- bound session-state validation to client origin and session salt so the value is not treated as a static presence marker
- made the session-management description truthful about what is and is not claimed in the current release path
- added explicit runtime description fields for:
  - `session_state_validation_supported`
  - `session_state_origin_bound`
  - `auth_code_linkage_supported`
  - `check_session_iframe_claimed`
- updated browser cookie policy reporting in `tigrbl_auth/standards/http/cookies.py` so rotation and invalidation behavior are reflected explicitly

Important truthfulness boundary:

- this checkpoint **does not** claim a mounted `check_session_iframe` route
- discovery/docs now remain truthful about that absence

## Implemented logout/runtime work

### OIDC RP-Initiated Logout

Completed work:

- updated `tigrbl_auth/standards/oidc/rp_initiated_logout.py` so it is dependency-light importable in this checkpoint environment
- added structured logout validation helpers:
  - `validate_id_token_hint(...)`
  - `resolve_logout_client_id(...)`
  - `assert_logout_session_active(...)`
  - `validate_logout_request(...)`
- enforced:
  - `id_token_hint` validation
  - `post_logout_redirect_uri` registration checks
  - client/session consistency checks
  - expired-session rejection
  - cross-client misuse rejection
- updated logout planning so replay/idempotent requests reuse persisted logout state rather than creating an unbounded series of independent logout artifacts
- updated `tigrbl_auth/ops/logout.py` so the runtime path uses the new validation layer and carries forward validated session/client metadata
- updated `tigrbl_auth/api/rest/routers/logout.py` so runtime observation artifacts can be derived from structured response payloads or fallback headers
- patched `tigrbl_auth/services/persistence.py` so repeated logout attempts for the same session can reuse and update the latest logout state record

### Supporting fixes

- fixed `tigrbl_auth/ops/login.py` to import `settings` correctly
- updated front-channel and back-channel logout helper modules so they can be imported without eagerly requiring the full SQLAlchemy/runtime stack in this checkpoint environment

## Contract/discovery truthfulness updates

Updated or regenerated:

- `tigrbl_auth/standards/oidc/session_mgmt.py`
- `tigrbl_auth/standards/http/cookies.py`
- `tigrbl_auth/standards/oidc/rp_initiated_logout.py`
- `tigrbl_auth/ops/logout.py`
- `tigrbl_auth/api/rest/routers/logout.py`
- discovery snapshots
- certification/current-state reports

Effects:

- the production profile now truthfully carries `end_session_endpoint`
- the current release path does **not** advertise `check_session_iframe`
- session/logout descriptions align with implemented validation and state semantics

## Test and evidence work completed

Dependency-light targeted tests added or refreshed:

- `tests/unit/test_RFC_FAMILY_RUNTIME_session_logout_cluster_b.py`
- `tests/conformance/production/test_oidc_session_management.py`
- `tests/conformance/production/test_oidc_rp_initiated_logout.py`
- `tests/negative/test_cookie_and_logout_abuse_cases.py`

Targeted checkpoint execution completed in this environment with:

```text
PYTHONPATH=. pytest --noconftest -q \
  tests/unit/test_RFC_FAMILY_RUNTIME_session_logout_cluster_b.py \
  tests/conformance/production/test_oidc_session_management.py \
  tests/conformance/production/test_oidc_rp_initiated_logout.py \
  tests/negative/test_cookie_and_logout_abuse_cases.py
```

Result:

- `21 passed`

Tier 3 evidence bundles were materialized at:

- `compliance/evidence/tier3/oidc-session-management/`
- `compliance/evidence/tier3/oidc-rp-initiated-logout/`

## Claim/mapping promotion completed

Updated:

- `compliance/claims/declared-target-claims.yaml`
- `compliance/mappings/target-to-module.yaml`
- `compliance/mappings/target-to-test.yaml`
- canonical test-classification mappings

Manifest effects:

- `OIDC Session Management` → Tier 3
- `OIDC RP-Initiated Logout` → Tier 3

## Validation completed in this environment

Completed successfully:

- targeted dependency-light RFC-family runtime checkpoint tests (`21 passed`)
- `scripts/generate_effective_release_manifests.py`
- `scripts/generate_certification_scope.py`
- `scripts/generate_openapi_contract.py`
- `scripts/generate_discovery_snapshots.py`
- `scripts/generate_state_reports.py`
- `scripts/run_release_gates.py`
- `scripts/build_release_bundle.py`
- `scripts/sign_release_bundle.py`
- `scripts/verify_release_signing.py`
- `scripts/run_recertification.py`

Release-gate result:

- `20/20 passing`

## Honest current state

This checkpoint materially improves the certification posture, but it **does not** make the package certifiably fully featured or certifiably fully RFC/spec compliant across the full retained boundary.

What is now true:

- cluster B production targets are promoted to Tier 3 in the repository manifests
- the package now has `26` Tier 3 targets in total
- release gates still pass end-to-end
- targeted session/logout validation and evidence are executable in this checkpoint environment without the full Tigrbl/SQLAlchemy runtime stack

What is still not true:

- the package is **not** yet certifiably fully featured
- the package is **not** yet certifiably fully RFC/spec compliant across the entire retained boundary
- remaining production and hardening targets still need Tier 3 closure
- Tier 4 independent claims are still absent
- runtime runner profiles remain invalid/missing in this checkpoint environment because the full published runtime dependency set is not installed
