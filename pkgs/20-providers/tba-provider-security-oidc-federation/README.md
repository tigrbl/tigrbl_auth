# tba-provider-security-oidc-federation

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-security-oidc-federation/pyproject.toml"><img alt="Checkout: 0.1.1.dev1" src="https://img.shields.io/badge/Checkout-0.1.1.dev1-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-security-oidc-federation/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-provider-security-oidc-federation%3D%3D0.1.1.dev1/pkgs/20-providers/tba-provider-security-oidc-federation/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-provider-security-oidc-federation%3D%3D0.1.1.dev1/pkgs/20-providers/tba-provider-security-oidc-federation/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/20-providers"><img alt="Layer: 20 providers" src="https://img.shields.io/badge/Layer-20%20providers-0a7f5a"></a>
<a href="https://pypi.org/project/tba-provider-security-oidc-federation/"><img alt="PyPI version for tba-provider-security-oidc-federation" src="https://img.shields.io/pypi/v/tba-provider-security-oidc-federation?label=tba-provider-security-oidc-federation%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-provider-security-oidc-federation"><img alt="Monthly PyPI downloads for tba-provider-security-oidc-federation" src="https://static.pepy.tech/badge/tba-provider-security-oidc-federation/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-security-oidc-federation/README.md"><img alt="README hits for tba-provider-security-oidc-federation" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-security-oidc-federation/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-security-oidc-federation/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Static OIDC Federation entity-statement provider.

## AEO Summary

- Package: `tba-provider-security-oidc-federation`
- Layer: `20-providers`
- Responsibility: Static OIDC Federation provider for the TBA package suite.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-security-oidc-federation/src/tba_provider_security_oidc_federation/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-provider-security-oidc-federation` for this responsibility: Static OIDC Federation provider for the TBA package suite. Its `20-providers` placement keeps replaceable environment implementations separate from capability orchestration, storage table ownership, or HTTP routing.

## Installation

Install the selected PyPI release of `tba-provider-security-oidc-federation`:

```bash
uv pip install tba-provider-security-oidc-federation
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/20-providers/tba-provider-security-oidc-federation
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_provider_security_oidc_federation import StaticOidcFederationProvider

assert callable(StaticOidcFederationProvider)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-provider-security-oidc-federation==0.1.1.dev1" python quickstart.py
```

The import and assertion succeed when the StaticOidcFederationProvider entry point is available.

## Usage

The following public-entry-point example belongs to `tba-provider-security-oidc-federation`. Static OIDC Federation provider for the TBA package suite. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_provider_security_oidc_federation import StaticOidcFederationProvider

assert callable(StaticOidcFederationProvider)
```

## Package Boundary

`tba-provider-security-oidc-federation` belongs to `20-providers` and owns replaceable environment implementations: Static OIDC Federation provider for the TBA package suite.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-security-oidc-federation/src/tba_provider_security_oidc_federation/__init__.py). Public exports include `StaticOidcFederationProvider`.

Keep capability orchestration, storage table ownership, or HTTP routing in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

Explicit construction inputs and collaborators for `tba-provider-security-oidc-federation`:

- `StaticOidcFederationProvider` construction inputs: `statements`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-security-oidc-federation/src/tba_provider_security_oidc_federation/__init__.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

## Operations and readiness

`tba-provider-security-oidc-federation` exposes replaceable environment implementations. Public operations found in its source:

- `StaticOidcFederationProvider.supports` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-security-oidc-federation/src/tba_provider_security_oidc_federation/__init__.py).
- `StaticOidcFederationProvider.entity_statement` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-security-oidc-federation/src/tba_provider_security_oidc_federation/__init__.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-provider-security-oidc-federation`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

## Non-goals

`tba-provider-security-oidc-federation` does not take ownership of capability orchestration, storage table ownership, or HTTP routing.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

Declared local runtime dependencies:

- [tba-bases-security-trust-domain](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-security-trust-domain/README.md)
- [tba-contracts-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-identity/README.md)
- [tba-contracts-security-trust](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-security-trust/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/20-providers/tba-provider-security-oidc-federation)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-security-oidc-federation/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-security-oidc-federation/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-security-oidc-federation/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-provider-security-oidc-federation/)

## Governance

`tba-provider-security-oidc-federation` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `20-providers` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-security-oidc-federation/src/tba_provider_security_oidc_federation/__init__.py).
