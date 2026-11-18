# tba-app-backend-wpt-verifier

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-wpt-verifier/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-wpt-verifier/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-app-backend-wpt-verifier%3D%3D0.4.0.dev3/pkgs/90-backend-apps/tba-app-backend-wpt-verifier/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-app-backend-wpt-verifier%3D%3D0.4.0.dev3/pkgs/90-backend-apps/tba-app-backend-wpt-verifier/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/90-backend-apps"><img alt="Layer: 90 backend apps" src="https://img.shields.io/badge/Layer-90%20backend%20apps-0a7f5a"></a>
<a href="https://pypi.org/project/tba-app-backend-wpt-verifier/"><img alt="PyPI version for tba-app-backend-wpt-verifier" src="https://img.shields.io/pypi/v/tba-app-backend-wpt-verifier?label=tba-app-backend-wpt-verifier%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-app-backend-wpt-verifier"><img alt="Monthly PyPI downloads for tba-app-backend-wpt-verifier" src="https://static.pepy.tech/badge/tba-app-backend-wpt-verifier/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-wpt-verifier/README.md"><img alt="README hits for tba-app-backend-wpt-verifier" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-wpt-verifier/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-wpt-verifier/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Deployable delegated WIT/WPT verification with recipient policy and replay protection.

## Quick start

```python
from tba_app_backend_wpt_verifier import WptVerifierSettings, build_app

def create_app(trusted_keys, replay_store, authenticate, authorize_verification):
    return build_app(
        WptVerifierSettings(
            audience="https://resource.example.org/work",
            trust_by_domain=trusted_keys,
            required_token_headers=("txn-token",),
        ),
        replay_store=replay_store,
        authenticate=authenticate,
        authorize_verification=authorize_verification,
    )
```

`trusted_keys` maps trusted WIMSE subject domains to public issuer JWKs. The
deployment supplies caller authentication/authorization and a synchronous atomic
`ReplayCheckPort` store shared by all verifier replicas. No keys are fetched from
caller-provided URLs and no default permissive policy or in-memory replay store
is selected by this app. Serve the returned `TigrblApp` with an ASGI runner.

The app composes `tba-router-wpt-verification` at `POST /wpt/verify`.
See that package's request/response contract. A successful verification consumes
the proof's replay identifier. The recipient uses the result for the original
request and performs its own resource authorization; this API is not a
non-consuming inspection endpoint. A caller must not choose a replacement
audience or issuer keys in its request.

Build from the repository root:

```bash
uv build --wheel pkgs/90-backend-apps/tba-app-backend-wpt-verifier
```

## Verification

```bash
uv run --extra test pytest pkgs/120-tests/tba-tests-workload-composition/tests/test_wit_wpt_services.py
```
