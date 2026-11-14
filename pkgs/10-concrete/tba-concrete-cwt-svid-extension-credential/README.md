# tba-concrete-cwt-svid-extension-credential

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-cwt-svid-extension-credential/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-cwt-svid-extension-credential/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-cwt-svid-extension-credential/pyproject.toml"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/10-concrete"><img alt="Layer: 10 concrete" src="https://img.shields.io/badge/Layer-10%20concrete-0a7f5a"></a>
<a href="https://pypi.org/project/tba-concrete-cwt-svid-extension-credential/"><img alt="PyPI version for tba-concrete-cwt-svid-extension-credential" src="https://img.shields.io/pypi/v/tba-concrete-cwt-svid-extension-credential?label=tba-concrete-cwt-svid-extension-credential%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-concrete-cwt-svid-extension-credential"><img alt="Monthly PyPI downloads for tba-concrete-cwt-svid-extension-credential" src="https://static.pepy.tech/badge/tba-concrete-cwt-svid-extension-credential/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-cwt-svid-extension-credential/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Owns an explicitly experimental Tigrbl CWT-SVID extension object. It is not an official SPIFFE SVID format and must never produce a SPIFFE conformance claim.

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This command uses the published package in an isolated Python 3.12 environment.

```python
from tba_concrete_cwt_svid_extension_credential import CwtSvidExtensionCredential

assert callable(CwtSvidExtensionCredential)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-concrete-cwt-svid-extension-credential==0.4.0.dev3" python quickstart.py
```

The import and assertion succeed when the CwtSvidExtensionCredential entry point is available.

## Verification

The quick start was run with the pinned distribution from PyPI and its declared dependencies. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-cwt-svid-extension-credential/src/tba_concrete_cwt_svid_extension_credential/__init__.py).
