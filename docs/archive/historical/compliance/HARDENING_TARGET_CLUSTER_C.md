<!-- NON_AUTHORITATIVE_HISTORICAL -->

> [!WARNING]
> Historical checkpoint / planning note — non-authoritative for the current release.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and `CERTIFICATION_STATUS.md` for current release truth.

> [!WARNING] Historical / non-authoritative document. This file is retained for provenance or implementation context only. Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md` and the generated current-state reports for current release truth.

> **Historical / non-authoritative** — This document is retained for planning or provenance only.
> Do **not** use it to determine the current certification state, executable surface, or release readiness.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and `CERTIFICATION_STATUS.md` instead.

# Tier 3 evidence checkpoint — hardening target cluster C checkpoint

## Scope completed in this checkpoint

This checkpoint closes the requested hardening cluster C targets:

- `RFC 8705`
- `RFC 9449`
- `RFC 9700`
- `OIDC Front-Channel Logout`
- `OIDC Back-Channel Logout`

The closure work was applied against the provided test-plane checkpoint checkpoint zip and then revalidated in this checkpoint environment.

## What changed

### RFC 8705

- promoted the repository claim for `RFC 8705` from Tier 2 to Tier 3
- replaced the previous bounded helper-only surface with a dependency-light mTLS runtime module that now exposes:
  - certificate thumbprint derivation from PEM material
  - registered-certificate lookup helpers
  - mTLS client authentication validation for `tls_client_auth` and `self_signed_tls_client_auth`
  - certificate-bound token confirmation claims and request-side certificate-binding checks
- integrated mTLS client-auth handling into the `/token` runtime so registered mTLS clients authenticate with presented certificate material instead of falling back to unrelated client-secret or assertion paths
- extended registration schemas and runtime validation so mTLS auth methods require the correct certificate thumbprint metadata
- made discovery truthfulness match runtime behavior by advertising mTLS token-endpoint auth methods only when the hardening profile enables them

### RFC 9449

- promoted the repository claim for `RFC 9449` from Tier 2 to Tier 3
- replaced the thin DPoP helpers with a dependency-light runtime that now supports:
  - structured DPoP proof claims
  - JWK thumbprint (`jkt`) computation
  - `ath` binding
  - nonce issue/consume helpers
  - replay-store enforcement
  - proof parsing and validation
- fixed the proof-construction path so it no longer breaks when a signer coroutine is invoked from an existing event loop
- wired DPoP proof verification into centralized sender-constraint enforcement for token verification and resource-side request processing
- updated compatibility surfaces so the repo’s legacy RFC facades reflect the canonical standards-tree implementation instead of drifting from it

### RFC 9700

- promoted the repository claim for `RFC 9700` from Tier 2 to Tier 3
- added a centralized `verify_access_token_sender_constraint(...)` helper so hardening resource paths fail closed for sender-constrained access tokens
- enforced:
  - DPoP proof requirement for `cnf.jkt`-bound tokens
  - `ath` binding and proof replay protection
  - certificate-thumbprint validation for `cnf.x5t#S256`-bound tokens
  - rejection of unexpected DPoP proofs on non-DPoP tokens
- aligned token verification services so certificate validation only runs when the token is actually certificate-bound, avoiding false failures for DPoP or bearer tokens
- preserved fail-closed hardening posture in the targeted validation suite for password grant, implicit flow, and PAR requirements

### OIDC Front-Channel Logout

- promoted the repository claim for `OIDC Front-Channel Logout` from Tier 2 to Tier 3
- preserved the fan-out descriptor model and strengthened it with durable delivery-state persistence via `mark_logout_channel_async(...)`
- validated front-channel request requirements through the standards-tree owner surface
- recorded delivery status, attempts, retry-after hints, failure reasons, and completion timestamps in logout persistence metadata
- kept front-channel logout discovery and contract surfaces truthful to the runtime-backed behavior shipped in this checkpoint

### OIDC Back-Channel Logout

- promoted the repository claim for `OIDC Back-Channel Logout` from Tier 2 to Tier 3
- preserved the back-channel logout token/runtime surface and strengthened it with:
  - fallback logout-token generation/validation for dependency-light evidence runs
  - replay-store enforcement for logout tokens
  - durable delivery-state persistence and retry metadata
- aligned completion/failure helpers with shared persistence so front-channel and back-channel logout fan-out now use the same durable delivery-state model
- kept back-channel logout discovery and contract surfaces truthful to the runtime-backed behavior shipped in this checkpoint

