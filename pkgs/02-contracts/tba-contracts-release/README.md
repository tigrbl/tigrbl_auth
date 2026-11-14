# tba-contracts-release

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-release/pyproject.toml"><img alt="Checkout: 0.1.0" src="https://img.shields.io/badge/Checkout-0.1.0-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-release/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-release/pyproject.toml"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/02-contracts"><img alt="Layer: 02 contracts" src="https://img.shields.io/badge/Layer-02%20contracts-0a7f5a"></a>
<a href="https://pypi.org/project/tba-contracts-release/"><img alt="PyPI version for tba-contracts-release" src="https://img.shields.io/pypi/v/tba-contracts-release?label=tba-contracts-release%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-contracts-release"><img alt="Monthly PyPI downloads for tba-contracts-release" src="https://static.pepy.tech/badge/tba-contracts-release/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-release/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Dependency-light contracts for release assurance, release attestation, runtime
qualification, and release gate evidence.

This package contains only dataclasses, enums, protocols, type aliases, and
contract errors. It does not implement signing, verification, evidence
collection, storage, routing, SSOT CLI integration, or release gate execution.

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This command uses the published package in an isolated Python 3.12 environment.

```python
from tba_contracts_release import AlgorithmPolicy

assert callable(AlgorithmPolicy)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-contracts-release==0.1.0" python quickstart.py
```

The import and assertion succeed when the AlgorithmPolicy entry point is available.

## Verification

The quick start was run with the pinned distribution from PyPI and its declared dependencies. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-release/src/tba_contracts_release/__init__.py).
