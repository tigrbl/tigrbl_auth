# TBA concrete TOTP

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-totp/pyproject.toml"><img alt="Checkout: 0.1.0" src="https://img.shields.io/badge/Checkout-0.1.0-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-totp/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-totp/pyproject.toml"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/10-concrete"><img alt="Layer: 10 concrete" src="https://img.shields.io/badge/Layer-10%20concrete-0a7f5a"></a>
<a href="https://pypi.org/project/tba-concrete-totp/"><img alt="PyPI version for tba-concrete-totp" src="https://img.shields.io/pypi/v/tba-concrete-totp?label=tba-concrete-totp%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-concrete-totp"><img alt="Monthly PyPI downloads for tba-concrete-totp" src="https://static.pepy.tech/badge/tba-concrete-totp/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-totp/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

HOTP and TOTP primitives for Python 3.10 and later. The package uses the standard library. Call `hotp` to generate a code from a key and counter, or `match_step` to find the matching step for a supplied TOTP code. Pass the last accepted step as `after_step` and persist the new value atomically with successful authentication.

See [RFC 4226](https://www.rfc-editor.org/rfc/rfc4226) and [RFC 6238](https://www.rfc-editor.org/rfc/rfc6238).

## Quick start

Build the package from the repository root.

```bash
uv build --wheel pkgs/10-concrete/tba-concrete-totp
```

## Verification

Check that the build produces a wheel with the package version declared in `pyproject.toml`.
