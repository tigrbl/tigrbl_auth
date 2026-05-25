# tigrbl-auth-api-service-admin

Service, machine, API-key, and workload identity API front door.

## Surface

| Property | Value |
| --- | --- |
| Product surface | `service-admin-api` |
| Intended UIX | `@tigrbl-auth/service-admin-uix` |
| Exposes | Services, service keys, API keys, token/audit inspection, validation metadata |
| Excludes | Tenant lifecycle operations, public human login/consent pages, developer app catalog management |

## Entrypoint

```python
from tigrbl_auth_api_service_admin import app, build_app
```
