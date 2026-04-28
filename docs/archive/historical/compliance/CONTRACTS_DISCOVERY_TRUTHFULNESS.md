<!-- NON_AUTHORITATIVE_HISTORICAL -->

> [!WARNING]
> Historical checkpoint / planning note — non-authoritative for the current release.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and `CERTIFICATION_STATUS.md` for current release truth.

> [!WARNING] Historical / non-authoritative document. This file is retained for provenance or implementation context only. Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md` and the generated current-state reports for current release truth.

> **Historical / non-authoritative** — This document is retained for planning or provenance only.
> Do **not** use it to determine the current certification state, executable surface, or release readiness.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and `CERTIFICATION_STATUS.md` instead.

# external peer validation checkpoint — Contracts, discovery, generated docs, and state truthfulness

## Scope completed in this checkpoint

This checkpoint completed the external peer validation checkpoint truthfulness and artifact-generation work for the current `tigrbl_auth` repository state.

The implementation updated the repository so that the primary public artifacts now derive from executable deployment, CLI, and target metadata rather than hand-maintained prose or stale static generators.

## What changed

### Runtime and surface metadata

Updated:

- `tigrbl_auth/config/deployment.py`
- `tigrbl_auth/config/surfaces.py`
- `tigrbl_auth/api/surfaces.py`

Implemented:

- active contract-route tracking on resolved deployments
- active discovery-route tracking on resolved deployments
- runner-invariant application hashing support for truthfulness checks
- route registry metadata for router references, publisher references, and discovery artifact names
- runtime surface binding manifest support for route/resource/publisher auditing

### Artifact generators

Updated:

- `tigrbl_auth/cli/artifacts.py`
- `scripts/generate_effective_release_manifests.py`
- `scripts/generate_state_reports.py`
- `scripts/generate_package_review_gap_analysis.py`
- `scripts/generate_release_decision_record.py`
- `scripts/generate_discovery_snapshots.py`

Implemented:

- generation of OpenAPI, OpenRPC, and discovery artifacts from executable deployment metadata
- generation of CLI docs, CLI contract artifacts, and CLI conformance snapshots from `tigrbl_auth/cli/metadata.py`
- generated root `CURRENT_STATE.md` and `CERTIFICATION_STATUS.md`
- generated artifact-truthfulness reporting
- generated discovery reference documentation for committed profile snapshots
- corrected package-review logic so it no longer reports `serve` as plan-only
- separated authoritative-current vs historical/planning stale-path findings

### Truthfulness checks added or strengthened

The checkpoint now generates and preserves an artifact-truthfulness report covering:

- contract-to-route sync
- route-to-contract sync
- target-to-contract sync
- CLI metadata-to-docs sync
- runtime-plan-to-discovery sync
- runner contract-hash invariance
- authoritative-current stale doc ref detection
- historical/planning stale doc ref detection

## Generated artifacts refreshed in this checkpoint

Regenerated and verified:

- `specs/openapi/**`
- `specs/openrpc/**`
- `specs/discovery/**`
- `docs/reference/CLI_SURFACE.md`
- `docs/reference/DISCOVERY_PROFILE_SNAPSHOTS.md`
- `CURRENT_STATE.md`
- `CERTIFICATION_STATUS.md`
- `docs/compliance/current_state_report.*`
- `docs/compliance/certification_state_report.*`
- `docs/compliance/artifact_truthfulness_report.*`
- `docs/compliance/PACKAGE_REVIEW_GAP_ANALYSIS.*`

## Measured external peer validation checkpoint state

- release gates: `20/20 passing`
- artifact truthfulness passed: `True`
- contract-to-route sync passed: `True`
- route-to-contract sync passed: `True`
- target-to-contract sync passed: `True`
- CLI metadata-to-docs sync passed: `True`
- runtime-plan-to-discovery sync passed: `True`
- runner contract-hash invariance passed: `True`
- authoritative current doc stale refs: `0`
- historical/planning stale refs: `77`
- declared targets: `48`
- Tier 3 targets: `39`
- Tier 4 targets: `0`

## Exit-criteria status

### Satisfied

- no current authoritative doc references missing code as if it exists
- no contract claims unmounted routes
- no runtime public routes lack contract or target mapping
- current-state and certification-state docs are generated rather than hand-maintained
- discovery profile snapshots are generated from executable deployment metadata
- CLI docs and CLI contract artifacts derive from the canonical CLI metadata source

### Still open outside external peer validation checkpoint

This checkpoint does **not** make the package certifiably fully featured or certifiably fully RFC/spec compliant across the full declared boundary.

The remaining blockers are outside the narrow external peer validation checkpoint scope:

- runtime/operator targets remain below Tier 3
- Tier 4 independent peer evidence remains absent
- clean-checkout runtime validation is still environment-limited here by missing published runtime dependencies for some runner profiles

## Truthful current status

This repository is now a stronger, more truthful, better-generated checkpoint.

It is still:

- **not** certifiably fully featured
- **not** certifiably fully RFC/spec compliant across the full retained certification boundary

It is truthfully a signed, release-gated checkpoint with generated public artifacts derived from executable metadata and with all currently declared RFC/OIDC/public-contract protocol targets at Tier 3.
