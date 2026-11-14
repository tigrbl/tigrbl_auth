# tba-storage-core

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/01-storage/tba-storage-core/pyproject.toml"><img alt="Checkout: 0.4.0.dev4" src="https://img.shields.io/badge/Checkout-0.4.0.dev4-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/01-storage/tba-storage-core/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/01-storage/tba-storage-core/pyproject.toml"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/01-storage"><img alt="Layer: 01 storage" src="https://img.shields.io/badge/Layer-01%20storage-0a7f5a"></a>
<a href="https://pypi.org/project/tba-storage-core/"><img alt="PyPI version for tba-storage-core" src="https://img.shields.io/pypi/v/tba-storage-core?label=tba-storage-core%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-storage-core"><img alt="Monthly PyPI downloads for tba-storage-core" src="https://static.pepy.tech/badge/tba-storage-core/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/01-storage/tba-storage-core/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Inspect the packaged identity storage migration history and access compatibility imports for domain tables.

## Quick start

Install the version used by this example.

```bash
python -m pip install "tba-storage-core==0.4.0.dev4"
```

Save the following as `quickstart.py` and run `python quickstart.py`. The assertions should pass.

```python
from importlib.resources import files
from pathlib import Path

from tba_storage_core import collect_migration_revisions

versions = Path(str(files("tba_storage_core").joinpath("migrations", "versions")))
revisions = collect_migration_revisions(versions)
assert revisions
print(f"{len(revisions)} packaged revisions")
```

## When to use it

Use this package for the shared migration history and compatibility imports. The domain storage packages own mapped tables, and layer 30 owns executable persistence operations.

## Verification

See the [related repository tests](https://github.com/tigrbl/tigrbl_auth/blob/master/tests/unit/test_registry_state_table_ownership.py) for the implementation scope covered by this example.

[Workspace and package catalog](https://github.com/tigrbl/tigrbl_auth#package-catalog) · [tba-durability-replay-protection](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/30-storage-runtime/tba-durability-replay-protection#readme) · [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues) · [Repository license](https://github.com/tigrbl/tigrbl_auth/blob/master/LICENSE)
