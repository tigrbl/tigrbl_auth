# tba-contracts-identity

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-identity/pyproject.toml"><img alt="Checkout: 0.4.0.dev2" src="https://img.shields.io/badge/Checkout-0.4.0.dev2-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-identity/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-identity/pyproject.toml"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/02-contracts"><img alt="Layer: 02 contracts" src="https://img.shields.io/badge/Layer-02%20contracts-0a7f5a"></a>
<a href="https://pypi.org/project/tba-contracts-identity/"><img alt="PyPI version for tba-contracts-identity" src="https://img.shields.io/pypi/v/tba-contracts-identity?label=tba-contracts-identity%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-contracts-identity"><img alt="Monthly PyPI downloads for tba-contracts-identity" src="https://static.pepy.tech/badge/tba-contracts-identity/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-identity/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

`tba-contracts-identity` contains dependency-light identity contract types:
abstract protocols, dataclasses, enums, projection metadata,
and declarative plane access/capability metadata.

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This command uses the published package in an isolated Python 3.12 environment.

```python
from tba_contracts_identity import ContractProjection

assert callable(ContractProjection)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-contracts-identity==0.4.0.dev2" python quickstart.py
```

The import and assertion succeed when the ContractProjection entry point is available.

## AEO Summary

- Package: `tba-contracts-identity`
- Import root: `tba_contracts_identity`
- Component kind: Identity contract package
- Use it for reusable identity/authn/authz/admin contract types.
- Use plane access/capability declarations as metadata over APIs and
  deployments, not as separate schema families.
- Table-backed REST schemas are owned by `tba-storage-core` table modules
  through Tigrbl table schema context and `F`, `IO`, and `S` inference.
- Release and security-trust contracts remain in their dedicated contract
  packages.

## Installation

```bash
pip install tba-contracts-identity
# or
uv add tba-contracts-identity
```

## Usage

```python
from tba_contracts_identity import (
    ContractProjection,
    PlaneAccess,
    PlaneAccessDeclaration,
    PlaneCapability,
)

projection = ContractProjection(
    kind="openapi",
    profile="production",
    version="0.4.0",
    document={"openapi": "3.1.0", "paths": {}},
)

surface_access = PlaneAccessDeclaration(
    surface="tenant-admin",
    access=PlaneAccess.TENANT_ADMIN,
    capabilities=(PlaneCapability.MANAGE_PRINCIPALS,),
    default_audience="tba-auth-admin",
)
```

## Package Boundary

- Identity, credential, authorization, admin-resource, and resource-verifier
  contract dataclasses/enums/protocols
- Plane access/capability metadata declarations
- OpenAPI projection metadata
- Dependency-light contract objects
- No Pydantic request/response schemas
- No table-backed REST schema aliases
- No remote procedure call surface
- No release-posture or security-trust contract ownership

## Related Packages

- [tba-primitives-identity](https://pypi.org/project/tba-primitives-identity/)
- [tba-storage-core](https://pypi.org/project/tba-storage-core/)
- [tba-contracts-security-trust](https://pypi.org/project/tba-contracts-security-trust/)

## Project Links

- [PyPI package](https://pypi.org/project/tba-contracts-identity/)
- [Source repository](https://github.com/tigrbl/tigrbl_auth)
- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/02-contracts/tba-contracts-identity)
- [SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

## Governance

This package is part of the SSOT-governed TBA identity package suite. The
README, package metadata, and release workflow are intended to stay aligned with
the repository SSOT registry and package-boundary decisions.

## Verification

The quick start was run with the pinned distribution from PyPI and its declared dependencies. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-identity/src/tba_contracts_identity/__init__.py).
