# tba-bases-identity

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-identity/pyproject.toml"><img alt="Checkout: 0.4.0.dev2" src="https://img.shields.io/badge/Checkout-0.4.0.dev2-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-identity/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-identity/pyproject.toml"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/05-bases"><img alt="Layer: 05 bases" src="https://img.shields.io/badge/Layer-05%20bases-0a7f5a"></a>
<a href="https://pypi.org/project/tba-bases-identity/"><img alt="PyPI version for tba-bases-identity" src="https://img.shields.io/pypi/v/tba-bases-identity?label=tba-bases-identity%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-bases-identity"><img alt="Monthly PyPI downloads for tba-bases-identity" src="https://static.pepy.tech/badge/tba-bases-identity/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-identity/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Reusable bases for concrete identities and subject-identifier strategies.

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This command uses the published package in an isolated Python 3.12 environment.

```python
from tba_bases_identity import SubjectIdentifierStrategyBase

assert callable(SubjectIdentifierStrategyBase)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-bases-identity==0.4.0.dev2" python quickstart.py
```

The import and assertion succeed when the SubjectIdentifierStrategyBase entry point is available.

## Verification

The quick start was run with the pinned distribution from PyPI and its declared dependencies. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-identity/src/tba_bases_identity/__init__.py).
