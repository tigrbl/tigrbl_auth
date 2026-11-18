# tba-provider-certificate-issuer-x509

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-certificate-issuer-x509/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-certificate-issuer-x509/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-provider-certificate-issuer-x509%3D%3D0.4.0.dev3/pkgs/20-providers/tba-provider-certificate-issuer-x509/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-provider-certificate-issuer-x509%3D%3D0.4.0.dev3/pkgs/20-providers/tba-provider-certificate-issuer-x509/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/20-providers"><img alt="Layer: 20 providers" src="https://img.shields.io/badge/Layer-20%20providers-0a7f5a"></a>
<a href="https://pypi.org/project/tba-provider-certificate-issuer-x509/"><img alt="PyPI version for tba-provider-certificate-issuer-x509" src="https://img.shields.io/pypi/v/tba-provider-certificate-issuer-x509?label=tba-provider-certificate-issuer-x509%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-provider-certificate-issuer-x509"><img alt="Monthly PyPI downloads for tba-provider-certificate-issuer-x509" src="https://static.pepy.tech/badge/tba-provider-certificate-issuer-x509/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-certificate-issuer-x509/README.md"><img alt="README hits for tba-provider-certificate-issuer-x509" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-certificate-issuer-x509/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-certificate-issuer-x509/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Create an `X509CertificateIssuer` from `X509IssuerConfig`, then call
`issue_certificate(CertificateRequest(op="issue_certificate", ...))`.

The signed CSR supplies the public key. The trusted caller supplies the subject
and SANs. The `san` mapping recognizes `dns`, `uri`, `email`, and `ip`.
Optional extensions map dotted OIDs to `(x509.ExtensionType, critical)` pairs.
The issuer supplies the CA identity, Basic Constraints, and key identifiers.
The result is an `Artifact` containing a PEM or DER leaf certificate.

## AEO Summary

- Package: `tba-provider-certificate-issuer-x509`
- Layer: `20-providers`
- Responsibility: Generic CSR-based X.509 leaf certificate issuer.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-certificate-issuer-x509/src/tba_provider_certificate_issuer_x509/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-provider-certificate-issuer-x509` for this responsibility: Generic CSR-based X.509 leaf certificate issuer. Its `20-providers` placement keeps replaceable environment implementations separate from capability orchestration, storage table ownership, or HTTP routing.

## Installation

Install the selected PyPI release of `tba-provider-certificate-issuer-x509`:

```bash
uv pip install tba-provider-certificate-issuer-x509
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/20-providers/tba-provider-certificate-issuer-x509
```

## Quick start

Build the package from the repository root:

```bash
uv build --wheel pkgs/20-providers/tba-provider-certificate-issuer-x509
```

## Usage

The following public-entry-point example belongs to `tba-provider-certificate-issuer-x509`. Generic CSR-based X.509 leaf certificate issuer. Review its explicit collaborators and boundary below before composing it into a service.

```python
import tba_provider_certificate_issuer_x509

print(tba_provider_certificate_issuer_x509.__name__)
```

## Package Boundary

`tba-provider-certificate-issuer-x509` belongs to `20-providers` and owns replaceable environment implementations: Generic CSR-based X.509 leaf certificate issuer.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-certificate-issuer-x509/src/tba_provider_certificate_issuer_x509/__init__.py). Public exports include `InvalidCertificateRequest`, `X509CertificateIssuer`, `X509IssuerConfig`.

Keep capability orchestration, storage table ownership, or HTTP routing in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

Explicit construction inputs and collaborators for `tba-provider-certificate-issuer-x509`:

- `X509CertificateIssuer` construction inputs: `config`, `clock`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-certificate-issuer-x509/src/tba_provider_certificate_issuer_x509/issuer.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

## Operations and readiness

`tba-provider-certificate-issuer-x509` exposes replaceable environment implementations. Public operations found in its source:

- `X509IssuerConfig.from_pem` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-certificate-issuer-x509/src/tba_provider_certificate_issuer_x509/config.py).
- `X509CertificateIssuer.supports` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-certificate-issuer-x509/src/tba_provider_certificate_issuer_x509/issuer.py).
- `X509CertificateIssuer.issue` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-certificate-issuer-x509/src/tba_provider_certificate_issuer_x509/issuer.py).
- `X509CertificateIssuer.issue_certificate` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-certificate-issuer-x509/src/tba_provider_certificate_issuer_x509/issuer.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-provider-certificate-issuer-x509`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

Other direct consumers include [tba-app-backend-wic-ca](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-wic-ca/README.md).

## Non-goals

`tba-provider-certificate-issuer-x509` does not take ownership of capability orchestration, storage table ownership, or HTTP routing.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

Declared local runtime dependencies:

- [tba-bases-certificate](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-certificate/README.md)
- [tba-contracts-security-trust](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-security-trust/README.md)

Direct downstream consumers:

- [tba-app-backend-wic-ca](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-wic-ca/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/20-providers/tba-provider-certificate-issuer-x509)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-certificate-issuer-x509/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-certificate-issuer-x509/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-certificate-issuer-x509/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-provider-certificate-issuer-x509/)

## Governance

`tba-provider-certificate-issuer-x509` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `20-providers` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

Exercise native WIC issuance and WIT/WPT runtime composition from the repository root:

```bash
uv run --extra test pytest pkgs/120-tests/tba-tests-workload-composition/tests/test_native_wimse_services.py
```
