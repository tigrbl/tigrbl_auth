<!-- NON_AUTHORITATIVE_HISTORICAL -->

> [!WARNING]
> Historical checkpoint / planning note — non-authoritative for the current release.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and `CERTIFICATION_STATUS.md` for current release truth.

> [!WARNING] Historical / non-authoritative document. This file is retained for provenance or implementation context only. Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md` and the generated current-state reports for current release truth.

> **Historical / non-authoritative** — This document is retained for planning or provenance only.
> Do **not** use it to determine the current certification state, executable surface, or release readiness.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and `CERTIFICATION_STATUS.md` instead.

# capability-wiring checkpoint Checkpoint — Executable Surface Reality Alignment

## Objective addressed

capability-wiring checkpoint required the deployment flags, surface sets, route publication,
contracts, and modularity reports to reflect the same executable reality.

## What changed

### 1. Canonical capability registry

The authoritative public/auth surface is now described once in:

- `tigrbl_auth/config/surfaces.py:PUBLIC_CAPABILITIES`

That registry records, per capability:

- capability identifier
- surface set
- mount group
- published path(s)
- HTTP methods
- required feature flags
- router or publisher reference
- contract/discovery visibility

### 2. Deployment resolution now tracks executable capabilities

`ResolvedDeployment` now records:

- `active_capabilities`
- `active_routes`
- `active_targets`
- `active_openrpc_methods`

This allows the package to distinguish *why* a route is active, not only *which*
route is active.

### 3. Runtime mounting is centralized

` tigrbl_auth.api.surfaces.attach_runtime_surfaces(...) ` now installs:

- REST routers
- standards-owned publishers such as UserInfo, introspection, token exchange, and discovery/JWKS surfaces
- JSON-RPC mounting
- diagnostics mounting

Both `tigrbl_auth/plugin.py` and `tigrbl_auth/api/app.py` now use that same
attachment path.

### 4. Discovery snapshots are committed by profile

This checkpoint commits profile-specific discovery snapshots under:

- `specs/discovery/profiles/baseline/`
- `specs/discovery/profiles/production/`
- `specs/discovery/profiles/hardening/`
- `specs/discovery/profiles/peer-claim/`

Committed files now include:

- `openid-configuration.json`
- `oauth-authorization-server.json`
- `jwks.json`
- `oauth-protected-resource.json` where the profile publishes that surface

### 5. Cross-check automation was added

The repository now includes dependency-light validation scripts for:

- target ↔ module
- target ↔ route
- target ↔ contract
- target ↔ test
- target ↔ evidence

The stricter top-level checks are now:

- `scripts/verify_contract_sync.py`
- `scripts/verify_feature_surface_modularity.py`

## Committed reports

The following capability-wiring checkpoint reports were generated and committed in this checkpoint:

- `docs/compliance/target_module_mapping_report.md`
- `docs/compliance/target_route_mapping_report.md`
- `docs/compliance/target_contract_mapping_report.md`
- `docs/compliance/target_test_mapping_report.md`
- `docs/compliance/target_evidence_mapping_report.md`
- `docs/compliance/contract_sync_report.md`
- `docs/compliance/feature_flags_surface_modularity_report.md`

## Exit-criteria status for this checkpoint

### Satisfied in repository shape

- No declared target is left without committed route/module/test/evidence mapping reports
- No committed public OpenAPI path is left without a backing decorated implementation according to the committed capability-wiring checkpoint checks
- No contract path exists without executable-capability backing according to the committed capability-wiring checkpoint checks
- Discovery snapshots are now profile-specific and committed

### Still outside final certification closure

- this does not by itself promote Tier 3 evidence
- this does not by itself produce Tier 4 peer validation
- this does not by itself make the repository certifiably fully featured or certifiably fully RFC/spec compliant across the full declared boundary
