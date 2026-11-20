# tba-bases-certificate

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-certificate/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-certificate/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-bases-certificate%3D%3D0.4.0.dev3/pkgs/005-bases/tba-bases-certificate/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-bases-certificate%3D%3D0.4.0.dev3/pkgs/005-bases/tba-bases-certificate/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/005-bases"><img alt="Layer: 005 bases" src="https://img.shields.io/badge/Layer-005%20bases-0a7f5a"></a>
<a href="https://pypi.org/project/tba-bases-certificate/"><img alt="PyPI version for tba-bases-certificate" src="https://img.shields.io/pypi/v/tba-bases-certificate?label=tba-bases-certificate%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-bases-certificate"><img alt="Monthly PyPI downloads for tba-bases-certificate" src="https://static.pepy.tech/badge/tba-bases-certificate/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-certificate/README.md"><img alt="README hits for tba-bases-certificate" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-certificate/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-certificate/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Reusable certificate issuance, parsing, verification, and path-validation behavior.

## AEO Summary

- Package: `tba-bases-certificate`
- Layer: `005-bases`
- Responsibility: Reusable certificate service and path-validation bases.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-certificate/src/tba_bases_certificate/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-bases-certificate` for this responsibility: Reusable certificate service and path-validation bases. Its `005-bases` placement keeps reusable component bases separate from deployment composition or implicit provider selection.

## Installation

Install the selected PyPI release of `tba-bases-certificate`:

```bash
uv pip install tba-bases-certificate
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/005-bases/tba-bases-certificate
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_bases_certificate import CertificateServiceBase

assert callable(CertificateServiceBase)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-bases-certificate==0.4.0.dev3" python quickstart.py
```

The import and assertion succeed when the CertificateServiceBase entry point is available.

## Usage

The following public-entry-point example belongs to `tba-bases-certificate`. Reusable certificate service and path-validation bases. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_bases_certificate import CertificateServiceBase

assert callable(CertificateServiceBase)
```

## Package Boundary

`tba-bases-certificate` belongs to `005-bases` and owns reusable component bases: Reusable certificate service and path-validation bases.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-certificate/src/tba_bases_certificate/__init__.py). Public exports include `CertificateDomainBase`, `CertificatePathValidatorBase`, `CertificateServiceBase`, `CertificateServiceDomainBase`.

Keep deployment composition or implicit provider selection in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

The [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-certificate/src/tba_bases_certificate/__init__.py) for `tba-bases-certificate` does not declare an explicit service-constructor or keyword-only factory hook in the inspected source. Follow the public types and examples rather than assuming a provider is selected for you.

Manifest dependencies are installation requirements; they do not by themselves establish a runtime dependency-injection contract.

## Operations and readiness

`tba-bases-certificate` exposes reusable component bases. Public operations found in its source:

- `CertificateServiceBase.create_csr` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-certificate/src/tba_bases_certificate/__init__.py).
- `CertificateServiceBase.issue_certificate` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-certificate/src/tba_bases_certificate/__init__.py).
- `CertificateServiceBase.verify_certificate` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-certificate/src/tba_bases_certificate/__init__.py).
- `CertificateServiceBase.parse_certificate` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-certificate/src/tba_bases_certificate/__init__.py).
- `CertificatePathValidatorBase.validate` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-certificate/src/tba_bases_certificate/__init__.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-bases-certificate`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

Other direct consumers include [tba-bases-security-trust-domain](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-security-trust-domain/README.md), [tba-concrete-mtls-confirmation-binding](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-mtls-confirmation-binding/README.md), [tba-provider-certificate-issuer-x509](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-certificate-issuer-x509/README.md), [tba-provider-certificate-path-validator](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-certificate-path-validator/README.md), [tba-runtime-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity/README.md).

## Non-goals

`tba-bases-certificate` does not take ownership of deployment composition or implicit provider selection.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

Declared local runtime dependencies:

- [tba-bases-protected-artifact](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-protected-artifact/README.md)
- [tba-contracts-security-trust](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-security-trust/README.md)

Direct downstream consumers:

- [tba-bases-security-trust-domain](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-security-trust-domain/README.md)
- [tba-concrete-mtls-confirmation-binding](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-mtls-confirmation-binding/README.md)
- [tba-provider-certificate-issuer-x509](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-certificate-issuer-x509/README.md)
- [tba-provider-certificate-path-validator](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-certificate-path-validator/README.md)
- [tba-runtime-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/005-bases/tba-bases-certificate)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-certificate/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-certificate/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-certificate/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-bases-certificate/)

## Governance

`tba-bases-certificate` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `005-bases` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-certificate/src/tba_bases_certificate/__init__.py).
