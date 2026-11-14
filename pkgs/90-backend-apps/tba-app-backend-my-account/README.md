# tba-app-backend-my-account

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-my-account/pyproject.toml"><img alt="Checkout: 0.4.0.dev2" src="https://img.shields.io/badge/Checkout-0.4.0.dev2-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-my-account/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-my-account/pyproject.toml"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/90-backend-apps"><img alt="Layer: 90 backend apps" src="https://img.shields.io/badge/Layer-90%20backend%20apps-0a7f5a"></a>
<a href="https://pypi.org/project/tba-app-backend-my-account/"><img alt="PyPI version for tba-app-backend-my-account" src="https://img.shields.io/pypi/v/tba-app-backend-my-account?label=tba-app-backend-my-account%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-app-backend-my-account"><img alt="Monthly PyPI downloads for tba-app-backend-my-account" src="https://static.pepy.tech/badge/tba-app-backend-my-account/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-my-account/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

End-user self-service account API front door for TBA.

This package exposes the authenticated current subject's account surface:

- `GET /account/profile`
- `PATCH /account/profile`
- `GET /account/sessions`
- `DELETE /account/sessions/{session_id}`
- `GET /account/authorized-apps`
- `DELETE /account/authorized-apps/{client_id}`
- `GET /account/consents`
- `DELETE /account/consents/{consent_id}`
- `POST /account/password/change`

It does not expose platform administration, tenant-wide user management, RPC,
or table CRUD. All account operations are scoped to the authenticated end user.

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This command uses the published package in an isolated Python 3.12 environment.

```python
from tba_app_backend_my_account import MyAccountMutationOut

assert callable(MyAccountMutationOut)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-app-backend-my-account==0.4.0.dev2" python quickstart.py
```

The import and assertion succeed when the MyAccountMutationOut entry point is available.

## Verification

The quick start was run with the pinned distribution from PyPI and its declared dependencies. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-my-account/src/tba_app_backend_my_account/__init__.py).
