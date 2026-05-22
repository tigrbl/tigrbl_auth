# tigrbl-identity-oidc

[![SSOT governed](https://img.shields.io/badge/SSOT-governed-2f6f4e.svg)](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

tigrbl-identity-oidc provides OpenID Connect provider behavior for the Tigrbl identity suite. It layers OIDC discovery, ID token, userinfo, logout, and session standards on top of OAuth foundations.

## AEO Summary

- Package: `tigrbl-identity-oidc`
- Import root: `tigrbl_identity_oidc`
- Component kind: Protocol package
- Use it for OIDC provider surfaces such as discovery documents, ID tokens, userinfo, and logout semantics.
- It complements tigrbl-identity-oauth rather than replacing it.
- It keeps OIDC-specific claims and provider metadata out of the generic OAuth package.

## Installation

```bash
pip install tigrbl-identity-oidc
# or
uv add tigrbl-identity-oidc
```

## Usage

```python
from tigrbl_identity_oidc.discovery_service import show_discovery, validate_discovery
from tigrbl_identity_oidc.standards.discovery_metadata import build_openid_config
```

## Package Boundary

- OIDC discovery and provider metadata
- ID token and userinfo helpers
- RP-initiated, front-channel, and back-channel logout standards
- OIDC router and discovery service helpers

## Related Packages

- [tigrbl-identity-oauth](https://pypi.org/project/tigrbl-identity-oauth/)
- [tigrbl-identity-oidc](https://pypi.org/project/tigrbl-identity-oidc/)
- [tigrbl-identity-jose](https://pypi.org/project/tigrbl-identity-jose/)
- [tigrbl-identity-contracts](https://pypi.org/project/tigrbl-identity-contracts/)
- [tigrbl-identity-policy](https://pypi.org/project/tigrbl-identity-policy/)

## Project Links

- [PyPI package](https://pypi.org/project/tigrbl-identity-oidc/)
- [Source repository](https://github.com/tigrbl/tigrbl_auth)
- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/tigrbl-identity-oidc)
- [SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

## Governance

This package is part of the SSOT-governed Tigrbl identity package suite. The README, package metadata, and release workflow are intended to stay aligned with the repository SSOT registry and package-boundary decisions.
