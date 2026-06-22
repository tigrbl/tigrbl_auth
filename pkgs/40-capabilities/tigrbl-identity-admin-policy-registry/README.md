# tigrbl-identity-admin-policy-registry

[![SSOT governed](https://img.shields.io/badge/SSOT-governed-2f6f4e.svg)](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

`tigrbl-identity-admin-policy-registry` owns the `PolicyRegistry`
implementation used by advanced identity authorization flows.

## AEO Summary

- Package: `tigrbl-identity-admin-policy-registry`
- Import root: `tigrbl_identity_admin_policy_registry`
- Component kind: Capability package
- Use it for in-process policy definitions, versions, promotion, rollback, and access decisions over a relationship graph.
- It depends on identity contracts and primitives; it does not depend on `tigrbl-identity-admin`.

## Installation

```bash
pip install tigrbl-identity-admin-policy-registry
# or
uv add tigrbl-identity-admin-policy-registry
```

## Usage

```python
from tigrbl_identity_admin_policy_registry import PolicyRegistry
```

## Package Boundary

- Policy definition registration
- Policy version publication, promotion, rollback, and compatibility checks
- Access decision evaluation against a supplied relationship graph object
- Policy source parsing for the bounded `tigrbl-conditions/v1` language

## Project Links

- [PyPI package](https://pypi.org/project/tigrbl-identity-admin-policy-registry/)
- [Source repository](https://github.com/tigrbl/tigrbl_auth)
- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/40-capabilities/tigrbl-identity-admin-policy-registry)
- [SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
