> [!WARNING] Non-authoritative active document. For current release and certification truth, use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md` and the generated current-state reports.

> **Historical / non-authoritative** — This document is retained for planning, provenance, or operator guidance only.
> Do **not** use it to determine the current certification state, executable surface, or release readiness.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and `CERTIFICATION_STATUS.md` instead.

# Clean Checkout Reproduction

## Goal

Reproduce the repository's supported clean-room certification profiles from a fresh checkout without relying on preinstalled local packages.

## Canonical local runner

Use `tox.ini` so local reproduction and CI call the same profile names.

### Examples

- `tox -e py310-base`
- `tox -e py311-sqlite-uvicorn`
- `tox -e py312-postgres-hypercorn`
- `tox -e py311-tigrcorn`
- `tox -e py312-devtest`
- `tox -e py311-gates`

## What each profile proves

- base: package install, import, and state-report generation on supported interpreters
- sqlite-uvicorn: runtime-path install plus Uvicorn adapter availability
- postgres-hypercorn: runtime-path install plus Hypercorn adapter availability against a reachable PostgreSQL DSN
- tigrcorn: runtime-path install plus Tigrcorn adapter availability on Python `3.11`/`3.12`
- devtest: pytest plugin loading in addition to runtime smoke
- gates: release-gate environment with all retained runner/storage/test surfaces present via the aggregate `servers` extra and the dedicated test/storage extras

## Current limitation

This repository checkpoint now defines the clean-room certification matrix, but it does not preserve successful execution evidence for the entire matrix inside this container. Final certification still requires CI execution and preserved artifacts.

## Runtime validation reality checkpoint

The clean-room matrix now performs real runtime validation in supported environments, not just metadata inspection. For each kept runner profile the matrix executes:

- `python scripts/clean_room_profile_smoke.py --runner <runner> --require-runner-installed --probe-surfaces --require-surface-probes`
- `tigrbl-auth serve --check --server <runner> --format json --output dist/runtime-smoke/<profile>-serve-check.json`
- `python scripts/generate_state_reports.py`

The release-gate tox environment runs the same serve-check and HTTP-surface probes for `uvicorn`, `hypercorn`, and `tigrcorn` so the generated `docs/compliance/runtime_profile_report.json` can be built from executable checks in a supported interpreter environment.

## Install-substrate proof step

Before treating a clean checkout as valid, run `python scripts/verify_clean_room_install_substrate.py --profile <profile> --strict-manifest` in the selected environment and preserve the resulting `docs/compliance/install_substrate_report.json` plus the per-profile `dist/install-substrate/<profile>.json` artifact.
