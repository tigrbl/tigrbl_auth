> [!WARNING] Non-authoritative active document. For current release and certification truth, use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md` and the generated current-state reports.

<!-- NON_AUTHORITATIVE_HISTORICAL -->
> [!WARNING]
> Historical / non-authoritative checkpoint document.
> Do **not** use this file to determine the current certification state, executable surface, or release readiness.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and `CERTIFICATION_STATUS.md` instead.

> [!WARNING] Historical / non-authoritative document. This file is retained for provenance or implementation context only. Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md` and the generated current-state reports for current release truth.

> **Historical / non-authoritative** — This document is retained for planning or provenance only.
> Do **not** use it to determine the current certification state, executable surface, or release readiness.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and `CERTIFICATION_STATUS.md` instead.

# Feature Flags and Installable Surfaces

## Purpose

This note describes the governed runtime and operator flag model and, as of the
capability-wiring checkpoint checkpoint, the executable capability registry that drives route
publication, discovery publication, and contract generation.

## Runtime flag groups

- baseline
- production
- hardening
- operations
- surface
- alignment-only
- extension-quarantine

## Executable capability registry

The authoritative public surface is now declared once in:

- `tigrbl_auth/config/surfaces.py:PUBLIC_CAPABILITIES`

Each capability record owns:

- the capability identifier used by deployment resolution
- the mount group used by runtime composition
- the published route path(s)
- the HTTP method set
- the required feature flags
- the router or publisher reference that backs the route
- contract/discovery visibility metadata

That registry is consumed by:

- `tigrbl_auth/config/deployment.py` to derive `active_capabilities` and `active_routes`
- `tigrbl_auth/api/surfaces.py` to mount routers and standards-owned publishers
- OpenAPI/discovery snapshot generation
- capability-wiring checkpoint target/module/route/contract/test/evidence cross-check scripts

The release path therefore no longer relies on one set of route lists for
contracts and a different hand-maintained set for runtime mounting.

## Downstream partial feature consumption

Downstream consumers may adopt only the capabilities they need.

### Profiles
- `baseline`
- `production`
- `hardening`
- `peer-claim`

### Surface sets
- `public-rest`
- `admin-rpc`
- `diagnostics`
- any combination of the above

### Protocol slices
- `device`
- `token-exchange`
- `par`
- `jar`
- `rar`
- `dpop`
- `mtls`

### Quarantined extensions
- `webauthn-passkeys`
- `set`
- `webpush`
- `dns-privacy`

### Runtime styles
- `plugin`
- `standalone`

## Partial feature consumption rule

A downstream deployment may consume any subset of the governed surfaces, but a
disabled feature must disappear from:

- mounted routes
- discovery/metadata output
- generated contracts
- compliance claims
- release evidence bundles

## Plugin modes

- `public-only`
- `admin-only`
- `mixed`
- `diagnostics-only`

## capability-wiring checkpoint reality checks

The capability-wiring checkpoint checkpoint adds dependency-light cross-checks so executable reality
can be validated without importing the full external Tigrbl workspace:

- `scripts/verify_target_module_mapping.py`
- `scripts/verify_target_route_mapping.py`
- `scripts/verify_target_contract_mapping.py`
- `scripts/verify_target_test_mapping.py`
- `scripts/verify_target_evidence_mapping.py`
- stricter `scripts/verify_contract_sync.py`
- stricter `scripts/verify_feature_surface_modularity.py`

Those checks validate that in-scope targets are connected to existing modules,
live mounted routes, committed contracts, mapped tests, and mapped evidence
references, and that no committed contract path lacks a decorated implementation
backed by the executable capability registry.
