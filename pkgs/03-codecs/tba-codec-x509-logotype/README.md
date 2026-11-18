# tba-codec-x509-logotype

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/03-codecs/tba-codec-x509-logotype/pyproject.toml"><img alt="Checkout: 0.4.0.dev2" src="https://img.shields.io/badge/Checkout-0.4.0.dev2-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/03-codecs/tba-codec-x509-logotype/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/03-codecs/tba-codec-x509-logotype/pyproject.toml"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/03-codecs"><img alt="Layer: 03 codecs" src="https://img.shields.io/badge/Layer-03%20codecs-0a7f5a"></a>
<a href="https://pypi.org/project/tba-codec-x509-logotype/"><img alt="PyPI version for tba-codec-x509-logotype" src="https://img.shields.io/pypi/v/tba-codec-x509-logotype?label=tba-codec-x509-logotype%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-codec-x509-logotype"><img alt="Monthly PyPI downloads for tba-codec-x509-logotype" src="https://static.pepy.tech/badge/tba-codec-x509-logotype/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/03-codecs/tba-codec-x509-logotype/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
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

## Quick start

Build the package from the repository root.

```bash
uv build --wheel pkgs/03-codecs/tba-codec-x509-logotype
```

## Verification

Check that the build produces a wheel with the package version declared in `pyproject.toml`.
