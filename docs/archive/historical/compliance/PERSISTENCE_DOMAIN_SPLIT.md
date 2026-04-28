<!-- NON_AUTHORITATIVE_HISTORICAL -->

> [!WARNING]
> Historical checkpoint / planning note — non-authoritative for the current release.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and `CERTIFICATION_STATUS.md` for current release truth.

> [!WARNING] Historical / non-authoritative document. This file is retained for provenance or implementation context only. Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md` and the generated current-state reports for current release truth.

> **Historical / non-authoritative** — This document is retained for planning or provenance only.
> Do **not** use it to determine the current certification state, executable surface, or release readiness.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and `CERTIFICATION_STATUS.md` instead.

# persistence-domain checkpoint — Durable Persistence and Lifecycle Foundation

This checkpoint implements the persistence-domain checkpoint objective of replacing non-durable and
ledger-style lifecycle state with repository-owned, database-backed persistence
artifacts for the in-scope authorization lifecycle.

## What changed in this checkpoint

The repository now includes durable persistence models for the previously
missing or incomplete lifecycle domains:

- token status and introspection backing via `tigrbl_auth/tables/token_record.py`
- revocation registry via `tigrbl_auth/tables/revoked_token.py`
- consent state via `tigrbl_auth/tables/consent.py`
- audit events via `tigrbl_auth/tables/audit_event.py`
- browser/server session lifecycle via `tigrbl_auth/tables/auth_session.py`
- logout propagation state via `tigrbl_auth/tables/logout_state.py`
- client registration metadata via `tigrbl_auth/tables/client_registration.py`
- device authorization lifecycle timestamps via `tigrbl_auth/tables/device_code.py`
- pushed authorization request lifecycle timestamps via
  `tigrbl_auth/tables/pushed_authorization_request.py`

The checkpoint also adds a repository-owned persistence service:

- `tigrbl_auth/services/persistence.py`

That service now owns the durable helpers for:

- token recording and introspection-backed status lookup
- revocation writes and revocation reads
- session creation, touch, and termination
- logout propagation progress tracking
- consent grant and consent revocation
- client registration metadata upsert
- audit event append

## Runtime behavior changes

The following runtime surfaces no longer depend on process-memory-only token
state for the authoritative implementation path:

- `tigrbl_auth/standards/oauth2/introspection.py`
- `tigrbl_auth/standards/oauth2/revocation.py`
- `tigrbl_auth/rfc/rfc7662.py`
- `tigrbl_auth/rfc/rfc7009.py`

Session/logout owner modules now have durable helper behavior rather than being
pure owner placeholders:

- `tigrbl_auth/standards/oidc/session_mgmt.py`
- `tigrbl_auth/standards/oidc/rp_initiated_logout.py`
- `tigrbl_auth/standards/oidc/frontchannel_logout.py`
- `tigrbl_auth/standards/oidc/backchannel_logout.py`

Lifecycle startup now applies repository-owned migrations before surface
initialization:

- `tigrbl_auth/api/lifecycle.py`

## Migration model changes

The old structured-ledger placeholder migration chain has been replaced by
executable migration modules backed by actual SQLAlchemy table metadata:

- `tigrbl_auth/migrations/helpers.py`
- `tigrbl_auth/migrations/runtime.py`
- `tigrbl_auth/migrations/versions/0001_*.py` through `0006_*.py`
- `scripts/verify_persistence_migrations.py`

Each migration version now creates or drops real tables, and the migration
runtime records applied revisions in a durable `schema_migrations` table.

## What this checkpoint now makes true

For the authoritative implementation path, this checkpoint now provides:

- durable storage for revocation state
- durable storage for token activity / introspection status
- durable storage for consent records
- durable storage for audit events
- durable storage for sessions and logout propagation
- durable storage for dynamic client registration metadata
- durable storage for PAR and device authorization lifecycle timestamps
- repository-owned executable migrations instead of documentation-only ledgers
- a migration verification script for fresh-install and upgrade checks

## What is still not complete

This checkpoint does **not** make the package certifiably fully featured or
certifiably fully RFC/spec compliant across the full declared boundary.

Remaining blockers include:

- canonical public route completion for `/register`, `/logout`,
  `/device_authorization`, `/par`, and `/revoke`
- complete browser logout/session public workflow semantics
- full runtime hardening enforcement across production/hardening profiles
- implementation-backed completion of the full OpenRPC control-plane surface
- preserved Tier 3 evidence across the full in-scope boundary
- Tier 4 independent peer validation
- full live verification of the new migration/runtime path in this execution
  environment

## Verification posture for this checkpoint

This environment did not include the runtime dependencies needed to execute the
package, open database providers, or run the release-gate pipeline end to end.

What **was** verified here:

- static repository edits completed successfully
- Python syntax compilation of `tigrbl_auth/**/*.py` and `scripts/**/*.py`
  completed without errors

What remains to be verified by downstream execution:

- migration application against a real provider
- migration upgrade/fresh-install equivalence
- runtime persistence behavior across process restart
- full repository release gates and integration tests
