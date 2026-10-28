# tba-contracts-identity

[![SSOT governed](https://img.shields.io/badge/SSOT-governed-2f6f4e.svg)](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

`tba-contracts-identity` contains dependency-light identity contract types:
abstract protocols, dataclasses, enums, projection metadata,
and declarative plane access/capability metadata.

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
