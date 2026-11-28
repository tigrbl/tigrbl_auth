<!-- NON_AUTHORITATIVE_HISTORICAL -->

> [!WARNING]
> Historical checkpoint / planning note — non-authoritative for the current release.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and `CERTIFICATION_STATUS.md` for current release truth.

> [!WARNING] Historical / non-authoritative document. This file is retained for provenance or implementation context only. Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md` and the generated current-state reports for current release truth.

> **Historical / non-authoritative** — This document is retained for planning or provenance only.
> Do **not** use it to determine the current certification state, executable surface, or release readiness.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and `CERTIFICATION_STATUS.md` instead.

# public-route checkpoint Public Route Completion

public-route checkpoint completes the missing canonical public auth routes for the authoritative
release path.

Completed routes:

- `/register`
- `/revoke`
- `/logout`
- `/device_authorization`
- `/par`

Also completed:

- canonical RFC 7009 path migration to `/revoke`
- explicit router/op/schema/persistence ownership for each route
- OpenAPI generation updates for the canonical route set
- target mapping updates for route/module/test alignment

This checkpoint does not claim that public-route checkpoint alone completes the entire
certification program.


Validation completed for this checkpoint:

- OpenAPI and OpenRPC artifacts regenerated
- effective claims/evidence manifests regenerated
- certification-scope and reality-matrix artifacts regenerated
- project-tree, boundary-enforcement, contract-sync, wrapper-hygiene, and
  feature-surface checks passed
- release gates passed
