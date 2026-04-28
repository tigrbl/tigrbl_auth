# Step 4 Runner Matrix Checkpoint — 2026-03-26

## Scope of this checkpoint

This checkpoint addresses Step 4 of the certification closeout plan:

> Certify all three runner profiles across the full supported matrix.

The retained runtime boundary remains:

- ASGI 3 application package
- Runner profile: Uvicorn
- Runner profile: Hypercorn
- Runner profile: Tigrcorn

The required runtime matrix remains **14 environments**:

- `py310-base`
- `py311-base`
- `py312-base`
- `py310-sqlite-uvicorn`
- `py311-sqlite-uvicorn`
- `py312-sqlite-uvicorn`
- `py310-postgres-hypercorn`
- `py311-postgres-hypercorn`
- `py312-postgres-hypercorn`
- `py311-tigrcorn`
- `py312-tigrcorn`
- `py310-devtest`
- `py311-devtest`
- `py312-devtest`

## What changed in this checkpoint

### 1. Runtime-profile validation was tightened

`docs/compliance/validated_execution_report.*` can no longer count a runtime-profile manifest as passing merely because a manifest file exists with `passed: true`.

A runtime-profile manifest now has to carry evidence that the environment actually satisfied the Step 4 runtime requirements:

- runtime smoke artifact passed
- application probe passed
- runtime HTTP surface probe passed
- runner module was available for runner-backed profiles
- `tigrbl-auth serve --check --server <runner>` passed for runner-backed profiles

This was implemented by tightening:

- `scripts/record_validated_run.py`
- `tigrbl_auth/cli/reports.py`

### 2. The base runtime smoke now probes HTTP surfaces as well

The `py{310,311,312}-base` tox environments now run:

```bash
python scripts/clean_room_profile_smoke.py --probe-surfaces --require-surface-probes
```

This closes the earlier Step 4 gap where base profiles only proved app materialization, not the active public discovery/contract surfaces.

### 3. Clean-room runtime smoke artifacts are now tox-env aware

`scripts/clean_room_profile_smoke.py` now records the active `TOX_ENV_NAME` and writes tox-env-specific artifact filenames when tox provides that environment variable.

This prevents local or merged artifact sets from silently overwriting runtime-smoke JSONs from different matrix cells.

### 4. Final GitHub Actions aggregation no longer merge-overwrites matrix artifacts

The final release-gates workflow previously used:

```yaml
merge-multiple: true
```

when downloading all `validated-*` artifacts. That could overwrite preserved `dist/runtime-smoke/*` and `dist/install-substrate/*` files from earlier matrix cells when filenames matched.

This checkpoint changes the final workflow to download into:

- `.artifacts/validated-downloads/`

without merge-overwrite, and adds an explicit normalization step via:

- `scripts/collect_validated_artifact_downloads.py`

The collector now:

- copies validated-run manifests into `dist/validated-runs/`
- preserves runtime-smoke JSONs under `dist/runtime-smoke/collected/<artifact>/...`
- preserves install-substrate artifacts under `dist/install-substrate/collected/<artifact>/...`
- preserves runtime-profile artifacts under `dist/runtime-profiles/collected/<artifact>/...`

This closes an operational evidence-retention gap that would otherwise make the final certification bundle incomplete or lossy.

### 5. `py311-final-certification` can now normalize downloaded artifacts automatically

`tox.ini` for `py311-final-certification` now runs the collector first in no-op-safe mode:

```bash
python scripts/collect_validated_artifact_downloads.py --download-root <...> --if-present
```

That allows the final certification tox env to work both:

- in GitHub Actions after artifact download
- locally, where no download root may exist yet

## Validation completed in this checkpoint

Focused regression set executed in this container:

- `tests/unit/test_runner_adapter_runtime_layer.py`
- `tests/runtime/test_runner_uvicorn.py`
- `tests/runtime/test_runner_hypercorn.py`
- `tests/runtime/test_runner_tigrcorn.py`
- `tests/runtime/test_runner_invariance.py`
- `tests/conformance/operator/test_cli_serve_runtime.py`
- `tests/unit/test_validated_execution_runtime_matrix.py`
- `tests/unit/test_collect_validated_artifact_downloads.py`

Result: **16 passed**.

## Current truthful status after this checkpoint

This checkpoint improves the repository’s ability to execute and preserve the Step 4 matrix **correctly**, but it does **not** prove the 14-environment matrix has actually been completed in this container.

`docs/compliance/validated_execution_report.md` still truthfully shows:

- runtime matrix expected count: `14`
- runtime matrix passed count: `0`
- runtime matrix green: `False`

That remains the correct state because the supported Python 3.10 / 3.11 / 3.12 clean-room matrix was **not executed here** and no preserved runtime-profile manifests for those matrix cells are present in this checkpoint.

## Remaining blockers for Step 4 exit

Step 4 is **not** exit-complete yet. The remaining work is external execution evidence, not more local static wiring:

1. run all 14 supported runtime tox environments in clean rooms
2. preserve runtime-smoke artifacts from every matrix cell
3. preserve runner `serve --check` JSON from every runner-backed matrix cell
4. materialize validated runtime-profile manifests from those runs
5. rerun final aggregation so `docs/compliance/validated_execution_report.md` can truthfully show `14/14`

## Files added or updated in this checkpoint

- `scripts/clean_room_profile_smoke.py`
- `scripts/record_validated_run.py`
- `scripts/collect_validated_artifact_downloads.py`
- `tigrbl_auth/cli/reports.py`
- `tox.ini`
- `.github/workflows/ci-release-gates.yml`
- `tests/unit/test_validated_execution_runtime_matrix.py`
- `tests/unit/test_collect_validated_artifact_downloads.py`
- `docs/compliance/validated_execution_report.*`
- `CURRENT_STATE.md`
- `CERTIFICATION_STATUS.md`
