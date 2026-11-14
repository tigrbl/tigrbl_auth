# tbauth

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/70-facade/tbauth/pyproject.toml"><img alt="Checkout: 0.1.0" src="https://img.shields.io/badge/Checkout-0.1.0-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/70-facade/tbauth/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/70-facade/tbauth/pyproject.toml"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/70-facade"><img alt="Layer: 70 facade" src="https://img.shields.io/badge/Layer-70%20facade-0a7f5a"></a>
<a href="https://pypi.org/project/tbauth/"><img alt="PyPI version for tbauth" src="https://img.shields.io/pypi/v/tbauth?label=tbauth%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tbauth"><img alt="Monthly PyPI downloads for tbauth" src="https://static.pepy.tech/badge/tbauth/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/70-facade/tbauth/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

`tbauth` reserves a short facade name for the TBA package suite while
its public contract is being planned.

This initial release intentionally provides no runtime API and installs no
TBA implementation dependencies. Do not build production integrations
against the placeholder module yet.

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This command uses the published package in an isolated Python 3.12 environment.

```python
from tbauth import __version__

assert __version__ == '0.1.0'
```

```bash
uv run --isolated --no-project --python 3.12 --with "tbauth==0.1.0" python quickstart.py
```

The placeholder reports the installed distribution version `0.1.0`.

## Installation

```bash
uv add tbauth
```

## Project links

- [TBA repository](https://github.com/tigrbl/tigrbl_auth)
- [PyPI project](https://pypi.org/project/tbauth/)

## Verification

The quick start was run with the pinned distribution from PyPI and its declared dependencies. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/70-facade/tbauth/src/tbauth/__init__.py).
