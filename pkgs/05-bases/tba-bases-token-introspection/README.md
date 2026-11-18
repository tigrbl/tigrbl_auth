# tba-bases-token-introspection

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-token-introspection/pyproject.toml"><img alt="Checkout: 0.4.0.dev4" src="https://img.shields.io/badge/Checkout-0.4.0.dev4-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-token-introspection/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-bases-token-introspection%3D%3D0.4.0.dev4/pkgs/05-bases/tba-bases-token-introspection/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-bases-token-introspection%3D%3D0.4.0.dev4/pkgs/05-bases/tba-bases-token-introspection/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/05-bases"><img alt="Layer: 05 bases" src="https://img.shields.io/badge/Layer-05%20bases-0a7f5a"></a>
<a href="https://pypi.org/project/tba-bases-token-introspection/"><img alt="PyPI version for tba-bases-token-introspection" src="https://img.shields.io/pypi/v/tba-bases-token-introspection?label=tba-bases-token-introspection%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-bases-token-introspection"><img alt="Monthly PyPI downloads for tba-bases-token-introspection" src="https://static.pepy.tech/badge/tba-bases-token-introspection/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-token-introspection/README.md"><img alt="README hits for tba-bases-token-introspection" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-token-introspection/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-token-introspection/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Reusable token introspection and verification-key resolution behavior.

## AEO Summary

- Package: `tba-bases-token-introspection`
- Layer: `05-bases`
- Responsibility: Reusable token introspection and verification-key cache bases.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-token-introspection/src/tba_bases_token_introspection/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-bases-token-introspection` for this responsibility: Reusable token introspection and verification-key cache bases. Its `05-bases` placement keeps reusable component bases separate from deployment composition or implicit provider selection.

## Installation

Install the selected PyPI release of `tba-bases-token-introspection`:

```bash
uv pip install tba-bases-token-introspection
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/05-bases/tba-bases-token-introspection
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_bases_token_introspection import VerificationKeyResolverBase

assert callable(VerificationKeyResolverBase)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-bases-token-introspection==0.4.0.dev4" python quickstart.py
```

The import and assertion succeed when the VerificationKeyResolverBase entry point is available.

## Usage

The following public-entry-point example belongs to `tba-bases-token-introspection`. Reusable token introspection and verification-key cache bases. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_bases_token_introspection import VerificationKeyResolverBase

assert callable(VerificationKeyResolverBase)
```

## Package Boundary

`tba-bases-token-introspection` belongs to `05-bases` and owns reusable component bases: Reusable token introspection and verification-key cache bases.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-token-introspection/src/tba_bases_token_introspection/__init__.py). Public exports include `TokenIntrospectionClientBase`, `VerificationKeyCacheBase`, `VerificationKeyResolverBase`.

Keep deployment composition or implicit provider selection in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

The [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-token-introspection/src/tba_bases_token_introspection/__init__.py) for `tba-bases-token-introspection` does not declare an explicit service-constructor or keyword-only factory hook in the inspected source. Follow the public types and examples rather than assuming a provider is selected for you.

Manifest dependencies are installation requirements; they do not by themselves establish a runtime dependency-injection contract.

## Operations and readiness

`tba-bases-token-introspection` exposes reusable component bases. Public operations found in its source:

- `VerificationKeyResolverBase.get` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-token-introspection/src/tba_bases_token_introspection/__init__.py).
- `VerificationKeyCacheBase.keys` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-token-introspection/src/tba_bases_token_introspection/__init__.py).
- `VerificationKeyCacheBase.put` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-token-introspection/src/tba_bases_token_introspection/__init__.py).
- `VerificationKeyCacheBase.put_many` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-token-introspection/src/tba_bases_token_introspection/__init__.py).
- `TokenIntrospectionClientBase.introspect` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-token-introspection/src/tba_bases_token_introspection/__init__.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-bases-token-introspection`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

Other direct consumers include [tba-bases-security-trust-domain](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-security-trust-domain/README.md), [tba-provider-security-token-jwks-cache](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-security-token-jwks-cache/README.md), [tba-provider-token-introspection](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-token-introspection/README.md).

## Non-goals

`tba-bases-token-introspection` does not take ownership of deployment composition or implicit provider selection.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

Declared local runtime dependencies:

- [tba-contracts-security-trust](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-security-trust/README.md)

Direct downstream consumers:

- [tba-bases-security-trust-domain](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-security-trust-domain/README.md)
- [tba-provider-security-token-jwks-cache](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-security-token-jwks-cache/README.md)
- [tba-provider-token-introspection](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-token-introspection/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/05-bases/tba-bases-token-introspection)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-token-introspection/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-token-introspection/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-token-introspection/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-bases-token-introspection/)

## Governance

`tba-bases-token-introspection` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `05-bases` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-token-introspection/src/tba_bases_token_introspection/__init__.py).
