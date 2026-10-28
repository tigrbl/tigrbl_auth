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

# Migration Move Plan

## Direct move map

- `tba_auth/app.py` → `tba_auth/api/app.py`
- `tba_auth/routers/surface.py` → `tba_auth/api/surfaces.py`
- `tba_auth/routers/auth_flows.py` → `tba_auth/api/rest/routers/login.py`
- `tba_auth/routers/authz/oidc.py` → `tba_auth/api/rest/routers/authorize.py`
- `tba_auth/orm/*` → `tba_auth/tables/*`
- `tba_auth/db.py` → `tba_auth/tables/engine.py`
- `tba_auth/runtime_cfg.py` → `tba_auth/config/settings.py`
- `tba_auth/backends.py` → `tba_auth/services/auth_backends.py` and `tba_auth/ops/authenticate.py`
- `tba_auth/crypto.py` + `tba_auth/jwtoken.py` → `tba_auth/services/key_management.py` + `tba_auth/services/token_service.py`
- `tba_auth/oidc_discovery.py` / `tba_auth/oidc_id_token.py` / `tba_auth/oidc_userinfo.py` → `tba_auth/standards/oidc/*`
- `tba_auth/rfc/*` → `tba_auth/standards/{oauth2,oidc,jose,http}/*`
- `vendor/*` → deleted / forbidden
- `tests/integration/*` → `tests/integration/*`

## Replacement order

1. framework and config
2. plugin, gateway, api app/lifecycle/surfaces
3. tables and migrations
4. services and ops
5. standards/jose
6. baseline standards/oauth2
7. baseline standards/oidc
8. api/rest routers
9. security
10. production targets
11. hardening targets
12. CLI, contracts, evidence, release automation
