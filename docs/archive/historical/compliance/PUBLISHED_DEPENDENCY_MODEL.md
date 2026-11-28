<!-- NON_AUTHORITATIVE_HISTORICAL -->

> [!WARNING]
> Historical checkpoint / planning note — non-authoritative for the current release.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and `CERTIFICATION_STATUS.md` for current release truth.

> [!WARNING] Historical / non-authoritative document. This file is retained for provenance or implementation context only. Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md` and the generated current-state reports for current release truth.

> **Historical / non-authoritative** — This document is retained for planning or provenance only.
> Do **not** use it to determine the current certification state, executable surface, or release readiness.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and `CERTIFICATION_STATUS.md` instead.

# runtime-foundation checkpoint — Published Dependency Model and Reproducible Installation

## Objective

Remove hidden workspace coupling from the package metadata and checkpoint a reproducible installation model.

## Completed in this checkpoint

- `pyproject.toml` now pins released versions of `tigrbl` and the required `swarmauri_*` packages directly in project metadata
- workspace-only `[tool.uv.sources]` release-path assumptions were removed
- storage extras are explicit:
  - `postgres`
  - `sqlite`
- runner extras are explicit:
  - `uvicorn`
  - `hypercorn`
  - `tigrcorn`
  - `servers`
- reproducibility artifacts were added:
  - `constraints/base.txt`
  - `constraints/runner-uvicorn.txt`
  - `constraints/runner-hypercorn.txt`
  - `constraints/runner-tigrcorn.txt`
  - `constraints/dependency-lock.json`
  - `docs/runbooks/INSTALLATION_PROFILES.md`
  - `docs/runbooks/CLEAN_CHECKOUT_REPRO.md`
- `Dockerfile` was changed from monorepo-relative installation to repository-root installation using committed constraints
- CI install-profile coverage was added through `.github/workflows/ci-install-profiles.yml`
- release bundles now preserve dependency provenance artifacts

## Validation completed in this checkpoint

- `python scripts/generate_state_reports.py`
- `python scripts/build_release_bundle.py`
- `python scripts/sign_release_bundle.py`
- `python scripts/verify_release_signing.py`
- `python scripts/run_recertification.py`
- `python scripts/run_release_gates.py`

## Validation still blocked in this container

- full `pytest` execution remains blocked here because the container does not have the published dependency set installed; test collection still fails early on `import tigrbl`
- a native `uv.lock` file was not regenerated in this environment because the container does not provide a supported Python `3.10`-`3.12` runtime plus external package resolution

## Truthful status after runtime-foundation checkpoint

This checkpoint improves package reproducibility and closes the workspace-coupling gap in package metadata.

It does **not** make the repository certifiably fully featured or certifiably fully RFC/spec compliant.

Remaining blockers still include:

- `serve` does not yet launch runtime
- runtime runner profiles are not yet fully implemented and evidenced
- multiple operator families remain incomplete
- Tier 3 and Tier 4 certification promotion remains incomplete across the full retained boundary

## Tigrcorn note

The `tigrcorn` installation profile is declared so the package surface and certification model remain stable, but this checkpoint does **not** commit an additional published Tigrcorn package pin. The extra is therefore metadata-only in runtime-foundation checkpoint.

## Lockfile note

A native `uv.lock` file was not regenerated in this checkpoint environment. The repository instead preserves an equivalent direct-dependency lock manifest at `constraints/dependency-lock.json`.
