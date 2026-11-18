# tba-app-backend-wic-ca

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-wic-ca/pyproject.toml"><img alt="Checkout: 0.4.0.dev2" src="https://img.shields.io/badge/Checkout-0.4.0.dev2-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-wic-ca/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-wic-ca/pyproject.toml"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/90-backend-apps"><img alt="Layer: 90 backend apps" src="https://img.shields.io/badge/Layer-90%20backend%20apps-0a7f5a"></a>
<a href="https://pypi.org/project/tba-app-backend-wic-ca/"><img alt="PyPI version for tba-app-backend-wic-ca" src="https://img.shields.io/pypi/v/tba-app-backend-wic-ca?label=tba-app-backend-wic-ca%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-app-backend-wic-ca"><img alt="Monthly PyPI downloads for tba-app-backend-wic-ca" src="https://static.pepy.tech/badge/tba-app-backend-wic-ca/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-wic-ca/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

In your deployment module, construct the ASGI application with
`build_app(WicCaSettings(...), authenticate=..., resolve_identity=...)`.
Settings point to the CA certificate and private key PEM files and set the
WIMSE trust domain and leaf lifetime. The authentication callback checks the
request's deployment-provided credential and returns an enrollment principal.
The identity resolver receives that principal and returns its authorized
`wimse://` URI or `None`. Serve the app over an authenticated transport.
Mount the WIT router separately if the deployment also issues workload tokens.

## Quick start

Build the package from the repository root:

```bash
uv build --wheel pkgs/90-backend-apps/tba-app-backend-wic-ca
```

## Verification

Exercise native WIC issuance and WIT/WPT runtime composition from the repository root:

```bash
uv run --extra test pytest pkgs/120-tests/tba-tests-workload-composition/tests/test_native_wimse_services.py
```
