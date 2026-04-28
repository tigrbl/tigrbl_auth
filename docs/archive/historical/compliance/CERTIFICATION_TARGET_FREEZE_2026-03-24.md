<!-- NON_AUTHORITATIVE_HISTORICAL -->
> [!WARNING]
> Historical / non-authoritative checkpoint document.
> Do **not** use this file to determine the current certification state, executable surface, or release readiness.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and `CERTIFICATION_STATUS.md` instead.

> [!WARNING] Historical / non-authoritative document. This file is retained for provenance or implementation context only. Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md` and the generated current-state reports for current release truth.

> **Historical / non-authoritative** — This document is retained for planning or provenance only.
> Do **not** use it to determine the current certification state, executable surface, or release readiness.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and `CERTIFICATION_STATUS.md` instead.

# Certification Target Freeze — 2026-03-24

## Decisions completed in this checkpoint

The following decisions are now frozen for the current repository checkpoint:

- fully featured boundary mode: `retained-48-target-package-boundary-with-production-grade-operator-control-plane`
- stronger production-grade durable control-plane boundary selected: `True`
- supported Python range for certification: `>=3.10,<3.13`
- supported Python versions for certification: `['3.10', '3.11', '3.12']`
- Python 3.13 status: `not-in-certification-scope-until-validated`
- kept runner profiles in the retained boundary: `['uvicorn', 'hypercorn', 'tigrcorn']`
- Tigrcorn boundary status: `retained-in-boundary-with-pinned-clean-room-profile-on-python-3.11-and-3.12-but-not-yet-independently-validated`

## Rationale

This checkpoint is a truth-alignment and certification-target-freeze update. It does **not** promote the package to final independent certification. Instead, it removes ambiguity about what is being certified and how current status artifacts should be interpreted.

The stronger production-grade durable control-plane boundary is now selected inside the retained 48-target package boundary because the authoritative operator surface routes through a durable SQLite-backed external state backend with tenant scoping, transactional mutation/audit durability, and versioned portability artifacts. The certified operator plane no longer depends on repository file mutation.

Tigrcorn remains in the retained boundary for continuity with the existing independent peer checkpoint target catalog and peer-profile matrix. This checkpoint now commits a published Tigrcorn runner pin and a clean-room CI/tox matrix for Python 3.11 and 3.12. That continuity choice still does **not** make Tigrcorn independently validated. It remains a blocker until preserved execution evidence and independent validation artifacts exist.

Python 3.13 is explicitly **not** part of the current certification boundary because `pyproject.toml` still declares `>=3.10,<3.13` and the package has not yet been fully validated on 3.13.

## Operator/control-plane posture after Item 6

- authoritative backend: `sqlite-authoritative`
- repository file mutation required for certified operator surface: `False`
- tenancy enforced in the authoritative backend: `True`
- portability schema version: `3`

## Current package-level status after the freeze

- retained target count: `48`
- fully certifiable now: `False`
- fully RFC/spec compliant now: `False`
- strict independent claims ready: `False`

## Why package-level status remains false

- preserved Tier 4 independent peer bundles are still missing for the retained boundary
- the clean-room certification matrix is now defined in-repository, but successful execution across the supported interpreter/profile matrix is not preserved in this container
- Tigrcorn is pinned and included in the clean-room matrix for Python 3.11/3.12, but independent validation remains absent
- Python 3.13 remains outside the current support boundary

## Files reconciled by this checkpoint

- `compliance/targets/certification_scope.yaml`
- `CURRENT_STATE.md`
- `CERTIFICATION_STATUS.md`
- `docs/compliance/certification_state_report.md`
- `docs/compliance/PACKAGE_REVIEW_GAP_ANALYSIS.md`
- `docs/compliance/final_target_decision_matrix.json`
- `docs/compliance/RELEASE_DECISION_RECORD.md`
- `docs/compliance/current_state.md`
- `docs/compliance/current_state_report.md`
- `docs/compliance/CERTIFICATION_TARGET_RECONCILIATION_2026-03-24.md`
- `docs/compliance/CERTIFICATION_TARGET_RECONCILIATION_2026-03-24.json`

## Interpretation rule

If any historical artifact disagrees with the files listed above, treat the historical artifact as archival context rather than as the authoritative current repository state.

## Added for Device-code polling item

- clean-room matrix manifest: `tox.ini`
- install workflow: `.github/workflows/ci-install-profiles.yml`
- release-gate workflow: `.github/workflows/ci-release-gates.yml`
- runtime smoke script: `scripts/clean_room_profile_smoke.py`
