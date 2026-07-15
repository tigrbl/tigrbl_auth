# tigrbl-auth-api-platform-admin

Platform-scoped tenant lifecycle and authority-assignment API front door.

## Surface

| Property | Value |
| --- | --- |
| Product surface | `platform-admin-api` |

The API package owns HTTP schemas and routes only. Tenant, realm, and identity
administration are invoked through request-scoped layer-40 capabilities composed
by `tigrbl-identity-server`; durable table operations and secret hashing remain
in the layer-60 runtime adapters and their lower-layer providers.
| Intended UIX | `@tigrbl-auth/platform-admin-uix` |
| Exposes | Tenant lifecycle, platform authority assignment, admin identity lookup, audit/session/profile RPC |
| Excludes | Public login/consent pages, tenant self-service-only workflows, developer app registration surface |

## Entrypoint

```python
from tigrbl_auth_api_platform_admin import app, build_app
```

## Local dev deployment

Run the isolated platform control-plane front door on port `8015`:

```bash
docker compose -f docker/docker-compose.platform-admin-api.yml up -d --build
```

The dev API key defaults to `dev-platform-admin-key`.

Useful endpoints:

| Endpoint | Purpose |
| --- | --- |
| `/openapi.json` | Platform-admin REST/control-plane contract. |
| `/openrpc.json` | Platform-admin JSON-RPC method contract. |
| `/rpc` | API-key-protected JSON-RPC dispatch. |
| `/tenant` | API-key-protected platform tenant lifecycle resource. |
