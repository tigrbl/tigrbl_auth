# RFC track closeout RFC Track Closeout Checkpoint — 2026-03-26

## Scope of this checkpoint

This checkpoint advances **RFC track closeout: Close the RFC track family-by-family**.

It does **not** truthfully complete final certification. The package remains blocked by missing supported-matrix runtime evidence, missing full supported test-lane evidence, missing PostgreSQL migration portability evidence, missing Tier 3 rebuild-from-validated-runs evidence, and missing Tier 4 external peer bundles.

## Repository changes made in this checkpoint

### 1. Closed RFC endpoint-surface drift

`compliance/mappings/target-to-endpoint.yaml` was updated so that:

- `RFC 6750` now maps to `/token`, `/userinfo`, and `/introspect`
- `RFC 7636` now maps to `/authorize` and `/token`

After regeneration, the authoritative certification scope no longer reports `surface-drift` for these two baseline RFC targets.

### 2. Added dependency-light conformance coverage for bounded/helper RFC targets

New conformance tests were added for:

- `RFC 7516` → `tests/conformance/production/test_rfc7516_jwe_profile.py`
- `RFC 7521` → `tests/conformance/production/test_rfc7521_assertion_framework.py`
- `RFC 7523` → `tests/conformance/production/test_rfc7523_jwt_profile.py`
- `RFC 8615` → `tests/conformance/production/test_rfc8615_well_known_uris.py`
- `RFC 9700` → `tests/conformance/hardening/test_rfc9700_security_bcp.py`
- `RFC 9728` → `tests/conformance/production/test_rfc9728_protected_resource_metadata.py`

The canonical and legacy test-classification manifests were updated accordingly, and target-to-test mappings were extended for those RFCs.

### 3. Added an RFC family status report

A new reproducible report generator now writes:

- `docs/compliance/rfc_family_status_report.json`
- `docs/compliance/rfc_family_status_report.md`

This report summarizes all **30 retained RFC targets** across these family groupings:

- OAuth core / metadata / discovery
- JOSE / JWT
- Revocation / introspection / client registration
- Native / device / exchange / resource indicators / JWT access tokens
- Hardening / advanced auth / metadata

## Validation performed in this checkpoint

A focused dependency-light RFC verification sweep was executed locally under Python `3.13` and preserved to:

- `dist/test-reports/rfc-focus-py313.json`

Result:

- `46 passed`
- `0 failed`
- `0 skipped`

The executed files covered:

- `RFC 7516`
- `RFC 7521`
- `RFC 7523`
- `RFC 7592`
- `RFC 7636`
- `RFC 8615`
- `RFC 9207`
- `RFC 9700`
- `RFC 9728`

This local evidence is useful for defect triage and checkpointing, but it is **not** supported-matrix certification evidence because Python `3.10`, `3.11`, and `3.12` were not all available in this container and the full published runtime stack was not installed here.

## Resulting RFC status after regeneration

From `docs/compliance/rfc_family_status_report.md`:

- retained RFC target count: `30`
- retained RFC targets with conformance-classified coverage: `30`
- retained RFC targets with peer-profile mappings: `30`
- retained RFC targets with authoritative-scope discrepancies still open: `3`

The remaining RFC-target discrepancies are:

- `RFC 7516`: `active-without-effective-claim:baseline`
- `RFC 7592`: `active-without-effective-claim:production`
- `RFC 9207`: `active-without-effective-claim:production`

## What still prevents truthful full RFC certification

Even with the RFC family improvements above, the package is still blocked by certification-wide requirements:

1. the supported runtime matrix is still missing `14 / 14` preserved validated profiles
2. the supported certification-lane matrix is still missing `10` of the required `15` preserved lane executions
3. migration portability is still not preserved for both SQLite and PostgreSQL
4. Tier 3 evidence has not yet been rebuilt from validated-run manifests
5. Tier 4 external peer validation is still absent for the retained boundary

## Practical interpretation

This checkpoint materially improves the RFC track, but it should be treated as a **truthful RFC-closeout progress checkpoint**, not as a final certified release.
