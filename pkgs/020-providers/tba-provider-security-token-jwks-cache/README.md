# tba-provider-security-token-jwks-cache

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-security-token-jwks-cache/pyproject.toml"><img alt="Checkout: 0.1.1.dev1" src="https://img.shields.io/badge/Checkout-0.1.1.dev1-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-security-token-jwks-cache/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-provider-security-token-jwks-cache%3D%3D0.1.1.dev1/pkgs/020-providers/tba-provider-security-token-jwks-cache/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-provider-security-token-jwks-cache%3D%3D0.1.1.dev1/pkgs/020-providers/tba-provider-security-token-jwks-cache/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/020-providers"><img alt="Layer: 020 providers" src="https://img.shields.io/badge/Layer-020%20providers-0a7f5a"></a>
<a href="https://pypi.org/project/tba-provider-security-token-jwks-cache/"><img alt="PyPI version for tba-provider-security-token-jwks-cache" src="https://img.shields.io/pypi/v/tba-provider-security-token-jwks-cache?label=tba-provider-security-token-jwks-cache%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-provider-security-token-jwks-cache"><img alt="Monthly PyPI downloads for tba-provider-security-token-jwks-cache" src="https://static.pepy.tech/badge/tba-provider-security-token-jwks-cache/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-security-token-jwks-cache/README.md"><img alt="README hits for tba-provider-security-token-jwks-cache" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-security-token-jwks-cache/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-security-token-jwks-cache/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Standalone 30-layer provider implementing `VerificationKeyCacheBase`.

## AEO Summary

- Package: `tba-provider-security-token-jwks-cache`
- Layer: `020-providers`
- Responsibility: JWKS-backed verification key cache provider for Tigrbl security token validation.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-security-token-jwks-cache/src/tba_provider_security_token_jwks_cache/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-provider-security-token-jwks-cache` for this responsibility: JWKS-backed verification key cache provider for Tigrbl security token validation. Its `020-providers` placement keeps replaceable environment implementations separate from capability orchestration, storage table ownership, or HTTP routing.

## Installation

Install the selected PyPI release of `tba-provider-security-token-jwks-cache`:

```bash
uv pip install tba-provider-security-token-jwks-cache
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/020-providers/tba-provider-security-token-jwks-cache
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_provider_security_token_jwks_cache import JWKSCache

assert callable(JWKSCache)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-provider-security-token-jwks-cache==0.1.1.dev1" python quickstart.py
```

The import and assertion succeed when the JWKSCache entry point is available.

## Usage

The following public-entry-point example belongs to `tba-provider-security-token-jwks-cache`. JWKS-backed verification key cache provider for Tigrbl security token validation. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_provider_security_token_jwks_cache import JWKSCache

assert callable(JWKSCache)
```

## Package Boundary

`tba-provider-security-token-jwks-cache` belongs to `020-providers` and owns replaceable environment implementations: JWKS-backed verification key cache provider for Tigrbl security token validation.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-security-token-jwks-cache/src/tba_provider_security_token_jwks_cache/__init__.py). Public exports include `JWKSCache`.

Keep capability orchestration, storage table ownership, or HTTP routing in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

The [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-security-token-jwks-cache/src/tba_provider_security_token_jwks_cache/__init__.py) for `tba-provider-security-token-jwks-cache` does not declare an explicit service-constructor or keyword-only factory hook in the inspected source. Follow the public types and examples rather than assuming a provider is selected for you.

Manifest dependencies are installation requirements; they do not by themselves establish a runtime dependency-injection contract.

## Operations and readiness

`tba-provider-security-token-jwks-cache` exposes replaceable environment implementations. Public operations found in its source:

- `JWKSCache.supports` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-security-token-jwks-cache/src/tba_provider_security_token_jwks_cache/__init__.py).
- `JWKSCache.keys` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-security-token-jwks-cache/src/tba_provider_security_token_jwks_cache/__init__.py).
- `JWKSCache.put` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-security-token-jwks-cache/src/tba_provider_security_token_jwks_cache/__init__.py).
- `JWKSCache.put_many` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-security-token-jwks-cache/src/tba_provider_security_token_jwks_cache/__init__.py).
- `JWKSCache.put_jwks` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-security-token-jwks-cache/src/tba_provider_security_token_jwks_cache/__init__.py).
- `JWKSCache.get` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-security-token-jwks-cache/src/tba_provider_security_token_jwks_cache/__init__.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-provider-security-token-jwks-cache`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

Other direct consumers include [tba-provider-authorization-resource-server-verifier](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-authorization-resource-server-verifier/README.md).

## Non-goals

`tba-provider-security-token-jwks-cache` does not take ownership of capability orchestration, storage table ownership, or HTTP routing.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

Declared local runtime dependencies:

- [tba-bases-token-introspection](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-token-introspection/README.md)
- [tba-contracts-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-identity/README.md)
- [tba-contracts-security-trust](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-security-trust/README.md)

Direct downstream consumers:

- [tba-provider-authorization-resource-server-verifier](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-authorization-resource-server-verifier/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/020-providers/tba-provider-security-token-jwks-cache)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-security-token-jwks-cache/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-security-token-jwks-cache/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-security-token-jwks-cache/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-provider-security-token-jwks-cache/)

## Governance

`tba-provider-security-token-jwks-cache` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `020-providers` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-security-token-jwks-cache/src/tba_provider_security_token_jwks_cache/__init__.py).
