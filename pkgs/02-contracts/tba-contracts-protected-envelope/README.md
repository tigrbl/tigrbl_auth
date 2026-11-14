# tba-contracts-protected-envelope

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-protected-envelope/pyproject.toml"><img alt="Checkout: 0.4.0.dev2" src="https://img.shields.io/badge/Checkout-0.4.0.dev2-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-protected-envelope/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-protected-envelope/pyproject.toml"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/02-contracts"><img alt="Layer: 02 contracts" src="https://img.shields.io/badge/Layer-02%20contracts-0a7f5a"></a>
<a href="https://pypi.org/project/tba-contracts-protected-envelope/"><img alt="PyPI version for tba-contracts-protected-envelope" src="https://img.shields.io/pypi/v/tba-contracts-protected-envelope?label=tba-contracts-protected-envelope%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-contracts-protected-envelope"><img alt="Monthly PyPI downloads for tba-contracts-protected-envelope" src="https://static.pepy.tech/badge/tba-contracts-protected-envelope/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-protected-envelope/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Protocol-neutral signed and encrypted envelope contracts.

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This command uses the published package in an isolated Python 3.12 environment.

```python
from tba_contracts_protected_envelope import EnvelopeProtectionRequest

assert callable(EnvelopeProtectionRequest)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-contracts-protected-envelope==0.4.0.dev2" python quickstart.py
```

The import and assertion succeed when the EnvelopeProtectionRequest entry point is available.

## Verification

The quick start was run with the pinned distribution from PyPI and its declared dependencies. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-protected-envelope/src/tba_contracts_protected_envelope/__init__.py).
