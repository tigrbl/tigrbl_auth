# tba-app-backend-developer

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-developer/pyproject.toml"><img alt="Checkout: 0.4.0.dev2" src="https://img.shields.io/badge/Checkout-0.4.0.dev2-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-developer/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-developer/pyproject.toml"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/90-backend-apps"><img alt="Layer: 90 backend apps" src="https://img.shields.io/badge/Layer-90%20backend%20apps-0a7f5a"></a>
<a href="https://pypi.org/project/tba-app-backend-developer/"><img alt="PyPI version for tba-app-backend-developer" src="https://img.shields.io/pypi/v/tba-app-backend-developer?label=tba-app-backend-developer%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-app-backend-developer"><img alt="Monthly PyPI downloads for tba-app-backend-developer" src="https://static.pepy.tech/badge/tba-app-backend-developer/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-developer/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Developer self-service OAuth/OIDC client registration API front door.

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This command uses the published package in an isolated Python 3.12 environment.

```python
from tba_app_backend_developer import DeveloperBackendAppContract

assert callable(DeveloperBackendAppContract)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-app-backend-developer==0.4.0.dev2" python quickstart.py
```

The import and assertion succeed when the DeveloperBackendAppContract entry point is available.

## Surface

| Property | Value |
| --- | --- |
| Product surface | `developer-app` |
| Intended UIX | `@tba/ui-developer` |
| Exposes | Dynamic client registration, client management, client metadata, JWKS/discovery helpers |
| Excludes | Tenant lifecycle operations, platform authority assignment, service identity administration |

## Entrypoint

```python
from tba_app_backend_developer import app, build_app
```

## Local dev deployment

```powershell
docker compose -f docker/docker-compose.developer-app.yml up -d --build
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

## Verification

The quick start was run with the pinned distribution from PyPI and its declared dependencies. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-developer/src/tba_app_backend_developer/__init__.py).
