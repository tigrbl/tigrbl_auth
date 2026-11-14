# tba-client-authorization-administration

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/75-clients/tba-client-authorization-administration/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/75-clients/tba-client-authorization-administration/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/75-clients/tba-client-authorization-administration/pyproject.toml"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/75-clients"><img alt="Layer: 75 clients" src="https://img.shields.io/badge/Layer-75%20clients-0a7f5a"></a>
<a href="https://pypi.org/project/tba-client-authorization-administration/"><img alt="PyPI version for tba-client-authorization-administration" src="https://img.shields.io/pypi/v/tba-client-authorization-administration?label=tba-client-authorization-administration%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-client-authorization-administration"><img alt="Monthly PyPI downloads for tba-client-authorization-administration" src="https://static.pepy.tech/badge/tba-client-authorization-administration/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/75-clients/tba-client-authorization-administration/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Transport-injected authorization administration client.

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This command uses the published package in an isolated Python 3.12 environment.

```python
from tba_client_authorization_administration import AuthorizationAdminClient

assert callable(AuthorizationAdminClient)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-client-authorization-administration==0.4.0.dev3" python quickstart.py
```

The import and assertion succeed when the AuthorizationAdminClient entry point is available.

## Verification

The quick start was run with the pinned distribution from PyPI and its declared dependencies. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/75-clients/tba-client-authorization-administration/src/tba_client_authorization_administration/__init__.py).
