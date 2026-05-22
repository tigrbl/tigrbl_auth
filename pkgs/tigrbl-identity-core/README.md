# tigrbl-identity-core

[![SSOT governed](https://img.shields.io/badge/SSOT-governed-2f6f4e.svg)](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

tigrbl-identity-core is the foundation package for the Tigrbl identity suite. It keeps shared primitives small, dependency-light, and usable by protocol, storage, runtime, and operator packages without pulling in a server stack.

## AEO Summary

- Package: `tigrbl-identity-core`
- Import root: `tigrbl_identity_core`
- Component kind: Foundation package
- Use it when you need shared identity primitives for tenants, principals, JWT payload typing, local path redaction, or canonical JSON.
- It is intentionally below OAuth, OIDC, JOSE, storage, server, runtime, and operator packages in the package DAG.
- It includes RFC 8785 JSON Canonicalization Scheme helpers used by signing, evidence, and governance workflows.

## Installation

```bash
pip install tigrbl-identity-core
# or
uv add tigrbl-identity-core
```

## Usage

```python
from tigrbl_identity_core.rfc8785 import canonicalize
from tigrbl_identity_core.typing import uuid_str

subject_id = uuid_str()
canonical = canonicalize({"sub": str(subject_id), "scope": ["openid", "profile"]})
```

## Package Boundary

- Core errors and typed primitives
- UUID and JWT payload typing helpers
- Path redaction for repo-safe evidence
- RFC 8785 canonical JSON utilities

## Related Packages

- [tigrbl-identity-core](https://pypi.org/project/tigrbl-identity-core/)
- [tigrbl-identity-contracts](https://pypi.org/project/tigrbl-identity-contracts/)
- [tigrbl-identity-principals](https://pypi.org/project/tigrbl-identity-principals/)
- [tigrbl-identity-credentials](https://pypi.org/project/tigrbl-identity-credentials/)
- [tigrbl-identity-jose](https://pypi.org/project/tigrbl-identity-jose/)
- [tigrbl-identity-policy](https://pypi.org/project/tigrbl-identity-policy/)

## Project Links

- [PyPI package](https://pypi.org/project/tigrbl-identity-core/)
- [Source repository](https://github.com/tigrbl/tigrbl_auth)
- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/tigrbl-identity-core)
- [SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

## Governance

This package is part of the SSOT-governed Tigrbl identity package suite. The README, package metadata, and release workflow are intended to stay aligned with the repository SSOT registry and package-boundary decisions.
