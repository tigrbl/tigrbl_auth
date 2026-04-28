# Clean-room executor and validated-evidence checkpoint — 2026-03-27

## Scope of this checkpoint

This checkpoint follows the retained target/profile truth reconciliation for **RFC 7516**, **RFC 7592**, and **RFC 9207**.

Its purpose is to tighten the certification executor and evidence plane so that any future claim of a green clean-room runtime matrix, a green in-scope test-lane matrix, or a green migration portability report must be backed by preserved manifests that are internally self-consistent and traceable to the exact execution substrate.

## What was implemented

### 1. Clean-room executor matrix remains declared and fail-closed

The repository already declared the supported certification matrix in `tox.ini` and GitHub Actions. This checkpoint preserves that matrix and tightens the proof model around it:

- runtime cells:
  - `base@py3.10`
  - `base@py3.11`
  - `base@py3.12`
  - `sqlite-uvicorn@py3.10`
  - `sqlite-uvicorn@py3.11`
  - `sqlite-uvicorn@py3.12`
  - `postgres-hypercorn@py3.10`
  - `postgres-hypercorn@py3.11`
  - `postgres-hypercorn@py3.12`
  - `tigrcorn@py3.11`
  - `tigrcorn@py3.12`
  - `devtest@py3.10`
  - `devtest@py3.11`
  - `devtest@py3.12`
- in-scope test lanes:
  - `core@py3.10/3.11/3.12`
  - `integration@py3.10/3.11/3.12`
  - `conformance@py3.10/3.11/3.12`
  - `security-negative@py3.10/3.11/3.12`
  - `interop@py3.10/3.11/3.12`
- migration portability:
  - SQLite + PostgreSQL, with exact revision inventory preserved in the report and validated manifest

### 2. Runtime manifests now require identity + install evidence + runtime proof

`dist/validated-runs/*.json` runtime manifests are now counted as passing only if they preserve all of the following:

- the expected runtime identity (`<profile>@py<major><minor>`)
- environment identity matching the manifest Python version
- install-substrate artifact linkage and SHA
- install-substrate pass signals for static manifest, import probe, and runtime surface probe
- runtime smoke artifact linkage and SHA
- application-factory proof
- HTTP surface probe counts
- serve-check artifact linkage and SHA for runner-qualified profiles

The fail-closed logic now lives in `tigrbl_auth/cli/certification_evidence.py` and is consumed by:

- `scripts/record_validated_run.py`
- `tigrbl_auth/cli/runtime.py`
- `tigrbl_auth/cli/reports.py`

### 3. Test-lane manifests now require identity + install evidence + pytest proof

A test-lane manifest now counts as passing only if it preserves:

- the expected lane identity (`<lane>@py<major><minor>`)
- environment identity matching the manifest Python version
- install-substrate artifact linkage and SHA
- install-substrate pass signals for static manifest, import probe, and runtime surface probe
- pytest report artifact linkage and SHA
- passing pytest exit codes
- a non-zero collected test count

### 4. Migration manifests now require exact revision-aware backend proof

Migration portability manifests now count as passing only if they preserve:

- the expected migration identity (`migration-portability@py<major><minor>`)
- environment identity matching the manifest Python version
- install-substrate artifact linkage and SHA
- required backends `sqlite` and `postgres`
- passed backends including both `sqlite` and `postgres`
- revision inventory
- expected head revision
- downgrade target revision
- backend-specific upgrade/downgrade/reapply artifact linkage
- backend-specific revision state after upgrade, downgrade, and reapply
- pytest report artifact linkage and SHA for the migration lane

The report generator `scripts/run_migration_portability.py` now emits those revision-aware backend artifacts.

## Current truthful status

The executor and evidence contract is materially stronger after this checkpoint, but the repository is still **not** truthfully certifiably fully featured and still **not** truthfully certifiably fully RFC/spec compliant.

The blocking reason is preserved evidence, not a total absence of implementation.

### Still missing for truthful final certification

- preserved green runtime manifests for the full supported runtime matrix
- preserved green manifests for all supported in-scope test lanes on Python `3.10`, `3.11`, and `3.12`
- preserved SQLite + PostgreSQL migration portability evidence from a supported clean-room executor
- preserved Tier 4 external peer bundles for the retained boundary

## Local execution limitation in this checkpoint environment

This container does **not** provide the full supported certification executor surface:

- only Python `3.13` is locally available here
- Python `3.10`, `3.11`, and `3.12` interpreters are not locally available in this container
- PostgreSQL is not locally provisioned in this container

Because of that, this checkpoint can tighten the evidence model, reports, tests, and documentation, but it cannot truthfully fabricate green preserved evidence for the supported certification matrix.

## Files changed in this checkpoint

- `tigrbl_auth/cli/certification_evidence.py`
- `tigrbl_auth/cli/runtime.py`
- `tigrbl_auth/cli/reports.py`
- `tigrbl_auth/cli/install_substrate.py`
- `scripts/clean_room_profile_smoke.py`
- `scripts/record_validated_run.py`
- `scripts/run_migration_portability.py`
- `scripts/generate_release_decision_record.py`
- `compliance/claims/repository-state.yaml`
- `CURRENT_STATE.md`
- `CERTIFICATION_STATUS.md`
- `README.md`
- unit tests under `tests/unit/`

## Recommended next execution action in a real certification environment

Run the declared GitHub Actions matrix or an equivalent clean-room executor pool that provides Python `3.10`, `3.11`, `3.12`, and PostgreSQL, then re-collect and normalize the resulting artifacts into `dist/validated-runs/` before re-running the release gates.
