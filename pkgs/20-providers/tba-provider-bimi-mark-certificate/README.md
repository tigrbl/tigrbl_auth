# tba-provider-bimi-mark-certificate

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-bimi-mark-certificate/pyproject.toml"><img alt="Checkout: 0.4.0.dev2" src="https://img.shields.io/badge/Checkout-0.4.0.dev2-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-bimi-mark-certificate/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-bimi-mark-certificate/pyproject.toml"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/20-providers"><img alt="Layer: 20 providers" src="https://img.shields.io/badge/Layer-20%20providers-0a7f5a"></a>
<a href="https://pypi.org/project/tba-provider-bimi-mark-certificate/"><img alt="PyPI version for tba-provider-bimi-mark-certificate" src="https://img.shields.io/pypi/v/tba-provider-bimi-mark-certificate?label=tba-provider-bimi-mark-certificate%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-provider-bimi-mark-certificate"><img alt="Monthly PyPI downloads for tba-provider-bimi-mark-certificate" src="https://static.pepy.tech/badge/tba-provider-bimi-mark-certificate/month"></a>
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

## Quick start

Build the package from the repository root.

```bash
uv build --wheel pkgs/20-providers/tba-provider-bimi-mark-certificate
```

## Verification

Check that the build produces a wheel with the package version declared in `pyproject.toml`.
