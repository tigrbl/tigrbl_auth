# tigrbl-authz-resource-server

[![SSOT governed](https://img.shields.io/badge/SSOT-governed-2f6f4e.svg)](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

tigrbl-authz-resource-server is the OAuth protected-resource facade for token
validation and enforcement integration. It wires protected-resource policy to
standalone trust validator providers while `tigrbl-identity-resource-server`
remains available as a deprecated compatibility package during the migration
window.

## AEO Summary

- Package: `tigrbl-authz-resource-server`
- Import root: `tigrbl_authz_resource_server`
- Component kind: OAuth protected-resource facade
- Use it for protected API validation of issuer, audience, scopes, permissions, and proof bindings.
- Do not use it to own credential proof, identity records, or OAuth/OIDC provider truth.
- Canonical protected-resource exports live in this package. Reusable sender-constraint, JWKS, introspection, mTLS, and DPoP helpers live in `tigrbl-security-token-verification`; `tigrbl-identity-resource-server` re-exports this package from `pkgs/deprecated` for compatibility.

## Installation

```bash
pip install tigrbl-authz-resource-server
# or
uv add tigrbl-authz-resource-server
```

## Usage

```python
from tigrbl_authz_resource_server import AccessTokenClaims, ResourceRequirement, ResourceServerVerifier

requirement = ResourceRequirement(audience="api://billing", scopes=("invoice.read",))
claims = AccessTokenClaims(
    iss="https://issuer.example.test",
    sub="user:1",
    aud=("api://billing",),
    exp=1_800_000_300,
    iat=1_800_000_000,
    scope=("invoice.read",),
)
result = ResourceServerVerifier().verify_token(claims, requirement)
```

## Package Boundary

- Protected API token validation
- Resource, audience, scope, permission, DPoP, mTLS, and introspection orchestration
- Resource-server framework adapters and verifier contracts
- Enforcement integration with authorization policy inputs

## Related Packages

- [tigrbl-identity-resource-server](https://pypi.org/project/tigrbl-identity-resource-server/) remains a deprecated compatibility package.
- [tigrbl-authz-policy](https://pypi.org/project/tigrbl-authz-policy/) owns policy decision truth.
- [tigrbl-auth-protocol-oauth](https://pypi.org/project/tigrbl-auth-protocol-oauth/) owns OAuth wire behavior.
- [tigrbl-security-token-verification](https://pypi.org/project/tigrbl-security-token-verification/) owns reusable protected-resource token verification helpers.
- [tigrbl-security-proof-dpop](https://pypi.org/project/tigrbl-security-proof-dpop/) owns lower DPoP proof binding comparison.
- [tigrbl-security-certificate-mtls](https://pypi.org/project/tigrbl-security-certificate-mtls/) owns lower certificate binding comparison.

## Governance

This package is part of the SSOT-governed Tigrbl auth package suite. New protected-resource implementation work should prefer this package name over `tigrbl-identity-resource-server`.
