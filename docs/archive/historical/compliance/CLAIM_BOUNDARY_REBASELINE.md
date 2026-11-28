<!-- NON_AUTHORITATIVE_HISTORICAL -->

> [!WARNING]
> Historical checkpoint / planning note — non-authoritative for the current release.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and `CERTIFICATION_STATUS.md` for current release truth.

> [!WARNING] Historical / non-authoritative document. This file is retained for provenance or implementation context only. Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md` and the generated current-state reports for current release truth.

> **Historical / non-authoritative** — This document is retained for planning or provenance only.
> Do **not** use it to determine the current certification state, executable surface, or release readiness.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and `CERTIFICATION_STATUS.md` instead.

# boundary-lock checkpoint Claim Boundary Rebaseline

## Objective

Rebaseline the certification scope for the updated package model so the package is evaluated as:

- a protocol implementation,
- an ASGI 3 application package with runner-qualified serving profiles,
- and an operator/lifecycle package with CLI, key/JWKS, import/export, and release surfaces.

## What was changed

- added `compliance/targets/runtime-targets.yaml`
- added `compliance/targets/operator-targets.yaml`
- updated `compliance/targets/certification_scope.yaml` to include protocol, runtime, and operator manifests
- updated declared claims and target mappings for the new runtime/operator targets
- added ADRs:
  - `docs/adr/ADR-0027-runner-profile-certification.md`
  - `docs/adr/ADR-0028-cli-operator-surface-is-certification-boundary.md`
- removed `key` from the certified CLI surface in favor of canonical `keys`
- regenerated:
  - ADR index
  - CLI docs
  - certification scope
  - certification boundary docs
  - target reality matrix
  - effective claims/evidence manifests
  - state reports

## Current truthful status

This checkpoint **does not** make the package fully featured or fully RFC compliant.

It does make the package boundary more truthful by declaring package-level targets that were previously only implicit, including:

- ASGI 3 application package
- runner profiles for Uvicorn, Hypercorn, and Tigrcorn
- CLI/operator surface
- bootstrap and migration lifecycle
- key lifecycle and JWKS publication
- import/export portability
- release bundle and signature verification

## Known remaining gaps after boundary-lock checkpoint

- `serve` still emits a plan instead of launching runtime
- runner profiles are declared but not implemented as first-class launch adapters
- multiple operator families remain list/show-only
- import/export remains declaration-level rather than portability-complete
- the retained boundary still contains many Tier 1 and Tier 2 targets
- no public independent claim is allowed because Tier 4 remains empty

## ADR numbering note

The plan text originally referenced new ADRs numbered `0023` and `0024`, but those numbers were already occupied in this repository. To preserve sequence integrity, the new decisions were added as:

- `ADR-0027-runner-profile-certification`
- `ADR-0028-cli-operator-surface-is-certification-boundary`
