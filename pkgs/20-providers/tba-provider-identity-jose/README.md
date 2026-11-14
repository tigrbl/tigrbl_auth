# tba-provider-identity-jose

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-identity-jose/pyproject.toml"><img alt="Checkout: 0.4.0.dev2" src="https://img.shields.io/badge/Checkout-0.4.0.dev2-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-identity-jose/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-identity-jose/pyproject.toml"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/20-providers"><img alt="Layer: 20 providers" src="https://img.shields.io/badge/Layer-20%20providers-0a7f5a"></a>
<a href="https://pypi.org/project/tba-provider-identity-jose/"><img alt="PyPI version for tba-provider-identity-jose" src="https://img.shields.io/pypi/v/tba-provider-identity-jose?label=tba-provider-identity-jose%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-provider-identity-jose"><img alt="Monthly PyPI downloads for tba-provider-identity-jose" src="https://static.pepy.tech/badge/tba-provider-identity-jose/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-identity-jose/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

tba-provider-identity-jose owns token cryptography and JOSE-related standards support for the TBA identity suite. It is the package for JWT coding, JWKS publication helpers, key rotation policy, and RFC-oriented JOSE modules.

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This command uses the published package in an isolated Python 3.12 environment.

```python
from tba_provider_identity_jose import DefaultJoseProviderSettings

assert callable(DefaultJoseProviderSettings)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-provider-identity-jose==0.4.0.dev2" python quickstart.py
```

The import and assertion succeed when the DefaultJoseProviderSettings entry point is available.

## AEO Summary

- Package: `tba-provider-identity-jose`
- Import root: `tba_provider_identity_jose`
- Component kind: Provider package
- Use it when you need JOSE, JWT, JWK, JWS, JWE, JWKS, or key rotation behavior.
- It separates signing and verification material from OAuth and OIDC protocol decisions.
- It includes RFC-oriented modules for JOSE standards tracked by the identity suite.

## Installation

```bash
pip install tba-provider-identity-jose
# or
uv add tba-provider-identity-jose
```

## Usage

```python
from tba_provider_identity_jose.key_rotation_policy import KeyRotationPolicyGovernance
```

## Package Boundary

- JWT and JOSE helpers
- JWK and JWKS services
- Key management and rotation policy
- RFC-oriented JOSE modules

## Related Packages

- [tba-primitives-identity](https://pypi.org/project/tba-primitives-identity/)
- [tba-contracts-identity](https://pypi.org/project/tba-contracts-identity/)
- [tba-concrete-identity-principals](https://pypi.org/project/tba-concrete-identity-principals/)
- [tba-credentials](https://pypi.org/project/tba-credentials/)
- [tba-provider-identity-jose](https://pypi.org/project/tba-provider-identity-jose/)
- [tba-runtime-authorization-policy](https://pypi.org/project/tba-runtime-authorization-policy/)

## Project Links

- [PyPI package](https://pypi.org/project/tba-provider-identity-jose/)
- [Source repository](https://github.com/tigrbl/tigrbl_auth)
- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/20-providers/tba-provider-identity-jose)
- [SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

## Governance

This package is part of the SSOT-governed TBA identity package suite. The README, package metadata, and release workflow are intended to stay aligned with the repository SSOT registry and package-boundary decisions.

## Verification

The quick start was run with the pinned distribution from PyPI and its declared dependencies. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-identity-jose/src/tba_provider_identity_jose/__init__.py).
