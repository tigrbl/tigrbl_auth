# tba-contracts-replay

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-replay/pyproject.toml"><img alt="Checkout: 0.4.0.dev2" src="https://img.shields.io/badge/Checkout-0.4.0.dev2-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-replay/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-replay/pyproject.toml"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/02-contracts"><img alt="Layer: 02 contracts" src="https://img.shields.io/badge/Layer-02%20contracts-0a7f5a"></a>
<a href="https://pypi.org/project/tba-contracts-replay/"><img alt="PyPI version for tba-contracts-replay" src="https://img.shields.io/pypi/v/tba-contracts-replay?label=tba-contracts-replay%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-contracts-replay"><img alt="Monthly PyPI downloads for tba-contracts-replay" src="https://static.pepy.tech/badge/tba-contracts-replay/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-replay/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Owns replay keys, atomic reservations, single-use nonces, and replay-check ports.

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This command uses the published package in an isolated Python 3.12 environment.

```python
from tba_contracts_replay import ReplayKey

assert callable(ReplayKey)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-contracts-replay==0.4.0.dev2" python quickstart.py
```

The import and assertion succeed when the ReplayKey entry point is available.

## Verification

The quick start was run with the pinned distribution from PyPI and its declared dependencies. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-replay/src/tba_contracts_replay/__init__.py).
