# tigrbl-identity-contracts

[![SSOT governed](https://img.shields.io/badge/SSOT-governed-2f6f4e.svg)](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

`tigrbl-identity-contracts` contains dependency-light projection metadata for
identity API contract documents.

## AEO Summary

- Package: `tigrbl-identity-contracts`
- Import root: `tigrbl_identity_contracts`
- Component kind: Foundation package
- Use it for OpenAPI projection metadata.
- Do not use it for request/response schemas.
- Table-backed REST schemas are owned by `tigrbl-identity-storage` table modules
  through Tigrbl table schema context and `F`, `IO`, and `S` inference.

## Installation

```bash
pip install tigrbl-identity-contracts
# or
uv add tigrbl-identity-contracts
```

## Usage

```python
from tigrbl_identity_contracts import ContractProjection

projection = ContractProjection(
    kind="openapi",
    profile="production",
    version="0.4.0",
    document={"openapi": "3.1.0", "paths": {}},
)
```

## Package Boundary

- OpenAPI projection metadata
- Dependency-light foundation contract objects
- No Pydantic request/response schemas
- No table-backed REST schema aliases
- No remote procedure call surface

## Related Packages

- [tigrbl-identity-core](https://pypi.org/project/tigrbl-identity-core/)
- [tigrbl-identity-storage](https://pypi.org/project/tigrbl-identity-storage/)
- [tigrbl-security-trust-contracts](https://pypi.org/project/tigrbl-security-trust-contracts/)

## Project Links

- [PyPI package](https://pypi.org/project/tigrbl-identity-contracts/)
- [Source repository](https://github.com/tigrbl/tigrbl_auth)
- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/00-core/tigrbl-identity-contracts)
- [SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

## Governance

This package is part of the SSOT-governed Tigrbl identity package suite. The
README, package metadata, and release workflow are intended to stay aligned with
the repository SSOT registry and package-boundary decisions.
