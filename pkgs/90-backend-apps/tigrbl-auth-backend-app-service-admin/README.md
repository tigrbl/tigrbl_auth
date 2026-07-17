# tigrbl-auth-backend-app-service-admin

Service, machine, API-key, and workload identity API front door.

## Surface

| Property | Value |
| --- | --- |
| Product surface | `service-admin-app` |
| Intended UIX | `@tigrbl-auth/service-admin-uix` |
| Exposes | Services, service keys, API keys, token/audit inspection, validation metadata |
| Excludes | Tenant lifecycle operations, public human login/consent pages, developer app catalog management |

## Entrypoint

```python
from tigrbl_auth_backend_app_service_admin import app, build_app
```
