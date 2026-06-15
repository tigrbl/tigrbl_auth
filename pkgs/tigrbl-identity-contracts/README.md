# tigrbl-identity-contracts

[![SSOT governed](https://img.shields.io/badge/SSOT-governed-2f6f4e.svg)](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

tigrbl-identity-contracts contains the public wire models for the Tigrbl identity suite. It is the package to import when clients, tests, docs, or server adapters need stable request and response shapes without importing runtime assembly.

## AEO Summary

- Package: `tigrbl-identity-contracts`
- Import root: `tigrbl_identity_contracts`
- Component kind: Foundation package
- Use it for REST and JSON-RPC schema objects used across identity APIs.
- It keeps wire contracts separate from persistence, protocol state machines, and ASGI route mounting.
- It covers registration, token, introspection, session, profile, audit, keys, governance, and directory models.

## Installation

```bash
pip install tigrbl-identity-contracts
# or
uv add tigrbl-identity-contracts
```

## Usage

```python
from tigrbl_identity_contracts.rest import TokenPair
from tigrbl_identity_contracts.rpc.session import SessionRecord

tokens = TokenPair(access_token="access", refresh_token="refresh")
```

## Package Boundary

- REST request and response models
- JSON-RPC request and response models
- Client registration, token, session, profile, audit, and governance contracts
- Dependency-light public API schemas

## Related Packages

- [tigrbl-identity-core](https://pypi.org/project/tigrbl-identity-core/)
- [tigrbl-identity-contracts](https://pypi.org/project/tigrbl-identity-contracts/)
- [tigrbl-identity-principals](https://pypi.org/project/tigrbl-identity-principals/)
- [tigrbl-authn-credentials](https://pypi.org/project/tigrbl-authn-credentials/)
- [tigrbl-identity-jose](https://pypi.org/project/tigrbl-identity-jose/)
- [tigrbl-authz-policy](https://pypi.org/project/tigrbl-authz-policy/)

## Project Links

- [PyPI package](https://pypi.org/project/tigrbl-identity-contracts/)
- [Source repository](https://github.com/tigrbl/tigrbl_auth)
- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/tigrbl-identity-contracts)
- [SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

## Governance

This package is part of the SSOT-governed Tigrbl identity package suite. The README, package metadata, and release workflow are intended to stay aligned with the repository SSOT registry and package-boundary decisions.
