> [!WARNING] Non-authoritative active document. For current release and certification truth, use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md` and the generated current-state reports.

<!-- NON_AUTHORITATIVE_HISTORICAL -->
> [!WARNING]
> Historical / non-authoritative checkpoint document.
> Do **not** use this file to determine the current certification state, executable surface, or release readiness.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and `CERTIFICATION_STATUS.md` instead.

> [!WARNING] Historical / non-authoritative document. This file is retained for provenance or implementation context only. Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md` and the generated current-state reports for current release truth.

> **Historical / non-authoritative** — This document is retained for planning or provenance only.
> Do **not** use it to determine the current certification state, executable surface, or release readiness.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and `CERTIFICATION_STATUS.md` instead.

# Migration Completion Report

## Scope

This report records the runtime-foundation checkpoint architectural migration work completed on top of
the boundary-lock checkpoint certification-boundary checkpoint.

The goal of this track was not to claim full feature or full RFC completion.
The goal was to finish the **authoritative migration** so that in-scope release
behavior resolves through domain-owned modules in the standards-oriented tree,
not through the legacy flat RFC tree or thin wrapper modules.

## runtime-foundation checkpoint completion statement

runtime-foundation checkpoint is complete for the authoritative release path.

That statement is supported by the following repository conditions:

- certified-core and release-path roots no longer import `tba_auth.rfc`
- certified-core and release-path roots no longer import the legacy top-level
  compatibility facades `tba_auth.backends`, `tba_auth.db`,
  `tba_auth.runtime_cfg`, or `tba_auth.orm`
- in-scope owner modules no longer resolve through thin wrapper modules
- standards-tree compatibility modules no longer proxy into `tba_auth/rfc/*`
- the migration map now marks `tba_auth/rfc -> tba_auth/standards` as
  completed for the authoritative path

Compatibility facades are still retained outside the certified core for test and
import continuity, but they are no longer authoritative.

## Work completed

### 1. Legacy facade cleanup

The following compatibility surfaces were converted from thin wrapper/star-import
behavior into explicit compatibility facades backed by canonical modules:

- `tba_auth/backends.py`
- `tba_auth/db.py`
- `tba_auth/runtime_cfg.py`
- `tba_auth/ops/authenticate.py`
- `tba_auth/orm/__init__.py`
- `tba_auth/orm/api_key.py`
- `tba_auth/orm/auth_code.py`
- `tba_auth/orm/auth_session.py`
- `tba_auth/orm/client.py`
- `tba_auth/orm/device_code.py`
- `tba_auth/orm/pushed_authorization_request.py`
- `tba_auth/orm/revoked_token.py`
- `tba_auth/orm/service.py`
- `tba_auth/orm/service_key.py`
- `tba_auth/orm/tenant.py`
- `tba_auth/orm/user.py`

These modules remain compatibility surfaces only. The authoritative runtime
implementations are under `tba_auth/services`, `tba_auth/tables`, and
`tba_auth/config`.

### 2. Standards-tree ownership completion

The standards tree now contains the authoritative owner/helper modules for the
previously wrapped production and hardening RFC workstreams.

Canonical OAuth 2.x owner/helper modules now backed directly in the standards tree:

- `tba_auth/standards/oauth2/revocation.py`
- `tba_auth/standards/oauth2/introspection.py`
- `tba_auth/standards/oauth2/native_apps.py`
- `tba_auth/standards/oauth2/token_exchange.py`
- `tba_auth/standards/oauth2/mtls.py`
- `tba_auth/standards/oauth2/dpop.py`
- `tba_auth/standards/oauth2/jwt_access_tokens.py`
- `tba_auth/standards/oauth2/assertion_framework.py`
- `tba_auth/standards/oauth2/jwt_client_auth.py`
- `tba_auth/standards/oauth2/dynamic_client_registration.py`
- `tba_auth/standards/oauth2/client_registration_management.py`
- `tba_auth/standards/oauth2/device_authorization.py`
- `tba_auth/standards/oauth2/resource_indicators.py`
- `tba_auth/standards/oauth2/jar.py`
- `tba_auth/standards/oauth2/par.py`
- `tba_auth/standards/oauth2/issuer_identification.py`
- `tba_auth/standards/oauth2/rar.py`

The numbered compatibility modules under `tba_auth/standards/oauth2/rfc*.py`
were also rewritten so that, where retained, they resolve into the canonical
standards-tree implementation instead of proxying back into `tba_auth/rfc/*`.

### 3. Secondary JOSE migration completion

