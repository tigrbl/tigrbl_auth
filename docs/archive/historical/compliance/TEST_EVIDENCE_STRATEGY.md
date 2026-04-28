<!-- NON_AUTHORITATIVE_HISTORICAL -->
> [!WARNING]
> Historical / non-authoritative checkpoint document.
> Do **not** use this file to determine the current certification state, executable surface, or release readiness.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and `CERTIFICATION_STATUS.md` instead.

> [!WARNING] Historical / non-authoritative document. This file is retained for provenance or implementation context only. Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md` and the generated current-state reports for current release truth.

> **Historical / non-authoritative** — This document is retained for planning or provenance only.
> Do **not** use it to determine the current certification state, executable surface, or release readiness.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and `CERTIFICATION_STATUS.md` instead.

# TEST_EVIDENCE_STRATEGY

## Objective

test-plane checkpoint turns the repository test corpus into a certification-usable matrix with a canonical classification manifest, explicit target mappings, and a heatmap that shows the mix of unit, integration, conformance, interop, end-to-end, security, negative, and performance coverage per in-scope target.

## Canonical manifests

The authoritative test-plane checkpoint test-plane artifacts are:

- `compliance/mappings/test_classification.yaml`
- `compliance/mappings/target-to-test.yaml`
- `docs/compliance/TEST_COVERAGE_HEATMAP.md`
- `docs/compliance/test_classification_report.md`
- `docs/compliance/target_test_mapping_report.md`

`compliance/mappings/test-classification.yaml` is retained as a compatibility mirror, but the canonical manifest for new work is `test_classification.yaml`.

## Taxonomy

The canonical classification uses exactly eight categories:

- `unit`
- `integration`
- `conformance`
- `interop`
- `e2e`
- `security`
- `negative`
- `perf`

Auxiliary documentation-driven example tests under `tests/examples/` are classified as `e2e` so the certification matrix remains category-complete without keeping a ninth class.

## Mapping rules

A test is considered certification-usable only when all of the following are true:

1. it exists under `tests/**/test_*.py`
2. it is present in `compliance/mappings/test_classification.yaml`
3. any in-scope target that depends on it lists it in `compliance/mappings/target-to-test.yaml`
4. it remains within the canonical test-plane checkpoint category set

test-plane checkpoint verification now fails closed on:

- unclassified test files
- classified files that do not exist
- legacy `tests/i9n/` files remaining in-tree
- in-scope targets missing explicit test mappings
- target mappings that reference tests outside the canonical classification manifest

## Coverage families addressed explicitly in test-plane checkpoint

test-plane checkpoint adds or formalizes explicit coverage for:

- new public routes and profile-visible surfaces
- durable persistence and lifecycle state
- profile-specific allow and deny behavior
- browser session, cookie, and logout durability
- revocation and introspection durability
- PAR, JAR, RAR, and resource indicators
- DPoP, mTLS, and token exchange routing/profile presence
- contract conformance by committed snapshot
- migration upgrade, downgrade, and reapply safety

The added integration tests are:

- `tests/integration/test_profile_surface_and_contract_alignment.py`
- `tests/integration/test_persistence_lifecycle_durability.py`
- `tests/integration/test_migration_upgrade_downgrade_safety.py`

## Evidence use by category

The categories are used differently in certification evidence:

- `conformance` is the strongest direct RFC/spec behavior evidence
- `integration` proves cross-module and durable-state behavior on the repository-owned runtime path
- `negative` proves reject/deny semantics and abuse handling
- `security` proves release-trust and control-plane security properties
- `interop` is reserved for peer-facing compatibility and Tier 4 style evidence inputs
- `unit` supports internal correctness and targeted standards helpers
- `e2e` supports release-path and documentation-driven flows
- `perf` supports artifact and footprint controls, not feature completeness by itself

## What test-plane checkpoint completes

test-plane checkpoint completes the structural test-plane work required before Tier 3 evidence promotion can be done honestly:

- legacy integration tests are migrated from `tests/i9n/` to `tests/integration/`
- the classification manifest is complete for the current corpus
- every in-scope target has explicit mapped tests
- a target-by-category heatmap is committed
- dependency-light static checks confirm the matrix is internally consistent

## What test-plane checkpoint does not claim

test-plane checkpoint does not by itself prove certification-grade execution. The repository still needs:

- executed Tier 3 preserved evidence across the retained boundary
- Tier 4 independent peer validation
- stronger release signing and attestation
- broader execution in a fully provisioned runtime environment for bounded/helper targets

## Current honest status

The test plane is now classification-complete for the repository checkpoint, but the package is still **not yet certifiably fully featured** and **not yet certifiably fully RFC/spec compliant across the full declared boundary**.
