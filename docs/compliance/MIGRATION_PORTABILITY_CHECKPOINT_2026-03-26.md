# Migration portability Migration Portability Checkpoint — 2026-03-26

## Truthful status

This checkpoint advances the Migration portability migration-portability closeout work, but it does **not** satisfy the full certification exit criterion yet.

- package certifiably fully featured: `False`
- package certifiably fully RFC/spec compliant: `False`
- migration_portability_passed: `False`

The repository now preserves a real local SQLite migration portability proof, but it still lacks preserved PostgreSQL portability evidence in a supported certification environment.

## What was fixed

### 1. Published Tigrbl resolver compatibility

The migration/runtime path and related tests were still using the historical resolver API shape (`router=` / `register_router`).

This checkpoint adds a compatibility adapter in:

- `tigrbl_auth/runtime/engine_resolver.py`

and updates these callers to the published public API boundary:

- `tigrbl_auth/migrations/runtime.py`
- `tigrbl_auth/services/persistence.py`
- `tests/conftest.py`
- `tests/unit/test_engine_initialization.py`

### 2. SQLite executable migration portability

The executable migration helpers still assumed schema-qualified table DDL would work directly on SQLite. That broke upgrade/downgrade execution when the migration chain used `authn.*` table names.

This checkpoint updates:

- `tigrbl_auth/migrations/helpers.py`

so that SQLite execution clones schema-qualified tables into schema-less metadata for DDL purposes, preserves prior-table dependency resolution, and rebuilds drop-column tables without reintroducing unsupported cross-schema FK resolution.

### 3. Migration portability evidence generation

This checkpoint adds a first-class migration-portability runner and report flow:

- `scripts/run_migration_portability.py`
- `scripts/record_validated_run.py`
- `tox.ini`
- `.github/workflows/ci-release-gates.yml`

The runner now preserves:

- backend upgrade artifacts
- backend downgrade artifacts
- backend reapply artifacts
- pytest JSON evidence
- a machine-readable migration portability report
- a validated-run manifest

## What was validated here

### SQLite

Validated locally in this container using the repository migration chain:

- upgrade: `passed`
- downgrade: `passed`
- reapply: `passed`

Artifacts preserved:

- `dist/migration-portability/sqlite/upgrade.json`
- `dist/migration-portability/sqlite/downgrade.json`
- `dist/migration-portability/sqlite/reapply.json`
- `dist/test-reports/local-migration-portability-py313.json`
- `dist/validated-runs/migration-portability-py313.json`
- `docs/compliance/migration_portability_report.json`
- `docs/compliance/migration_portability_report.md`

### Focused regression coverage

Local focused regression run:

- `tests/integration/test_migration_upgrade_downgrade_safety.py` → `2 passed`
- `tests/unit/test_engine_initialization.py` → `1 passed`

Total focused regression result:

- `3 passed`

## What still blocks the Migration portability exit criterion

### PostgreSQL portability evidence is still missing

The Migration portability exit criterion requires preserved proof for **both**:

- SQLite
- PostgreSQL

In this container:

- `POSTGRES_URL` was not set
- PostgreSQL server binaries were not available
- no PostgreSQL clean-room service was materialized

So the repository cannot truthfully mark migration portability as fully passed.

### Supported certification runtime is still missing here

The declared supported certification runtime remains:

- Python 3.10
- Python 3.11
- Python 3.12

This container only provided Python `3.13`, so the local migration evidence captured here is useful for defect triage and checkpointing, but it is **not** a substitute for the supported `py311-migration-portability` certification run.

## Current repository meaning

The repository now has:

- a repaired migration/runtime resolver boundary
- a repaired SQLite executable migration chain
- preserved SQLite upgrade/downgrade/reapply evidence
- preserved migration-portability reporting machinery for CI and certification closeout

The repository still does **not** have:

- preserved PostgreSQL portability evidence
- supported Python certification-grade Migration portability proof
- final certification readiness

## Recommended next action

Run the declared certification target directly in a real supported clean room with PostgreSQL available:

```bash
tox -e py311-migration-portability
```

and preserve the resulting:

- `dist/migration-portability/*`
- `dist/test-reports/*`
- `dist/validated-runs/migration-portability-*.json`

Only after both SQLite and PostgreSQL pass in a supported certification environment can `migration_portability_passed` become `True`.
