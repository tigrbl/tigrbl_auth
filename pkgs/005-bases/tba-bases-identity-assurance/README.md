# tba-bases-identity-assurance

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-identity-assurance/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-identity-assurance/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-bases-identity-assurance%3D%3D0.4.0.dev3/pkgs/005-bases/tba-bases-identity-assurance/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-bases-identity-assurance%3D%3D0.4.0.dev3/pkgs/005-bases/tba-bases-identity-assurance/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/005-bases"><img alt="Layer: 005 bases" src="https://img.shields.io/badge/Layer-005%20bases-0a7f5a"></a>
<a href="https://pypi.org/project/tba-bases-identity-assurance/"><img alt="PyPI version for tba-bases-identity-assurance" src="https://img.shields.io/pypi/v/tba-bases-identity-assurance?label=tba-bases-identity-assurance%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-bases-identity-assurance"><img alt="Monthly PyPI downloads for tba-bases-identity-assurance" src="https://static.pepy.tech/badge/tba-bases-identity-assurance/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-identity-assurance/README.md"><img alt="README hits for tba-bases-identity-assurance" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-identity-assurance/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-identity-assurance/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Owns protocol-neutral verified-claims provision and identity-assurance validation behavior.

## AEO Summary

- Package: `tba-bases-identity-assurance`
- Layer: `005-bases`
- Responsibility: Protocol-neutral identity assurance bases.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-identity-assurance/src/tba_bases_identity_assurance/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-bases-identity-assurance` for this responsibility: Protocol-neutral identity assurance bases. Its `005-bases` placement keeps reusable component bases separate from deployment composition or implicit provider selection.

## Installation

Install the selected PyPI release of `tba-bases-identity-assurance`:

```bash
uv pip install tba-bases-identity-assurance
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/005-bases/tba-bases-identity-assurance
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_bases_identity_assurance import IdentityAssuranceClaimsProviderBase

assert callable(IdentityAssuranceClaimsProviderBase)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-bases-identity-assurance==0.4.0.dev3" python quickstart.py
```

The import and assertion succeed when the IdentityAssuranceClaimsProviderBase entry point is available.

## Usage

The following public-entry-point example belongs to `tba-bases-identity-assurance`. Protocol-neutral identity assurance bases. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_bases_identity_assurance import IdentityAssuranceClaimsProviderBase

assert callable(IdentityAssuranceClaimsProviderBase)
```

## Package Boundary

`tba-bases-identity-assurance` belongs to `005-bases` and owns reusable component bases: Protocol-neutral identity assurance bases.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-identity-assurance/src/tba_bases_identity_assurance/__init__.py). Public exports include `AssuranceEvidenceEvaluatorBase`, `IdentityAssuranceClaimsProviderBase`, `VerifiedClaimsValidatorBase`.

Keep deployment composition or implicit provider selection in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

The [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-identity-assurance/src/tba_bases_identity_assurance/__init__.py) for `tba-bases-identity-assurance` does not declare an explicit service-constructor or keyword-only factory hook in the inspected source. Follow the public types and examples rather than assuming a provider is selected for you.

Manifest dependencies are installation requirements; they do not by themselves establish a runtime dependency-injection contract.

## Operations and readiness

`tba-bases-identity-assurance` exposes reusable component bases. Public operations found in its source:

- `IdentityAssuranceClaimsProviderBase.provide` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-identity-assurance/src/tba_bases_identity_assurance/__init__.py).
- `VerifiedClaimsValidatorBase.validate` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-identity-assurance/src/tba_bases_identity_assurance/__init__.py).
- `AssuranceEvidenceEvaluatorBase.evaluate_evidence` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-identity-assurance/src/tba_bases_identity_assurance/__init__.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-bases-identity-assurance`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

Other direct consumers include [tba-bases-authentication-assurance](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-authentication-assurance/README.md).

## Non-goals

`tba-bases-identity-assurance` does not take ownership of deployment composition or implicit provider selection.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

Declared local runtime dependencies:

- [tba-contracts-identity-assurance](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-identity-assurance/README.md)

Direct downstream consumers:

- [tba-bases-authentication-assurance](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-authentication-assurance/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/005-bases/tba-bases-identity-assurance)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-identity-assurance/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-identity-assurance/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-identity-assurance/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-bases-identity-assurance/)

## Governance

`tba-bases-identity-assurance` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `005-bases` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-identity-assurance/src/tba_bases_identity_assurance/__init__.py).
