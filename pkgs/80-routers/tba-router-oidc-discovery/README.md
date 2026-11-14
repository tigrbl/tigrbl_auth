# tba-router-oidc-discovery

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-oidc-discovery/pyproject.toml"><img alt="Checkout: 0.4.0.dev2" src="https://img.shields.io/badge/Checkout-0.4.0.dev2-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-oidc-discovery/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-oidc-discovery/pyproject.toml"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/80-routers"><img alt="Layer: 80 routers" src="https://img.shields.io/badge/Layer-80%20routers-0a7f5a"></a>
<a href="https://pypi.org/project/tba-router-oidc-discovery/"><img alt="PyPI version for tba-router-oidc-discovery" src="https://img.shields.io/pypi/v/tba-router-oidc-discovery?label=tba-router-oidc-discovery%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-router-oidc-discovery"><img alt="Monthly PyPI downloads for tba-router-oidc-discovery" src="https://static.pepy.tech/badge/tba-router-oidc-discovery/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-oidc-discovery/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Thin HTTP carrier for OIDC discovery and issuer, tenant, and realm JWKS
publication. Metadata construction, durable existence checks, and key material
resolution are injected by runtime composition.

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This command uses the published package in an isolated Python 3.12 environment.

```python
from tba_router_oidc_discovery import build_oidc_discovery_routers

assert callable(build_oidc_discovery_routers)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-router-oidc-discovery==0.4.0.dev2" python quickstart.py
```

The import and assertion succeed when the build_oidc_discovery_routers entry point is available.

## Verification

The quick start was run with the pinned distribution from PyPI and its declared dependencies. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-oidc-discovery/src/tba_router_oidc_discovery/__init__.py).
