# tba-runtime-relying-party-session

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/30-storage-runtime/tba-runtime-relying-party-session/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/30-storage-runtime/tba-runtime-relying-party-session/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/30-storage-runtime/tba-runtime-relying-party-session/pyproject.toml"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/30-storage-runtime"><img alt="Layer: 30 storage runtime" src="https://img.shields.io/badge/Layer-30%20storage%20runtime-0a7f5a"></a>
<a href="https://pypi.org/project/tba-runtime-relying-party-session/"><img alt="PyPI version for tba-runtime-relying-party-session" src="https://img.shields.io/pypi/v/tba-runtime-relying-party-session?label=tba-runtime-relying-party-session%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-runtime-relying-party-session"><img alt="Monthly PyPI downloads for tba-runtime-relying-party-session" src="https://static.pepy.tech/badge/tba-runtime-relying-party-session/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/30-storage-runtime/tba-runtime-relying-party-session/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Server-owned, expiring, one-time RP login transaction state. The in-memory repository is intended for tests and single-process development; production adapters implement the same repository boundary.

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This command uses the published package in an isolated Python 3.12 environment.

```python
from tba_runtime_relying_party_session import RPTransaction

assert callable(RPTransaction)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-runtime-relying-party-session==0.4.0.dev3" python quickstart.py
```

The import and assertion succeed when the RPTransaction entry point is available.

## Verification

The quick start was run with the pinned distribution from PyPI and its declared dependencies. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/30-storage-runtime/tba-runtime-relying-party-session/src/tba_runtime_relying_party_session/__init__.py).
