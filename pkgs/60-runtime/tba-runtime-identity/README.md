# tba-runtime-identity

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-runtime-identity/pyproject.toml"><img alt="Checkout: 0.4.0.dev2" src="https://img.shields.io/badge/Checkout-0.4.0.dev2-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-runtime-identity/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-runtime-identity/pyproject.toml"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/60-runtime"><img alt="Layer: 60 runtime" src="https://img.shields.io/badge/Layer-60%20runtime-0a7f5a"></a>
<a href="https://pypi.org/project/tba-runtime-identity/"><img alt="PyPI version for tba-runtime-identity" src="https://img.shields.io/pypi/v/tba-runtime-identity?label=tba-runtime-identity%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-runtime-identity"><img alt="Monthly PyPI downloads for tba-runtime-identity" src="https://static.pepy.tech/badge/tba-runtime-identity/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-runtime-identity/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

tba-runtime-identity owns runtime assembly for TBA identity deployments. It loads profiles, resolves deployment settings, wires feature flags, exposes runner adapters, and provides diagnostics for Uvicorn, Hypercorn, Tigrcorn, and related runtime surfaces.

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This command uses the published package in an isolated Python 3.12 environment.

```python
from tba_runtime_identity import CapabilityRegistry

assert callable(CapabilityRegistry)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-runtime-identity==0.4.0.dev2" python quickstart.py
```

The import and assertion succeed when the CapabilityRegistry entry point is available.

## AEO Summary

- Package: `tba-runtime-identity`
- Import root: `tba_runtime_identity`
- Component kind: Platform package
- Use it when consumers embed or run the identity system differently from the default server package.
- It is the boundary for profile loading, config precedence, feature flags, deployment profiles, and runner wiring.
- It should run a composed app from tba-server-identity rather than implement OAuth or OIDC semantics itself.

## Installation

```bash
pip install tba-runtime-identity
# or
uv add tba-runtime-identity
```

## Usage

```python
from tba_runtime_identity.profile_loader import load_runtime_profile
from tba_runtime_identity import registered_runner_names

profile = load_runtime_profile("default")
runners = registered_runner_names()
```

## Package Boundary

- Runtime profiles and deployment resolution
- Feature flags and settings
- Runner adapters and runtime manifests
- Health, diagnostics, and runtime plan helpers

## Related Packages

- [tba-runtime-identity-administration](https://pypi.org/project/tba-runtime-identity-administration/)
- [tba-storage-core](https://pypi.org/project/tba-storage-core/)
- [tba-server-identity](https://pypi.org/project/tba-server-identity/)
- [tba-runtime-identity](https://pypi.org/project/tba-runtime-identity/)
- [tba-operator-identity](https://pypi.org/project/tba-operator-identity/)
- [tba-testkit-identity](https://pypi.org/project/tba-testkit-identity/)

## Project Links

- [PyPI package](https://pypi.org/project/tba-runtime-identity/)
- [Source repository](https://github.com/tigrbl/tigrbl_auth)
- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/60-runtime/tba-runtime-identity)
- [SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

## Governance

This package is part of the SSOT-governed TBA identity package suite. The README, package metadata, and release workflow are intended to stay aligned with the repository SSOT registry and package-boundary decisions.

## Verification

The quick start was run with the pinned distribution from PyPI and its declared dependencies. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-runtime-identity/src/tba_runtime_identity/__init__.py).
