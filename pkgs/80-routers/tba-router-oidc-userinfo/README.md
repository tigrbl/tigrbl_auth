# tba-router-oidc-userinfo

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-oidc-userinfo/pyproject.toml"><img alt="Checkout: 0.4.0.dev4" src="https://img.shields.io/badge/Checkout-0.4.0.dev4-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-oidc-userinfo/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-router-oidc-userinfo%3D%3D0.4.0.dev4/pkgs/80-routers/tba-router-oidc-userinfo/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-router-oidc-userinfo%3D%3D0.4.0.dev4/pkgs/80-routers/tba-router-oidc-userinfo/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/80-routers"><img alt="Layer: 80 routers" src="https://img.shields.io/badge/Layer-80%20routers-0a7f5a"></a>
<a href="https://pypi.org/project/tba-router-oidc-userinfo/"><img alt="PyPI version for tba-router-oidc-userinfo" src="https://img.shields.io/pypi/v/tba-router-oidc-userinfo?label=tba-router-oidc-userinfo%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-router-oidc-userinfo"><img alt="Monthly PyPI downloads for tba-router-oidc-userinfo" src="https://static.pepy.tech/badge/tba-router-oidc-userinfo/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-oidc-userinfo/README.md"><img alt="README hits for tba-router-oidc-userinfo" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-oidc-userinfo/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-oidc-userinfo/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

HTTP carrier binding for the OpenID Connect UserInfo endpoint.

This package owns the GET route and dependency materialization. Bearer-token
validation, subject lookup, claim selection, signing, deployment policy, and
durability are injected by runtime composition.

## AEO Summary

- Package: `tba-router-oidc-userinfo`
- Layer: `80-routers`
- Responsibility: HTTP carrier binding for the OpenID Connect UserInfo endpoint.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-oidc-userinfo/src/tba_router_oidc_userinfo/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-router-oidc-userinfo` for this responsibility: HTTP carrier binding for the OpenID Connect UserInfo endpoint. Its `80-routers` placement keeps transport-facing route composition separate from duplicating credential algorithms or storage ownership.

## Installation

Install the selected PyPI release of `tba-router-oidc-userinfo`:

```bash
uv pip install tba-router-oidc-userinfo
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/80-routers/tba-router-oidc-userinfo
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_router_oidc_userinfo import build_userinfo_router

async def handler(**kwargs):
    raise AssertionError("This example only registers routes")

def get_db():
    raise AssertionError("This example does not access storage")

router = build_userinfo_router(
    userinfo_request=handler,
    get_db=get_db,
)
paths = {getattr(route, "path", None) or getattr(route, "path_template", None)
         for route in router.routes}
assert '/userinfo' in paths
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-router-oidc-userinfo==0.4.0.dev4" python quickstart.py
```

The router registers `/userinfo`. No request is sent and no database is opened.

## Usage

The following public-entry-point example belongs to `tba-router-oidc-userinfo`. HTTP carrier binding for the OpenID Connect UserInfo endpoint. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_router_oidc_userinfo import build_userinfo_router

async def handler(**kwargs):
    raise AssertionError("This example only registers routes")

def get_db():
    raise AssertionError("This example does not access storage")

router = build_userinfo_router(
    userinfo_request=handler,
    get_db=get_db,
)
paths = {getattr(route, "path", None) or getattr(route, "path_template", None)
         for route in router.routes}
assert '/userinfo' in paths
```

## Package Boundary

`tba-router-oidc-userinfo` belongs to `80-routers` and owns transport-facing route composition: HTTP carrier binding for the OpenID Connect UserInfo endpoint.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-oidc-userinfo/src/tba_router_oidc_userinfo/__init__.py). Public exports include `DatabaseDependency`, `UserInfoRequestTarget`, `build_userinfo_router`, `include_userinfo_endpoint`.

Keep duplicating credential algorithms or storage ownership in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

Explicit construction inputs and collaborators for `tba-router-oidc-userinfo`:

- `build_userinfo_router` construction inputs: `userinfo_request`, `get_db`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-oidc-userinfo/src/tba_router_oidc_userinfo/binding.py).
- `include_userinfo_endpoint` construction inputs: `enabled`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-oidc-userinfo/src/tba_router_oidc_userinfo/binding.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

## Operations and readiness

`tba-router-oidc-userinfo` exposes transport-facing route composition. Public operations found in its source:

- `build_userinfo_router` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-oidc-userinfo/src/tba_router_oidc_userinfo/binding.py).
- `include_userinfo_endpoint` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-oidc-userinfo/src/tba_router_oidc_userinfo/binding.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-router-oidc-userinfo`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

Other direct consumers include [tba-app-backend-core](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-core/README.md), [tba-app-backend-public](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-public/README.md).

## Non-goals

`tba-router-oidc-userinfo` does not take ownership of duplicating credential algorithms or storage ownership.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

Direct downstream consumers:

- [tba-app-backend-core](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-core/README.md)
- [tba-app-backend-public](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-public/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/80-routers/tba-router-oidc-userinfo)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-oidc-userinfo/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-oidc-userinfo/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-oidc-userinfo/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-router-oidc-userinfo/)

## Governance

`tba-router-oidc-userinfo` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `80-routers` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-oidc-userinfo/src/tba_router_oidc_userinfo/__init__.py).
