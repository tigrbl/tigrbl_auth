<!-- NON_AUTHORITATIVE_HISTORICAL -->

> [!WARNING]
> Historical checkpoint / planning note — non-authoritative for the current release.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and `CERTIFICATION_STATUS.md` for current release truth.

> [!WARNING] Historical / non-authoritative document. This file is retained for provenance or implementation context only. Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md` and the generated current-state reports for current release truth.

> **Historical / non-authoritative** — This document is retained for planning or provenance only.
> Do **not** use it to determine the current certification state, executable surface, or release readiness.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and `CERTIFICATION_STATUS.md` instead.

# runtime-hardening checkpoint — production target cluster A checkpoint

## Scope completed in this checkpoint

This checkpoint implements the requested runtime-hardening checkpoint work for the remaining production targets in cluster A:

- `RFC 7516`
- `RFC 7521`
- `RFC 7523`
- `RFC 8252`

The checkpoint closes the helper-only gap for those targets at the standards/module/contract/evidence plane and promotes them to Tier 3 in the repository claim manifests.

## Implemented standards/runtime work

### RFC 7516 — JWE

Completed work:

- replaced helper-only JWE behavior with a dependency-light compact JWE implementation in `tigrbl_auth/standards/jose/rfc7516.py`
- enforced a real bounded JWE policy:
  - `alg=dir`
  - `enc=A256GCM`
  - symmetric `oct` keys with exact key-length checks
- added fail-closed header validation, key validation, malformed-token checks, and wrong-key rejection
- wired OIDC discovery truthfulness through `jwe_policy_metadata()`
- enabled dependency-light encrypted ID token validation through the compatibility `oidc_id_token`/`oidc_discovery` facades for checkpoint evidence generation

### RFC 7521 — assertion framework

Completed work:

- converted `tigrbl_auth/standards/oauth2/assertion_framework.py` into a runtime-oriented validator for JWT bearer assertion grants
- added strict required-claim, temporal-claim, issuer/subject, and audience validation
- integrated assertion grant handling into `/token` in `tigrbl_auth/ops/token.py`
- added auditable token issuance for assertion grants
- added token-contract examples for assertion grants

### RFC 7523 — JWT client authentication / authorization grants

Completed work:

- converted `tigrbl_auth/standards/oauth2/jwt_client_auth.py` into a runtime-oriented validator for `private_key_jwt`
- enforced strict `iat` + `jti` claim requirements for token-endpoint client assertions
- integrated JWT client assertion authentication into `/token`
- coupled registration policy to runtime auth policy in `tigrbl_auth/ops/register.py`
- made discovery truthful for:
  - `token_endpoint_auth_methods_supported`
  - `token_endpoint_auth_signing_alg_values_supported`
- added contract examples for JWT client authentication
- added the missing `enable_rfc7521` / `enable_rfc7523` production flags to the canonical feature-flag registry and deployment active-target logic

### RFC 8252 — native apps

Completed work:

- strengthened native redirect classification and validation in `tigrbl_auth/standards/oauth2/native_apps.py`
- enforced:
  - loopback redirects must use `http`
  - explicit loopback port is required
  - private-use scheme redirects must not contain an authority component
  - native apps must use `response_type=code`
  - PKCE is mandatory for native apps
  - `S256` is mandatory for native apps
  - token exchange for native apps requires `code_verifier`
- wired native validation into:
  - dynamic client registration
  - authorization runtime
  - token runtime

## Contract/discovery truthfulness updates

Updated:

- `tigrbl_auth/standards/oidc/discovery_metadata.py`
- `tigrbl_auth/cli/artifacts.py`
- `tigrbl_auth/standards/oauth2/rfc9700.py`
- `tigrbl_auth/config/feature_flags.py`
- `tigrbl_auth/config/deployment.py`

Effects:

- production discovery now truthfully advertises JWT client-auth methods/signing algorithms
- production discovery now truthfully advertises ID token encryption support when enabled
- production grant-type support now includes JWT bearer assertions in the profile metadata when the flags are enabled
- the public OpenAPI token form now includes assertion-grant and JWT client-auth request properties/examples

## Test and evidence work completed

Dependency-light targeted tests added or refreshed:

- `tests/unit/test_rfc7516_jwe.py`
- `tests/unit/test_oidc_id_token_encryption.py`
- `tests/unit/test_rfc7521_assertion_framework.py`
- `tests/unit/test_rfc7523_jwt_profile.py`
- `tests/unit/test_rfc8252_native_app_redirects.py`

Targeted checkpoint execution completed in this environment with:

```text
PYTHONPATH=. pytest --noconftest -q \
  tests/unit/test_rfc7516_jwe.py \
  tests/unit/test_oidc_id_token_encryption.py \
  tests/unit/test_rfc7521_assertion_framework.py \
  tests/unit/test_rfc7523_jwt_profile.py \
  tests/unit/test_rfc8252_native_app_redirects.py
```

Result:

- `35 passed`

Tier 3 evidence bundles were materialized at:

- `compliance/evidence/tier3/jwe/`
- `compliance/evidence/tier3/assertion-framework/`
- `compliance/evidence/tier3/jwt-client-auth/`
- `compliance/evidence/tier3/native-apps/`

## Claim/mapping promotion completed

Updated:

- `compliance/claims/declared-target-claims.yaml`
- `compliance/mappings/target-to-module.yaml`
- `compliance/mappings/target-to-test.yaml`
- `compliance/mappings/target-to-endpoint.yaml`
- `compliance/mappings/target-to-peer-profile.yaml`

Manifest effects:

- `RFC 7516` → Tier 3
- `RFC 7521` → Tier 3
- `RFC 7523` → Tier 3
- `RFC 8252` → Tier 3

## Validation completed in this environment

Completed successfully:

- targeted dependency-light runtime-hardening checkpoint unit coverage (`35 passed`)
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

This checkpoint improves the certification posture materially, but it **does not** make the package certifiably fully featured or certifiably fully RFC/spec compliant across the full retained boundary.

What is now true:

- cluster A production targets are promoted to Tier 3 in the repository manifests
- the package now has `24` Tier 3 targets in total
- release gates still pass end-to-end
- targeted runtime-hardening checkpoint standards/runtime coverage is executable in this checkpoint environment without the full Tigrbl/SQLAlchemy runtime stack

What is still not true:

- the package is **not** yet certifiably fully featured
- the package is **not** yet certifiably fully RFC/spec compliant across the entire retained boundary
- remaining production and hardening targets still need Tier 3 closure
- Tier 4 independent claims are still absent
- runtime runner profiles remain invalid/missing in this checkpoint environment because the full published runtime dependency set is not installed
