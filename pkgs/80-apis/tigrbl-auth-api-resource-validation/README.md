# tigrbl-auth-api-resource-validation

Resource-server validation API front door for protected APIs that need issuer metadata.

## Surface

| Property | Value |
| --- | --- |
| Product surface | `resource-validation-api` |
| Intended consumers | Resource servers, API gateways, validation middleware |
| Exposes | JWKS, tenant JWKS, introspection, OIDC discovery, protected-resource metadata |
| Excludes | Public human login/consent pages, dynamic client registration, admin resources, `/rpc` |

## Entrypoint

```python
from tigrbl_auth_api_resource_validation import app, build_app
```

## Local dev deployment

Run the isolated validation front door on port `8014`:

```bash
docker compose -f docker/docker-compose.resource-validation-api.yml up -d --build
```

Useful endpoints:

| Endpoint | Purpose |
| --- | --- |
| `/.well-known/openid-configuration` | Issuer metadata needed by validators. |
| `/.well-known/oauth-protected-resource` | Protected-resource metadata and verifier contract projection. |
| `/.well-known/jwks.json` | Issuer key set for local JWT validation. |
| `/tenants/{tenant_slug}/.well-known/jwks.json` | Tenant-scoped key set. |
| `/introspect` | RFC 7662 token status checks for authorized callers. |
