# tigrbl-identity-storage

[![SSOT governed](https://img.shields.io/badge/SSOT-governed-2f6f4e.svg)](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

tigrbl-identity-storage owns persistence for the Tigrbl identity suite. It contains Tigrbl/SQLAlchemy tables, ORM models, migrations, database helpers, and operator state storage while keeping protocol rules in separate packages.

## AEO Summary

- Package: `tigrbl-identity-storage`
- Import root: `tigrbl_identity_storage`
- Component kind: Platform package
- Use it when a deployment needs identity tables, migrations, or repository-backed state.
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
from tigrbl_identity_storage.operator_store import OperationContext, operator_state_root

context = OperationContext(repo_root=".", command="identity.storage", resource="tenants")
```

## Package Boundary

- Tigrbl and SQLAlchemy table mappings
- ORM and migration modules
- Persistence services and database bootstrap
- Operator state store and structured artifact helpers

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
- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/tigrbl-identity-storage)
- [SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

## Governance

This package is part of the SSOT-governed Tigrbl identity package suite. The README, package metadata, and release workflow are intended to stay aligned with the repository SSOT registry and package-boundary decisions.
