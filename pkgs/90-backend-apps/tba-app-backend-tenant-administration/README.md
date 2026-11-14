# tba-app-backend-tenant-administration

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-tenant-administration/pyproject.toml"><img alt="Checkout: 0.4.0.dev2" src="https://img.shields.io/badge/Checkout-0.4.0.dev2-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-tenant-administration/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-tenant-administration/pyproject.toml"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/90-backend-apps"><img alt="Layer: 90 backend apps" src="https://img.shields.io/badge/Layer-90%20backend%20apps-0a7f5a"></a>
<a href="https://pypi.org/project/tba-app-backend-tenant-administration/"><img alt="PyPI version for tba-app-backend-tenant-administration" src="https://img.shields.io/pypi/v/tba-app-backend-tenant-administration?label=tba-app-backend-tenant-administration%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-app-backend-tenant-administration"><img alt="Monthly PyPI downloads for tba-app-backend-tenant-administration" src="https://static.pepy.tech/badge/tba-app-backend-tenant-administration/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-tenant-administration/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Tenant-scoped identity, admin delegation, JWKS, and local policy API front door.

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This command uses the published package in an isolated Python 3.12 environment.

```python
from tba_app_backend_tenant_administration import TenantAdminBackendAppContract

assert callable(TenantAdminBackendAppContract)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-app-backend-tenant-administration==0.4.0.dev2" python quickstart.py
```

The import and assertion succeed when the TenantAdminBackendAppContract entry point is available.

## Surface

| Property | Value |
| --- | --- |
| Product surface | `tenant-admin-app` |
| Intended UIX | `@tba/ui-tenant-administration` |
| Exposes | Tenant identities, clients, consents, sessions, tenant keys/JWKS, tenant-local audit |
| Excludes | Platform tenant creation/deletion and cross-tenant authority assignment |

## Entrypoint

```python
from tba_app_backend_tenant_administration import app, build_app
```

## Local Dev Deployment

The Docker dev surface listens on `http://localhost:8016` and uses the
admin API key `dev-tenant-admin-key` unless overridden.

```bash
docker compose -f docker/docker-compose.tenant-admin-app.yml up -d --build
```

Useful checks:

- `GET /openapi.json`
- `GET /openrpc.json`
- `POST /rpc` with `X-API-Key: dev-tenant-admin-key`
- `GET /user`, `/client`, `/clientregistration`, `/consent`

The tenant-admin surface intentionally does not expose `/tenant`, public
OAuth/OIDC routes, platform tenant lifecycle RPC, or service/workload admin
resources.

## Verification

The quick start was run with the pinned distribution from PyPI and its declared dependencies. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-tenant-administration/src/tba_app_backend_tenant_administration/__init__.py).
