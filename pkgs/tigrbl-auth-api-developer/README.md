# tigrbl-auth-api-developer

Developer self-service OAuth/OIDC client registration API front door.

## Surface

| Property | Value |
| --- | --- |
| Product surface | `developer-api` |
| Intended UIX | `@tigrbl-auth/developer-uix` |
| Exposes | Dynamic client registration, client management, client metadata, JWKS/discovery helpers |
| Excludes | Tenant lifecycle operations, platform authority assignment, service identity administration |

## Entrypoint

```python
from tigrbl_auth_api_developer import app, build_app
```
