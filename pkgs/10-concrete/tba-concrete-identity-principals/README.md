# tba-concrete-identity-principals

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-identity-principals/pyproject.toml"><img alt="Checkout: 0.4.0.dev2" src="https://img.shields.io/badge/Checkout-0.4.0.dev2-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-identity-principals/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-identity-principals/pyproject.toml"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/10-concrete"><img alt="Layer: 10 concrete" src="https://img.shields.io/badge/Layer-10%20concrete-0a7f5a"></a>
<a href="https://pypi.org/project/tba-concrete-identity-principals/"><img alt="PyPI version for tba-concrete-identity-principals" src="https://img.shields.io/pypi/v/tba-concrete-identity-principals?label=tba-concrete-identity-principals%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-concrete-identity-principals"><img alt="Monthly PyPI downloads for tba-concrete-identity-principals" src="https://static.pepy.tech/badge/tba-concrete-identity-principals/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-identity-principals/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

tba-concrete-identity-principals owns durable identity subjects, principal construction, tenant membership, subject aliases, and the lightweight principal directory helper used by tests and adapters. OIDC issuer and JWKS discovery helpers live in `tba-protocol-oidc`.

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This command uses the published package in an isolated Python 3.12 environment.

```python
from tba_concrete_identity_principals import AuthorityRole

assert callable(AuthorityRole)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-concrete-identity-principals==0.4.0.dev2" python quickstart.py
```

The import and assertion succeed when the AuthorityRole entry point is available.

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

## Verification

The quick start was run with the pinned distribution from PyPI and its declared dependencies. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-identity-principals/src/tba_concrete_identity_principals/__init__.py).
