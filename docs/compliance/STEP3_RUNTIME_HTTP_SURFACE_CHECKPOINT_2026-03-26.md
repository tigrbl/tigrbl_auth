# Step 3 Runtime HTTP Surface Checkpoint — 2026-03-26

## Scope

This checkpoint addresses the Step 3 closeout task:

> Make the runtime HTTP surface probes pass.

The retained probe target set for this step is:

- `/.well-known/openid-configuration`
- `/.well-known/oauth-authorization-server`
- `/.well-known/oauth-protected-resource`
- `/.well-known/jwks.json`
- `/openapi.json`

Primary owner areas for this checkpoint:

- `tigrbl_auth/api/surfaces.py`
- `tigrbl_auth/api/rest/*`
- `tigrbl_auth/standards/oidc/discovery.py`
- `tigrbl_auth/standards/oidc/discovery_metadata.py`
- `tigrbl_auth/standards/oauth2/rfc8414.py`
- `tigrbl_auth/standards/oauth2/rfc8414_metadata.py`
- `tigrbl_auth/standards/oauth2/rfc9728.py`
- `tigrbl_auth/standards/http/well_known.py`
- `tigrbl_auth/standards/jose/rfc7517.py`

## What was fixed

### 1. Runtime HTTP surface probing is now deployment-aware

The earlier probe helper treated all five endpoints as mandatory for every profile. That was incorrect for the retained deployment boundary because the baseline profile intentionally does **not** expose RFC 9728 protected-resource metadata.

This checkpoint makes runtime HTTP surface probing profile-aware:

- the built ASGI app now carries the resolved deployment on `app.state`
- the runtime probe helper filters the surface target set to the deployment's active routes
- `/openapi.json` remains required when the public REST surface is enabled
- inactive profile routes are no longer reported as false-negative runtime failures

Result:

- baseline probe target set is now `4` endpoints
- production probe target set is now `5` endpoints, including RFC 9728

### 2. Clean-room smoke execution now resolves the real configured deployment profile

`scripts/clean_room_profile_smoke.py` previously called `resolve_deployment()` without passing the configured settings object, which forced the probe to behave as the default baseline profile even when environment overrides were supplied.

This checkpoint changes the smoke script to resolve deployment from `tigrbl_auth.config.settings.settings`, so profile-specific execution now works as intended.

Result:

- baseline smoke probes baseline surfaces
- production smoke probes production surfaces
- profile-specific runtime artifacts can now be preserved truthfully in `dist/runtime-smoke/`

### 3. Public REST shared helpers no longer trigger an import-time circular dependency

`tigrbl_auth/api/rest/shared.py` eagerly constructed `JWTCoder.default()` at import time. During production-profile materialization that import path fed back into RFC 7662 introspection support, which forced `tigrbl_auth.standards.oauth2.introspection` into its dependency-light fallback router.

That fallback router emitted route objects without the public `name` attribute expected by published `tigrbl==0.3.15`, which caused production app materialization to fail before the HTTP probes could run.

This checkpoint replaces the eager helpers with lazy runtime proxies.

Result:

- RFC 7662 introspection now imports against the real runtime router in a dependency-complete environment
- production app materialization succeeds
- RFC 9728 protected-resource metadata can now be exercised in the production surface probe

## Verification performed in this checkpoint

A dependency-complete local verification environment was used to run the surface probes from published pins.

Because this container only provides Python `3.13.5`, the probes ran in an **unsupported local verification environment** using the already-materialized dependency-complete venv from Step 2. That is useful engineering evidence, but it is **not certification-grade proof** for the retained support boundary of Python `3.10`, `3.11`, and `3.12`.

### Baseline probe

Command shape:

```bash
TIGRBL_AUTH_MATRIX_PROFILE=baseline \
python scripts/clean_room_profile_smoke.py --probe-surfaces --require-surface-probes
```

Result:

- app materialization: **passed**
- surface probe: **passed**
- endpoint count: **4 / 4**
- probed endpoints:
  - `/.well-known/openid-configuration`
  - `/.well-known/oauth-authorization-server`
  - `/.well-known/jwks.json`
  - `/openapi.json`

Artifact preserved at:

- `dist/runtime-smoke/baseline-base.json`

### Production probe

Command shape:

```bash
TIGRBL_AUTH_PROFILE=production \
TIGRBL_AUTH_MATRIX_PROFILE=production \
python scripts/clean_room_profile_smoke.py --probe-surfaces --require-surface-probes
```

Result:

- app materialization: **passed**
- surface probe: **passed**
- endpoint count: **5 / 5**
- probed endpoints:
  - `/.well-known/openid-configuration`
  - `/.well-known/oauth-authorization-server`
  - `/.well-known/oauth-protected-resource`
  - `/.well-known/jwks.json`
  - `/openapi.json`

Artifact preserved at:

- `dist/runtime-smoke/production-base.json`

### Generated current-state/runtime reports

The generated runtime report now truthfully records the baseline application and surface probe as passing:

- `docs/compliance/runtime_profile_report.md`
- `CURRENT_STATE.md`
- `CERTIFICATION_STATUS.md`

## What is complete for Step 3

This checkpoint removes the concrete Step 3 runtime-surface blocker seen in the previous checkpoint:

- baseline runtime surface probe no longer falsely fails on the intentionally inactive RFC 9728 route
- production profile now materializes and exposes protected-resource metadata
- the smoke tool can now preserve profile-accurate probe artifacts in `dist/runtime-smoke/`

## What is still blocking certification-grade Step 3 closeout

The Step 3 exit criterion was:

> application probe and surface probe both pass in clean-room execution

That criterion is **engineering-complete in this checkpoint for local dependency-complete probes**, but it is **not yet certification-grade complete** because:

1. this container does not provide Python `3.10`, `3.11`, or `3.12` interpreter binaries;
2. the preserved probe evidence in this checkpoint was produced under Python `3.13.5`, outside the retained support range;
3. the clean-room matrix artifacts required by the validated execution reports are still missing;
4. hypercorn and tigrcorn were not installed in this local probe environment, so only the baseline app/surface execution proof and uvicorn serve-check are presently represented in generated runtime state.

## Current truthful status

- Step 3 code-level runtime HTTP surface blocker removal: **complete for this checkpoint**
- baseline app + surface probe in a dependency-complete local environment: **passed**
- production app + surface probe in a dependency-complete local environment: **passed**
- certification-grade supported-interpreter matrix evidence: **not complete**
- package certifiably fully featured: **no**
- package certifiably fully RFC compliant: **no**

## Files changed by this checkpoint

- `tigrbl_auth/api/app.py`
- `tigrbl_auth/api/rest/shared.py`
- `tigrbl_auth/plugin.py`
- `tigrbl_auth/cli/runtime.py`
- `scripts/clean_room_profile_smoke.py`
- `tests/unit/test_app_factory_materialization.py`
- `tests/unit/test_runtime_validation_matrix.py`
- generated runtime/state documentation under `docs/compliance/`
- `CURRENT_STATE.md`
- `CERTIFICATION_STATUS.md`

## Focused regression evidence

The following focused regression set passed in this checkpoint:

- `tests/unit/test_app_factory_materialization.py`
- `tests/unit/test_public_route_contracts.py`
- `tests/unit/test_runtime_validation_matrix.py`
- `tests/unit/test_deployment_resolver.py`
- `tests/unit/test_rfc9728_metadata_checkpoint.py`

Total passed in the focused set: **14**.
