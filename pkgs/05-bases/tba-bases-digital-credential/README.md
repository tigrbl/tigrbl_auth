# tba-bases-digital-credential

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-digital-credential/pyproject.toml"><img alt="Checkout: 0.4.0.dev4" src="https://img.shields.io/badge/Checkout-0.4.0.dev4-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-digital-credential/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-bases-digital-credential%3D%3D0.4.0.dev4/pkgs/05-bases/tba-bases-digital-credential/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-bases-digital-credential%3D%3D0.4.0.dev4/pkgs/05-bases/tba-bases-digital-credential/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/05-bases"><img alt="Layer: 05 bases" src="https://img.shields.io/badge/Layer-05%20bases-0a7f5a"></a>
<a href="https://pypi.org/project/tba-bases-digital-credential/"><img alt="PyPI version for tba-bases-digital-credential" src="https://img.shields.io/pypi/v/tba-bases-digital-credential?label=tba-bases-digital-credential%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-bases-digital-credential"><img alt="Monthly PyPI downloads for tba-bases-digital-credential" src="https://static.pepy.tech/badge/tba-bases-digital-credential/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-digital-credential/README.md"><img alt="README hits for tba-bases-digital-credential" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-digital-credential/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-digital-credential/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Owns reusable implementation bases.

## AEO Summary

- Package: `tba-bases-digital-credential`
- Layer: `05-bases`
- Responsibility: Protocol-neutral digital credential provider bases.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-digital-credential/src/tba_bases_digital_credential/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-bases-digital-credential` for this responsibility: Protocol-neutral digital credential provider bases. Its `05-bases` placement keeps reusable component bases separate from deployment composition or implicit provider selection.

## Installation

Install the selected PyPI release of `tba-bases-digital-credential`:

```bash
uv pip install tba-bases-digital-credential
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/05-bases/tba-bases-digital-credential
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_bases_digital_credential import CredentialFormatBase

assert callable(CredentialFormatBase)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-bases-digital-credential==0.4.0.dev4" python quickstart.py
```

The import and assertion succeed when the CredentialFormatBase entry point is available.

## Usage

The following public-entry-point example belongs to `tba-bases-digital-credential`. Protocol-neutral digital credential provider bases. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_bases_digital_credential import CredentialFormatBase

assert callable(CredentialFormatBase)
```

## Package Boundary

`tba-bases-digital-credential` belongs to `05-bases` and owns reusable component bases: Protocol-neutral digital credential provider bases.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-digital-credential/src/tba_bases_digital_credential/__init__.py). Public exports include `CredentialFormatBase`, `CredentialIssuerBase`, `CredentialStatusResolverBase`, `CredentialVerifierBase`, `PresentationVerifierBase`, `PresentationFormatBase`, `WalletAttestationVerifierBase`.

Keep deployment composition or implicit provider selection in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

The [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-digital-credential/src/tba_bases_digital_credential/__init__.py) for `tba-bases-digital-credential` does not declare an explicit service-constructor or keyword-only factory hook in the inspected source. Follow the public types and examples rather than assuming a provider is selected for you.

Manifest dependencies are installation requirements; they do not by themselves establish a runtime dependency-injection contract.

## Operations and readiness

`tba-bases-digital-credential` exposes reusable component bases. Public operations found in its source:

- `CredentialIssuerBase.issue` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-digital-credential/src/tba_bases_digital_credential/__init__.py).
- `CredentialVerifierBase.verify` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-digital-credential/src/tba_bases_digital_credential/__init__.py).
- `PresentationVerifierBase.verify` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-digital-credential/src/tba_bases_digital_credential/__init__.py).
- `CredentialStatusResolverBase.resolve` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-digital-credential/src/tba_bases_digital_credential/__init__.py).
- `WalletAttestationVerifierBase.verify_wallet_attestation` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-digital-credential/src/tba_bases_digital_credential/__init__.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

The following layer-50 manifests directly depend on `tba-bases-digital-credential`:

- [tba-protocol-credential-iso-mdoc](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-credential-iso-mdoc/README.md)

Other direct consumers include [tba-concrete-cwt-svid-extension-credential](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-cwt-svid-extension-credential/README.md), [tba-concrete-jwt-svid-credential](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-jwt-svid-credential/README.md), [tba-concrete-mdoc-credential](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-mdoc-credential/README.md), [tba-concrete-sd-jwt-vc-credential](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-sd-jwt-vc-credential/README.md), [tba-concrete-vc-cose-credential](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-vc-cose-credential/README.md), [tba-concrete-vc-jose-credential](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-vc-jose-credential/README.md), [tba-concrete-verifiable-credential](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-verifiable-credential/README.md), [tba-concrete-verifiable-presentation](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-verifiable-presentation/README.md).

## Non-goals

Higher-layer orchestration, lower-layer persistence, and protocol behavior outside this package's declared layer are not owned here.

## Related Packages

Declared local runtime dependencies:

- [tba-contracts-digital-credential](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-digital-credential/README.md)

Direct downstream consumers:

- [tba-concrete-cwt-svid-extension-credential](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-cwt-svid-extension-credential/README.md)
- [tba-concrete-jwt-svid-credential](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-jwt-svid-credential/README.md)
- [tba-concrete-mdoc-credential](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-mdoc-credential/README.md)
- [tba-concrete-sd-jwt-vc-credential](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-sd-jwt-vc-credential/README.md)
- [tba-concrete-vc-cose-credential](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-vc-cose-credential/README.md)
- [tba-concrete-vc-jose-credential](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-vc-jose-credential/README.md)
- [tba-concrete-verifiable-credential](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-verifiable-credential/README.md)
- [tba-concrete-verifiable-presentation](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-verifiable-presentation/README.md)
- [tba-concrete-wit-svid-credential](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-wit-svid-credential/README.md)
- [tba-concrete-x509-svid-credential](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-x509-svid-credential/README.md)
- [tba-protocol-credential-iso-mdoc](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-credential-iso-mdoc/README.md)
- [tba-provider-digital-credential-status](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-digital-credential-status/README.md)

15 packages directly declare this dependency; the [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records the complete graph.

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/05-bases/tba-bases-digital-credential)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-digital-credential/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-digital-credential/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-digital-credential/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-bases-digital-credential/)

## Governance

`tba-bases-digital-credential` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `05-bases` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-digital-credential/src/tba_bases_digital_credential/__init__.py).
