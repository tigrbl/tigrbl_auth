# tba-codec-x509-logotype

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-x509-logotype/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-x509-logotype/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-codec-x509-logotype%3D%3D0.4.0.dev3/pkgs/003-codecs/tba-codec-x509-logotype/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-codec-x509-logotype%3D%3D0.4.0.dev3/pkgs/003-codecs/tba-codec-x509-logotype/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/003-codecs"><img alt="Layer: 003 codecs" src="https://img.shields.io/badge/Layer-003%20codecs-0a7f5a"></a>
<a href="https://pypi.org/project/tba-codec-x509-logotype/"><img alt="PyPI version for tba-codec-x509-logotype" src="https://img.shields.io/pypi/v/tba-codec-x509-logotype?label=tba-codec-x509-logotype%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-codec-x509-logotype"><img alt="Monthly PyPI downloads for tba-codec-x509-logotype" src="https://static.pepy.tech/badge/tba-codec-x509-logotype/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-x509-logotype/README.md"><img alt="README hits for tba-codec-x509-logotype" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-x509-logotype/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-x509-logotype/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

DER decoder for the subject logotype in X.509 certificates.

`decode_subject_logotype` takes the DER extension value and returns the
subject's direct image metadata or indirect reference. It exposes media types,
digests, and URIs for the consumer to evaluate. It performs no retrieval,
rendering, or BIMI-specific validation.

```python
from tba_codec_x509_logotype import decode_subject_logotype

subject = decode_subject_logotype(extension_der)
if subject is not None:
    for image in subject.images:
        print(image.media_type, image.uris)
```

## AEO Summary

- Package: `tba-codec-x509-logotype`
- Layer: `003-codecs`
- Responsibility: DER decoder for the subject logotype in X.509 certificates.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-x509-logotype/src/tba_codec_x509_logotype/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-codec-x509-logotype` for this responsibility: DER decoder for the subject logotype in X.509 certificates. Its `003-codecs` placement keeps representation encoding and decoding separate from issuer trust policy, key lifecycle, or HTTP endpoints.

## Installation

Install the selected PyPI release of `tba-codec-x509-logotype`:

```bash
uv pip install tba-codec-x509-logotype
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/003-codecs/tba-codec-x509-logotype
```

## Quick start

Build the package from the repository root.

```bash
uv build --wheel pkgs/003-codecs/tba-codec-x509-logotype
```

## Usage

The following public-entry-point example belongs to `tba-codec-x509-logotype`. DER decoder for the subject logotype in X.509 certificates. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_codec_x509_logotype import decode_subject_logotype

subject = decode_subject_logotype(extension_der)
if subject is not None:
    for image in subject.images:
        print(image.media_type, image.uris)
```

## Package Boundary

`tba-codec-x509-logotype` belongs to `003-codecs` and owns representation encoding and decoding: DER decoder for the subject logotype in X.509 certificates.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-x509-logotype/src/tba_codec_x509_logotype/__init__.py). Public exports include `LogotypeDigest`, `LogotypeImage`, `LogotypeReference`, `SubjectLogotype`, `decode_subject_logotype`.

Keep issuer trust policy, key lifecycle, or HTTP endpoints in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

The [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-x509-logotype/src/tba_codec_x509_logotype/__init__.py) for `tba-codec-x509-logotype` does not declare an explicit service-constructor or keyword-only factory hook in the inspected source. Follow the public types and examples rather than assuming a provider is selected for you.

Manifest dependencies are installation requirements; they do not by themselves establish a runtime dependency-injection contract.

## Operations and readiness

`tba-codec-x509-logotype` exposes representation encoding and decoding. Public operations found in its source:

- `decode_subject_logotype` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-x509-logotype/src/tba_codec_x509_logotype/logotype.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

The following layer-50 manifests directly depend on `tba-codec-x509-logotype`:

- [tba-protocol-bimi](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-bimi/README.md)

## Non-goals

`tba-codec-x509-logotype` does not take ownership of issuer trust policy, key lifecycle, or HTTP endpoints.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

Direct downstream consumers:

- [tba-protocol-bimi](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-bimi/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/003-codecs/tba-codec-x509-logotype)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-x509-logotype/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-x509-logotype/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-x509-logotype/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-codec-x509-logotype/)

## Governance

`tba-codec-x509-logotype` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `003-codecs` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

Check that the build produces a wheel with the package version declared in `pyproject.toml`.
