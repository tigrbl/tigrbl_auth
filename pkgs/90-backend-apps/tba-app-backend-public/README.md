# tba-app-backend-public

Public OAuth/OIDC and white-label login API front door.

## Surface

| Property | Value |
| --- | --- |
| Product surface | `public-app` |
| Intended UIX | `@tba/ui-public` |
| Exposes | Login, authorize, token, logout, registration, discovery, JWKS, and public OAuth/OIDC helpers |
| Excludes | `/admin/*`, `/rpc`, diagnostics, tenant lifecycle administration |

## Entrypoint

```python
from tba_app_backend_public import app, build_app
```

## Docker dev deployment

From the repository root:

```bash
docker compose -f docker/docker-compose.public-app.yml up -d --build
```

The dev deployment publishes the public API on `http://localhost:8013`.
It runs the `production` profile with TLS disabled for local development so
registration, login, authorization, token, discovery, and JWKS routes are
available on the same localhost issuer.

Useful checks:

```bash
curl http://localhost:8013/.well-known/openid-configuration
curl http://localhost:8013/.well-known/jwks.json
curl -i http://localhost:8013/tenant
curl -i http://localhost:8013/diagnostics
```
