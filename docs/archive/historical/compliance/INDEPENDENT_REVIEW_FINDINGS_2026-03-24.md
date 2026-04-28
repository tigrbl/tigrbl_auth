<!-- NON_AUTHORITATIVE_HISTORICAL -->

> [!WARNING]
> Historical checkpoint / planning note — non-authoritative for the current release.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and `CERTIFICATION_STATUS.md` for current release truth.

> [!WARNING] Historical / non-authoritative document. This file is retained for provenance or implementation context only. Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md` and the generated current-state reports for current release truth.

> **Historical / non-authoritative** — This document is retained for planning or provenance only.
> Do **not** use it to determine the current certification state, executable surface, or release readiness.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and `CERTIFICATION_STATUS.md` instead.

# Independent Review Findings — 2026-03-24

> Note: parts of this review were superseded by the later persistence-domain checkpoint/public-route checkpoint follow-on checkpoints. The published-dependency and runner-gap items now close the Tigrcorn placeholder issue, but they do not close Tier 4 independent validation.

## Scope

This document records a fresh repository review of the independent peer checkpoint checkpoint delivered in this zip, plus the corrective changes applied during the review.

## Executive summary

`tigrbl_auth` is **not yet certifiably fully featured** and **not yet certifiably fully RFC compliant under a strict independent-claims standard**.

The repository's internal governance artifacts still support a stronger, narrower statement:

- the retained certification boundary is internally mapped and promoted to **Tier 3**
- the retained target set is reported as **48 complete targets** with **0 partial targets** at the repository-evidence tier
- strict public claims are still blocked because **Tier 4 independent peer bundles are absent**

## Corrective changes applied in this review

1. Restored a dependency-light top-level helper export surface in `tigrbl_auth/__init__.py` for commonly referenced RFC helpers and selected module exports.
2. Added dependency-light compatibility behavior for legacy helper modules and facades that previously failed immediately when the full runtime stack was absent:
   - `tigrbl_auth/rfc/rfc7515.py`
   - `tigrbl_auth/rfc/rfc8628.py`
   - `tigrbl_auth/rfc/rfc8932.py`
   - `tigrbl_auth/rfc/rfc9101.py`
   - `tigrbl_auth/rfc/rfc9396.py`
   - `tigrbl_auth/rfc/rfc7662.py`
   - `tigrbl_auth/standards/oauth2/introspection.py`
   - `tigrbl_auth/standards/jose/rfc7515.py`
   - `tigrbl_auth/standards/jose/rfc7517.py`
   - `tigrbl_auth/standards/jose/rfc7518.py`
3. Tightened pytest collection hygiene in `pyproject.toml` by switching to `--import-mode=importlib`, adding `pythonpath = ["."]`, and excluding cache directories from recursive discovery.
4. Updated `tigrbl_auth/runtime_cfg.py` so reloading the compatibility facade refreshes the canonical settings module, allowing environment-driven helper tests to reflect current environment values.
5. Corrected stale documentation that still said `serve` could not launch runtime.
6. Removed checked-in cache directories from the checkpoint output package.

## Verification performed during this review

### Dependency-light import verification

A direct smoke import confirmed that the following top-level helpers now import cleanly in a dependency-light environment:

- JOSE helpers: `sign_jws`, `verify_jws`, `load_signing_jwk`, `load_public_jwk`, `supported_algorithms`
- PKCE helpers: `makeCodeVerifier`, `makeCodeChallenge`, `verify_code_challenge`
- RFC helpers: `RFC7520_SPEC_URL`, `jws_then_jwe`, `jwe_then_jws`, `RFC8628_SPEC_URL`, `generate_user_code`, `validate_user_code`, `generate_device_code`, `RFC9207_SPEC_URL`, `extract_issuer`, `AuthorizationDetail`, `RFC9396_SPEC_URL`, `parse_authorization_details`, `RFC8932_SPEC_URL`, `enforce_encrypted_dns`
- module exports: `runtime_cfg`, `rfc7591`, `rfc7592`, `rfc7662`, `rfc9101`

### Focused test slice

The following focused dependency-light test slice passed in this container:

- `tests/unit/test_rfc7515_jws.py`
- `tests/unit/test_rfc7517_jwk.py`
- `tests/unit/test_rfc7518_jwa.py`
- `tests/unit/test_rfc7636_pkce.py`
- `tests/unit/test_rfc8628_device_authorization.py`
- `tests/unit/test_rfc9396_authorization_details.py`
- `tests/unit/test_rfc8932_dns_privacy.py`
- `tests/unit/test_rfc7520_examples.py`
- `tests/unit/test_rfc7662_unit.py`
- `tests/unit/test_rfc9101_jwt_secured_authorization_request.py`
- `tests/unit/test_runtime_cfg.py`
- `tests/unit/test_rfc9207_issuer_identification.py`
- `tests/unit/test_rfc8812_webauthn_algorithms.py`

Observed result: **52 passed**.

### Broader repository test pass

A broad `pytest -q` pass in this container still fails during collection with **52 collection errors**. Those remaining errors are dominated by missing external runtime dependencies such as:

- `sqlalchemy`
- `tigrbl`
- `swarmauri_signing_jws`
- `bcrypt`

Those failures are concentrated in runtime-heavy modules such as `tigrbl_auth/framework.py`, `tigrbl_auth/security/*`, `tigrbl_auth/orm/*`, `tigrbl_auth/tables/*`, `tigrbl_auth/jwtoken.py`, runtime endpoint modules, migration runtime paths, and full application/integration tests.

## What is complete

The repository's own package review artifacts still mark the following retained targets as complete at Tier 3:

### Baseline protocol targets

- RFC 6749
- RFC 6750
- RFC 7636
- RFC 8414
- RFC 8615
- RFC 7515
- RFC 7517
- RFC 7518
- RFC 7519
- OIDC Core 1.0
- OIDC Discovery 1.0

### Production protocol targets

- RFC 7516
- RFC 7009
- RFC 7521
- RFC 7523
- RFC 7591
- RFC 7662
- RFC 8252
- RFC 9068
- RFC 9728
- RFC 6265
- OIDC UserInfo
- OIDC Session Management
- OIDC RP-Initiated Logout

### Hardening protocol targets

- RFC 7592
- RFC 8628
- RFC 8693
- RFC 8705
- RFC 8707
- RFC 9101
- RFC 9126
- RFC 9207
- RFC 9396
- RFC 9449
- RFC 9700
- OIDC Front-Channel Logout
- OIDC Back-Channel Logout

### Runtime / contract / operator targets

- OpenAPI 3.1 / 3.2 compatible public contract
- OpenRPC 1.4.x admin/control-plane contract
- ASGI 3 application package
- Runner profile: Uvicorn
- Runner profile: Hypercorn
- Runner profile: Tigrcorn
- CLI operator surface
- Bootstrap and migration lifecycle
- Key lifecycle and JWKS publication
- Import/export portability
- Release bundle and signature verification

## What remains incomplete or non-certifiable

### Certification blockers

- No retained target is promoted to Tier 4 in this checkpoint.
- No preserved independent peer bundles exist for the full retained boundary.
- Strict public independent claims therefore remain blocked even if the internal Tier 3 boundary is closed.

### Environment and reproducibility blockers

- The package declares `requires-python = ">=3.10,<3.13"`; Python 3.13 remains outside the declared support boundary.
- A fresh runtime probe in this container still fails to build the application because `tigrbl` is not installed.
- Runtime-qualified serving profiles are therefore not fully runnable in this container even though the operator surface exists.
- The `tigrcorn` extra still exists only as metadata; no additional published runner pin is committed here.
- The broader test suite still requires external runtime packages that are not vendored into this zip.

### Operational / production-grade gaps

- `tigrbl_auth/services/operator_service.py` explicitly describes the operator service as **checkpoint-grade** and uses repository-backed JSON state under `dist/operator-state/` rather than a live integrated control-plane datastore.
- `tigrbl_auth/services/import_export_service.py` remains a thin wrapper over the same checkpoint operator-state model.
- `tigrbl_auth/migrations/versions/0007_browser_session_cookie_and_auth_code_linkage.py` has a downgrade that intentionally returns `None`, leaving that migration effectively forward-only in checkpoint tooling.

### Documentation / repo hygiene gaps found in this review

- `README.md` and `docs/runbooks/CLEAN_CHECKOUT_REPRO.md` had stale statements claiming `serve` could not launch runtime; those statements were corrected in this review.
- The repository shipped cache directories (`__pycache__`, `.pytest_cache`) that should not be preserved in a certification checkpoint output.

## Files or modules that still require work before full-feature or full-certification claims

### Hard blockers

- `compliance/evidence/tier4/` (candidate structure exists, preserved independent bundles do not)
- `docs/compliance/TIER4_PROMOTION_MATRIX.md`
- `docs/compliance/PEER_MATRIX_REPORT.md`

### Runtime / packaging / environment blockers

- `pyproject.toml` (support boundary remains `<3.13` and external runtime dependencies are still required)
- `docs/runbooks/INSTALLATION_PROFILES.md`
- `docs/runbooks/CLEAN_CHECKOUT_REPRO.md`
- `tigrbl_auth/framework.py`
- `tigrbl_auth/api/app.py` and the full app factory path
- `tigrbl_auth/security/*`
- `tigrbl_auth/orm/*`
- `tigrbl_auth/tables/*`
- `tigrbl_auth/runtime/*` runner adapters when their backing packages or Tigrbl runtime imports are unavailable
- migration/runtime paths that depend on SQLAlchemy being present

### Production-grade feature maturity blockers

- `tigrbl_auth/services/operator_service.py`
- `tigrbl_auth/services/_operator_store.py`
- `tigrbl_auth/services/import_export_service.py`
- `tigrbl_auth/api/rpc/methods/*` that front repository-backed operator state rather than a live control plane
- `tigrbl_auth/migrations/versions/0007_browser_session_cookie_and_auth_code_linkage.py`

## Public operator surface status

The executable CLI surface is broad and present: `serve`, `verify`, `gate`, `spec`, `claims`, `evidence`, `adr`, `doctor`, `bootstrap`, `migrate`, `release`, `tenant`, `client`, `identity`, `flow`, `session`, `token`, `keys`, `discovery`, `import`, and `export` are all present.

However, certifiable operational maturity is still limited by the facts above:

- runtime launch depends on missing external runtime packages in a clean checkout
- Superseded by the public-route checkpoint follow-on checkpoint: Tigrcorn is now pinned to a published runner package in packaging terms, but independent validation is still incomplete
- some admin/control-plane actions are repository-backed checkpoint operations rather than fully integrated production control-plane behavior

## Specific review observations from the current container

- Supported Python boundary in metadata: `>=3.10,<3.13`
- Observed interpreter during review: `Python 3.13.5`
- Runtime profile probe summary: Uvicorn and Hypercorn were present as runner packages in the container but still reported invalid because the application factory probe failed to import `tigrbl`; Tigrcorn reported missing.
- A raw `pytest -q` run in this container is still not a valid clean-checkout certification signal because the environment lacks required runtime packages and is outside the declared Python boundary.
- The dependency-light standards/helper slice is materially healthier than before this review and now passes the focused 52-test slice listed above.

## What would be required to reach a certifiably fully featured and certifiably fully RFC compliant package

1. Preserve complete Tier 4 independent peer bundles for the full retained boundary and promote the retained targets accordingly.
2. Re-run clean-room installation and runtime validation on supported Python versions with published `tigrbl` and `swarmauri_*` dependencies available from the declared installation profiles.
3. Publish or pin a real Tigrcorn runner package if Tigrcorn remains inside the certified runner boundary.
4. Replace checkpoint-grade repository-backed operator/control-plane state with a production-integrated durable control plane, or explicitly narrow the certified boundary so the package stops claiming that richer operational behavior.
5. Implement a portable reverse path for forward-only migration segments if downgrade/rollback remains inside the lifecycle certification target.
6. Continue reconciling historical planning/reference docs with the executable package surface so public documentation never overstates package capabilities.
7. Either fully vendor or make reliably installable the runtime-heavy dependencies required by `framework`, ORM/table paths, security dependencies, migrations, and full app-factory startup on supported interpreters.

## Bottom line

This checkpoint is a **truthful Tier 3 repository-evidence checkpoint**, not a final independently certifiable release.
