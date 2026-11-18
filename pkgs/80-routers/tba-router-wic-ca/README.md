# tba-router-wic-ca

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-wic-ca/pyproject.toml"><img alt="Checkout: 0.4.0.dev2" src="https://img.shields.io/badge/Checkout-0.4.0.dev2-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-wic-ca/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-wic-ca/pyproject.toml"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/80-routers"><img alt="Layer: 80 routers" src="https://img.shields.io/badge/Layer-80%20routers-0a7f5a"></a>
<a href="https://pypi.org/project/tba-router-wic-ca/"><img alt="PyPI version for tba-router-wic-ca" src="https://img.shields.io/pypi/v/tba-router-wic-ca?label=tba-router-wic-ca%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-router-wic-ca"><img alt="Monthly PyPI downloads for tba-router-wic-ca" src="https://static.pepy.tech/badge/tba-router-wic-ca/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-wic-ca/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Mount `build_wic_ca_router(service=..., authenticate=...)` on a Tigrbl app.
`POST /wic/issue` accepts JSON with `csr_pem` and returns `certificate_pem`.
The async authenticator must return a trusted enrollment principal or `None`.

## Quick start

Build the package from the repository root:

```bash
uv build --wheel pkgs/80-routers/tba-router-wic-ca
```

## Verification

Exercise native WIC issuance and WIT/WPT runtime composition from the repository root:

```bash
uv run --extra test pytest pkgs/120-tests/tba-tests-workload-composition/tests/test_native_wimse_services.py
```
