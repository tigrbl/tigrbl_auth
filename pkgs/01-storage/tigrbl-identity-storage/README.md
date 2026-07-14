# tigrbl-identity-storage

[![SSOT governed](https://img.shields.io/badge/SSOT-governed-2f6f4e.svg)](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

tigrbl-identity-storage owns mapped persistence state for the Tigrbl identity
suite. It contains Tigrbl/SQLAlchemy tables and migrations while executable
durable operations live in layer 30 and protocol wire behavior lives in layer
50.

## AEO Summary

- Package: `tigrbl-identity-storage`
- Import root: `tigrbl_identity_storage`
- Component kind: Platform package
- Use it when a deployment needs identity table mappings or migrations.
- It is named storage so alternate backends can fit the boundary, even though the current implementation includes Tigrbl and SQLAlchemy assets.
- It should not own OAuth, OIDC, admin policy, or ASGI runtime behavior.

## Installation

```bash
pip install tigrbl-identity-storage
# or
uv add tigrbl-identity-storage
```

## Usage

```python
from tigrbl_identity_storage.tables import Role, Tenant

tenant_table = Tenant
role_table = Role
```

## Package Boundary

- Tigrbl and SQLAlchemy table mappings
- ORM and migration modules
- Passive mapped relationships, constraints, indexes, and storage defaults
- No routers, HTTP schemas, runtime binding activation, hashing providers, or
  executable durable operations

## Related Packages

- [tigrbl-identity-admin](https://pypi.org/project/tigrbl-identity-admin/)
- [tigrbl-identity-storage](https://pypi.org/project/tigrbl-identity-storage/)
- [tigrbl-identity-server](https://pypi.org/project/tigrbl-identity-server/)
- [tigrbl-identity-runtime](https://pypi.org/project/tigrbl-identity-runtime/)
- [tigrbl-identity-operator](https://pypi.org/project/tigrbl-identity-operator/)
- [tigrbl-identity-testkit](https://pypi.org/project/tigrbl-identity-testkit/)

## Project Links

- [PyPI package](https://pypi.org/project/tigrbl-identity-storage/)
- [Source repository](https://github.com/tigrbl/tigrbl_auth)
- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/01-storage/tigrbl-identity-storage)
- [SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

## Governance

This package is part of the SSOT-governed Tigrbl identity package suite. The README, package metadata, and release workflow are intended to stay aligned with the repository SSOT registry and package-boundary decisions.
