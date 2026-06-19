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

## Local dev deployment

```powershell
docker compose -f docker/docker-compose.developer-api.yml up -d --build
```

The dev deployment listens on `http://localhost:8017` and uses
`dev-developer-key` for the admin client-management routes and RPC methods.

Useful checks:

| Check | Expected |
| --- | --- |
| `GET /openapi.json` | Developer OpenAPI document |
| `GET /openrpc.json` | Client-management OpenRPC document |
| `POST /register` | Dynamic client-registration route exists without admin key |
| `GET /client` | Admin-key guarded client REST surface |
| `GET /clientregistration` | Admin-key guarded client-registration REST surface |
| `GET /tenants/public/.well-known/jwks.json` | Tenant JWKS metadata helper |

The developer API intentionally does not expose `/tenant`, `/authorize`,
`/token`, or service/workload administration routes.
