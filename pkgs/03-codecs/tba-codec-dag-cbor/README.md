# tba-codec-dag-cbor

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/03-codecs/tba-codec-dag-cbor/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/03-codecs/tba-codec-dag-cbor/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-codec-dag-cbor%3D%3D0.4.0.dev3/pkgs/03-codecs/tba-codec-dag-cbor/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-codec-dag-cbor%3D%3D0.4.0.dev3/pkgs/03-codecs/tba-codec-dag-cbor/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/03-codecs"><img alt="Layer: 03 codecs" src="https://img.shields.io/badge/Layer-03%20codecs-0a7f5a"></a>
<a href="https://pypi.org/project/tba-codec-dag-cbor/"><img alt="PyPI version for tba-codec-dag-cbor" src="https://img.shields.io/pypi/v/tba-codec-dag-cbor?label=tba-codec-dag-cbor%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-codec-dag-cbor"><img alt="Monthly PyPI downloads for tba-codec-dag-cbor" src="https://static.pepy.tech/badge/tba-codec-dag-cbor/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/03-codecs/tba-codec-dag-cbor/README.md"><img alt="README hits for tba-codec-dag-cbor" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/03-codecs/tba-codec-dag-cbor/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/03-codecs/tba-codec-dag-cbor/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Use `encode` and `decode` for canonical DAG-CBOR. CID links use tag 42 and the binary identity prefix. Decoding rejects duplicate keys, trailing data and noncanonical encodings. Callers set message size limits and protocol constraints.

[Specification](https://ipld.io/specs/codecs/dag-cbor/spec/)

## Quick start

Build the package from the repository root.

```bash
uv build --wheel pkgs/03-codecs/tba-codec-dag-cbor
```

## Verification

Check that the build produces a wheel with the package version declared in `pyproject.toml`.
