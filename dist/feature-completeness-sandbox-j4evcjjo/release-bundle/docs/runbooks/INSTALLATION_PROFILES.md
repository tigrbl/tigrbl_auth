> [!WARNING] Non-authoritative active document. For current release and certification truth, use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md` and the generated current-state reports.

> **Historical / non-authoritative** — This document is retained for planning, provenance, or operator guidance only.
> Do **not** use it to determine the current certification state, executable surface, or release readiness.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and `CERTIFICATION_STATUS.md` instead.

# Installation Profiles

## Clean-room certification profiles

All clean-room certification installs are now modeled with the same profile vocabulary in both CI and `tox.ini`.

### Base

- install: `pip install -c constraints/base.txt .`
- purpose: prove fresh-checkout install, `import tigrbl_auth`, and `python scripts/generate_state_reports.py`
- note: the base dependency set now includes `aiosqlite==0.22.1` so the default local runtime/report smoke path works in a clean room

### SQLite + Uvicorn

- install: `pip install -c constraints/base.txt -c constraints/runner-uvicorn.txt '.[sqlite,uvicorn]'`
- tox: `tox -e py311-sqlite-uvicorn`

### PostgreSQL + Hypercorn

- install: `pip install -c constraints/base.txt -c constraints/runner-hypercorn.txt '.[postgres,hypercorn]'`
- tox: `tox -e py311-postgres-hypercorn`
- requires: reachable PostgreSQL DSN, defaulted in CI to `postgresql://postgres:postgres@127.0.0.1:5432/tigrbl_auth_ci`

### Tigrcorn

- install: `pip install -c constraints/base.txt -c constraints/runner-tigrcorn.txt '.[tigrcorn]'`
- tox: `tox -e py311-tigrcorn` or `tox -e py312-tigrcorn`
- support note: Tigrcorn is only included in the clean-room matrix on Python `3.11` and `3.12`; the aggregate `servers` extra also includes Tigrcorn on those interpreters

### Dev/test

- install: `pip install -c constraints/base.txt -c constraints/test.txt -c constraints/runner-uvicorn.txt '.[test,sqlite,uvicorn]'`
- tox: `tox -e py311-devtest`
- smoke guarantee: `pytest --help` is executed so plugin loading failures break the profile

### Release gates

- tox only: `tox -e py311-gates`
- includes: test tooling, SQLite, PostgreSQL, the aggregate `servers` runner extra (Uvicorn + Hypercorn + Tigrcorn on supported interpreters), CLI doc generation, state report generation, and release-gate execution

## Runtime validation reality checkpoint

The clean-room matrix now performs real runtime validation in supported environments, not just metadata inspection. For each kept runner profile the matrix executes:

- `python scripts/clean_room_profile_smoke.py --runner <runner> --require-runner-installed --probe-surfaces --require-surface-probes`
- `tigrbl-auth serve --check --server <runner> --format json --output dist/runtime-smoke/<profile>-serve-check.json`
- `python scripts/generate_state_reports.py`

The release-gate tox environment runs the same serve-check and HTTP-surface probes for `uvicorn`, `hypercorn`, and `tigrcorn` so the generated `docs/compliance/runtime_profile_report.json` can be built from executable checks in a supported interpreter environment.

## Install-substrate verification checkpoint

Every certification tox template now runs `python -I -m pip check` and `python scripts/verify_clean_room_install_substrate.py --profile <profile> --strict-manifest --strict-imports --artifact-dir dist/install-substrate` before the runtime smoke, lane tests, migration portability checks, or final certification aggregation.

## Certification lane install profiles

The certification lane tox environments are now explicitly modeled as install profiles in `constraints/dependency-lock.json`: `test-core`, `test-integration`, `test-conformance`, `test-security-negative`, `test-interop`, `test-extension`, `migration-portability`, and `final-certification`.
