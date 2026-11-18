# tba-codec-jcs

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/03-codecs/tba-codec-jcs/pyproject.toml"><img alt="Checkout: 0.4.0.dev2" src="https://img.shields.io/badge/Checkout-0.4.0.dev2-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/03-codecs/tba-codec-jcs/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/03-codecs/tba-codec-jcs/pyproject.toml"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/03-codecs"><img alt="Layer: 03 codecs" src="https://img.shields.io/badge/Layer-03%20codecs-0a7f5a"></a>
<a href="https://pypi.org/project/tba-codec-jcs/"><img alt="PyPI version for tba-codec-jcs" src="https://img.shields.io/pypi/v/tba-codec-jcs?label=tba-codec-jcs%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-codec-jcs"><img alt="Monthly PyPI downloads for tba-codec-jcs" src="https://static.pepy.tech/badge/tba-codec-jcs/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/03-codecs/tba-codec-jcs/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Use `canonicalize` for JSON values or `canonicalize_json` for raw JSON. Both produce canonical UTF-8 bytes using the rfc8785 library. The raw JSON entry point rejects duplicate keys.

This package owns TBA’s strict JCS API. New callers should import from `tba_codec_jcs`.
The [RFC 8785 conformance suite](../../../tests/conformance/backlog/test_rfc8785_jcs.py) verifies this package.

[Specification](https://www.rfc-editor.org/rfc/rfc8785.html)

## Quick start

Build the package from the repository root.

```bash
uv build --wheel pkgs/03-codecs/tba-codec-jcs
```

## Verification

Check that the build produces a wheel with the package version declared in `pyproject.toml`.
