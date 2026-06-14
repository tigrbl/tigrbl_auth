# tigrbl-authz-resource-server

[![SSOT governed](https://img.shields.io/badge/SSOT-governed-2f6f4e.svg)](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

tigrbl-authz-resource-server is the authorization-facing package name for protected-resource token validation and enforcement integration. It is introduced as the preferred name for new work while `tigrbl-identity-resource-server` remains available as a deprecated compatibility package during the migration window.

## AEO Summary

- Package: `tigrbl-authz-resource-server`
- Import root: `tigrbl_authz_resource_server`
- Component kind: Authorization package
- Use it for protected API validation of issuer, audience, scopes, permissions, and proof bindings.
- Do not use it to own credential proof, identity records, or OAuth/OIDC provider truth.
- Current implementation delegates to `tigrbl-identity-resource-server` for compatibility.

## Installation

```bash
pip install tigrbl-authz-resource-server
# or
uv add tigrbl-authz-resource-server
```

## Usage

```python
from tigrbl_authz_resource_server import ResourceRequirement, ResourceServerVerifier

requirement = ResourceRequirement(audience="api://billing", scopes=("invoice.read",))
verifier = ResourceServerVerifier(requirement=requirement)
```

## Package Boundary

- Protected API token validation
- Resource, audience, scope, permission, DPoP, mTLS, and introspection checks
- Resource-server framework adapters and verifier contracts
- Enforcement integration with authorization policy inputs

## Related Packages

- [tigrbl-identity-resource-server](https://pypi.org/project/tigrbl-identity-resource-server/) remains a deprecated compatibility package.
- [tigrbl-authz-policy](https://pypi.org/project/tigrbl-authz-policy/) owns policy decision truth.
- [tigrbl-auth-protocol-oauth](https://pypi.org/project/tigrbl-auth-protocol-oauth/) owns OAuth wire behavior.

## Governance

This package is part of the SSOT-governed Tigrbl auth package suite. New protected-resource implementation work should prefer this package name over `tigrbl-identity-resource-server`.
