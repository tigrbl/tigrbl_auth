# Non-RFC track closeout Non-RFC Track Closeout Checkpoint — 2026-03-26

## Scope of work completed

This checkpoint addressed the retained non-RFC standards/specs track:

- OIDC Core 1.0
- OIDC Discovery 1.0
- OIDC UserInfo
- OIDC Session Management
- OIDC RP-Initiated Logout
- OIDC Front-Channel Logout
- OIDC Back-Channel Logout
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

## Code / repo changes made

### Runtime and OIDC compatibility repairs

- `tigrbl_auth/runtime/base.py`
  - `LazyASGIApplication` now proxies attribute access so runtime consumers and tests can use `app.router`, `app.state`, and similar members safely after lazy materialization.
- `tigrbl_auth/config/deployment.py`
  - added `deployment_from_app(...)` and `deployment_from_request(...)` so route inclusion and handler metadata follow the materialized deployment instead of silently re-resolving global baseline settings.
- `tigrbl_auth/standards/oidc/discovery.py`
- `tigrbl_auth/standards/oauth2/rfc8414.py`
- `tigrbl_auth/standards/oauth2/rfc9728.py`
- `tigrbl_auth/standards/oidc/userinfo.py`
  - switched handler/include logic to app/request deployment resolution.
- `tigrbl_auth/app.py`
  - package-level `app` now defaults to **production** when the ambient configured profile is still baseline.
- `tigrbl_auth/oidc_id_token.py`
  - compatibility facade now mirrors mutable provider/cache state expected by legacy fixtures when the canonical runtime implementation is available.
- `tigrbl_auth/standards/oidc/backchannel_logout.py`
  - checkpoint logout-token minting stays self-contained so validation does not require initialized token-record tables.
- `tigrbl_auth/oidc_userinfo.py`
  - aligned legacy compatibility surface with the deployment-aware/runtime-patchable UserInfo behavior.
- `tigrbl_auth/__init__.py`
  - installs `HTTPStatus.HTTP_<code>_<NAME>` aliases used by the repository’s compatibility surface and tests.

### Target / contract truth alignment

- `compliance/claims/declared-target-claims.yaml`
  - moved `OpenRPC 1.4.x admin/control-plane contract` to baseline claim truth, which matches the retained baseline runtime/contract reality.
- regenerated:
  - `compliance/claims/effective-target-claims.*.yaml`
  - `compliance/evidence/effective-release-evidence.*.yaml`
  - `specs/openapi/profiles/*/openapi.json`
  - `specs/openrpc/profiles/*/tigrbl_auth.admin.openrpc.json`
  - `specs/discovery/profiles/*/*.json`
  - `docs/reference/CLI_SURFACE.md`
  - `docs/compliance/cli_conformance_snapshot.*`
  - `compliance/targets/certification_scope.yaml`
  - `docs/compliance/TARGET_REALITY_MATRIX.md`
  - `docs/compliance/CERTIFICATION_BOUNDARY.md`
  - `docs/compliance/rfc_family_status_report.*`
  - `docs/compliance/non_rfc_status_report.*`
  - `docs/compliance/current_state_report.*`
  - `docs/compliance/certification_state_report.*`

## Verification completed in this container

### Focused Non-RFC track closeout non-RFC verification reports

- `dist/test-reports/non-rfc-oidc-contracts-py313.json`: `22 / 22` passed
- `dist/test-reports/non-rfc-surface-cli-py313.json`: `9 / 9` passed
- `dist/test-reports/non-rfc-operator-runtime-py313.json`: `21 / 21` passed

Combined Non-RFC track closeout focus total: **52 / 52 passed**.

### Additional checkpoint regressions

- `tests/unit/test_non_rfc_track_checkpoint.py`: passed
- `tests/unit/test_profile_discovery_runtime.py`: passed
- `tests/unit/test_rpc_registry_live.py`: passed

## Truthful status after this checkpoint

### What is now true

- the retained non-RFC target set shows **18 / 18 internally backed** targets in `docs/compliance/non_rfc_status_report.json`
- the retained non-RFC target set shows **0 non-RFC scope discrepancies** in `compliance/targets/certification_scope.yaml`
- OIDC discovery, UserInfo, logout/session surfaces, OpenAPI, OpenRPC, CLI/operator lifecycle, JWKS publication, import/export, and release-bundle signing all have focused local verification evidence preserved in this checkpoint

### What is still not true

- this repository is **not yet certifiably fully featured**
- this repository is **not yet certifiably fully RFC compliant**
- this repository is **not yet certifiably fully non-RFC spec/standard compliant**

The remaining blockers are still certification-evidence blockers:

- supported runtime matrix remains `0 / 14`
- supported certification lanes remain `5 / 15`
- PostgreSQL migration portability evidence is still missing
- Tier 3 rebuild-from-validated-runs is still incomplete
- Tier 4 external peer bundles are still incomplete
- retained RFC discrepancies remain open for `RFC 7516`, `RFC 7592`, and `RFC 9207`
