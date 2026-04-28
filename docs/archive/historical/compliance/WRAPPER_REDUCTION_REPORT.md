<!-- NON_AUTHORITATIVE_HISTORICAL -->
> [!WARNING]
> Historical / non-authoritative checkpoint document.
> Do **not** use this file to determine the current certification state, executable surface, or release readiness.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and `CERTIFICATION_STATUS.md` instead.

> [!WARNING] Historical / non-authoritative document. This file is retained for provenance or implementation context only. Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md` and the generated current-state reports for current release truth.

> **Historical / non-authoritative** — This document is retained for planning or provenance only.
> Do **not** use it to determine the current certification state, executable surface, or release readiness.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and `CERTIFICATION_STATUS.md` instead.

# Wrapper Reduction Report

## Scope

This report documents the wrapper/shim reduction work completed during runtime-foundation checkpoint.
It compares the boundary-lock checkpoint scope-lock checkpoint against the current repository
state after migration cleanup and stricter wrapper hygiene enforcement.

## Baseline versus current state

| Metric | boundary-lock checkpoint checkpoint | runtime-foundation checkpoint checkpoint |
|---|---:|---:|
| certified-core wrapper count | 0 | 0 |
| non-certified wrapper count | 45 | 4 |
| in-scope target wrapper count | n/a | 0 |
| standards legacy-proxy count | n/a | 0 |
| entrypoint legacy-import count | n/a | 0 |

Net reduction in non-certified wrapper/shim modules: **41**.

The remaining four wrapper modules are all extension-quarantine wrappers and are
outside the certified-core boundary:

- `tigrbl_auth/extensions/rfc7952.py`
- `tigrbl_auth/extensions/rfc8291.py`
- `tigrbl_auth/extensions/rfc8812.py`
- `tigrbl_auth/extensions/rfc8932.py`

## What was removed from the wrapper population

### Legacy compatibility shims converted to explicit facades

The following categories were removed from wrapper/shim classification by
rewriting them as explicit compatibility facades instead of star-import shims:

- top-level compatibility facades:
  - `backends.py`
  - `db.py`
  - `runtime_cfg.py`
  - `ops/authenticate.py`
- legacy ORM facade package:
  - `orm/__init__.py`
  - `orm/*.py`

### Standards-tree RFC compatibility shims eliminated

The numbered standards/oauth2 compatibility modules were rewritten so they no
longer proxy into the flat legacy RFC tree:

- `rfc7009.py`
- `rfc7521.py`
- `rfc7523.py`
- `rfc7591.py`
- `rfc7592.py`
- `rfc7662.py`
- `rfc7662_introspection.py`
- `rfc8252.py`
- `rfc8523.py`
- `rfc8628.py`
- `rfc8693.py`
- `rfc8705.py`
- `rfc8707.py`
- `rfc9068.py`
- `rfc9101.py`
- `rfc9126.py`
- `rfc9207.py`
- `rfc9396.py`
- `rfc9449_dpop.py`

These modules may still exist as compatibility surfaces, but they are no longer
counted as thin wrappers and they no longer forward into `tigrbl_auth/rfc/*`.

### Secondary JOSE shims eliminated

The following modules were rewritten as real standards-tree implementations and
promoted into the certified core:

- `tigrbl_auth/standards/jose/rfc7520.py`
- `tigrbl_auth/standards/jose/rfc7638.py`
- `tigrbl_auth/standards/jose/rfc8037.py`
- `tigrbl_auth/standards/jose/rfc8176.py`
- `tigrbl_auth/standards/jose/rfc8725.py`

### In-scope owner-module aggregation fixed

`OIDC Core 1.0` had an in-scope owner module that was still a star-import
aggregator:

- `tigrbl_auth/standards/oidc/core.py`

That module is now a named aggregator with explicit exports and no longer trips
wrapper hygiene.

## Stricter gate now enforced

The wrapper hygiene gate now checks more than certified-core wrapper count.
It also fails when any of the following conditions are true:

- an in-scope owner module is still a thin wrapper
- a standards-tree module still imports `tigrbl_auth.rfc/*`
- a release-path or entrypoint module still imports a legacy compatibility root
  (`tigrbl_auth.rfc`, `backends`, `db`, `runtime_cfg`, `orm`)

This stricter posture is enforced by:

- `scripts/verify_wrapper_hygiene.py`
- `tigrbl_auth/cli/boundary.py`

## Current interpretation

The repository now has:

- zero certified-core wrappers
- zero in-scope target wrappers
- zero standards-tree legacy proxies
- zero release-path entrypoint imports of legacy compatibility roots

The only remaining wrappers are explicit extension-quarantine compatibility
modules outside the certified-core certification boundary.

## Implication for certification

This closes the architectural migration blocker that previously prevented a
truthful claim that the in-scope release path had been migrated away from the
legacy flat RFC tree.

It does **not** by itself establish full feature completion or full RFC
compliance. Those remain blocked by later-runtime, persistence, public
surface, hardening, and evidence work.
