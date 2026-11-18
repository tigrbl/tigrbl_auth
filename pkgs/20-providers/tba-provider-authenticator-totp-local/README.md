# TBA local TOTP authenticator

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-authenticator-totp-local/pyproject.toml"><img alt="Checkout: 0.1.1.dev1" src="https://img.shields.io/badge/Checkout-0.1.1.dev1-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-authenticator-totp-local/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-provider-authenticator-totp-local%3D%3D0.1.1.dev1/pkgs/20-providers/tba-provider-authenticator-totp-local/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-provider-authenticator-totp-local%3D%3D0.1.1.dev1/pkgs/20-providers/tba-provider-authenticator-totp-local/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/20-providers"><img alt="Layer: 20 providers" src="https://img.shields.io/badge/Layer-20%20providers-0a7f5a"></a>
<a href="https://pypi.org/project/tba-provider-authenticator-totp-local/"><img alt="PyPI version for tba-provider-authenticator-totp-local" src="https://img.shields.io/pypi/v/tba-provider-authenticator-totp-local?label=tba-provider-authenticator-totp-local%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-provider-authenticator-totp-local"><img alt="Monthly PyPI downloads for tba-provider-authenticator-totp-local" src="https://static.pepy.tech/badge/tba-provider-authenticator-totp-local/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-authenticator-totp-local/README.md"><img alt="README hits for tba-provider-authenticator-totp-local" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-authenticator-totp-local/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-authenticator-totp-local/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Generate a Base32 secret with `new_secret()` and pass it with the account and issuer labels to `provisioning_uri()`. The URI uses the SHA-1, six-digit, 30-second profile understood by authenticator apps.

Use `TotpLocalAuthenticator().verify_step()` to verify a code and obtain the matched step. Store the secret encrypted and advance the last accepted step in the same transaction as successful verification. Each installation controls its own secret storage, retry limits, and clock-drift policy.

## Quick start

Build the package from the repository root.

```bash
uv build --wheel pkgs/20-providers/tba-provider-authenticator-totp-local
```

## Verification

Check that the build produces a wheel with the package version declared in `pyproject.toml`.
