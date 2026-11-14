# tba-router-authorization-administration

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-authorization-administration/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-authorization-administration/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-authorization-administration/pyproject.toml"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/80-routers"><img alt="Layer: 80 routers" src="https://img.shields.io/badge/Layer-80%20routers-0a7f5a"></a>
<a href="https://pypi.org/project/tba-router-authorization-administration/"><img alt="PyPI version for tba-router-authorization-administration" src="https://img.shields.io/pypi/v/tba-router-authorization-administration?label=tba-router-authorization-administration%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-router-authorization-administration"><img alt="Monthly PyPI downloads for tba-router-authorization-administration" src="https://static.pepy.tech/badge/tba-router-authorization-administration/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-authorization-administration/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Reusable route contract for tenant-contained and separately authorized internal IAM administration.

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This command uses the published package in an isolated Python 3.12 environment.

```python
from tba_router_authorization_administration import assert_tenant_scope

assert callable(assert_tenant_scope)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-router-authorization-administration==0.4.0.dev3" python quickstart.py
```

The import and assertion succeed when the assert_tenant_scope entry point is available.

## Verification

The quick start was run with the pinned distribution from PyPI and its declared dependencies. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-authorization-administration/src/tba_router_authorization_administration/__init__.py).
