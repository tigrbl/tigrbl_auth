# tba-concrete-claim-nationalities

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-claim-nationalities/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-claim-nationalities/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-concrete-claim-nationalities%3D%3D0.4.0.dev3/pkgs/010-concrete/tba-concrete-claim-nationalities/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-concrete-claim-nationalities%3D%3D0.4.0.dev3/pkgs/010-concrete/tba-concrete-claim-nationalities/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/010-concrete"><img alt="Layer: 010 concrete" src="https://img.shields.io/badge/Layer-010%20concrete-0a7f5a"></a>
<a href="https://pypi.org/project/tba-concrete-claim-nationalities/"><img alt="PyPI version for tba-concrete-claim-nationalities" src="https://img.shields.io/pypi/v/tba-concrete-claim-nationalities?label=tba-concrete-claim-nationalities%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-concrete-claim-nationalities"><img alt="Monthly PyPI downloads for tba-concrete-claim-nationalities" src="https://static.pepy.tech/badge/tba-concrete-claim-nationalities/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-claim-nationalities/README.md"><img alt="README hits for tba-concrete-claim-nationalities" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-claim-nationalities/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-claim-nationalities/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Owns `NationalitiesClaim` as protocol-neutral layer-10 value semantics.

## AEO Summary

- Package: `tba-concrete-claim-nationalities`
- Layer: `010-concrete`
- Responsibility: Owns NationalitiesClaim as protocol-neutral layer-10 value semantics.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-claim-nationalities/src/tba_concrete_claim_nationalities/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-concrete-claim-nationalities` for this responsibility: Owns NationalitiesClaim as protocol-neutral layer-10 value semantics. Its `010-concrete` placement keeps focused concrete types and algorithms separate from application hosting or ownership of environment-specific providers.

## Installation

Install the selected PyPI release of `tba-concrete-claim-nationalities`:

```bash
uv pip install tba-concrete-claim-nationalities
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/010-concrete/tba-concrete-claim-nationalities
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_concrete_claim_nationalities import NationalitiesClaim

claim = NationalitiesClaim(('example',))
assert claim.name == 'nationalities'
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-concrete-claim-nationalities==0.4.0.dev3" python quickstart.py
```

The example constructs a claim named `nationalities`.

## Usage

The following public-entry-point example belongs to `tba-concrete-claim-nationalities`. Owns NationalitiesClaim as protocol-neutral layer-10 value semantics. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_concrete_claim_nationalities import NationalitiesClaim

claim = NationalitiesClaim(('example',))
assert claim.name == 'nationalities'
```

## Package Boundary

`tba-concrete-claim-nationalities` belongs to `010-concrete` and owns focused concrete types and algorithms: Owns NationalitiesClaim as protocol-neutral layer-10 value semantics.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-claim-nationalities/src/tba_concrete_claim_nationalities/__init__.py). Public exports include `NationalitiesClaim`.

Keep application hosting or ownership of environment-specific providers in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

The [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-claim-nationalities/src/tba_concrete_claim_nationalities/__init__.py) for `tba-concrete-claim-nationalities` does not declare an explicit service-constructor or keyword-only factory hook in the inspected source. Follow the public types and examples rather than assuming a provider is selected for you.

Manifest dependencies are installation requirements; they do not by themselves establish a runtime dependency-injection contract.

## Operations and readiness

`tba-concrete-claim-nationalities` exposes focused concrete types and algorithms. Public operations found in its source:

- `NationalitiesClaim.validate_value` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-claim-nationalities/src/tba_concrete_claim_nationalities/__init__.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

The following layer-50 manifests directly depend on `tba-concrete-claim-nationalities`:

- [tba-protocol-oidc](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oidc/README.md)

## Non-goals

Protocol claim-set composition, version selection, persistence, trust resolution, and environment-backed claim retrieval are not owned here.

## Related Packages

Declared local runtime dependencies:

- [tba-bases-claim](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-claim/README.md)

Direct downstream consumers:

- [tba-protocol-oidc](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oidc/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/010-concrete/tba-concrete-claim-nationalities)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-claim-nationalities/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-claim-nationalities/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-claim-nationalities/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-concrete-claim-nationalities/)

## Governance

`tba-concrete-claim-nationalities` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `010-concrete` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-claim-nationalities/src/tba_concrete_claim_nationalities/__init__.py).
