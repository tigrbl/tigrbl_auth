# tba-provider-digital-credential-status

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-digital-credential-status/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-digital-credential-status/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-digital-credential-status/pyproject.toml"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/20-providers"><img alt="Layer: 20 providers" src="https://img.shields.io/badge/Layer-20%20providers-0a7f5a"></a>
<a href="https://pypi.org/project/tba-provider-digital-credential-status/"><img alt="PyPI version for tba-provider-digital-credential-status" src="https://img.shields.io/pypi/v/tba-provider-digital-credential-status?label=tba-provider-digital-credential-status%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-provider-digital-credential-status"><img alt="Monthly PyPI downloads for tba-provider-digital-credential-status" src="https://static.pepy.tech/badge/tba-provider-digital-credential-status/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-digital-credential-status/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Owns environment-backed provider integration.

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This command uses the published package in an isolated Python 3.12 environment.

```python
from tba_provider_digital_credential_status import InMemoryCredentialStatusProvider

assert callable(InMemoryCredentialStatusProvider)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-provider-digital-credential-status==0.4.0.dev3" python quickstart.py
```

The import and assertion succeed when the InMemoryCredentialStatusProvider entry point is available.

## Non-goals

Higher-layer orchestration, lower-layer persistence, and protocol behavior outside this package's declared layer are not owned here.

## Verification

The quick start was run with the pinned distribution from PyPI and its declared dependencies. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-digital-credential-status/src/tba_provider_digital_credential_status/__init__.py).
