# tigrbl-auth-api-public

Public OAuth/OIDC and white-label login API front door.

## Surface

| Property | Value |
| --- | --- |
| Product surface | `public-api` |
| Intended UIX | `@tigrbl-auth/public-uix` |
| Exposes | Login, authorize, token, logout, registration, discovery, JWKS, and public OAuth/OIDC helpers |
| Excludes | `/admin/*`, `/rpc`, diagnostics, tenant lifecycle administration |

## Entrypoint

```python
from tigrbl_auth_api_public import app, build_app
```
