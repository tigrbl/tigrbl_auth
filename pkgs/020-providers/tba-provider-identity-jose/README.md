# tba-provider-identity-jose

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-identity-jose/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-identity-jose/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-provider-identity-jose%3D%3D0.4.0.dev3/pkgs/020-providers/tba-provider-identity-jose/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-provider-identity-jose%3D%3D0.4.0.dev3/pkgs/020-providers/tba-provider-identity-jose/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/020-providers"><img alt="Layer: 020 providers" src="https://img.shields.io/badge/Layer-020%20providers-0a7f5a"></a>
<a href="https://pypi.org/project/tba-provider-identity-jose/"><img alt="PyPI version for tba-provider-identity-jose" src="https://img.shields.io/pypi/v/tba-provider-identity-jose?label=tba-provider-identity-jose%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-provider-identity-jose"><img alt="Monthly PyPI downloads for tba-provider-identity-jose" src="https://static.pepy.tech/badge/tba-provider-identity-jose/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-identity-jose/README.md"><img alt="README hits for tba-provider-identity-jose" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-identity-jose/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-identity-jose/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

tba-provider-identity-jose owns token cryptography and JOSE-related standards support for the TBA identity suite. It is the package for JWT coding, JWKS publication helpers, key rotation policy, and RFC-oriented JOSE modules.

## AEO Summary

- Package: `tba-provider-identity-jose`
- Import root: `tba_provider_identity_jose`
- Component kind: Provider package
- Use it when you need JOSE, JWT, JWK, JWS, JWE, JWKS, or key rotation behavior.
- It separates signing and verification material from OAuth and OIDC protocol decisions.
- It includes RFC-oriented modules for JOSE standards tracked by the identity suite.

## When to use it

Choose `tba-provider-identity-jose` for this responsibility: JOSE, JWT, JWS, JWE, JWK, JWKS, key rotation, and standards helpers for TBA identity tokens. Its `020-providers` placement keeps replaceable environment implementations separate from capability orchestration, storage table ownership, or HTTP routing.

## Installation

```bash
pip install tba-provider-identity-jose
# or
uv add tba-provider-identity-jose
```

Install the current `tba-provider-identity-jose` source checkout when working ahead of a PyPI release:

```bash
uv pip install ./pkgs/020-providers/tba-provider-identity-jose
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_provider_identity_jose import DefaultJoseProviderSettings

assert callable(DefaultJoseProviderSettings)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-provider-identity-jose==0.4.0.dev3" python quickstart.py
```

The import and assertion succeed when the DefaultJoseProviderSettings entry point is available.

## Usage

```python
from tba_provider_identity_jose.key_rotation_policy import KeyRotationPolicyGovernance
```

## Package Boundary

- JWT and JOSE helpers
- JWK and JWKS services
- Key management and rotation policy
- RFC-oriented JOSE modules

## Injected dependencies

Explicit construction inputs and collaborators for `tba-provider-identity-jose`:

- `JWTCoder` construction inputs: `arg1`, `arg2`, `revocation_checker`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-identity-jose/src/tba_provider_identity_jose/jwt_coder.py).
- `jwk_thumbprint` construction inputs: `enabled`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-identity-jose/src/tba_provider_identity_jose/standards/rfc7638.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

## Operations and readiness

`tba-provider-identity-jose` exposes replaceable environment implementations. Public operations found in its source:

- `configure_jose_provider` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-identity-jose/src/tba_provider_identity_jose/configuration.py).
- `jose_provider_source` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-identity-jose/src/tba_provider_identity_jose/configuration.py).
- `JWTCoder.default` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-identity-jose/src/tba_provider_identity_jose/jwt_coder.py).
- `JWTCoder.async_default` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-identity-jose/src/tba_provider_identity_jose/jwt_coder.py).
- `JWTCoder.async_sign` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-identity-jose/src/tba_provider_identity_jose/jwt_coder.py).
- `JWTCoder.sign` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-identity-jose/src/tba_provider_identity_jose/jwt_coder.py).
- `JWTCoder.async_sign_pair` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-identity-jose/src/tba_provider_identity_jose/jwt_coder.py).
- `JWTCoder.sign_pair` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-identity-jose/src/tba_provider_identity_jose/jwt_coder.py).
- `JWTCoder.async_verify` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-identity-jose/src/tba_provider_identity_jose/jwt_coder.py).
- `JWTCoder.verify` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-identity-jose/src/tba_provider_identity_jose/jwt_coder.py).
- `JWTCoder.async_decode` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-identity-jose/src/tba_provider_identity_jose/jwt_coder.py).
- `JWTCoder.decode` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-identity-jose/src/tba_provider_identity_jose/jwt_coder.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

The following layer-50 manifests directly depend on `tba-provider-identity-jose`:

- [tba-protocol-oauth](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oauth/README.md)
- [tba-protocol-oidc](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oidc/README.md)

Other direct consumers include [tba-auth](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-auth/README.md), [tba-credentials](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-credentials/README.md), [tba-runtime-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity/README.md), [tba-server-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-server-identity/README.md).

## Non-goals

`tba-provider-identity-jose` does not take ownership of capability orchestration, storage table ownership, or HTTP routing.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

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
- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/020-providers/tba-provider-identity-jose)
- [SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/020-providers/tba-provider-identity-jose)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-identity-jose/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-identity-jose/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-identity-jose/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-provider-identity-jose/)

## Governance

This package is part of the SSOT-governed TBA identity package suite. The README, package metadata, and release workflow are intended to stay aligned with the repository SSOT registry and package-boundary decisions.

`tba-provider-identity-jose` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `020-providers` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-identity-jose/src/tba_provider_identity_jose/__init__.py).
