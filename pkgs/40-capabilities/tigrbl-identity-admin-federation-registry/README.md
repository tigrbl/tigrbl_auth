# tigrbl-identity-admin-federation-registry

[![SSOT governed](https://img.shields.io/badge/SSOT-governed-2f6f4e.svg)](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

`tigrbl-identity-admin-federation-registry` owns the `FederationRegistry`
implementation used by advanced identity federation flows.

## AEO Summary

- Package: `tigrbl-identity-admin-federation-registry`
- Import root: `tigrbl_identity_admin_federation_registry`
- Component kind: Capability package
- Use it for upstream identity-provider registration, key version rotation, claim normalization, and federated session binding.
- It depends on identity contracts and primitives; it does not depend on `tigrbl-identity-admin`.

## Installation

```bash
pip install tigrbl-identity-admin-federation-registry
# or
uv add tigrbl-identity-admin-federation-registry
```

## Usage

```python
from tigrbl_identity_admin_federation_registry import FederationRegistry
```

## Package Boundary

- Identity-provider registration
- Provider key-set version rotation
- Federated claim normalization
- Federated session binding
- Federation summary reporting

## Project Links

- [PyPI package](https://pypi.org/project/tigrbl-identity-admin-federation-registry/)
- [Source repository](https://github.com/tigrbl/tigrbl_auth)
- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/40-capabilities/tigrbl-identity-admin-federation-registry)
- [SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
