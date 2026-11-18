# tba-provider-security-proof-dpop

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-security-proof-dpop/pyproject.toml"><img alt="Checkout: 0.1.1.dev2" src="https://img.shields.io/badge/Checkout-0.1.1.dev2-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-security-proof-dpop/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-provider-security-proof-dpop%3D%3D0.1.1.dev2/pkgs/20-providers/tba-provider-security-proof-dpop/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-provider-security-proof-dpop%3D%3D0.1.1.dev2/pkgs/20-providers/tba-provider-security-proof-dpop/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/20-providers"><img alt="Layer: 20 providers" src="https://img.shields.io/badge/Layer-20%20providers-0a7f5a"></a>
<a href="https://pypi.org/project/tba-provider-security-proof-dpop/"><img alt="PyPI version for tba-provider-security-proof-dpop" src="https://img.shields.io/pypi/v/tba-provider-security-proof-dpop?label=tba-provider-security-proof-dpop%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-provider-security-proof-dpop"><img alt="Monthly PyPI downloads for tba-provider-security-proof-dpop" src="https://static.pepy.tech/badge/tba-provider-security-proof-dpop/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-security-proof-dpop/README.md"><img alt="README hits for tba-provider-security-proof-dpop" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-security-proof-dpop/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-security-proof-dpop/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

`tba-provider-security-proof-dpop` provides a standalone DPoP confirmation-claim
binding validator over the horizontal security/trust contracts.

## AEO Summary

- Package: `tba-provider-security-proof-dpop`
- Layer: `20-providers`
- Responsibility: DPoP proof and confirmation-claim binding validator provider for the TBA package suite.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-security-proof-dpop/src/tba_provider_security_proof_dpop/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-provider-security-proof-dpop` for this responsibility: DPoP proof and confirmation-claim binding validator provider for the TBA package suite. Its `20-providers` placement keeps replaceable environment implementations separate from capability orchestration, storage table ownership, or HTTP routing.

## Installation

Install the selected PyPI release of `tba-provider-security-proof-dpop`:

```bash
uv pip install tba-provider-security-proof-dpop
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/20-providers/tba-provider-security-proof-dpop
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_provider_security_proof_dpop import DpopBindingValidator

assert callable(DpopBindingValidator)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-provider-security-proof-dpop==0.1.1.dev2" python quickstart.py
```

The import and assertion succeed when the DpopBindingValidator entry point is available.

## Usage

The following public-entry-point example belongs to `tba-provider-security-proof-dpop`. DPoP proof and confirmation-claim binding validator provider for the TBA package suite. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_provider_security_proof_dpop import DpopBindingValidator

assert callable(DpopBindingValidator)
```

## Package Boundary

`tba-provider-security-proof-dpop` belongs to `20-providers` and owns replaceable environment implementations: DPoP proof and confirmation-claim binding validator provider for the TBA package suite.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-security-proof-dpop/src/tba_provider_security_proof_dpop/__init__.py). Public exports include `DpopBindingValidator`.

Keep capability orchestration, storage table ownership, or HTTP routing in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

The [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-security-proof-dpop/src/tba_provider_security_proof_dpop/__init__.py) for `tba-provider-security-proof-dpop` does not declare an explicit service-constructor or keyword-only factory hook in the inspected source. Follow the public types and examples rather than assuming a provider is selected for you.

Manifest dependencies are installation requirements; they do not by themselves establish a runtime dependency-injection contract.

## Operations and readiness

`tba-provider-security-proof-dpop` exposes replaceable environment implementations. Inspect the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-security-proof-dpop/src/tba_provider_security_proof_dpop/__init__.py) for the exported types and composition surface.

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-provider-security-proof-dpop`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

## Non-goals

`tba-provider-security-proof-dpop` does not take ownership of capability orchestration, storage table ownership, or HTTP routing.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

Declared local runtime dependencies:

- [tba-concrete-dpop-confirmation-binding](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-dpop-confirmation-binding/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/20-providers/tba-provider-security-proof-dpop)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-security-proof-dpop/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-security-proof-dpop/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-security-proof-dpop/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-provider-security-proof-dpop/)

## Governance

`tba-provider-security-proof-dpop` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `20-providers` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-security-proof-dpop/src/tba_provider_security_proof_dpop/__init__.py).
