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
