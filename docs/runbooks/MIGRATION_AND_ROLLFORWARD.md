> [!WARNING] Non-authoritative active document. For current release and certification truth, use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md` and the generated current-state reports.

> **Historical / non-authoritative** — This document is retained for planning, provenance, or operator guidance only.
> Do **not** use it to determine the current certification state, executable surface, or release readiness.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and `CERTIFICATION_STATUS.md` instead.

<!-- NON_AUTHORITATIVE_HISTORICAL -->
> [!WARNING]
> Historical / non-authoritative checkpoint document.
> Do **not** use this file to determine the current certification state, executable surface, or release readiness.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and `CERTIFICATION_STATUS.md` instead.

> [!WARNING] Historical / non-authoritative document. This file is retained for provenance or implementation context only. Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md` and the generated current-state reports for current release truth.

# Migration and Roll-Forward Runbook

## Purpose

This runbook describes how to apply, verify, and advance the repository-owned
migration chain introduced in the persistence-domain checkpoint persistence checkpoint.

The migration system is owned by the repository and is implemented under:

- `tigrbl_auth/migrations/helpers.py`
- `tigrbl_auth/migrations/runtime.py`
- `tigrbl_auth/migrations/versions/*.py`

## Preconditions

Before applying migrations, ensure:

- the configured database provider is reachable
- the repository runtime dependencies are installed
- the target database credentials and DSN are correct
- the deployment profile is pointed at the intended database

## Migration chain

The authoritative migration order is:

1. `0001_initial_identity_tables`
2. `0002_client_and_service_tables`
3. `0003_authorization_runtime_tables`
4. `0004_device_par_revocation_tables`
5. `0005_session_logout_tables`
6. `0006_key_rotation_and_audit_tables`

The migration runtime stores applied revisions in a durable
`schema_migrations` table.

## Fresh install procedure

From a clean environment:

1. install the repository and runtime dependencies
2. configure the target provider / DSN
3. run the repository migration verification script:

```bash
python scripts/verify_persistence_migrations.py
```

Expected outcome:

- all migration revisions apply in order
- no expected tables are missing
- the script exits successfully

## Upgrade procedure

For an existing deployment:

1. back up the database
2. deploy the new application package without serving traffic yet
3. run:

```bash
python scripts/verify_persistence_migrations.py
```

4. confirm that:
   - pending revisions were applied
   - schema verification passed
   - application startup also completes successfully
5. cut traffic to the upgraded deployment

## Startup behavior

Application startup now invokes migration application before surface
initialization via:

- `tigrbl_auth/api/lifecycle.py`

That means a standard application start should converge the schema to the latest
owned revision set before the package begins serving requests.

## Roll-forward policy

Preferred operational posture is **roll forward**, not destructive rollback.

When a deployment issue is found after migration application:

1. preserve the upgraded database state
2. diagnose the application/runtime issue
3. ship a forward corrective revision or application fix
4. re-run migration verification
5. redeploy

## Rollback cautions

The repository includes `downgrade()` functions for each migration module, but a
blind downgrade is not the preferred production response.

Use downgrade only when:

- the release window requires immediate reversal
- data-loss implications are understood
- the affected tables are known to be safe to remove or restore
- a backup or snapshot exists

## Post-migration checks

After migration application, verify at minimum:

- revocation persists across process restart
- token introspection uses stored token state
- consent grants persist across process restart
- session create/touch/terminate persists across process restart
- logout propagation state is durable
- client registration metadata persists across process restart
- audit events are written durably

## Failure handling

If migration verification fails:

1. stop deployment promotion
2. capture the migration output JSON
3. inspect missing or unexpected tables
4. confirm that the provider DSN points to the intended database
5. confirm the repository version and migration chain are aligned
6. fix forward and re-run verification

## Operational notes

- the migration helpers create the `authn` schema for non-SQLite providers
- SQLite uses top-level tables plus a top-level `schema_migrations` table
- non-SQLite providers use `authn.schema_migrations`
- migration modules create/drop tables from the authoritative SQLAlchemy table
  metadata instead of maintaining a documentation-only ledger

## Current limitations

This runbook covers the persistence and schema lifecycle foundation only. The
full certification program still requires later lifecycle work, including:

- canonical route completion
- browser/logout public surface completion
- hardening-runtime enforcement
- complete evidence promotion
- external peer validation

## Portable downgrade guarantee for revision `0007_browser_session_cookie_and_auth_code_linkage`

Revision `0007_browser_session_cookie_and_auth_code_linkage` is now expected to support:

- upgrade on SQLite
- upgrade on PostgreSQL
- downgrade on SQLite
- downgrade on PostgreSQL
- reapply after downgrade on both backends

The rollback policy for this revision is explicit:

1. use downgrade only to remove the cookie/session-linkage columns introduced in `0007`
2. preserve all rows in `sessions` and `auth_codes` during downgrade
3. immediately verify that the downgraded schema still contains the full retained table set
4. re-apply the revision before resuming normal forward motion unless the rollback window is still active
5. treat PostgreSQL and SQLite downgrade+reapply as certification evidence only when the integration test `tests/integration/test_migration_upgrade_downgrade_safety.py` has passed on both backends