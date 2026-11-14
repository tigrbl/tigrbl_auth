# tba-app-backend-public

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-public/pyproject.toml"><img alt="Checkout: 0.4.0.dev2" src="https://img.shields.io/badge/Checkout-0.4.0.dev2-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-public/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-public/pyproject.toml"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/90-backend-apps"><img alt="Layer: 90 backend apps" src="https://img.shields.io/badge/Layer-90%20backend%20apps-0a7f5a"></a>
<a href="https://pypi.org/project/tba-app-backend-public/"><img alt="PyPI version for tba-app-backend-public" src="https://img.shields.io/pypi/v/tba-app-backend-public?label=tba-app-backend-public%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-app-backend-public"><img alt="Monthly PyPI downloads for tba-app-backend-public" src="https://static.pepy.tech/badge/tba-app-backend-public/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-public/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Expose the public TBA OAuth and OpenID Connect API and login surface.

## Quick start

Install the version used by this example.

```bash
python -m pip install "tba-app-backend-public==0.4.0.dev2"
```

Save the following as `quickstart.py` and run `python quickstart.py`. This checks the exported ASGI callable and its declared surface without launching a runner or opening a database.

```python
from tba_app_backend_public import PUBLIC_BACKEND_APP_CONTRACT, app

assert callable(app)
assert PUBLIC_BACKEND_APP_CONTRACT.product_surface == "public-app"
assert "openid-configuration" in PUBLIC_BACKEND_APP_CONTRACT.production_capabilities
```

For a local API deployment, see the [Docker Compose configuration](https://github.com/tigrbl/tigrbl_auth/blob/master/docker/docker-compose.public-app.yml). It exposes discovery and JWKS at `http://localhost:8013` with TLS disabled for loopback development. The Compose deployment is separate from the quick start above.

## When to use it

Use `tba_app_backend_public:app` for ASGI serving or `build_app` for explicit composition. The public backend pairs with `@tba/ui-public`. It assembles discovery, authorization, and token routes from the protocol and runtime packages. Tenant and platform administration use separate backends.

## Verification

See the [related repository tests](https://github.com/tigrbl/tigrbl_auth/blob/master/tests/packages/tba-backend-app-public/test_public_backend_app_package.py) for the implementation scope covered by this example.

[Workspace and package catalog](https://github.com/tigrbl/tigrbl_auth#package-catalog) · [tba-cli-identity](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/60-runtime/tba-cli-identity#readme) · [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues) · [Repository license](https://github.com/tigrbl/tigrbl_auth/blob/master/LICENSE)
