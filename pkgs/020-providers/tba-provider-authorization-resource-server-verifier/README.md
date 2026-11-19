# tba-provider-authorization-resource-server-verifier

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-authorization-resource-server-verifier/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-authorization-resource-server-verifier/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-provider-authorization-resource-server-verifier%3D%3D0.4.0.dev3/pkgs/020-providers/tba-provider-authorization-resource-server-verifier/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-provider-authorization-resource-server-verifier%3D%3D0.4.0.dev3/pkgs/020-providers/tba-provider-authorization-resource-server-verifier/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/020-providers"><img alt="Layer: 020 providers" src="https://img.shields.io/badge/Layer-020%20providers-0a7f5a"></a>
<a href="https://pypi.org/project/tba-provider-authorization-resource-server-verifier/"><img alt="PyPI version for tba-provider-authorization-resource-server-verifier" src="https://img.shields.io/pypi/v/tba-provider-authorization-resource-server-verifier?label=tba-provider-authorization-resource-server-verifier%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-provider-authorization-resource-server-verifier"><img alt="Monthly PyPI downloads for tba-provider-authorization-resource-server-verifier" src="https://static.pepy.tech/badge/tba-provider-authorization-resource-server-verifier/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-authorization-resource-server-verifier/README.md"><img alt="README hits for tba-provider-authorization-resource-server-verifier" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-authorization-resource-server-verifier/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-authorization-resource-server-verifier/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Standalone 30-layer provider implementing the protected-resource verifier port.

## AEO Summary

- Package: `tba-provider-authorization-resource-server-verifier`
- Layer: `020-providers`
- Responsibility: Protected-resource verifier provider for TBAorization resource servers.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-authorization-resource-server-verifier/src/tba_provider_authorization_resource_server_verifier/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-provider-authorization-resource-server-verifier` for this responsibility: Protected-resource verifier provider for TBAorization resource servers. Its `020-providers` placement keeps replaceable environment implementations separate from capability orchestration, storage table ownership, or HTTP routing.

## Installation

Install the selected PyPI release of `tba-provider-authorization-resource-server-verifier`:

```bash
uv pip install tba-provider-authorization-resource-server-verifier
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/020-providers/tba-provider-authorization-resource-server-verifier
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_provider_authorization_resource_server_verifier import bearer_token_from_authorization

assert callable(bearer_token_from_authorization)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-provider-authorization-resource-server-verifier==0.4.0.dev3" python quickstart.py
```

The import and assertion succeed when the bearer_token_from_authorization entry point is available.

## Usage

The following public-entry-point example belongs to `tba-provider-authorization-resource-server-verifier`. Protected-resource verifier provider for TBAorization resource servers. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_provider_authorization_resource_server_verifier import bearer_token_from_authorization

assert callable(bearer_token_from_authorization)
```

## Package Boundary

`tba-provider-authorization-resource-server-verifier` belongs to `020-providers` and owns replaceable environment implementations: Protected-resource verifier provider for TBAorization resource servers.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-authorization-resource-server-verifier/src/tba_provider_authorization_resource_server_verifier/__init__.py). Public exports include `AccessTokenClaims`, `DPoPBinding`, `FrameworkRequest`, `IntrospectionClient`, `IntrospectionTransport`, `JWKSCache`, `MTLSBinding`, `PolicyHook`, `ResourceRequirement`, `ResourceServerError`, `ResourceServerVerifier`, `TokenValidationError`.

Keep capability orchestration, storage table ownership, or HTTP routing in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

Explicit construction inputs and collaborators for `tba-provider-authorization-resource-server-verifier`:

- `ResourceServerVerifier` construction inputs: `jwks_cache`, `introspection_client`, `policy_hook`, `now`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-authorization-resource-server-verifier/src/tba_provider_authorization_resource_server_verifier/__init__.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

## Operations and readiness

`tba-provider-authorization-resource-server-verifier` exposes replaceable environment implementations. Public operations found in its source:

- `bearer_token_from_authorization` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-authorization-resource-server-verifier/src/tba_provider_authorization_resource_server_verifier/__init__.py).
- `ResourceServerVerifier.verify_claims` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-authorization-resource-server-verifier/src/tba_provider_authorization_resource_server_verifier/__init__.py).
- `ResourceServerVerifier.verify_token` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-authorization-resource-server-verifier/src/tba_provider_authorization_resource_server_verifier/__init__.py).
- `verify_framework_request` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-authorization-resource-server-verifier/src/tba_provider_authorization_resource_server_verifier/__init__.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

The following layer-50 manifests directly depend on `tba-provider-authorization-resource-server-verifier`:

- [tba-protocol-oauth-protected-resource](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oauth-protected-resource/README.md)

## Non-goals

`tba-provider-authorization-resource-server-verifier` does not take ownership of capability orchestration, storage table ownership, or HTTP routing.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

Declared local runtime dependencies:

- [tba-bases-resource-server](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-resource-server/README.md)
- [tba-contracts-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-identity/README.md)
- [tba-contracts-security-trust](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-security-trust/README.md)
- [tba-provider-security-dpop-cnf-binding-validator](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-security-dpop-cnf-binding-validator/README.md)
- [tba-provider-security-mtls-cnf-binding-validator](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-security-mtls-cnf-binding-validator/README.md)
- [tba-provider-security-token-jwks-cache](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-security-token-jwks-cache/README.md)
- [tba-provider-token-introspection](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-token-introspection/README.md)

Direct downstream consumers:

- [tba-protocol-oauth-protected-resource](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oauth-protected-resource/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/020-providers/tba-provider-authorization-resource-server-verifier)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-authorization-resource-server-verifier/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-authorization-resource-server-verifier/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-authorization-resource-server-verifier/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-provider-authorization-resource-server-verifier/)

## Governance

`tba-provider-authorization-resource-server-verifier` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `020-providers` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-authorization-resource-server-verifier/src/tba_provider_authorization_resource_server_verifier/__init__.py).
