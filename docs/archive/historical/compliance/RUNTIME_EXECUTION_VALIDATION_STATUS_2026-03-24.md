<!-- NON_AUTHORITATIVE_HISTORICAL -->

> [!WARNING]
> Historical checkpoint / planning note — non-authoritative for the current release.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and `CERTIFICATION_STATUS.md` for current release truth.

> [!WARNING] Historical / non-authoritative document. This file is retained for provenance or implementation context only. Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md` and the generated current-state reports for current release truth.

> **Historical / non-authoritative** — This document is retained for planning or provenance only.
> Do **not** use it to determine the current certification state, executable surface, or release readiness.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and `CERTIFICATION_STATUS.md` instead.

# Runtime Execution Validation Status — 2026-03-24

## Scope of this checkpoint

This checkpoint converts runtime validation from a **declared metadata posture** into an **executable clean-room validation posture**.

The repository now contains runnable clean-room commands that perform all of the following in supported environments:

- application-factory import and build
- `tba-auth serve --check --server uvicorn`
- `tba-auth serve --check --server hypercorn`
- `tba-auth serve --check --server tigrcorn` for the kept Tigrcorn profile on Python 3.11 / 3.12
- smoke probes for discovery, JWKS, and public contract endpoints against the ASGI application

These commands are now wired into both `tox.ini` and the clean-room CI workflows so the runtime path is exercised rather than inferred from metadata alone.

## Implemented runtime-validation surfaces

### Local and CI command parity

The same runtime-validation commands now run in both local and CI environments through `tox.ini`:

- `py{310,311,312}-sqlite-uvicorn`
- `py{310,311,312}-postgres-hypercorn`
- `py{311,312}-tigrcorn`
- `py{310,311,312}-devtest`
- `py311-gates`

### Runtime execution helpers

The repository now exposes executable helpers and reporting for:

- application-factory probing
- ASGI HTTP surface probing for discovery, JWKS, and OpenAPI endpoints
- per-runner `serve --check` command probing
- runtime profile artifact generation with execution-probe truth fields

## Current repository truth

The implementation work for real runtime validation is complete **as repository logic and CI/tox wiring**, but the current container still does **not** satisfy the runtime exit criteria.

Current generated runtime-profile state remains:

- `application_probe.passed = false`
- `ready_count = 0`
- `invalid_count = 2`
- `missing_count = 1`
- `surface_probe_passed = false`
- `serve_check_passed_count = 0`
- `execution_probe_complete = false`

## Why the exit criteria are still not met here

This container is not a supported certification runtime for the package:

- the supported interpreter boundary remains Python `>=3.10,<3.13`
- the current container is Python `3.13`
- the Tigrbl-first runtime dependency set is therefore not installable here in the supported form required by the package boundary
- the application probe still fails with `ModuleNotFoundError: No module named 'tigrbl'`

Accordingly, this checkpoint truthfully proves that the repository now has **real executable runtime validation logic**, but it does **not** prove successful runtime execution across the supported certification matrix from this container.

## Honest certification status after this checkpoint

The package remains:

- **not yet certifiably fully featured**
- **not yet certifiably fully RFC/spec compliant**

The remaining blockers are now dominated by:

- missing preserved successful runtime-execution evidence for the full supported interpreter/profile matrix
- missing Tier 4 independent peer evidence for the retained certification boundary

## Authoritative supporting artifacts

- `docs/compliance/runtime_profile_report.json`
- `docs/compliance/runtime_profile_report.md`
- `docs/compliance/current_state_report.json`
- `docs/compliance/certification_state_report.json`
- `CURRENT_STATE.md`
- `CERTIFICATION_STATUS.md`
- `tox.ini`
- `.github/workflows/ci-install-profiles.yml`
- `.github/workflows/ci-release-gates.yml`
- `scripts/clean_room_profile_smoke.py`
