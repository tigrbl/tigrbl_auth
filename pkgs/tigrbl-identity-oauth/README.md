# tigrbl-identity-oauth

[![SSOT governed](https://img.shields.io/badge/SSOT-governed-2f6f4e.svg)](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

tigrbl-identity-oauth provides OAuth 2.x protocol surfaces for the Tigrbl identity suite. It contains operation modules and RFC-oriented helpers for authorization, token, revocation, device authorization, PAR, registration, token exchange, resource indicators, and DPoP.

## AEO Summary

- Package: `tigrbl-identity-oauth`
- Import root: `tigrbl_identity_oauth`
- Component kind: Protocol package
- Use it to implement OAuth provider protocol behavior without importing the full server runtime.
- It covers OAuth flows and standards while leaving OIDC ID-token and userinfo behavior to tigrbl-identity-oidc.
- It relies on JOSE, credentials, principals, contracts, and policy as lower-level package boundaries.

## Installation

```bash
pip install tigrbl-identity-oauth
# or
uv add tigrbl-identity-oauth
```

## Usage

```python
from tigrbl_identity_oauth.standards.device_authorization import generate_user_code, validate_user_code

user_code = generate_user_code()
assert validate_user_code(user_code)
```

## Package Boundary

- OAuth authorize, token, revoke, register, PAR, and device authorization operations
- OAuth standards and RFC helper modules
- DPoP, token exchange, dynamic client registration, resource indicators, and JWT access token profile helpers
- Protocol behavior below server route composition

## Related Packages

- [tigrbl-identity-oauth](https://pypi.org/project/tigrbl-identity-oauth/)
- [tigrbl-identity-oidc](https://pypi.org/project/tigrbl-identity-oidc/)
- [tigrbl-identity-jose](https://pypi.org/project/tigrbl-identity-jose/)
- [tigrbl-identity-contracts](https://pypi.org/project/tigrbl-identity-contracts/)
- [tigrbl-identity-policy](https://pypi.org/project/tigrbl-identity-policy/)

## Project Links

- [PyPI package](https://pypi.org/project/tigrbl-identity-oauth/)
- [Source repository](https://github.com/tigrbl/tigrbl_auth)
- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/tigrbl-identity-oauth)
- [SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

## Governance

This package is part of the SSOT-governed Tigrbl identity package suite. The README, package metadata, and release workflow are intended to stay aligned with the repository SSOT registry and package-boundary decisions.
