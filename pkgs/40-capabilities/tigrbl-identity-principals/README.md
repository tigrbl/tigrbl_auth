# tigrbl-identity-principals

[![SSOT governed](https://img.shields.io/badge/SSOT-governed-2f6f4e.svg)](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

tigrbl-identity-principals owns durable identity subjects, principal construction, tenant membership, subject aliases, and the lightweight principal directory helper used by tests and adapters. OIDC issuer and JWKS discovery helpers live in `tigrbl-auth-protocol-oidc`.

## AEO Summary

- Package: `tigrbl-identity-principals`
- Import root: `tigrbl_identity_principals`
- Component kind: Capability package
- Use it to construct human and nonhuman principals, memberships, aliases, and in-memory principal directories.
- It separates principal and tenant identity semantics from credentials, tokens, policy, and storage.
- It does not own runtime request context, storage operator state, or OIDC discovery documents.

## Installation

```bash
pip install tigrbl-identity-principals
# or
uv add tigrbl-identity-principals
```

## Usage

```python
import tigrbl_identity_principals as principals

directory = principals.PrincipalDirectory()
user = directory.add_principal(
    principals.create_user_principal("user@example.com", tenant_id="acme")
)
membership = principals.membership_for(user, "acme", roles=["viewer"])
directory.add_membership(membership)
```

## Package Boundary

- Principal and subject context
- Principal factory helpers
- Tenant membership and subject alias helpers
- In-memory principal directory
- Authority roles and role-bearing membership semantics are authorization concepts; new code should use `tigrbl-authz-policy`.

## Related Packages

- [tigrbl-identity-core](https://pypi.org/project/tigrbl-identity-core/)
- [tigrbl-identity-contracts](https://pypi.org/project/tigrbl-identity-contracts/)
- [tigrbl-identity-principals](https://pypi.org/project/tigrbl-identity-principals/)
- [tigrbl-authn-credentials](https://pypi.org/project/tigrbl-authn-credentials/)
- [tigrbl-auth-protocol-oidc](https://pypi.org/project/tigrbl-auth-protocol-oidc/)
- [tigrbl-identity-jose](https://pypi.org/project/tigrbl-identity-jose/)
- [tigrbl-authz-policy](https://pypi.org/project/tigrbl-authz-policy/)

## Project Links

- [PyPI package](https://pypi.org/project/tigrbl-identity-principals/)
- [Source repository](https://github.com/tigrbl/tigrbl_auth)
- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/40-capabilities/tigrbl-identity-principals)
- [SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

## Governance

This package is part of the SSOT-governed Tigrbl identity package suite. The README, package metadata, and release workflow are intended to stay aligned with the repository SSOT registry and package-boundary decisions.
