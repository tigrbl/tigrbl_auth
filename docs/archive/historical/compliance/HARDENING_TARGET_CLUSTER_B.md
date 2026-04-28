<!-- NON_AUTHORITATIVE_HISTORICAL -->

> [!WARNING]
> Historical checkpoint / planning note — non-authoritative for the current release.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and `CERTIFICATION_STATUS.md` for current release truth.

> [!WARNING] Historical / non-authoritative document. This file is retained for provenance or implementation context only. Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md` and the generated current-state reports for current release truth.

> **Historical / non-authoritative** — This document is retained for planning or provenance only.
> Do **not** use it to determine the current certification state, executable surface, or release readiness.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and `CERTIFICATION_STATUS.md` instead.

# test-plane checkpoint — hardening target cluster B checkpoint

## Scope completed in this checkpoint

This checkpoint closes the requested hardening cluster B targets:

- `RFC 9101`
- `RFC 9126`
- `RFC 9207`
- `RFC 9396`

The closure work was applied against the provided capability-wiring checkpoint checkpoint zip and then revalidated in this checkpoint environment.

## What changed

### RFC 9101

- promoted the repository claim for `RFC 9101` from Tier 2 to Tier 3
- replaced the prior helper-only request-object parsing with a bounded, dependency-light compact JWS request-object runtime
- enforced signed request objects only (`alg=none` is rejected)
- enforced temporal validation for `exp`, `nbf`, and `iat` when present
- enforced client/audience consistency checks and deterministic merge behavior between request-object claims and direct request parameters
- preserved request-object handling on both `/authorize` and `/par`

### RFC 9126

- promoted the repository claim for `RFC 9126` from Tier 2 to Tier 3
- turned the standards-tree owner module into a real request-uri validation/consumption policy surface
- enforced durable request-uri validation with:
  - prefix validation
  - expiration checks
  - client binding checks
  - one-time consumption semantics
- tightened authorize-side request-uri handling so hardening requests are self-contained instead of silently merging arbitrary direct query overrides
- preserved request-object and rich-authorization-details normalization through the `/par` runtime path

### RFC 9207

- promoted the repository claim for `RFC 9207` from Tier 2 to Tier 3
- fixed a real deployment bug: `RFC 9207` was enabled by flags in hardening, but it was missing from `TARGET_FLAG_REQUIREMENTS`, so it never became an active target
- added bounded issuer-identifier validation for query and fragment redirect responses
- made the hardening OpenAPI contract require `iss` on authorization responses when issuer identification is active
- preserved truthful discovery metadata via `authorization_response_iss_parameter_supported`

### RFC 9396

- promoted the repository claim for `RFC 9396` from Tier 2 to Tier 3
- replaced the minimal parser with a richer normalization/binding layer for `authorization_details`
- enforced:
  - object/array JSON structure
  - required `type`
  - absolute-URI validation for `locations`, `resource`, and `resource_indicator`
  - policy coupling between `authorization_details` and effective request resource/audience binding
- preserved normalized authorization-details propagation through `/par` and the authorization-code runtime

## Additional fixes discovered during validation

These fixes were necessary to make the checkpoint honest and testable:

- made `tigrbl_auth.ops` namespace imports dependency-light so targeted standards tests can import individual operation modules without pulling in the full runtime stack
- added dependency-light fallbacks in `ops/par.py` so test-plane checkpoint standards evidence can execute without the full SQLAlchemy/Tigrbl runtime stack
- updated CLI/OpenAPI contract generation so hardening authorization responses require `iss` when RFC 9207 is active
- refreshed target/test/module/peer mappings so the promoted Tier 3 claims point at the current test-plane checkpoint closure surfaces

## Files materially updated

Primary implementation surfaces:

- `tigrbl_auth/standards/oauth2/jar.py`
- `tigrbl_auth/standards/oauth2/par.py`
- `tigrbl_auth/standards/oauth2/issuer_identification.py`
- `tigrbl_auth/standards/oauth2/rar.py`
- `tigrbl_auth/ops/par.py`
- `tigrbl_auth/ops/authorize.py`
- `tigrbl_auth/config/deployment.py`
- `tigrbl_auth/cli/artifacts.py`
- `tigrbl_auth/tables/pushed_authorization_request.py`
- `tigrbl_auth/ops/__init__.py`
- `tests/unit/test_TEST_PLANE_hardening_cluster_b.py`
- `tests/conformance/hardening/test_rfc9207_issuer_identification.py`

Claims / mappings / evidence:

- `compliance/claims/declared-target-claims.yaml`
- `compliance/mappings/target-to-module.yaml`
- `compliance/mappings/target-to-test.yaml`
- `compliance/mappings/target-to-peer-profile.yaml`
- `compliance/mappings/test_classification.yaml`
- `compliance/mappings/test-classification.yaml`
- `compliance/evidence/tier3/jar/**`
- `compliance/evidence/tier3/par/**`
- `compliance/evidence/tier3/issuer-identification/**`
- `compliance/evidence/tier3/rar/**`

## Validation performed in this environment

Targeted dependency-light test-plane checkpoint validation:

```text
PYTHONPATH=. pytest --noconftest -q \
  tests/unit/test_TEST_PLANE_hardening_cluster_b.py \
  tests/conformance/hardening/test_rfc9101_jar.py \
  tests/conformance/hardening/test_rfc9126_par.py \
  tests/conformance/hardening/test_rfc9207_issuer_identification.py \
  tests/conformance/hardening/test_rfc9396_rar.py
```

Result:

- `12 passed`

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
- Tier 3 targets: `34`
- Tier 4 targets: `0`

## Honest current status

This checkpoint **does not** make the package certifiably fully featured and **does not** make the package certifiably fully RFC/spec compliant across the full retained boundary.

The test-plane checkpoint work closes the requested hardening cluster B targets and preserves Tier 3 evidence for them, but the repository still has open gaps in:

- the remaining hardening targets (`RFC 8705`, `RFC 9449`, `RFC 9700`, `OIDC Front-Channel Logout`, `OIDC Back-Channel Logout`)
- the runtime/operator certification targets
- the Tier 4 independent claim boundary
- end-to-end runner validation in this environment
