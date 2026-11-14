# tba-router-oauth-protected-resource-metadata

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-oauth-protected-resource-metadata/pyproject.toml"><img alt="Checkout: 0.4.0.dev2" src="https://img.shields.io/badge/Checkout-0.4.0.dev2-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-oauth-protected-resource-metadata/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-oauth-protected-resource-metadata/pyproject.toml"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/80-routers"><img alt="Layer: 80 routers" src="https://img.shields.io/badge/Layer-80%20routers-0a7f5a"></a>
<a href="https://pypi.org/project/tba-router-oauth-protected-resource-metadata/"><img alt="PyPI version for tba-router-oauth-protected-resource-metadata" src="https://img.shields.io/pypi/v/tba-router-oauth-protected-resource-metadata?label=tba-router-oauth-protected-resource-metadata%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-router-oauth-protected-resource-metadata"><img alt="Monthly PyPI downloads for tba-router-oauth-protected-resource-metadata" src="https://static.pepy.tech/badge/tba-router-oauth-protected-resource-metadata/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-oauth-protected-resource-metadata/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Bind OAuth protected-resource metadata to a Tigrbl HTTP route.

## Quick start

Install the version used by this example.

```bash
python -m pip install "tba-router-oauth-protected-resource-metadata==0.4.0.dev2"
```

Save the following as `quickstart.py` and run `python quickstart.py`. The assertions should pass.

```python
from tigrbl import TigrblApp
from tba_router_oauth_protected_resource_metadata import (
    build_protected_resource_metadata_router,
    include_protected_resource_metadata,
)

async def metadata(request):
    return {"resource": "https://api.example",
            "authorization_servers": ["https://issuer.example"]}

app = TigrblApp()
router = build_protected_resource_metadata_router(protected_resource_metadata=metadata)
include_protected_resource_metadata(app, router, enabled=True)
assert any(
    (getattr(route, "path", None) or getattr(route, "path_template", None))
    == "/.well-known/oauth-protected-resource"
    for route in app.router.routes
)
```

## When to use it

Supply an async handler backed by your resource metadata configuration. The router exposes `GET /.well-known/oauth-protected-resource`. The protocol and runtime layers own metadata semantics and deployment policy.

## Verification

See the [related repository tests](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-oauth/tests/conformance/production/test_rfc9728_protected_resource_metadata.py) for the implementation scope covered by this example.

[Workspace and package catalog](https://github.com/tigrbl/tigrbl_auth#package-catalog) · [tba-app-backend-public](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/90-backend-apps/tba-app-backend-public#readme) · [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues) · [Repository license](https://github.com/tigrbl/tigrbl_auth/blob/master/LICENSE)
