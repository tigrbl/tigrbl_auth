# tba-storage-access-governance

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/01-storage/tba-storage-access-governance/pyproject.toml"><img alt="Checkout: 0.4.0.dev2" src="https://img.shields.io/badge/Checkout-0.4.0.dev2-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/01-storage/tba-storage-access-governance/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/01-storage"><img alt="Layer: 01 storage" src="https://img.shields.io/badge/Layer-01%20storage-0a7f5a"></a>
<a href="https://pypi.org/project/tba-storage-access-governance/"><img alt="PyPI version for tba-storage-access-governance" src="https://img.shields.io/pypi/v/tba-storage-access-governance?label=tba-storage-access-governance%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-storage-access-governance"><img alt="Monthly PyPI downloads for tba-storage-access-governance" src="https://static.pepy.tech/badge/tba-storage-access-governance/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/01-storage/tba-storage-access-governance/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Owns the `tigrbl.identity.storage.access-governance` schema component.

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This command uses the published package in an isolated Python 3.12 environment.

```python
from tba_storage_access_governance import TABLE_MODELS

assert TABLE_MODELS
print(len(TABLE_MODELS))
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-storage-access-governance==0.4.0.dev2" python quickstart.py
```

The command prints a positive inventory count.

## Verification

The quick start was run with the pinned distribution from PyPI and its declared dependencies. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/01-storage/tba-storage-access-governance/src/tba_storage_access_governance/__init__.py).
