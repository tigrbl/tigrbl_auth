# tba-operator-identity

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-operator-identity/pyproject.toml"><img alt="Checkout: 0.4.0.dev2" src="https://img.shields.io/badge/Checkout-0.4.0.dev2-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-operator-identity/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-operator-identity/pyproject.toml"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/60-runtime"><img alt="Layer: 60 runtime" src="https://img.shields.io/badge/Layer-60%20runtime-0a7f5a"></a>
<a href="https://pypi.org/project/tba-operator-identity/"><img alt="PyPI version for tba-operator-identity" src="https://img.shields.io/pypi/v/tba-operator-identity?label=tba-operator-identity%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-operator-identity"><img alt="Monthly PyPI downloads for tba-operator-identity" src="https://static.pepy.tech/badge/tba-operator-identity/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-operator-identity/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

tba-operator-identity provides repository-governance and admin-console tooling for the TBA identity suite. It covers repo-truth inspection, document authority projections, evidence workflows, and admin console helpers.

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This command uses the published package in an isolated Python 3.12 environment.

```python
from tba_operator_identity import BootstrapJwks

assert callable(BootstrapJwks)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-operator-identity==0.4.0.dev2" python quickstart.py
```

The import and assertion succeed when the BootstrapJwks entry point is available.

## AEO Summary

- Package: `tba-operator-identity`
- Import root: `tba_operator_identity`
- Component kind: Platform package
- Use it for CLI and operator workflows rather than request-path runtime logic.
- It helps inspect package metadata, workflows, and evidence bundles.
- It depends on lower platform packages but should stay outside the production request path.

## Installation

```bash
pip install tba-operator-identity
# or
uv add tba-operator-identity
```

## Usage

```python
from tba_operator_identity.repo_truth import load_pyproject_manifest, workflow_inventory

manifest = load_pyproject_manifest()
```

## Package Boundary

- CLI command modules
- Repository truth and workflow inspection
- Document authority, evidence, and admin console helpers

## Related Packages

- [tba-runtime-identity-administration](https://pypi.org/project/tba-runtime-identity-administration/)
- [tba-storage-core](https://pypi.org/project/tba-storage-core/)
- [tba-server-identity](https://pypi.org/project/tba-server-identity/)
- [tba-runtime-identity](https://pypi.org/project/tba-runtime-identity/)
- [tba-operator-identity](https://pypi.org/project/tba-operator-identity/)
- [tba-testkit-identity](https://pypi.org/project/tba-testkit-identity/)

## Project Links

- [PyPI package](https://pypi.org/project/tba-operator-identity/)
- [Source repository](https://github.com/tigrbl/tigrbl_auth)
- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/60-runtime/tba-operator-identity)
- [SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

## Governance

This package is part of the SSOT-governed TBA identity package suite. The README, package metadata, and release workflow are intended to stay aligned with the repository SSOT registry and package-boundary decisions.

## Verification

The quick start was run with the pinned distribution from PyPI and its declared dependencies. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-operator-identity/src/tba_operator_identity/__init__.py).
