# tba-app-backend-wit-issuance

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-wit-issuance/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-wit-issuance/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-app-backend-wit-issuance%3D%3D0.4.0.dev3/pkgs/90-backend-apps/tba-app-backend-wit-issuance/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-app-backend-wit-issuance%3D%3D0.4.0.dev3/pkgs/90-backend-apps/tba-app-backend-wit-issuance/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/90-backend-apps"><img alt="Layer: 90 backend apps" src="https://img.shields.io/badge/Layer-90%20backend%20apps-0a7f5a"></a>
<a href="https://pypi.org/project/tba-app-backend-wit-issuance/"><img alt="PyPI version for tba-app-backend-wit-issuance" src="https://img.shields.io/pypi/v/tba-app-backend-wit-issuance?label=tba-app-backend-wit-issuance%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-app-backend-wit-issuance"><img alt="Monthly PyPI downloads for tba-app-backend-wit-issuance" src="https://static.pepy.tech/badge/tba-app-backend-wit-issuance/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-wit-issuance/README.md"><img alt="README hits for tba-app-backend-wit-issuance" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-wit-issuance/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-wit-issuance/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Deployable WIMSE WIT issuance with explicit enrollment and key policy.

## Quick start

Compose an app with deployment-owned signing and enrollment dependencies:

```python
from tba_app_backend_wit_issuance import WitIssuerConfig, build_app

def create_app(signer, authenticate, resolve_identity, authorize_confirmation_key):
    return build_app(
        WitIssuerConfig(
            trust_domain="example.org",
            issuer="https://issuer.example.org",
            key_reference="workload-issuer",
            key_id="issuer-2026",
            algorithm="EdDSA",
        ),
        signer=signer,
        authenticate=authenticate,
        resolve_identity=resolve_identity,
        authorize_confirmation_key=authorize_confirmation_key,
    )
```

Serve the returned `TigrblApp` with the deployment's ASGI runner. The app
mounts `POST /wit/issue`; its JSON body is `{"confirmation_jwk": {...}}`.
The authenticated principal is resolved to an enrolled identity, and the
proposed public key must be explicitly authorized. The workload identity is
never selected from the request body. Success returns
`{"workload_identity_token": "<compact JWT>"}` with `Cache-Control: no-store`.
The caller retains its workload private key; the issuer receives only its public JWK.

Build from the repository root:

```bash
uv build --wheel pkgs/90-backend-apps/tba-app-backend-wit-issuance
```

## Verification

```bash
uv run --extra test pytest pkgs/120-tests/tba-tests-workload-composition/tests/test_wit_wpt_services.py
```
