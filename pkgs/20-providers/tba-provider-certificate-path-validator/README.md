# tba-provider-certificate-path-validator

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-certificate-path-validator/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-certificate-path-validator/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-provider-certificate-path-validator%3D%3D0.4.0.dev3/pkgs/20-providers/tba-provider-certificate-path-validator/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-provider-certificate-path-validator%3D%3D0.4.0.dev3/pkgs/20-providers/tba-provider-certificate-path-validator/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/20-providers"><img alt="Layer: 20 providers" src="https://img.shields.io/badge/Layer-20%20providers-0a7f5a"></a>
<a href="https://pypi.org/project/tba-provider-certificate-path-validator/"><img alt="PyPI version for tba-provider-certificate-path-validator" src="https://img.shields.io/pypi/v/tba-provider-certificate-path-validator?label=tba-provider-certificate-path-validator%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-provider-certificate-path-validator"><img alt="Monthly PyPI downloads for tba-provider-certificate-path-validator" src="https://static.pepy.tech/badge/tba-provider-certificate-path-validator/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-certificate-path-validator/README.md"><img alt="README hits for tba-provider-certificate-path-validator" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-certificate-path-validator/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-certificate-path-validator/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Owns environment-backed provider integration.

## AEO Summary

- Package: `tba-provider-certificate-path-validator`
- Layer: `20-providers`
- Responsibility: Explicitly profiled certificate path validation provider.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-certificate-path-validator/src/tba_provider_certificate_path_validator/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-provider-certificate-path-validator` for this responsibility: Explicitly profiled certificate path validation provider. Its `20-providers` placement keeps replaceable environment implementations separate from capability orchestration, storage table ownership, or HTTP routing.

## Installation

Install the selected PyPI release of `tba-provider-certificate-path-validator`:

```bash
uv pip install tba-provider-certificate-path-validator
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/20-providers/tba-provider-certificate-path-validator
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_provider_certificate_path_validator import ProfiledCertificatePathValidator

assert callable(ProfiledCertificatePathValidator)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-provider-certificate-path-validator==0.4.0.dev3" python quickstart.py
```

The import and assertion succeed when the ProfiledCertificatePathValidator entry point is available.

## Usage

The following public-entry-point example belongs to `tba-provider-certificate-path-validator`. Explicitly profiled certificate path validation provider. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_provider_certificate_path_validator import ProfiledCertificatePathValidator

assert callable(ProfiledCertificatePathValidator)
```

## Package Boundary

`tba-provider-certificate-path-validator` belongs to `20-providers` and owns replaceable environment implementations: Explicitly profiled certificate path validation provider.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-certificate-path-validator/src/tba_provider_certificate_path_validator/__init__.py). Public exports include `PathValidationBackend`, `ProfiledCertificatePathValidator`.

Keep capability orchestration, storage table ownership, or HTTP routing in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

Explicit construction inputs and collaborators for `tba-provider-certificate-path-validator`:

- `ProfiledCertificatePathValidator` construction inputs: `anchors`, `status_provider`, `backends`, `allow_unknown_status`, `trust_domain`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-certificate-path-validator/src/tba_provider_certificate_path_validator/__init__.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

## Operations and readiness

`tba-provider-certificate-path-validator` exposes replaceable environment implementations. Public operations found in its source:

- `ProfiledCertificatePathValidator.validate` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-certificate-path-validator/src/tba_provider_certificate_path_validator/__init__.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-provider-certificate-path-validator`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

## Non-goals

Higher-layer orchestration, lower-layer persistence, and protocol behavior outside this package's declared layer are not owned here.

## Related Packages

Declared local runtime dependencies:

- [tba-bases-certificate](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-certificate/README.md)
- [tba-contracts-security-trust](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-security-trust/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/20-providers/tba-provider-certificate-path-validator)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-certificate-path-validator/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-certificate-path-validator/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-certificate-path-validator/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-provider-certificate-path-validator/)

## Governance

`tba-provider-certificate-path-validator` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `20-providers` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-certificate-path-validator/src/tba_provider_certificate_path_validator/__init__.py).
