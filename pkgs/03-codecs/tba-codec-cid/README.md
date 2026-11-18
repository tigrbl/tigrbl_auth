# tba-codec-cid

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/03-codecs/tba-codec-cid/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/03-codecs/tba-codec-cid/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-codec-cid%3D%3D0.4.0.dev3/pkgs/03-codecs/tba-codec-cid/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-codec-cid%3D%3D0.4.0.dev3/pkgs/03-codecs/tba-codec-cid/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/03-codecs"><img alt="Layer: 03 codecs" src="https://img.shields.io/badge/Layer-03%20codecs-0a7f5a"></a>
<a href="https://pypi.org/project/tba-codec-cid/"><img alt="PyPI version for tba-codec-cid" src="https://img.shields.io/pypi/v/tba-codec-cid?label=tba-codec-cid%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-codec-cid"><img alt="Monthly PyPI downloads for tba-codec-cid" src="https://static.pepy.tech/badge/tba-codec-cid/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/03-codecs/tba-codec-cid/README.md"><img alt="README hits for tba-codec-cid" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/03-codecs/tba-codec-cid/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/03-codecs/tba-codec-cid/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Use `Cid.from_bytes` or `Cid.from_text` to parse a content identifier. The codec checks canonical unsigned varints and multihash length. Text support covers base58btc. Callers choose which codec, hash and digest length they trust.

[Specification](https://specs.ipfs.tech/cid/)

## Quick start

Build the package from the repository root.

```bash
uv build --wheel pkgs/03-codecs/tba-codec-cid
```

## Verification

Check that the build produces a wheel with the package version declared in `pyproject.toml`.
