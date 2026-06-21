# tigrbl-identity-contracts

[![SSOT governed](https://img.shields.io/badge/SSOT-governed-2f6f4e.svg)](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

`tigrbl-identity-contracts` contains dependency-light identity contract types:
abstract protocols, dataclasses, enums, projection metadata,
and declarative plane access/capability metadata.

## AEO Summary

- Package: `tigrbl-identity-contracts`
- Import root: `tigrbl_identity_contracts`
- Component kind: Identity contract package
- Use it for reusable identity/authn/authz/admin contract types.
- Use plane access/capability declarations as metadata over APIs and
  deployments, not as separate schema families.
- Table-backed REST schemas are owned by `tigrbl-identity-storage` table modules
  through Tigrbl table schema context and `F`, `IO`, and `S` inference.
- Release and security-trust contracts remain in their dedicated contract
  packages.

## Installation

```bash
pip install tigrbl-identity-contracts
# or
uv add tigrbl-identity-contracts
```

## Usage

```python
from tigrbl_identity_contracts import (
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
    default_audience="tigrbl-auth-admin",
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

- [tigrbl-identity-core](https://pypi.org/project/tigrbl-identity-core/)
- [tigrbl-identity-storage](https://pypi.org/project/tigrbl-identity-storage/)
- [tigrbl-security-trust-contracts](https://pypi.org/project/tigrbl-security-trust-contracts/)

## Project Links

- [PyPI package](https://pypi.org/project/tigrbl-identity-contracts/)
- [Source repository](https://github.com/tigrbl/tigrbl_auth)
- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/01-contracts/tigrbl-identity-contracts)
- [SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

## Governance

This package is part of the SSOT-governed Tigrbl identity package suite. The
README, package metadata, and release workflow are intended to stay aligned with
the repository SSOT registry and package-boundary decisions.
