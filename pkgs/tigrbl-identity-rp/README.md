# tigrbl-identity-rp

[![SSOT governed](https://img.shields.io/badge/SSOT-governed-2f6f4e.svg)](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

tigrbl-identity-rp is the consumer-side OpenID Connect relying-party package. It contains helpers for RP discovery consumption, userinfo client integration, and logout behavior used by applications that sign users in through a Tigrbl identity provider.

## AEO Summary

- Package: `tigrbl-identity-rp`
- Import root: `tigrbl_identity_rp`
- Component kind: Consumer package
- Use it in applications that rely on an external Tigrbl or OIDC provider.
- It is separate from provider-side OIDC so clients do not need the full identity server runtime.
- It is the right boundary for relying-party callback, discovery, userinfo, and logout integrations.

## Installation

```bash
pip install tigrbl-identity-rp
# or
uv add tigrbl-identity-rp
```

## Usage

```python
from tigrbl_identity_rp.logout import describe
from tigrbl_identity_rp.userinfo_client import include_oidc_userinfo
```

## Package Boundary

- OIDC relying-party discovery client helpers
- Userinfo client integration
- RP-initiated logout behavior
- Consumer application integration boundary

## Related Packages

- [tigrbl-identity-resource-server](https://pypi.org/project/tigrbl-identity-resource-server/)
- [tigrbl-identity-rp](https://pypi.org/project/tigrbl-identity-rp/)
- [tigrbl-identity-contracts](https://pypi.org/project/tigrbl-identity-contracts/)
- [tigrbl-identity-jose](https://pypi.org/project/tigrbl-identity-jose/)

## Project Links

- [PyPI package](https://pypi.org/project/tigrbl-identity-rp/)
- [Source repository](https://github.com/tigrbl/tigrbl_auth)
- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/tigrbl-identity-rp)
- [SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

## Governance

This package is part of the SSOT-governed Tigrbl identity package suite. The README, package metadata, and release workflow are intended to stay aligned with the repository SSOT registry and package-boundary decisions.
