# Step 2 App-Factory Materialization Checkpoint — 2026-03-26

## Scope

This checkpoint addresses the Step 2 closeout task:

> Make the ASGI application factory materialize in a real clean room.

The retained target for this step is the application factory at:

- `tigrbl_auth.api.app.build_app`

with focus files:

- `tigrbl_auth/api/app.py`
- `tigrbl_auth/app.py`
- `tigrbl_auth/plugin.py`
- `tigrbl_auth/gateway.py`
- `tigrbl_auth/config/deployment.py`

## What was fixed

### 1. Pip constraints were normalized to a pip-legal clean-room form

The published dependency metadata in `pyproject.toml` intentionally retains extras-bearing requirements such as:

- `sqlalchemy[asyncio]==2.0.48`
- `pydantic[email]==2.12.5`
- `uvicorn[standard]==0.41.0`

Those are valid package requirements, but modern `pip` rejects them when they appear inside `constraints/*.txt`.

This checkpoint normalizes the committed constraint files to pip-legal constraint form:

- `sqlalchemy==2.0.48`
- `pydantic==2.12.5`
- `uvicorn==0.41.0`

The repository now preserves both truths:

- `pyproject.toml` keeps the extras-bearing requirement intent.
- `constraints/*.txt` are installable by `pip` in constraint mode.

### 2. The framework shim was aligned to the published `tigrbl==0.3.15` public API

The source tree expected two public imports that are not exported by the published wheel in the way the repository assumed:

- `tigrbl.TigrblRouter`
- `tigrbl.core.crud.Header`

The pinned published runtime exposes:

- `tigrbl.TigrblApi`
- `tigrbl.core.crud.params.Header`

This checkpoint updates `tigrbl_auth/framework.py` to stay on the published Tigrbl public surface while preserving the package's existing router-facing call sites.

### 3. `build_app()` now materializes against the published runtime surface

`TigrblApp(..., docs_url=None)` raised an exception in the published runtime because the docs-mounting path handling does not accept `None`.

This checkpoint switches the release-path app construction to a concrete docs path so the app factory can materialize cleanly.

## Verification performed in this checkpoint

A dependency-complete local probe environment was built from the repository's published pins. Because this container only provides Python `3.13.5`, the probe had to run in an **unsupported local verification environment** using `--ignore-requires-python`.

That is useful engineering evidence, but it is **not certification-grade proof** for the retained support boundary of Python `3.10`, `3.11`, and `3.12`.

### Results

- application factory materialization: **passed**
- application type: `TigrblApp`
- baseline runtime HTTP surface probe: **4 / 5 passed**
- failing surface: `/.well-known/oauth-protected-resource` returned `404`

The detailed machine-readable probe payload is preserved at:

- `docs/compliance/app_factory_materialization_probe.json`
- `dist/runtime-smoke/unsupported-py313-base-base.json`

## What is complete for Step 2

The repository no longer fails Step 2 immediately on the earlier hard blockers:

- missing `tigrbl` runtime in the probe environment
- non-installable extras syntax inside committed constraints files
- stale import assumptions about the published `tigrbl` router/header public API
- `docs_url=None` app-factory crash against the published runtime

## What is still blocking full Step 2 closeout

Step 2's stated exit criterion is:

> the application probe passes in all base environments.

That criterion is **not yet certifiably satisfied** in this checkpoint because:

1. this container does not provide Python `3.10`, `3.11`, or `3.12` interpreter binaries;
2. the repository therefore did **not** execute:
   - `tox -e py310-base`
   - `tox -e py311-base`
   - `tox -e py312-base`
3. the preserved local probe used Python `3.13.5`, which is outside the declared certification support range;
4. the baseline runtime surface probe still fails on `/.well-known/oauth-protected-resource`, which is a Step 3/runtime-surface blocker even though the application factory itself now materializes.

## Current truthful status

- Step 2 code-level blocker removal: **substantially complete**
- Step 2 certification-grade matrix evidence: **not complete**
- package certifiably fully featured: **no**
- package certifiably fully RFC compliant: **no**

## Files changed by this checkpoint

- `tigrbl_auth/framework.py`
- `tigrbl_auth/api/app.py`
- `tigrbl_auth/cli/install_substrate.py`
- `constraints/base.txt`
- `constraints/runner-uvicorn.txt`
- `constraints/dependency-lock.json`
- `tests/unit/test_published_dependency_model.py`
- `tests/unit/test_app_factory_materialization.py`
- generated current-state/compliance reports under `docs/compliance/`
- `CURRENT_STATE.md`
- `CERTIFICATION_STATUS.md`

## Focused regression evidence

The following focused regression set passed in this checkpoint:

- `tests/unit/test_published_dependency_model.py`
- `tests/unit/test_clean_room_install_substrate.py`
- `tests/unit/test_app_factory_materialization.py`
- `tests/unit/test_runner_adapter_runtime_layer.py`

Total passed in the focused set: **15**.
