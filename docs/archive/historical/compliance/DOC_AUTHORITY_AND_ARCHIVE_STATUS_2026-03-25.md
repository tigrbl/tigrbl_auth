<!-- NON_AUTHORITATIVE_HISTORICAL -->
> [!WARNING]
> Historical / non-authoritative checkpoint document.
> Do **not** use this file to determine the current certification state, executable surface, or release readiness.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and `CERTIFICATION_STATUS.md` instead.

# Document Authority and Archive Status — 2026-03-25

## What changed

- current authoritative docs are declared explicitly in `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`
- historical reference/planning docs are preserved under `docs/archive/historical/`
- non-authoritative checkpoint and notes are banner-marked in place where retained outside the archive tree
- certification bundles now copy only generated current-state docs and certification artifacts from the authority manifest

## Current rule

Use only the files listed in `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md` to determine current release truth.

All other preserved historical docs are non-authoritative and must not be used to resolve current certification readiness, RFC readiness, or release status.
