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
