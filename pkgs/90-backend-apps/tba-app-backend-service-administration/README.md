# tba-app-backend-service-administration

Service, machine, API-key, and workload identity API front door.

## Surface

| Property | Value |
| --- | --- |
| Product surface | `service-admin-app` |
| Intended UIX | `@tba/ui-service-administration` |
| Exposes | Services, service keys, API keys, token/audit inspection, validation metadata |
| Excludes | Tenant lifecycle operations, public human login/consent pages, developer app catalog management |

## Entrypoint

```python
from tba_app_backend_service_administration import app, build_app
```
