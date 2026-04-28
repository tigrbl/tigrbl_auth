<!-- NON_AUTHORITATIVE_HISTORICAL -->

> [!WARNING]
> Historical checkpoint / planning note — non-authoritative for the current release.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and `CERTIFICATION_STATUS.md` for current release truth.

> [!WARNING] Historical / non-authoritative document. This file is retained for provenance or implementation context only. Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md` and the generated current-state reports for current release truth.

> **Historical / non-authoritative** — This document is retained for planning or provenance only.
> Do **not** use it to determine the current certification state, executable surface, or release readiness.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and `CERTIFICATION_STATUS.md` instead.

# Published Dependency and Runner Status — 2026-03-24

- checkpoint kind: `public-route checkpoint published dependency and runner gap closeout`
- certifiably fully featured now: `False`
- certifiably fully RFC compliant now: `False`

## What was closed in this checkpoint

- all pinned runtime-heavy package names kept in `pyproject.toml` and `constraints/*.txt` are now preserved as published-package pins rather than workspace or placeholder references
- the kept runner set remains `uvicorn`, `hypercorn`, and `tigrcorn`
- Tigrcorn is no longer modeled as a metadata-only profile; it is now a published pin in both the dedicated `tigrcorn` extra and the aggregate `servers` extra
- the runtime profile report now records both current-environment readiness and repository-declared CI install/probe coverage for every kept runner
- dev/test installs remain explicit through `constraints/test.txt` and the `test` extra, so `pytest-timeout` and the other declared pytest plugins are part of test-capable installs

## Published-package verification basis

- package support boundary: `>=3.10,<3.13`
- certification interpreter minors: `3.10`, `3.11`, `3.12`
- Tigrcorn interpreter boundary: `>=3.11`
- verification artifact: `constraints/dependency-lock.json`
- verification source captured in this checkpoint: `PyPI release metadata verified on 2026-03-24`

## Runtime-profile truth after this update

- placeholder-supported runners: `0`
- declared CI-installable runners: `3`
- declared CI install/probe complete: `True`
- current container runtime readiness remains below certification because the active container still lacks the full Tigrbl runtime import stack

## Remaining blockers

- Tier 4 independent peer validation is still absent
- successful execution evidence for the full clean-room matrix is still not preserved from this container
- the runtime profile report still shows current-environment invalid/missing runner states because this container does not include the full published Tigrbl runtime stack
