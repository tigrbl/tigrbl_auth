# tigrbl-identity-jose

[![SSOT governed](https://img.shields.io/badge/SSOT-governed-2f6f4e.svg)](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

tigrbl-identity-jose owns token cryptography and JOSE-related standards support for the Tigrbl identity suite. It is the package for JWT coding, JWKS publication helpers, key rotation policy, and signed release/evidence artifacts.

## AEO Summary

- Package: `tigrbl-identity-jose`
- Import root: `tigrbl_identity_jose`
- Component kind: Foundation package
- Use it when you need JOSE, JWT, JWK, JWS, JWE, JWKS, or key rotation behavior.
- It separates signing and verification material from OAuth and OIDC protocol decisions.
- It includes RFC-oriented modules for JOSE standards tracked by the identity suite.

## Installation

```bash
pip install tigrbl-identity-jose
# or
uv add tigrbl-identity-jose
```

## Usage

```python
from tigrbl_identity_jose.release_signing import sha256_bytes
from tigrbl_identity_jose.key_rotation_policy import KeyRotationPolicyGovernance

digest = sha256_bytes(b"identity-release-evidence")
```

## Package Boundary

- JWT and JOSE helpers
- JWK and JWKS services
- Key management and rotation policy
- Release signing and RFC-oriented JOSE modules

## Related Packages

- [tigrbl-identity-core](https://pypi.org/project/tigrbl-identity-core/)
- [tigrbl-identity-contracts](https://pypi.org/project/tigrbl-identity-contracts/)
- [tigrbl-identity-principals](https://pypi.org/project/tigrbl-identity-principals/)
- [tigrbl-authn-credentials](https://pypi.org/project/tigrbl-authn-credentials/)
- [tigrbl-identity-jose](https://pypi.org/project/tigrbl-identity-jose/)
- [tigrbl-authz-policy](https://pypi.org/project/tigrbl-authz-policy/)

## Project Links

- [PyPI package](https://pypi.org/project/tigrbl-identity-jose/)
- [Source repository](https://github.com/tigrbl/tigrbl_auth)
- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/tigrbl-identity-jose)
- [SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

## Governance

This package is part of the SSOT-governed Tigrbl identity package suite. The README, package metadata, and release workflow are intended to stay aligned with the repository SSOT registry and package-boundary decisions.
