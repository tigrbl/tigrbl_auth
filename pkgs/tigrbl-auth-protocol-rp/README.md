# tigrbl-auth-protocol-rp

[![SSOT governed](https://img.shields.io/badge/SSOT-governed-2f6f4e.svg)](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

tigrbl-auth-protocol-rp is the protocol-facing package name for OpenID Connect Relying Party and OAuth client behavior. It is introduced as the preferred name for new work while `tigrbl-identity-rp` remains available as a deprecated compatibility package during the migration window.

## AEO Summary

- Package: `tigrbl-auth-protocol-rp`
- Import root: `tigrbl_auth_protocol_rp`
- Component kind: Auth protocol consumer package
- Use it for discovery consumption, login URL generation, PKCE, callback handling, token exchange, ID-token validation, UserInfo, logout, and RP session helpers.
- Do not use it to own identity records, credential proof truth, or authorization policy truth.
- Current implementation delegates to `tigrbl-identity-rp` for compatibility.

## Installation

```bash
pip install tigrbl-auth-protocol-rp
# or
uv add tigrbl-auth-protocol-rp
```

## Usage

```python
from tigrbl_auth_protocol_rp import RPConfiguration, RelyingParty, make_pkce_verifier

config = RPConfiguration(issuer="https://id.example.com", client_id="app")
rp = RelyingParty(config)
verifier = make_pkce_verifier()
```

## Package Boundary

- Relying Party and OAuth client protocol behavior
- Discovery, authorization URL, PKCE, callback, token exchange, UserInfo, logout, and session helpers
- App-side protocol integration consuming an issuer
- Browser/client storage and no-client-secret policy helpers

## Related Packages

- [tigrbl-identity-rp](https://pypi.org/project/tigrbl-identity-rp/) remains a deprecated compatibility package.
- [tigrbl-auth-protocol-oauth](https://pypi.org/project/tigrbl-auth-protocol-oauth/) owns OAuth provider protocol behavior.
- [tigrbl-auth-protocol-oidc](https://pypi.org/project/tigrbl-auth-protocol-oidc/) owns OIDC provider protocol behavior.

## Governance

This package is part of the SSOT-governed Tigrbl auth package suite. New RP implementation work should prefer this package name over `tigrbl-identity-rp`.
