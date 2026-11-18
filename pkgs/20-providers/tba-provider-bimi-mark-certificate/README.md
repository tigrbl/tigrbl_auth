# tba-provider-bimi-mark-certificate

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-bimi-mark-certificate/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-bimi-mark-certificate/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-provider-bimi-mark-certificate%3D%3D0.4.0.dev3/pkgs/20-providers/tba-provider-bimi-mark-certificate/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-provider-bimi-mark-certificate%3D%3D0.4.0.dev3/pkgs/20-providers/tba-provider-bimi-mark-certificate/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/20-providers"><img alt="Layer: 20 providers" src="https://img.shields.io/badge/Layer-20%20providers-0a7f5a"></a>
<a href="https://pypi.org/project/tba-provider-bimi-mark-certificate/"><img alt="PyPI version for tba-provider-bimi-mark-certificate" src="https://img.shields.io/pypi/v/tba-provider-bimi-mark-certificate?label=tba-provider-bimi-mark-certificate%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-provider-bimi-mark-certificate"><img alt="Monthly PyPI downloads for tba-provider-bimi-mark-certificate" src="https://static.pepy.tech/badge/tba-provider-bimi-mark-certificate/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-bimi-mark-certificate/README.md"><img alt="README hits for tba-provider-bimi-mark-certificate" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-bimi-mark-certificate/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-bimi-mark-certificate/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

BIMI Mark Certificate path and evidence verification.

`MarkCertificatePathBackend` accepts an explicit set of RFC 6962 CT log public
keys in PEM format and a callable that supplies CRL bytes by distribution-point
URL. It validates the X.509 path against BIMI-scoped anchors, verifies signed
CRL coverage for the leaf and intermediates, and verifies at least one
embedded SCT against the configured keys. Callers configure which roots and
logs they trust and how they obtain fresh CRLs.

The provider delegates PKIX, CRL, and SCT verification to
`tba-provider-certificate-evidence`. This package applies the Mark Certificate
algorithm and EKU rules and scopes the permitted trust anchors.

Supply a TBA `TrustAnchorProviderPort` to use the backend directly as a
`CertificatePathValidatorPort`. To use existing
`ProfiledCertificatePathValidator` dispatch, register the callable backend
under `CertificateProfile.BIMI_MARK`. The dispatcher's leaf status provider is
an additional check in that composition. The backend performs its own
request-local evidence verification in both cases.

The backend uses supplied CRLs and performs no HTTP requests. A missing fresh
CRL or an unconfigured CT log can yield an indeterminate decision. The provider
doesn't use the system Web PKI trust store for Mark Certificates.

## AEO Summary

- Package: `tba-provider-bimi-mark-certificate`
- Layer: `20-providers`
- Responsibility: BIMI Mark Certificate path and evidence verification.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-bimi-mark-certificate/src/tba_provider_bimi_mark_certificate/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-provider-bimi-mark-certificate` for this responsibility: BIMI Mark Certificate path and evidence verification. Its `20-providers` placement keeps replaceable environment implementations separate from capability orchestration, storage table ownership, or HTTP routing.

## Installation

Install the selected PyPI release of `tba-provider-bimi-mark-certificate`:

```bash
uv pip install tba-provider-bimi-mark-certificate
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/20-providers/tba-provider-bimi-mark-certificate
```

## Quick start

Build the package from the repository root.

```bash
uv build --wheel pkgs/20-providers/tba-provider-bimi-mark-certificate
```

## Usage

The following public-entry-point example belongs to `tba-provider-bimi-mark-certificate`. BIMI Mark Certificate path and evidence verification. Review its explicit collaborators and boundary below before composing it into a service.

```python
import tba_provider_bimi_mark_certificate

print(tba_provider_bimi_mark_certificate.__name__)
```

## Package Boundary

`tba-provider-bimi-mark-certificate` belongs to `20-providers` and owns replaceable environment implementations: BIMI Mark Certificate path and evidence verification.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-bimi-mark-certificate/src/tba_provider_bimi_mark_certificate/__init__.py). Public exports include `CrlSource`, `MarkCertificatePathBackend`.

Keep capability orchestration, storage table ownership, or HTTP routing in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

Explicit construction inputs and collaborators for `tba-provider-bimi-mark-certificate`:

- `MarkCertificatePathBackend` construction inputs: `crl_source`, `ct_logs`, `anchors`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-bimi-mark-certificate/src/tba_provider_bimi_mark_certificate/path.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

## Operations and readiness

`tba-provider-bimi-mark-certificate` exposes replaceable environment implementations. Public operations found in its source:

- `MarkCertificatePathBackend.validate` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-bimi-mark-certificate/src/tba_provider_bimi_mark_certificate/path.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-provider-bimi-mark-certificate`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

## Non-goals

`tba-provider-bimi-mark-certificate` does not take ownership of capability orchestration, storage table ownership, or HTTP routing.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

Declared local runtime dependencies:

- [tba-contracts-security-trust](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-security-trust/README.md)
- [tba-provider-certificate-evidence](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-certificate-evidence/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/20-providers/tba-provider-bimi-mark-certificate)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-bimi-mark-certificate/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-bimi-mark-certificate/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-bimi-mark-certificate/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-provider-bimi-mark-certificate/)

## Governance

`tba-provider-bimi-mark-certificate` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `20-providers` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

Check that the build produces a wheel with the package version declared in `pyproject.toml`.
