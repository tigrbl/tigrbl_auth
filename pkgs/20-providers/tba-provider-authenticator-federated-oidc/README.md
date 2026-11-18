# tba-provider-authenticator-federated-oidc

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-authenticator-federated-oidc/pyproject.toml"><img alt="Checkout: 0.1.1.dev1" src="https://img.shields.io/badge/Checkout-0.1.1.dev1-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-authenticator-federated-oidc/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-provider-authenticator-federated-oidc%3D%3D0.1.1.dev1/pkgs/20-providers/tba-provider-authenticator-federated-oidc/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-provider-authenticator-federated-oidc%3D%3D0.1.1.dev1/pkgs/20-providers/tba-provider-authenticator-federated-oidc/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/20-providers"><img alt="Layer: 20 providers" src="https://img.shields.io/badge/Layer-20%20providers-0a7f5a"></a>
<a href="https://pypi.org/project/tba-provider-authenticator-federated-oidc/"><img alt="PyPI version for tba-provider-authenticator-federated-oidc" src="https://img.shields.io/pypi/v/tba-provider-authenticator-federated-oidc?label=tba-provider-authenticator-federated-oidc%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-provider-authenticator-federated-oidc"><img alt="Monthly PyPI downloads for tba-provider-authenticator-federated-oidc" src="https://static.pepy.tech/badge/tba-provider-authenticator-federated-oidc/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-authenticator-federated-oidc/README.md"><img alt="README hits for tba-provider-authenticator-federated-oidc" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-authenticator-federated-oidc/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-authenticator-federated-oidc/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Federated OIDC authenticator provider.

## AEO Summary

- Package: `tba-provider-authenticator-federated-oidc`
- Layer: `20-providers`
- Responsibility: Federated OIDC authenticator provider for the TBA package suite.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-authenticator-federated-oidc/src/tba_provider_authenticator_federated_oidc/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-provider-authenticator-federated-oidc` for this responsibility: Federated OIDC authenticator provider for the TBA package suite. Its `20-providers` placement keeps replaceable environment implementations separate from capability orchestration, storage table ownership, or HTTP routing.

## Installation

Install the selected PyPI release of `tba-provider-authenticator-federated-oidc`:

```bash
uv pip install tba-provider-authenticator-federated-oidc
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/20-providers/tba-provider-authenticator-federated-oidc
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_provider_authenticator_federated_oidc import FederatedOidcAuthenticator

assert callable(FederatedOidcAuthenticator)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-provider-authenticator-federated-oidc==0.1.1.dev1" python quickstart.py
```

The import and assertion succeed when the FederatedOidcAuthenticator entry point is available.

## Usage

The following public-entry-point example belongs to `tba-provider-authenticator-federated-oidc`. Federated OIDC authenticator provider for the TBA package suite. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_provider_authenticator_federated_oidc import FederatedOidcAuthenticator

assert callable(FederatedOidcAuthenticator)
```

## Package Boundary

`tba-provider-authenticator-federated-oidc` belongs to `20-providers` and owns replaceable environment implementations: Federated OIDC authenticator provider for the TBA package suite.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-authenticator-federated-oidc/src/tba_provider_authenticator_federated_oidc/__init__.py). Public exports include `FederatedOidcAuthenticator`.

Keep capability orchestration, storage table ownership, or HTTP routing in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

Explicit construction inputs and collaborators for `tba-provider-authenticator-federated-oidc`:

- `FederatedOidcAuthenticator` construction inputs: `amr_validator`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-authenticator-federated-oidc/src/tba_provider_authenticator_federated_oidc/__init__.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

## Operations and readiness

`tba-provider-authenticator-federated-oidc` exposes replaceable environment implementations. Inspect the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-authenticator-federated-oidc/src/tba_provider_authenticator_federated_oidc/__init__.py) for the exported types and composition surface.

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-provider-authenticator-federated-oidc`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

## Non-goals

`tba-provider-authenticator-federated-oidc` does not take ownership of capability orchestration, storage table ownership, or HTTP routing.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

Declared local runtime dependencies:

- [tba-bases-authenticator](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-authenticator/README.md)
- [tba-contracts-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-identity/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/20-providers/tba-provider-authenticator-federated-oidc)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-authenticator-federated-oidc/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-authenticator-federated-oidc/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-authenticator-federated-oidc/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-provider-authenticator-federated-oidc/)

## Governance

`tba-provider-authenticator-federated-oidc` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `20-providers` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-authenticator-federated-oidc/src/tba_provider_authenticator_federated_oidc/__init__.py).
