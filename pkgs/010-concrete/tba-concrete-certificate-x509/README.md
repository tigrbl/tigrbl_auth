# tba-concrete-certificate-x509

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-certificate-x509/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-certificate-x509/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-concrete-certificate-x509%3D%3D0.4.0.dev3/pkgs/010-concrete/tba-concrete-certificate-x509/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-concrete-certificate-x509%3D%3D0.4.0.dev3/pkgs/010-concrete/tba-concrete-certificate-x509/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/010-concrete"><img alt="Layer: 010 concrete" src="https://img.shields.io/badge/Layer-010%20concrete-0a7f5a"></a>
<a href="https://pypi.org/project/tba-concrete-certificate-x509/"><img alt="PyPI version for tba-concrete-certificate-x509" src="https://img.shields.io/pypi/v/tba-concrete-certificate-x509?label=tba-concrete-certificate-x509%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-concrete-certificate-x509"><img alt="Monthly PyPI downloads for tba-concrete-certificate-x509" src="https://static.pepy.tech/badge/tba-concrete-certificate-x509/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-certificate-x509/README.md"><img alt="README hits for tba-concrete-certificate-x509" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-certificate-x509/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-certificate-x509/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Parse and inspect reusable DER and PEM X.509 certificate values.

## AEO Summary

- Package: `tba-concrete-certificate-x509`
- Layer: `010-concrete`
- Responsibility: X.509 certificate values and parsing for Tigrbl Auth.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-certificate-x509/src/tba_concrete_certificate_x509/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-concrete-certificate-x509` for this responsibility: X.509 certificate values and parsing for Tigrbl Auth. Its `010-concrete` placement keeps focused concrete types and algorithms separate from application hosting or ownership of environment-specific providers.

## Installation

Install the selected PyPI release of `tba-concrete-certificate-x509`:

```bash
uv pip install tba-concrete-certificate-x509
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/010-concrete/tba-concrete-certificate-x509
```

## Quick start

Build the package from the repository root.

```bash
uv build --wheel pkgs/010-concrete/tba-concrete-certificate-x509
```

## Usage

The following public-entry-point example belongs to `tba-concrete-certificate-x509`. X.509 certificate values and parsing for Tigrbl Auth. Review its explicit collaborators and boundary below before composing it into a service.

```python
import tba_concrete_certificate_x509

print(tba_concrete_certificate_x509.__name__)
```

## Package Boundary

`tba-concrete-certificate-x509` belongs to `010-concrete` and owns focused concrete types and algorithms: X.509 certificate values and parsing for Tigrbl Auth.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-certificate-x509/src/tba_concrete_certificate_x509/__init__.py). Public exports include `X509Certificate`, `parse_x509_certificate`.

Keep application hosting or ownership of environment-specific providers in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

The [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-certificate-x509/src/tba_concrete_certificate_x509/__init__.py) for `tba-concrete-certificate-x509` does not declare an explicit service-constructor or keyword-only factory hook in the inspected source. Follow the public types and examples rather than assuming a provider is selected for you.

Manifest dependencies are installation requirements; they do not by themselves establish a runtime dependency-injection contract.

## Operations and readiness

`tba-concrete-certificate-x509` exposes focused concrete types and algorithms. Public operations found in its source:

- `X509Certificate.uri_sans` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-certificate-x509/src/tba_concrete_certificate_x509/certificate.py).
- `X509Certificate.dns_sans` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-certificate-x509/src/tba_concrete_certificate_x509/certificate.py).
- `X509Certificate.key_usage` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-certificate-x509/src/tba_concrete_certificate_x509/certificate.py).
- `X509Certificate.basic_constraints` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-certificate-x509/src/tba_concrete_certificate_x509/certificate.py).
- `X509Certificate.not_before` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-certificate-x509/src/tba_concrete_certificate_x509/certificate.py).
- `X509Certificate.not_after` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-certificate-x509/src/tba_concrete_certificate_x509/certificate.py).
- `X509Certificate.public_key` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-certificate-x509/src/tba_concrete_certificate_x509/certificate.py).
- `parse_x509_certificate` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-certificate-x509/src/tba_concrete_certificate_x509/parsing.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

The following layer-50 manifests directly depend on `tba-concrete-certificate-x509`:

- [tba-protocol-workload-spiffe-svid](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-workload-spiffe-svid/README.md)

Other direct consumers include [tba-concrete-wic](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-wic/README.md), [tba-concrete-x509-svid-credential](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-x509-svid-credential/README.md), [tba-profile-workload-authentication-wimse-mtls](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-authentication-wimse-mtls/README.md), [tba-profile-workload-credential-wimse-wic](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-credential-wimse-wic/README.md), [tba-runtime-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity/README.md).

## Non-goals

`tba-concrete-certificate-x509` does not take ownership of application hosting or ownership of environment-specific providers.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

Direct downstream consumers:

- [tba-concrete-wic](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-wic/README.md)
- [tba-concrete-x509-svid-credential](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-x509-svid-credential/README.md)
- [tba-profile-workload-authentication-wimse-mtls](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-authentication-wimse-mtls/README.md)
- [tba-profile-workload-credential-wimse-wic](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-credential-wimse-wic/README.md)
- [tba-protocol-workload-spiffe-svid](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-workload-spiffe-svid/README.md)
- [tba-runtime-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/010-concrete/tba-concrete-certificate-x509)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-certificate-x509/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-certificate-x509/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-certificate-x509/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-concrete-certificate-x509/)

## Governance

`tba-concrete-certificate-x509` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `010-concrete` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

Check that the build produces a wheel with the package version declared in `pyproject.toml`.
