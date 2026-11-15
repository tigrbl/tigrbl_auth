# TbA interop matrix validation

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-interop-wimse-matrix/pyproject.toml"><img alt="Checkout: 0.4.0.dev2" src="https://img.shields.io/badge/Checkout-0.4.0.dev2-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-interop-wimse-matrix/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-interop-wimse-matrix/pyproject.toml"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/120-tests"><img alt="Layer: 120 tests" src="https://img.shields.io/badge/Layer-120%20tests-0a7f5a"></a>
<a href="https://pypi.org/project/tba-tests-interop-wimse-matrix/"><img alt="PyPI version for tba-tests-interop-wimse-matrix" src="https://img.shields.io/pypi/v/tba-tests-interop-wimse-matrix?label=tba-tests-interop-wimse-matrix%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-tests-interop-wimse-matrix"><img alt="Monthly PyPI downloads for tba-tests-interop-wimse-matrix" src="https://static.pepy.tech/badge/tba-tests-interop-wimse-matrix/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-interop-wimse-matrix/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

T0–T2 checks for the [interop distribution](https://github.com/tigrbl/tba-tests-interop-wimse).

## Quick start

Set `TBA_WIMSE_INTEROP_PACKAGE` to the package at the revision in
`interop-revision.txt` and `TBA_WIMSE_INTEROP_WHEEL` to its built wheel.
From the TbA checkout, run:

```sh
uv run --locked --extra test pytest pkgs/120-tests/tba-tests-interop-wimse-matrix/tests
```

## Verification

The TbA WIMSE matrix validation workflow runs the catalog, inventory, evidence,
and installed-wheel checks against the pinned interop revision.
