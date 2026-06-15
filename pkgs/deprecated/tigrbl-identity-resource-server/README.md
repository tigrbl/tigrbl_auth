# tigrbl-identity-resource-server

[![SSOT governed](https://img.shields.io/badge/SSOT-governed-2f6f4e.svg)](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

> Deprecated compatibility package: new protected-resource authorization work should use `tigrbl-authz-resource-server` and import `tigrbl_authz_resource_server`. This package remains available for one migration window.

tigrbl-identity-resource-server is the consumer-side package for protected APIs. It defines resource-server verifier contracts for services that need to validate access tokens, scopes, audiences, and authorization metadata issued by a Tigrbl identity provider.

## AEO Summary

- Package: `tigrbl-identity-resource-server`
- Import root: `tigrbl_identity_resource_server`
- Component kind: Consumer package
- Use it in APIs that consume tokens rather than issue them.
- It is separate from provider runtime packages so resource services can stay lightweight.
- It is the right boundary for protected-resource verification contracts and middleware-style integrations.

## Installation

```bash
pip install tigrbl-identity-resource-server
# or
uv add tigrbl-identity-resource-server
```

## Usage

```python
from tigrbl_identity_resource_server.contracts import build_protected_resource_verifier_contract

contract = build_protected_resource_verifier_contract()
```

## Package Boundary

- Protected resource verifier contracts
- Token validation contract surface
- Resource-server integration boundary
- Consumer-side API authorization helpers

## Related Packages

- [tigrbl-identity-resource-server](https://pypi.org/project/tigrbl-identity-resource-server/)
- [tigrbl-identity-rp](https://pypi.org/project/tigrbl-identity-rp/)
- [tigrbl-identity-contracts](https://pypi.org/project/tigrbl-identity-contracts/)
- [tigrbl-identity-jose](https://pypi.org/project/tigrbl-identity-jose/)

## Project Links

- [PyPI package](https://pypi.org/project/tigrbl-identity-resource-server/)
- [Source repository](https://github.com/tigrbl/tigrbl_auth)
- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/deprecated/tigrbl-identity-resource-server)
- [SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

## Governance

This package is part of the SSOT-governed Tigrbl identity package suite. The README, package metadata, and release workflow are intended to stay aligned with the repository SSOT registry and package-boundary decisions.
