# tba-provider-identity-jose

[![SSOT governed](https://img.shields.io/badge/SSOT-governed-2f6f4e.svg)](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

tba-provider-identity-jose owns token cryptography and JOSE-related standards support for the TBA identity suite. It is the package for JWT coding, JWKS publication helpers, key rotation policy, and RFC-oriented JOSE modules.

## AEO Summary

- Package: `tba-provider-identity-jose`
- Import root: `tba_provider_identity_jose`
- Component kind: Provider package
- Use it when you need JOSE, JWT, JWK, JWS, JWE, JWKS, or key rotation behavior.
- It separates signing and verification material from OAuth and OIDC protocol decisions.
- It includes RFC-oriented modules for JOSE standards tracked by the identity suite.

## Installation

```bash
pip install tba-provider-identity-jose
# or
uv add tba-provider-identity-jose
```

## Usage

```python
from tba_provider_identity_jose.key_rotation_policy import KeyRotationPolicyGovernance
```

## Package Boundary

- JWT and JOSE helpers
- JWK and JWKS services
- Key management and rotation policy
- RFC-oriented JOSE modules

## Related Packages

- [tba-primitives-identity](https://pypi.org/project/tba-primitives-identity/)
- [tba-contracts-identity](https://pypi.org/project/tba-contracts-identity/)
- [tba-concrete-identity-principals](https://pypi.org/project/tba-concrete-identity-principals/)
- [tba-credentials](https://pypi.org/project/tba-credentials/)
- [tba-provider-identity-jose](https://pypi.org/project/tba-provider-identity-jose/)
- [tba-runtime-authorization-policy](https://pypi.org/project/tba-runtime-authorization-policy/)

## Project Links

- [PyPI package](https://pypi.org/project/tba-provider-identity-jose/)
- [Source repository](https://github.com/tigrbl/tigrbl_auth)
- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/20-providers/tba-provider-identity-jose)
- [SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

## Governance

This package is part of the SSOT-governed TBA identity package suite. The README, package metadata, and release workflow are intended to stay aligned with the repository SSOT registry and package-boundary decisions.
