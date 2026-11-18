# tba-concrete-claim-cwt-confirmation

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-claim-cwt-confirmation/pyproject.toml"><img alt="Checkout: 0.4.0.dev4" src="https://img.shields.io/badge/Checkout-0.4.0.dev4-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-claim-cwt-confirmation/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-concrete-claim-cwt-confirmation%3D%3D0.4.0.dev4/pkgs/10-concrete/tba-concrete-claim-cwt-confirmation/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-concrete-claim-cwt-confirmation%3D%3D0.4.0.dev4/pkgs/10-concrete/tba-concrete-claim-cwt-confirmation/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/10-concrete"><img alt="Layer: 10 concrete" src="https://img.shields.io/badge/Layer-10%20concrete-0a7f5a"></a>
<a href="https://pypi.org/project/tba-concrete-claim-cwt-confirmation/"><img alt="PyPI version for tba-concrete-claim-cwt-confirmation" src="https://img.shields.io/pypi/v/tba-concrete-claim-cwt-confirmation?label=tba-concrete-claim-cwt-confirmation%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-concrete-claim-cwt-confirmation"><img alt="Monthly PyPI downloads for tba-concrete-claim-cwt-confirmation" src="https://static.pepy.tech/badge/tba-concrete-claim-cwt-confirmation/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-claim-cwt-confirmation/README.md"><img alt="README hits for tba-concrete-claim-cwt-confirmation" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-claim-cwt-confirmation/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-claim-cwt-confirmation/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Owns integer-labelled CWT cnf claim validation for RFC 8747 methods 1-3 and RFC 9679 ckt method 5. Envelope confidentiality and key resolution remain protocol/provider concerns.

## AEO Summary

- Package: `tba-concrete-claim-cwt-confirmation`
- Layer: `10-concrete`
- Responsibility: Standalone RFC 8747 CWT cnf claim implementation.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-claim-cwt-confirmation/src/tba_concrete_claim_cwt_confirmation/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-concrete-claim-cwt-confirmation` for this responsibility: Standalone RFC 8747 CWT cnf claim implementation. Its `10-concrete` placement keeps focused concrete types and algorithms separate from application hosting or ownership of environment-specific providers.

## Installation

Install the selected PyPI release of `tba-concrete-claim-cwt-confirmation`:

```bash
uv pip install tba-concrete-claim-cwt-confirmation
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/10-concrete/tba-concrete-claim-cwt-confirmation
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_concrete_claim_cwt_confirmation import CwtConfirmationClaim

assert callable(CwtConfirmationClaim)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-concrete-claim-cwt-confirmation==0.4.0.dev4" python quickstart.py
```

The import and assertion succeed when the CwtConfirmationClaim entry point is available.

## Usage

The following public-entry-point example belongs to `tba-concrete-claim-cwt-confirmation`. Standalone RFC 8747 CWT cnf claim implementation. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_concrete_claim_cwt_confirmation import CwtConfirmationClaim

assert callable(CwtConfirmationClaim)
```

## Package Boundary

`tba-concrete-claim-cwt-confirmation` belongs to `10-concrete` and owns focused concrete types and algorithms: Standalone RFC 8747 CWT cnf claim implementation.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-claim-cwt-confirmation/src/tba_concrete_claim_cwt_confirmation/__init__.py). Public exports include `CwtConfirmationClaim`.

Keep application hosting or ownership of environment-specific providers in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

The [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-claim-cwt-confirmation/src/tba_concrete_claim_cwt_confirmation/__init__.py) for `tba-concrete-claim-cwt-confirmation` does not declare an explicit service-constructor or keyword-only factory hook in the inspected source. Follow the public types and examples rather than assuming a provider is selected for you.

Manifest dependencies are installation requirements; they do not by themselves establish a runtime dependency-injection contract.

## Operations and readiness

`tba-concrete-claim-cwt-confirmation` exposes focused concrete types and algorithms. Public operations found in its source:

- `CwtConfirmationClaim.validate_value` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-claim-cwt-confirmation/src/tba_concrete_claim_cwt_confirmation/__init__.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-concrete-claim-cwt-confirmation`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

## Non-goals

`tba-concrete-claim-cwt-confirmation` does not take ownership of application hosting or ownership of environment-specific providers.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

Declared local runtime dependencies:

- [tba-bases-claim](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-claim/README.md)
- [tba-primitives-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/00-primitives/tba-primitives-identity/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/10-concrete/tba-concrete-claim-cwt-confirmation)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-claim-cwt-confirmation/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-claim-cwt-confirmation/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-claim-cwt-confirmation/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-concrete-claim-cwt-confirmation/)

## Governance

`tba-concrete-claim-cwt-confirmation` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `10-concrete` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-claim-cwt-confirmation/src/tba_concrete_claim_cwt_confirmation/__init__.py).
