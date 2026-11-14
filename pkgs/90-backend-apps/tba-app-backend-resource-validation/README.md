# tba-app-backend-resource-validation

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-resource-validation/pyproject.toml"><img alt="Checkout: 0.4.0.dev2" src="https://img.shields.io/badge/Checkout-0.4.0.dev2-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-resource-validation/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-resource-validation/pyproject.toml"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/90-backend-apps"><img alt="Layer: 90 backend apps" src="https://img.shields.io/badge/Layer-90%20backend%20apps-0a7f5a"></a>
<a href="https://pypi.org/project/tba-app-backend-resource-validation/"><img alt="PyPI version for tba-app-backend-resource-validation" src="https://img.shields.io/pypi/v/tba-app-backend-resource-validation?label=tba-app-backend-resource-validation%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-app-backend-resource-validation"><img alt="Monthly PyPI downloads for tba-app-backend-resource-validation" src="https://static.pepy.tech/badge/tba-app-backend-resource-validation/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-resource-validation/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Resource-server validation API front door for protected APIs that need issuer metadata.

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This command uses the published package in an isolated Python 3.12 environment.

```python
from tba_app_backend_resource_validation import ResourceValidationBackendAppContract

assert callable(ResourceValidationBackendAppContract)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-app-backend-resource-validation==0.4.0.dev2" python quickstart.py
```

The import and assertion succeed when the ResourceValidationBackendAppContract entry point is available.

## Surface

| Property | Value |
| --- | --- |
| Product surface | `resource-validation-app` |
| Intended consumers | Resource servers, API gateways, validation middleware |
| Exposes | JWKS, tenant JWKS, introspection, OIDC discovery, protected-resource metadata |
| Excludes | Public human login/consent pages, dynamic client registration, admin resources, `/rpc` |

## Entrypoint

```python
from tba_app_backend_resource_validation import app, build_app
```

## Local dev deployment

Run the isolated validation front door on port `8014`:

```bash
docker compose -f docker/docker-compose.resource-validation-app.yml up -d --build
```

Useful endpoints:

| Endpoint | Purpose |
| --- | --- |
| `/.well-known/openid-configuration` | Issuer metadata needed by validators. |
| `/.well-known/oauth-protected-resource` | Protected-resource metadata and verifier contract projection. |
| `/.well-known/jwks.json` | Issuer key set for local JWT validation. |
| `/tenants/{tenant_slug}/.well-known/jwks.json` | Tenant-scoped key set. |
| `/introspect` | RFC 7662 token status checks for authorized callers. |

## Verification

The quick start was run with the pinned distribution from PyPI and its declared dependencies. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-resource-validation/src/tba_app_backend_resource_validation/__init__.py).