## Additional fixes discovered during validation

These fixes were necessary to make the checkpoint honest and releasable:

- removed non-certified compatibility modules from the Tier 3 evidence checkpoint owner-module mappings so boundary enforcement and wrapper-hygiene gates stay truthful
- regenerated certification scope and state reports after that mapping correction
- refreshed generated contracts, discovery snapshots, effective claim/evidence manifests, release bundles, release attestations, and recertification fingerprints after the Tier 3 evidence checkpoint changes stabilized

## Files materially updated

Primary implementation surfaces:

- `tigrbl_auth/standards/oauth2/mtls.py`
- `tigrbl_auth/standards/oauth2/dpop.py`
- `tigrbl_auth/standards/oauth2/rfc9700.py`
- `tigrbl_auth/standards/oauth2/rfc8705.py`
- `tigrbl_auth/rfc/rfc8705.py`
- `tigrbl_auth/standards/oauth2/rfc9449_dpop.py`
- `tigrbl_auth/rfc/rfc9449_dpop.py`
- `tigrbl_auth/ops/token.py`
- `tigrbl_auth/ops/register.py`
- `tigrbl_auth/services/token_service.py`
- `tigrbl_auth/jwtoken.py`
- `tigrbl_auth/security/auth.py`
- `tigrbl_auth/security/deps.py`
- `tigrbl_auth/services/persistence.py`
- `tigrbl_auth/standards/oidc/frontchannel_logout.py`
- `tigrbl_auth/standards/oidc/backchannel_logout.py`
- `tigrbl_auth/api/rest/schemas.py`
- `tigrbl_auth/cli/artifacts.py`
- `tests/unit/test_10_hardening_cluster_c.py`
- `tests/unit/test_rfc9700_security_bcp_profile_checkpoint.py`
- `tests/conformance/hardening/test_rfc8705_mtls.py`
- `tests/conformance/hardening/test_oidc_frontchannel_logout.py`
- `tests/conformance/hardening/test_oidc_backchannel_logout.py`

Claims / mappings / evidence:

- `compliance/claims/declared-target-claims.yaml`
- `compliance/mappings/target-to-module.yaml`
- `compliance/mappings/target-to-test.yaml`
- `compliance/mappings/target-to-peer-profile.yaml`
- `compliance/mappings/test_classification.yaml`
- `compliance/mappings/test-classification.yaml`
- `compliance/evidence/tier3/mtls/**`
- `compliance/evidence/tier3/dpop/**`
- `compliance/evidence/tier3/security-bcp/**`
- `compliance/evidence/tier3/oidc-frontchannel-logout/**`
- `compliance/evidence/tier3/oidc-backchannel-logout/**`

## Validation performed in this environment

Targeted dependency-light Tier 3 evidence checkpoint validation:

```text
PYTHONPATH=. pytest --noconftest -q \
  tests/unit/test_10_hardening_cluster_c.py \
  tests/conformance/hardening/test_rfc8705_mtls.py \
  tests/conformance/hardening/test_rfc9449_dpop.py \
  tests/unit/test_rfc9700_security_bcp_profile_checkpoint.py \
  tests/negative/test_6_hardening_runtime_enforcement.py \
  tests/conformance/hardening/test_oidc_frontchannel_logout.py \
  tests/conformance/hardening/test_oidc_backchannel_logout.py
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
- Tier 3 targets: `39`
- Tier 4 targets: `0`

## Honest current status

This checkpoint **does not** make the package certifiably fully featured and **does not** make the package certifiably fully RFC/spec compliant across the full retained boundary.

The Tier 3 evidence checkpoint work closes the requested hardening cluster C targets and preserves Tier 3 evidence for them. It also means that **all currently declared RFC / OIDC / public-contract protocol targets are now promoted to Tier 3**.

The repository still has open gaps in:

- the runtime/operator certification targets (`ASGI 3 application package`, runner profiles, CLI operator surface, bootstrap/migration lifecycle, key lifecycle/JWKS publication, import/export portability, and release verification scope)
- final production admin/RPC/runtime parity for the operator plane
- the Tier 4 independent claim boundary
- end-to-end runner validation in this environment (`uvicorn` and `hypercorn` remain invalid here because the runtime stack is incomplete; `tigrcorn` remains unavailable)
