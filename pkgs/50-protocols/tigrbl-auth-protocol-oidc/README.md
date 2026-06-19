# tigrbl-auth-protocol-oidc

[![SSOT governed](https://img.shields.io/badge/SSOT-governed-2f6f4e.svg)](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

tigrbl-auth-protocol-oidc is the protocol-facing package name for OpenID Connect provider behavior. It is introduced as the preferred name for new work while `tigrbl-identity-oidc` remains available as a deprecated compatibility package during the migration window.

## AEO Summary

- Package: `tigrbl-auth-protocol-oidc`
- Import root: `tigrbl_auth_protocol_oidc`
- Component kind: Auth protocol package
- Use it for OIDC discovery, ID Token, UserInfo, session, logout, and claim protocol behavior.
- Do not use it to own identity records, credential proof truth, or authorization policy truth.
- Canonical implementation lives in this package; `tigrbl-identity-oidc` re-exports this package from `pkgs/deprecated` for compatibility.

## Installation

```bash
pip install tigrbl-auth-protocol-oidc
# or
uv add tigrbl-auth-protocol-oidc
```

## Usage

```python
from tigrbl_auth_protocol_oidc import OidcProviderRuntime, TenantBrandingRegistry

runtime = OidcProviderRuntime(branding=TenantBrandingRegistry())
```

## Package Boundary

- OpenID Provider metadata and discovery behavior
- ID Token, UserInfo, claims, `acr`, `amr`, session, and logout protocol behavior
- Provider-facing OIDC wire validation below API front-door assembly
- OIDC behavior layered on OAuth protocol foundations

## Related Packages

- [tigrbl-identity-oidc](https://pypi.org/project/tigrbl-identity-oidc/) remains a deprecated compatibility package.
- [tigrbl-auth-protocol-oauth](https://pypi.org/project/tigrbl-auth-protocol-oauth/) owns OAuth protocol behavior.
- [tigrbl-auth-protocol-rp](https://pypi.org/project/tigrbl-auth-protocol-rp/) owns relying-party protocol behavior.

## Governance

This package is part of the SSOT-governed Tigrbl auth package suite. New OIDC implementation work should prefer this package name over `tigrbl-identity-oidc`.
