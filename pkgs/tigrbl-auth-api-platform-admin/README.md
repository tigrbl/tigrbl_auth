# tigrbl-auth-api-platform-admin

Platform-scoped tenant lifecycle and authority-assignment API front door.

## Surface

| Property | Value |
| --- | --- |
| Product surface | `platform-admin-api` |
| Intended UIX | `@tigrbl-auth/platform-admin-uix` |
| Exposes | Tenant lifecycle, platform authority assignment, admin identity lookup, audit/session/profile RPC |
| Excludes | Public login/consent pages, tenant self-service-only workflows, developer app registration surface |

## Entrypoint

```python
from tigrbl_auth_api_platform_admin import app, build_app
```
