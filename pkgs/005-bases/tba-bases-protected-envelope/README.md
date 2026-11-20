# tba-bases-protected-envelope

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-protected-envelope/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-protected-envelope/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-bases-protected-envelope%3D%3D0.4.0.dev3/pkgs/005-bases/tba-bases-protected-envelope/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-bases-protected-envelope%3D%3D0.4.0.dev3/pkgs/005-bases/tba-bases-protected-envelope/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/005-bases"><img alt="Layer: 005 bases" src="https://img.shields.io/badge/Layer-005%20bases-0a7f5a"></a>
<a href="https://pypi.org/project/tba-bases-protected-envelope/"><img alt="PyPI version for tba-bases-protected-envelope" src="https://img.shields.io/pypi/v/tba-bases-protected-envelope?label=tba-bases-protected-envelope%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-bases-protected-envelope"><img alt="Monthly PyPI downloads for tba-bases-protected-envelope" src="https://static.pepy.tech/badge/tba-bases-protected-envelope/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-protected-envelope/README.md"><img alt="README hits for tba-bases-protected-envelope" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-protected-envelope/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-protected-envelope/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Protocol-neutral bases for protecting and verifying signed, MACed, and encrypted envelopes. Exact JOSE and COSE structures belong to versioned layer-50 packages.

## AEO Summary

- Package: `tba-bases-protected-envelope`
- Layer: `005-bases`
- Responsibility: Protocol-neutral protected-envelope issuance and verification bases.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-protected-envelope/src/tba_bases_protected_envelope/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-bases-protected-envelope` for this responsibility: Protocol-neutral protected-envelope issuance and verification bases. Its `005-bases` placement keeps reusable component bases separate from deployment composition or implicit provider selection.

## Installation

Install the selected PyPI release of `tba-bases-protected-envelope`:

```bash
uv pip install tba-bases-protected-envelope
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/005-bases/tba-bases-protected-envelope
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_bases_protected_envelope import ProtectedEnvelopeIssuerBase

assert callable(ProtectedEnvelopeIssuerBase)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-bases-protected-envelope==0.4.0.dev3" python quickstart.py
```

The import and assertion succeed when the ProtectedEnvelopeIssuerBase entry point is available.

## Usage

The following public-entry-point example belongs to `tba-bases-protected-envelope`. Protocol-neutral protected-envelope issuance and verification bases. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_bases_protected_envelope import ProtectedEnvelopeIssuerBase

assert callable(ProtectedEnvelopeIssuerBase)
```

## Package Boundary

`tba-bases-protected-envelope` belongs to `005-bases` and owns reusable component bases: Protocol-neutral protected-envelope issuance and verification bases.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-protected-envelope/src/tba_bases_protected_envelope/__init__.py). Public exports include `ProtectedEnvelopeIssuerBase`, `ProtectedEnvelopeVerifierBase`, `VerificationKeyResolverBase`.

Keep deployment composition or implicit provider selection in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

The [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-protected-envelope/src/tba_bases_protected_envelope/__init__.py) for `tba-bases-protected-envelope` does not declare an explicit service-constructor or keyword-only factory hook in the inspected source. Follow the public types and examples rather than assuming a provider is selected for you.

Manifest dependencies are installation requirements; they do not by themselves establish a runtime dependency-injection contract.

## Operations and readiness

`tba-bases-protected-envelope` exposes reusable component bases. Public operations found in its source:

- `ProtectedEnvelopeIssuerBase.protect` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-protected-envelope/src/tba_bases_protected_envelope/__init__.py).
- `ProtectedEnvelopeVerifierBase.verify` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-protected-envelope/src/tba_bases_protected_envelope/__init__.py).
- `VerificationKeyResolverBase.resolve_verification_key` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-protected-envelope/src/tba_bases_protected_envelope/__init__.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-bases-protected-envelope`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

Other direct consumers include [tba-bases-cose](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-cose/README.md), [tba-bases-jose](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-jose/README.md), [tba-provider-jose-cryptography](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-jose-cryptography/README.md).

## Non-goals

`tba-bases-protected-envelope` does not take ownership of deployment composition or implicit provider selection.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

Declared local runtime dependencies:

- [tba-contracts-protected-envelope](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-protected-envelope/README.md)

Direct downstream consumers:

- [tba-bases-cose](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-cose/README.md)
- [tba-bases-jose](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-jose/README.md)
- [tba-provider-jose-cryptography](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-jose-cryptography/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/005-bases/tba-bases-protected-envelope)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-protected-envelope/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-protected-envelope/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-protected-envelope/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-bases-protected-envelope/)

## Governance

`tba-bases-protected-envelope` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `005-bases` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-protected-envelope/src/tba_bases_protected_envelope/__init__.py).
