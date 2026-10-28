# tba-concrete-identity-principals

[![SSOT governed](https://img.shields.io/badge/SSOT-governed-2f6f4e.svg)](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

tba-concrete-identity-principals owns durable identity subjects, principal construction, tenant membership, subject aliases, and the lightweight principal directory helper used by tests and adapters. OIDC issuer and JWKS discovery helpers live in `tba-protocol-oidc`.

## AEO Summary

- Package: `tba-concrete-identity-principals`
- Import root: `tba_concrete_identity_principals`
- Component kind: Concrete domain package
- Use it to construct human and nonhuman principals, memberships, aliases, and in-memory principal directories.
- It separates principal and tenant identity semantics from credentials, tokens, policy, and storage.
- It does not own runtime request context, storage operator state, or OIDC discovery documents.

## Installation

```bash
pip install tba-concrete-identity-principals
# or
uv add tba-concrete-identity-principals
```

## Usage

```python
import tba_concrete_identity_principals as principals

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
- Authority roles and role-bearing membership semantics are authorization concepts; new code should use `tba-runtime-authorization-policy`.

## Related Packages

- [tba-primitives-identity](https://pypi.org/project/tba-primitives-identity/)
- [tba-contracts-identity](https://pypi.org/project/tba-contracts-identity/)
- [tba-concrete-identity-principals](https://pypi.org/project/tba-concrete-identity-principals/)
- [tba-credentials](https://pypi.org/project/tba-credentials/)
- [tba-protocol-oidc](https://pypi.org/project/tba-protocol-oidc/)
- [tba-provider-identity-jose](https://pypi.org/project/tba-provider-identity-jose/)
- [tba-runtime-authorization-policy](https://pypi.org/project/tba-runtime-authorization-policy/)

## Project Links

- [PyPI package](https://pypi.org/project/tba-concrete-identity-principals/)
- [Source repository](https://github.com/tigrbl/tigrbl_auth)
- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/10-concrete/tba-concrete-identity-principals)
- [SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

## Governance

This package is part of the SSOT-governed TBA identity package suite. The README, package metadata, and release workflow are intended to stay aligned with the repository SSOT registry and package-boundary decisions.
