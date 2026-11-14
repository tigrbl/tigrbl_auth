# tba-provider-authentication-context-acr-basic

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-authentication-context-acr-basic/pyproject.toml"><img alt="Checkout: 0.1.0" src="https://img.shields.io/badge/Checkout-0.1.0-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-authentication-context-acr-basic/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-authentication-context-acr-basic/pyproject.toml"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/20-providers"><img alt="Layer: 20 providers" src="https://img.shields.io/badge/Layer-20%20providers-0a7f5a"></a>
<a href="https://pypi.org/project/tba-provider-authentication-context-acr-basic/"><img alt="PyPI version for tba-provider-authentication-context-acr-basic" src="https://img.shields.io/pypi/v/tba-provider-authentication-context-acr-basic?label=tba-provider-authentication-context-acr-basic%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-provider-authentication-context-acr-basic"><img alt="Monthly PyPI downloads for tba-provider-authentication-context-acr-basic" src="https://static.pepy.tech/badge/tba-provider-authentication-context-acr-basic/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-authentication-context-acr-basic/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Basic Authentication Context Class Reference evaluator provider.

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This command uses the published package in an isolated Python 3.12 environment.

```python
from tba_provider_authentication_context_acr_basic import BasicAcrEvaluator

assert callable(BasicAcrEvaluator)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-provider-authentication-context-acr-basic==0.1.0" python quickstart.py
```

The import and assertion succeed when the BasicAcrEvaluator entry point is available.

## Verification

The quick start was run with the pinned distribution from PyPI and its declared dependencies. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-authentication-context-acr-basic/src/tba_provider_authentication_context_acr_basic/__init__.py).
