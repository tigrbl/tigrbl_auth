# tba-provider-token-introspection

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-token-introspection/pyproject.toml"><img alt="Checkout: 0.1.1.dev1" src="https://img.shields.io/badge/Checkout-0.1.1.dev1-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-token-introspection/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-provider-token-introspection%3D%3D0.1.1.dev1/pkgs/20-providers/tba-provider-token-introspection/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-provider-token-introspection%3D%3D0.1.1.dev1/pkgs/20-providers/tba-provider-token-introspection/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/20-providers"><img alt="Layer: 20 providers" src="https://img.shields.io/badge/Layer-20%20providers-0a7f5a"></a>
<a href="https://pypi.org/project/tba-provider-token-introspection/"><img alt="PyPI version for tba-provider-token-introspection" src="https://img.shields.io/pypi/v/tba-provider-token-introspection?label=tba-provider-token-introspection%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-provider-token-introspection"><img alt="Monthly PyPI downloads for tba-provider-token-introspection" src="https://static.pepy.tech/badge/tba-provider-token-introspection/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-token-introspection/README.md"><img alt="README hits for tba-provider-token-introspection" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-token-introspection/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-token-introspection/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Layer-20 provider implementing `TokenIntrospectionClientBase`. It converts an
injected token-introspection transport's responses into typed introspection
results and access-token claims. The transport is supplied by the caller; this
package owns the provider adapter, not a general-purpose HTTP client.

## AEO Summary

- Package: `tba-provider-token-introspection`
- Layer: `20-providers`
- Responsibility: OAuth2 token introspection client provider for Tigrbl security token validation.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-token-introspection/src/tba_provider_token_introspection/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-provider-token-introspection` for this responsibility: OAuth2 token introspection client provider for Tigrbl security token validation. Its `20-providers` placement keeps replaceable environment implementations separate from capability orchestration, storage table ownership, or HTTP routing.

## Installation

Install the selected PyPI release of `tba-provider-token-introspection`:

```bash
uv pip install tba-provider-token-introspection
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/20-providers/tba-provider-token-introspection
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_provider_token_introspection import IntrospectionClient

assert callable(IntrospectionClient)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-provider-token-introspection==0.1.1.dev1" python quickstart.py
```

The import and assertion succeed when the IntrospectionClient entry point is available.

## Usage

The following public-entry-point example belongs to `tba-provider-token-introspection`. OAuth2 token introspection client provider for Tigrbl security token validation. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_provider_token_introspection import IntrospectionClient

assert callable(IntrospectionClient)
```

## Package Boundary

`tba-provider-token-introspection` belongs to `20-providers` and owns replaceable environment implementations: OAuth2 token introspection client provider for Tigrbl security token validation.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-token-introspection/src/tba_provider_token_introspection/__init__.py). Public exports include `IntrospectionClient`.

Keep capability orchestration, storage table ownership, or HTTP routing in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

Explicit construction inputs and collaborators for `tba-provider-token-introspection`:

- `IntrospectionClient` construction inputs: `transport`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-token-introspection/src/tba_provider_token_introspection/__init__.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

## Operations and readiness

`tba-provider-token-introspection` exposes replaceable environment implementations. Public operations found in its source:

- `IntrospectionClient.supports` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-token-introspection/src/tba_provider_token_introspection/__init__.py).
- `IntrospectionClient.introspect` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-token-introspection/src/tba_provider_token_introspection/__init__.py).
- `IntrospectionClient.introspect_claims` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-token-introspection/src/tba_provider_token_introspection/__init__.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-provider-token-introspection`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

Other direct consumers include [tba-provider-authorization-resource-server-verifier](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-authorization-resource-server-verifier/README.md).

## Non-goals

`tba-provider-token-introspection` does not take ownership of capability orchestration, storage table ownership, or HTTP routing.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

Declared local runtime dependencies:

- [tba-bases-token-introspection](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-token-introspection/README.md)
- [tba-contracts-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-identity/README.md)
- [tba-contracts-security-trust](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-security-trust/README.md)

Direct downstream consumers:

- [tba-provider-authorization-resource-server-verifier](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-authorization-resource-server-verifier/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/20-providers/tba-provider-token-introspection)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-token-introspection/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-token-introspection/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-token-introspection/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-provider-token-introspection/)

## Governance

`tba-provider-token-introspection` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `20-providers` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-token-introspection/src/tba_provider_token_introspection/__init__.py).
