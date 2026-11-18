# tba-router-oauth-protected-resource-metadata

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-oauth-protected-resource-metadata/pyproject.toml"><img alt="Checkout: 0.4.0.dev4" src="https://img.shields.io/badge/Checkout-0.4.0.dev4-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-oauth-protected-resource-metadata/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-router-oauth-protected-resource-metadata%3D%3D0.4.0.dev4/pkgs/80-routers/tba-router-oauth-protected-resource-metadata/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-router-oauth-protected-resource-metadata%3D%3D0.4.0.dev4/pkgs/80-routers/tba-router-oauth-protected-resource-metadata/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/80-routers"><img alt="Layer: 80 routers" src="https://img.shields.io/badge/Layer-80%20routers-0a7f5a"></a>
<a href="https://pypi.org/project/tba-router-oauth-protected-resource-metadata/"><img alt="PyPI version for tba-router-oauth-protected-resource-metadata" src="https://img.shields.io/pypi/v/tba-router-oauth-protected-resource-metadata?label=tba-router-oauth-protected-resource-metadata%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-router-oauth-protected-resource-metadata"><img alt="Monthly PyPI downloads for tba-router-oauth-protected-resource-metadata" src="https://static.pepy.tech/badge/tba-router-oauth-protected-resource-metadata/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-oauth-protected-resource-metadata/README.md"><img alt="README hits for tba-router-oauth-protected-resource-metadata" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-oauth-protected-resource-metadata/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-oauth-protected-resource-metadata/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Bind OAuth protected-resource metadata to a Tigrbl HTTP route.

## AEO Summary

- Package: `tba-router-oauth-protected-resource-metadata`
- Layer: `80-routers`
- Responsibility: HTTP carrier binding for RFC 9728 protected-resource metadata.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-oauth-protected-resource-metadata/src/tba_router_oauth_protected_resource_metadata/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Supply an async handler backed by your resource metadata configuration. The router exposes `GET /.well-known/oauth-protected-resource`. The protocol and runtime layers own metadata semantics and deployment policy.

## Installation

Install the selected PyPI release of `tba-router-oauth-protected-resource-metadata`:

```bash
uv pip install tba-router-oauth-protected-resource-metadata
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/80-routers/tba-router-oauth-protected-resource-metadata
```

## Quick start

Install the version used by this example.

```bash
python -m pip install "tba-router-oauth-protected-resource-metadata==0.4.0.dev4"
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

## Usage

The following public-entry-point example belongs to `tba-router-oauth-protected-resource-metadata`. HTTP carrier binding for RFC 9728 protected-resource metadata. Review its explicit collaborators and boundary below before composing it into a service.

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

## Package Boundary

`tba-router-oauth-protected-resource-metadata` belongs to `80-routers` and owns transport-facing route composition: HTTP carrier binding for RFC 9728 protected-resource metadata.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-oauth-protected-resource-metadata/src/tba_router_oauth_protected_resource_metadata/__init__.py). Public exports include `build_protected_resource_metadata_router`, `include_protected_resource_metadata`.

Keep duplicating credential algorithms or storage ownership in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

Explicit construction inputs and collaborators for `tba-router-oauth-protected-resource-metadata`:

- `build_protected_resource_metadata_router` construction inputs: `protected_resource_metadata`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-oauth-protected-resource-metadata/src/tba_router_oauth_protected_resource_metadata/binding.py).
- `include_protected_resource_metadata` construction inputs: `enabled`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-oauth-protected-resource-metadata/src/tba_router_oauth_protected_resource_metadata/binding.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

## Operations and readiness

`tba-router-oauth-protected-resource-metadata` exposes transport-facing route composition. Public operations found in its source:

- `build_protected_resource_metadata_router` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-oauth-protected-resource-metadata/src/tba_router_oauth_protected_resource_metadata/binding.py).
- `include_protected_resource_metadata` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-oauth-protected-resource-metadata/src/tba_router_oauth_protected_resource_metadata/binding.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-router-oauth-protected-resource-metadata`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

Other direct consumers include [tba-app-backend-core](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-core/README.md), [tba-app-backend-public](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-public/README.md), [tba-app-backend-resource-validation](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-resource-validation/README.md), [tba-app-backend-service-administration](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-service-administration/README.md).

## Non-goals

`tba-router-oauth-protected-resource-metadata` does not take ownership of duplicating credential algorithms or storage ownership.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

Declared local runtime dependencies:

- [tba-protocol-oauth](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-oauth/README.md)

Direct downstream consumers:

- [tba-app-backend-core](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-core/README.md)
- [tba-app-backend-public](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-public/README.md)
- [tba-app-backend-resource-validation](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-resource-validation/README.md)
- [tba-app-backend-service-administration](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-service-administration/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/80-routers/tba-router-oauth-protected-resource-metadata)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-oauth-protected-resource-metadata/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-oauth-protected-resource-metadata/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-oauth-protected-resource-metadata/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-router-oauth-protected-resource-metadata/)

## Governance

`tba-router-oauth-protected-resource-metadata` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `80-routers` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

See the [related repository tests](https://github.com/tigrbl/tigrbl_auth/blob/master/tests/conformance/production/test_rfc9728_protected_resource_metadata.py) for the implementation scope covered by this example.

[Workspace and package catalog](https://github.com/tigrbl/tigrbl_auth#package-catalog) · [tba-app-backend-public](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/90-backend-apps/tba-app-backend-public#readme) · [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues) · [Repository license](https://github.com/tigrbl/tigrbl_auth/blob/master/LICENSE)
