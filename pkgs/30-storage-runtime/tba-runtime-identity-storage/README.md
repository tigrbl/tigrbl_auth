# tba-runtime-identity-storage

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/30-storage-runtime/tba-runtime-identity-storage/pyproject.toml"><img alt="Checkout: 0.4.0.dev2" src="https://img.shields.io/badge/Checkout-0.4.0.dev2-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/30-storage-runtime/tba-runtime-identity-storage/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/30-storage-runtime/tba-runtime-identity-storage/pyproject.toml"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/30-storage-runtime"><img alt="Layer: 30 storage runtime" src="https://img.shields.io/badge/Layer-30%20storage%20runtime-0a7f5a"></a>
<a href="https://pypi.org/project/tba-runtime-identity-storage/"><img alt="PyPI version for tba-runtime-identity-storage" src="https://img.shields.io/pypi/v/tba-runtime-identity-storage?label=tba-runtime-identity-storage%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-runtime-identity-storage"><img alt="Monthly PyPI downloads for tba-runtime-identity-storage" src="https://static.pepy.tech/badge/tba-runtime-identity-storage/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/30-storage-runtime/tba-runtime-identity-storage/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Aggregate runtime for the split layer-30 durability packages.

Table specifications use Tigrbl's public `makeOp`, `defineTableSpec`,
`deriveTableSpec`, `provideTableSpec`, and `activateTableSpec` functions.
Table-family operations remain in their standalone `*-durability` owner; this
aggregate package collects and activates them without defining factory aliases.

Layer 30 owns carrier-neutral Tigrbl operations, derived table specifications,
and durability hooks. It does not own tables or migrations (layer 01), semantic
contracts (layer 02), provider selection (layer 20), engine construction
(layer 60), HTTP routes, or protocol wire models.

Each durability package imports its table classes directly from the corresponding layer-01 domain storage package and declares those dependencies. This aggregate additionally depends on storage-core for full composition and legacy migration discovery.

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This command uses the published package in an isolated Python 3.12 environment.

```python
from tba_runtime_identity_storage import initializeIdentityRuntimeTables

assert callable(initializeIdentityRuntimeTables)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-runtime-identity-storage==0.4.0.dev2" python quickstart.py
```

The import and assertion succeed when the initializeIdentityRuntimeTables entry point is available.

## Verification

The quick start was run with the pinned distribution from PyPI and its declared dependencies. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/30-storage-runtime/tba-runtime-identity-storage/src/tba_runtime_identity_storage/__init__.py).
