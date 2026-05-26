# tigrbl-auth-api-tenant-admin

Tenant-scoped identity, admin delegation, JWKS, and local policy API front door.

## Surface

| Property | Value |
| --- | --- |
| Product surface | `tenant-admin-api` |
| Intended UIX | `@tigrbl-auth/tenant-admin-uix` |
| Exposes | Tenant identities, clients, consents, sessions, tenant keys/JWKS, tenant-local audit |
| Excludes | Platform tenant creation/deletion and cross-tenant authority assignment |

## Entrypoint

```python
from tigrbl_auth_api_tenant_admin import app, build_app
```

## Local Dev Deployment

The Docker dev surface listens on `http://localhost:8016` and uses the
admin API key `dev-tenant-admin-key` unless overridden.

```bash
docker compose -f docker-compose.tenant-admin-api.yml up -d --build
```

Useful checks:

- `GET /openapi.json`
- `GET /openrpc.json`
- `POST /rpc` with `X-API-Key: dev-tenant-admin-key`
- `GET /user`, `/client`, `/clientregistration`, `/consent`

The tenant-admin surface intentionally does not expose `/tenant`, public
OAuth/OIDC routes, platform tenant lifecycle RPC, or service/workload admin
resources.
