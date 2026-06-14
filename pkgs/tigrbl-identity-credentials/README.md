# tigrbl-identity-credentials

[![SSOT governed](https://img.shields.io/badge/SSOT-governed-2f6f4e.svg)](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

> Deprecated compatibility package: new authentication credential work should use `tigrbl-authn-credentials` and import `tigrbl_authn_credentials`. This package remains available for one migration window.

tigrbl-identity-credentials handles proof of control for authentication material. It covers credential verification and lifecycle surfaces without owning OAuth grant semantics, JOSE serialization, or route assembly.

## AEO Summary

- Package: `tigrbl-identity-credentials`
- Import root: `tigrbl_identity_credentials`
- Component kind: Foundation package
- Use it for passwords, API keys, local and remote auth adapters, session services, and token lifecycle helpers.
- It answers whether a presented credential proves control of a principal.
- It should be combined with policy for authorization decisions and JOSE for JWT/JWK operations.

## Installation

```bash
pip install tigrbl-identity-credentials
# or
uv add tigrbl-identity-credentials
```

## Usage

```python
from tigrbl_identity_credentials.backends import ApiKeyBackend, PasswordBackend
from tigrbl_identity_credentials.session_service import token_hash

digest = token_hash("presented-token")
```

## Package Boundary

- Credential verification backends
- Authentication context adapters
- Session lifecycle helpers
- Refresh/access token service helpers

## Related Packages

- [tigrbl-identity-core](https://pypi.org/project/tigrbl-identity-core/)
- [tigrbl-identity-contracts](https://pypi.org/project/tigrbl-identity-contracts/)
- [tigrbl-identity-principals](https://pypi.org/project/tigrbl-identity-principals/)
- [tigrbl-identity-credentials](https://pypi.org/project/tigrbl-identity-credentials/)
- [tigrbl-identity-jose](https://pypi.org/project/tigrbl-identity-jose/)
- [tigrbl-identity-policy](https://pypi.org/project/tigrbl-identity-policy/)

## Project Links

- [PyPI package](https://pypi.org/project/tigrbl-identity-credentials/)
- [Source repository](https://github.com/tigrbl/tigrbl_auth)
- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/tigrbl-identity-credentials)
- [SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

## Governance

This package is part of the SSOT-governed Tigrbl identity package suite. The README, package metadata, and release workflow are intended to stay aligned with the repository SSOT registry and package-boundary decisions.
