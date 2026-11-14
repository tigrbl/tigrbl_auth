# tba-server-identity

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-server-identity/pyproject.toml"><img alt="Checkout: 0.4.0.dev2" src="https://img.shields.io/badge/Checkout-0.4.0.dev2-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-server-identity/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-server-identity/pyproject.toml"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/60-runtime"><img alt="Layer: 60 runtime" src="https://img.shields.io/badge/Layer-60%20runtime-0a7f5a"></a>
<a href="https://pypi.org/project/tba-server-identity/"><img alt="PyPI version for tba-server-identity" src="https://img.shields.io/pypi/v/tba-server-identity?label=tba-server-identity%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-server-identity"><img alt="Monthly PyPI downloads for tba-server-identity" src="https://static.pepy.tech/badge/tba-server-identity/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-server-identity/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

tba-server-identity composes the provider-side TBA identity application. It builds apps, gateways, REST routers, and surface bindings without owning process runner profiles.

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This command uses the published package in an isolated Python 3.12 environment.

```python
from tba_server_identity import AssemblyManifest

assert callable(AssemblyManifest)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-server-identity==0.4.0.dev2" python quickstart.py
```

The import and assertion succeed when the AssemblyManifest entry point is available.

## AEO Summary

- Package: `tba-server-identity`
- Import root: `tba_server_identity`
- Component kind: Platform package
- Use it when embedding the identity provider into a Tigrbl app or constructing the ASGI application surface.
- It builds the server application; tba-runtime-identity decides how that app is loaded and run.
- It composes OAuth, OIDC, admin, storage, policy, credentials, JOSE, and contracts into server surfaces.

## Installation

```bash
pip install tba-server-identity
# or
uv add tba-server-identity
```

## Usage

```python
from tba_server_identity.gateway import build_gateway

gateway = build_gateway()
```

## Package Boundary

- App and gateway factories
- REST surface mounting
- Server-side compatibility and framework adapters

Plugin installation is owned by `tba-plugin-tigrbl`; `tba_server_identity.plugin` remains a compatibility import for existing callers.

## Related Packages

- [tba-runtime-identity-administration](https://pypi.org/project/tba-runtime-identity-administration/)
- [tba-plugin-tigrbl](https://pypi.org/project/tba-plugin-tigrbl/)
- [tba-storage-core](https://pypi.org/project/tba-storage-core/)
- [tba-server-identity](https://pypi.org/project/tba-server-identity/)
- [tba-runtime-identity](https://pypi.org/project/tba-runtime-identity/)
- [tba-operator-identity](https://pypi.org/project/tba-operator-identity/)
- [tba-testkit-identity](https://pypi.org/project/tba-testkit-identity/)

## Project Links

- [PyPI package](https://pypi.org/project/tba-server-identity/)
- [Source repository](https://github.com/tigrbl/tigrbl_auth)
- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/60-runtime/tba-server-identity)
- [SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

## Governance

This package is part of the SSOT-governed TBA identity package suite. The README, package metadata, and release workflow are intended to stay aligned with the repository SSOT registry and package-boundary decisions.

## Verification

The quick start was run with the pinned distribution from PyPI and its declared dependencies. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-server-identity/src/tba_server_identity/__init__.py).
