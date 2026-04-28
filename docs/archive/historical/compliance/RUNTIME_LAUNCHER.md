<!-- NON_AUTHORITATIVE_HISTORICAL -->

> [!WARNING]
> Historical checkpoint / planning note — non-authoritative for the current release.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and `CERTIFICATION_STATUS.md` for current release truth.

> [!WARNING] Historical / non-authoritative document. This file is retained for provenance or implementation context only. Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md` and the generated current-state reports for current release truth.

> **Historical / non-authoritative** — This document is retained for planning or provenance only.
> Do **not** use it to determine the current certification state, executable surface, or release readiness.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and `CERTIFICATION_STATUS.md` instead.

# public-route checkpoint — Real runtime launcher checkpoint

## Objective

Replace the plan-only `serve` operator path with a real runtime launcher while preserving the server-agnostic ASGI 3 application model and the runner-adapter boundary introduced in persistence-domain checkpoint.

## Scope completed in this checkpoint

### Runtime launch path

`handle_serve()` now performs the required public-route checkpoint flow:

1. resolve deployment
2. materialize a runner-qualified runtime plan
3. build/probe the application factory
4. validate runner availability and adapter configuration
5. launch the selected server when launch-ready
6. emit structured startup metadata
7. install signal handlers and support graceful shutdown
8. write runtime startup/shutdown evidence for the chosen profile

### Serve flags

The serve command now supports the requested portable runtime flags and backend-scoped flags derived from runner metadata.

Portable serve flags implemented in this checkpoint include:

- `--server {uvicorn,hypercorn,tigrcorn}`
- `--host`
- `--port`
- `--workers`
- `--uds`
- `--log-level`
- `--access-log/--no-access-log`
- `--proxy-headers`
- `--lifespan {auto,on,off}`
- `--graceful-timeout`
- `--pid-file`
- `--health/--no-health`
- `--metrics/--no-metrics`
- `--public/--no-public`
- `--admin/--no-admin`
- `--rpc/--no-rpc`
- `--diagnostics/--no-diagnostics`
- `--require-tls/--no-require-tls`
- `--enable-mtls/--no-enable-mtls`
- `--cookies/--no-cookies`
- `--jwks-refresh-seconds`
- `--dry-run`
- `--check`

Backend-scoped flags are now supplied by typed runner metadata, not by unbounded free-form shims.

Examples now supported:

- `--uvicorn-loop`, `--uvicorn-http`, `--uvicorn-ws`
- `--hypercorn-worker-class`, `--hypercorn-http2/--no-hypercorn-http2`
- `--tigrcorn-contract`, `--tigrcorn-mode`

### Reporting and evidence

Added and regenerated:

- `scripts/verify_runner_profiles.py`
- `docs/compliance/runtime_profile_report.json`
- `docs/compliance/runtime_profile_report.md`
- `docs/reference/CLI_SURFACE.md`

Runtime startup/shutdown evidence now writes under:

- `dist/runtime-profiles/uvicorn/`
- `dist/runtime-profiles/hypercorn/`
- `dist/runtime-profiles/tigrcorn/`

`doctor` now surfaces runner-profile state as `ready`, `missing`, or `invalid`.

## Validation performed

### CLI/operator validation

Validated in this environment:

- `python -m tigrbl_auth.cli.main serve --server uvicorn --dry-run` returns success and emits a runtime plan without launch
- `python -m tigrbl_auth.cli.main doctor` returns success and reports runner-profile state
- generated CLI docs include the new serve flags and backend-scoped runner flags

### Direct runner validation

A direct dummy-ASGI validation was executed against the runner adapters in this environment.

Observed results:

- `uvicorn` live launch path: success (`rc=0`)
- `hypercorn` live launch path: success (`rc=0`)
- `tigrcorn` simulated contract launch path: success (`rc=0`)

This validates that the public-route checkpoint launcher substrate is executable at the adapter layer.

## Truthful limitations that remain

This checkpoint still does **not** justify claims that the package is certifiably fully featured or certifiably fully RFC/spec compliant.

Reasons:

- the clean-checkout application probe still fails in this container because `build_app()` requires published runtime dependencies such as `sqlalchemy` and `tigrbl` that are not installed here
- the generated runtime profile report therefore marks installed runners such as `uvicorn` and `hypercorn` as `invalid` in this environment because the application factory cannot materialize here
- `tigrcorn` is not installed in this environment, so its readiness remains `missing`
- multiple operator families are still not lifecycle-complete
- full Tier 3 closure and all Tier 4 independent claims remain open

## Exit-criteria status for this checkpoint

- `tigrbl-auth serve --server uvicorn` launches a live process: **implemented**, adapter-level validated, environment app probe still blocked by missing dependencies
- `tigrbl-auth serve --server hypercorn` launches a live process: **implemented**, adapter-level validated, environment app probe still blocked by missing dependencies
- `tigrbl-auth serve --server tigrcorn` launches a live process: **implemented through adapter contract**, installed-environment validation still pending
- `--dry-run` produces a runtime plan without launch: **complete**
- `doctor` reports installed / missing / invalid runner profiles: **complete**

## Current truthful repository state

- release gates pass: `20/20`
- fully certifiably featured now: `False`
- fully certifiably RFC/spec compliant now: `False`
- Tier 4 independent public claim boundary complete: `False`