The following JOSE modules were promoted from wrapper-style transition modules to
real standards-tree implementations and reclassified into the certified core:

- `tba_auth/standards/jose/rfc7520.py`
- `tba_auth/standards/jose/rfc7638.py`
- `tba_auth/standards/jose/rfc8037.py`
- `tba_auth/standards/jose/rfc8176.py`
- `tba_auth/standards/jose/rfc8725.py`

`RFC 7800` remains explicitly deferred/quarantined at the certification-scope
level even though its owner module now exists in the standards tree.

### 4. Entrypoint and release-path canonicalization

The following entrypoint or release-path-adjacent modules were updated so they
now import from canonical standards/config/services/tables locations rather than
legacy facades or the flat RFC tree:

- `tba_auth/app.py`
- `tba_auth/security/deps.py`
- `tba_auth/jwtoken.py`
- `tba_auth/oidc_discovery.py`
- `tba_auth/oidc_id_token.py`
- `tba_auth/oidc_userinfo.py`
- `tba_auth/routers/shared.py`
- `tba_auth/routers/auth_flows.py`
- `tba_auth/routers/authz/__init__.py`
- `tba_auth/routers/authz/oidc.py`
- `tba_auth/routers/surface.py`

The active certified/core release path was already largely canonical before this
checkpoint; this track removes the remaining migration leaks and closes the
import-path story.

### 5. Standards aggregation cleanup

`OIDC Core 1.0` previously depended on a star-import aggregation module at
`tba_auth/standards/oidc/core.py`.

That file has been rewritten as an explicit certified-core aggregator with named
exports so the in-scope owner module is no longer treated as a thin wrapper.

## Mapping and boundary updates

The following governance artifacts were updated to match repository reality:

- `compliance/mappings/current-to-target-paths.yaml`
  - `tba_auth/rfc -> tba_auth/standards` is now marked `completed`
- `compliance/mappings/module-to-boundary.yaml`
  - promoted the migrated secondary JOSE modules into `certified_core`
  - promoted `tba_auth/security/deps.py` into `certified_core`
- `scripts/verify_wrapper_hygiene.py`
  - now runs the stricter runtime-foundation checkpoint hygiene mode
- `tba_auth/cli/boundary.py`
  - now enforces stricter wrapper hygiene checks for in-scope owner modules,
    standards-tree legacy proxies, and release-path entrypoint imports

## Exit-criteria results

The runtime-foundation checkpoint exit criteria are now satisfied.

### Exit criterion: No in-scope production/hardening RFC resolves through legacy tree or thin wrapper

Satisfied.

Machine-checkable evidence:

- `docs/compliance/wrapper_hygiene_report.md`
  - `certified_core_wrapper_count = 0`
  - `in_scope_target_wrapper_count = 0`
  - `standards_legacy_proxy_count = 0`
  - `entrypoint_legacy_import_count = 0`

### Exit criterion: Wrapper hygiene passes for the declared certification boundary

Satisfied.

Machine-checkable evidence:

- `docs/compliance/wrapper_hygiene_report.md`
- `docs/compliance/boundary_enforcement_report.md`
- `docs/compliance/migration_plan_status_report.md`
- `docs/compliance/release_gate_report.md`

## Compatibility surfaces intentionally retained

The following surfaces remain in the repository but are not authoritative for
certification or release-path ownership:

- `tba_auth/rfc/*`
- top-level compatibility facades such as `backends.py`, `db.py`, `runtime_cfg.py`
- legacy routers under `tba_auth/routers/*`
- quarantined extension wrappers under `tba_auth/extensions/*`

These retained modules serve backward-compatibility and test-preservation
purposes only.

## Remaining work outside runtime-foundation checkpoint

runtime-foundation checkpoint migration completion does **not** mean the package is already
certifiably fully featured or certifiably fully RFC compliant.

Outstanding work remains in later phases, including:

- runtime-complete cookie/session/logout behavior
- mounted `/register`, `/logout`, `/device_authorization`, `/par`, and canonical
  `/revoke` surface completion
- durable revocation/introspection/session/consent/audit persistence
- implementation-backed OpenRPC methods and schemas
- hardening runtime enforcement for disallowed grants/response types
- Tier 3 evidence population and Tier 4 external peer validation
- stronger release signing and attestation

## Conclusion

The repository now has a **completed authoritative architectural migration** for
its in-scope release path. Legacy compatibility surfaces remain available, but
runtime-foundation checkpoint no longer depends on them for certified-core ownership or release-path
resolution.
