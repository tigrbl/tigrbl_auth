# tba-app-backend-platform-administration

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-platform-administration/pyproject.toml"><img alt="Checkout: 0.4.0.dev2" src="https://img.shields.io/badge/Checkout-0.4.0.dev2-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-platform-administration/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-platform-administration/pyproject.toml"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/90-backend-apps"><img alt="Layer: 90 backend apps" src="https://img.shields.io/badge/Layer-90%20backend%20apps-0a7f5a"></a>
<a href="https://pypi.org/project/tba-app-backend-platform-administration/"><img alt="PyPI version for tba-app-backend-platform-administration" src="https://img.shields.io/pypi/v/tba-app-backend-platform-administration?label=tba-app-backend-platform-administration%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-app-backend-platform-administration"><img alt="Monthly PyPI downloads for tba-app-backend-platform-administration" src="https://static.pepy.tech/badge/tba-app-backend-platform-administration/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-platform-administration/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Platform-scoped tenant lifecycle and authority-assignment API front door.

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This command uses the published package in an isolated Python 3.12 environment.

```python
from tba_app_backend_platform_administration import AdminIdentityOut

assert callable(AdminIdentityOut)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-app-backend-platform-administration==0.4.0.dev2" python quickstart.py
```

The import and assertion succeed when the AdminIdentityOut entry point is available.

## Surface

| Property | Value |
| --- | --- |
| Product surface | `platform-admin-app` |

The backend app owns HTTP schemas and routes only. Tenant, realm, and identity
administration are invoked through request-scoped layer-40 capabilities composed
by `tba-server-identity`; durable table operations and secret hashing remain
in the layer-60 runtime adapters and their lower-layer providers.
| Intended UIX | `@tba/ui-platform-administration` |
| Exposes | Tenant lifecycle, platform authority assignment, admin identity lookup, audit/session/profile RPC |
| Excludes | Public login/consent pages, tenant self-service-only workflows, developer app registration surface |

## Entrypoint

```python
from tba_app_backend_platform_administration import app, build_app
```

## Local dev deployment

Run the isolated platform control-plane front door on port `8015`:

```bash
docker compose -f docker/docker-compose.platform-admin-app.yml up -d --build
```

The dev API key defaults to `dev-platform-admin-key`.

Useful endpoints:

| Endpoint | Purpose |
| --- | --- |
| `/openapi.json` | Platform-admin REST/control-plane contract. |
| `/openrpc.json` | Platform-admin JSON-RPC method contract. |
| `/rpc` | API-key-protected JSON-RPC dispatch. |
| `/tenant` | API-key-protected platform tenant lifecycle resource. |

## Verification

The quick start was run with the pinned distribution from PyPI and its declared dependencies. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-platform-administration/src/tba_app_backend_platform_administration/__init__.py).
