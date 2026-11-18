# tba-router-oauth-authorization-server-metadata

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-oauth-authorization-server-metadata/pyproject.toml"><img alt="Checkout: 0.4.0.dev4" src="https://img.shields.io/badge/Checkout-0.4.0.dev4-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-oauth-authorization-server-metadata/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-router-oauth-authorization-server-metadata%3D%3D0.4.0.dev4/pkgs/80-routers/tba-router-oauth-authorization-server-metadata/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-router-oauth-authorization-server-metadata%3D%3D0.4.0.dev4/pkgs/80-routers/tba-router-oauth-authorization-server-metadata/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/80-routers"><img alt="Layer: 80 routers" src="https://img.shields.io/badge/Layer-80%20routers-0a7f5a"></a>
<a href="https://pypi.org/project/tba-router-oauth-authorization-server-metadata/"><img alt="PyPI version for tba-router-oauth-authorization-server-metadata" src="https://img.shields.io/pypi/v/tba-router-oauth-authorization-server-metadata?label=tba-router-oauth-authorization-server-metadata%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-router-oauth-authorization-server-metadata"><img alt="Monthly PyPI downloads for tba-router-oauth-authorization-server-metadata" src="https://static.pepy.tech/badge/tba-router-oauth-authorization-server-metadata/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-oauth-authorization-server-metadata/README.md"><img alt="README hits for tba-router-oauth-authorization-server-metadata" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-oauth-authorization-server-metadata/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-oauth-authorization-server-metadata/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

HTTP carrier binding for OAuth 2.0 Authorization Server Metadata (RFC 8414).
Protocol semantics and runtime policy remain owned by upstream layers.

## AEO Summary

- Package: `tba-router-oauth-authorization-server-metadata`
- Layer: `80-routers`
- Responsibility: HTTP carrier binding for RFC 8414 authorization-server metadata.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-oauth-authorization-server-metadata/src/tba_router_oauth_authorization_server_metadata/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-router-oauth-authorization-server-metadata` for this responsibility: HTTP carrier binding for RFC 8414 authorization-server metadata. Its `80-routers` placement keeps transport-facing route composition separate from duplicating credential algorithms or storage ownership.

## Installation

Install the selected PyPI release of `tba-router-oauth-authorization-server-metadata`:

```bash
uv pip install tba-router-oauth-authorization-server-metadata
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/80-routers/tba-router-oauth-authorization-server-metadata
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_router_oauth_authorization_server_metadata import build_authorization_server_metadata_router

assert callable(build_authorization_server_metadata_router)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-router-oauth-authorization-server-metadata==0.4.0.dev4" python quickstart.py
```

The import and assertion succeed when the build_authorization_server_metadata_router entry point is available.

## Usage

The following public-entry-point example belongs to `tba-router-oauth-authorization-server-metadata`. HTTP carrier binding for RFC 8414 authorization-server metadata. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_router_oauth_authorization_server_metadata import build_authorization_server_metadata_router

assert callable(build_authorization_server_metadata_router)
```

## Package Boundary

`tba-router-oauth-authorization-server-metadata` belongs to `80-routers` and owns transport-facing route composition: HTTP carrier binding for RFC 8414 authorization-server metadata.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-oauth-authorization-server-metadata/src/tba_router_oauth_authorization_server_metadata/__init__.py). Public exports include `build_authorization_server_metadata_router`, `include_authorization_server_metadata`.

Keep duplicating credential algorithms or storage ownership in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

Explicit construction inputs and collaborators for `tba-router-oauth-authorization-server-metadata`:

- `build_authorization_server_metadata_router` construction inputs: `authorization_server_metadata`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-oauth-authorization-server-metadata/src/tba_router_oauth_authorization_server_metadata/binding.py).
- `include_authorization_server_metadata` construction inputs: `enabled`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-oauth-authorization-server-metadata/src/tba_router_oauth_authorization_server_metadata/binding.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

## Operations and readiness

`tba-router-oauth-authorization-server-metadata` exposes transport-facing route composition. Public operations found in its source:

- `build_authorization_server_metadata_router` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-oauth-authorization-server-metadata/src/tba_router_oauth_authorization_server_metadata/binding.py).
- `include_authorization_server_metadata` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-oauth-authorization-server-metadata/src/tba_router_oauth_authorization_server_metadata/binding.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-router-oauth-authorization-server-metadata`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

Other direct consumers include [tba-app-backend-core](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-core/README.md), [tba-app-backend-developer](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-developer/README.md), [tba-app-backend-public](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-public/README.md).

## Non-goals

`tba-router-oauth-authorization-server-metadata` does not take ownership of duplicating credential algorithms or storage ownership.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

Declared local runtime dependencies:

- [tba-protocol-oauth](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-oauth/README.md)

Direct downstream consumers:

- [tba-app-backend-core](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-core/README.md)
- [tba-app-backend-developer](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-developer/README.md)
- [tba-app-backend-public](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-public/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/80-routers/tba-router-oauth-authorization-server-metadata)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-oauth-authorization-server-metadata/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-oauth-authorization-server-metadata/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-oauth-authorization-server-metadata/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-router-oauth-authorization-server-metadata/)

## Governance

`tba-router-oauth-authorization-server-metadata` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `80-routers` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-oauth-authorization-server-metadata/src/tba_router_oauth_authorization_server_metadata/__init__.py).
