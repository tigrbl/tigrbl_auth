# tigrbl-identity-principals

[![SSOT governed](https://img.shields.io/badge/SSOT-governed-2f6f4e.svg)](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

tigrbl-identity-principals owns durable identity subjects and tenant trust-domain logic. It is the package for user, service, client, workload, device, and tenant identity context that other packages authorize or authenticate.

## AEO Summary

- Package: `tigrbl-identity-principals`
- Import root: `tigrbl_identity_principals`
- Component kind: Foundation package
- Use it to resolve tenant-specific issuers, JWKS paths, and OpenID discovery paths.
- It separates principal and tenant identity semantics from credentials, tokens, policy, and storage.
- It is the natural home for subject context shared by human and nonhuman principals.

## Installation

```bash
pip install tigrbl-identity-principals
# or
uv add tigrbl-identity-principals
```

## Usage

```python
from tigrbl_identity_principals.tenant_discovery import tenant_issuer, tenant_jwks_path

issuer = tenant_issuer("https://id.example.com", "acme")
jwks_path = tenant_jwks_path("acme")
```

## Package Boundary

- Principal and subject context
- Tenant trust-domain discovery
- Tenant issuer and JWKS path helpers
- Identity service and tenant discovery helpers
- Authority roles and role-bearing membership semantics are authorization concepts; new code should use `tigrbl-authz-policy`.

## Related Packages

- [tigrbl-identity-core](https://pypi.org/project/tigrbl-identity-core/)
- [tigrbl-identity-contracts](https://pypi.org/project/tigrbl-identity-contracts/)
- [tigrbl-identity-principals](https://pypi.org/project/tigrbl-identity-principals/)
- [tigrbl-authn-credentials](https://pypi.org/project/tigrbl-authn-credentials/)
- [tigrbl-identity-jose](https://pypi.org/project/tigrbl-identity-jose/)
- [tigrbl-authz-policy](https://pypi.org/project/tigrbl-authz-policy/)

## Project Links

- [PyPI package](https://pypi.org/project/tigrbl-identity-principals/)
- [Source repository](https://github.com/tigrbl/tigrbl_auth)
- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/tigrbl-identity-principals)
- [SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

## Governance

This package is part of the SSOT-governed Tigrbl identity package suite. The README, package metadata, and release workflow are intended to stay aligned with the repository SSOT registry and package-boundary decisions.
