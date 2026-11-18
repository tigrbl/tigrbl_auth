# tba-router-oauth-pushed-authorization-request

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-oauth-pushed-authorization-request/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-oauth-pushed-authorization-request/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-router-oauth-pushed-authorization-request%3D%3D0.4.0.dev3/pkgs/80-routers/tba-router-oauth-pushed-authorization-request/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-router-oauth-pushed-authorization-request%3D%3D0.4.0.dev3/pkgs/80-routers/tba-router-oauth-pushed-authorization-request/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/80-routers"><img alt="Layer: 80 routers" src="https://img.shields.io/badge/Layer-80%20routers-0a7f5a"></a>
<a href="https://pypi.org/project/tba-router-oauth-pushed-authorization-request/"><img alt="PyPI version for tba-router-oauth-pushed-authorization-request" src="https://img.shields.io/pypi/v/tba-router-oauth-pushed-authorization-request?label=tba-router-oauth-pushed-authorization-request%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-router-oauth-pushed-authorization-request"><img alt="Monthly PyPI downloads for tba-router-oauth-pushed-authorization-request" src="https://static.pepy.tech/badge/tba-router-oauth-pushed-authorization-request/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-oauth-pushed-authorization-request/README.md"><img alt="README hits for tba-router-oauth-pushed-authorization-request" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-oauth-pushed-authorization-request/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-oauth-pushed-authorization-request/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

HTTP carrier binding for OAuth 2.0 Pushed Authorization Requests (RFC 9126).

This package owns request decoding, `/par` routing, HTTP error mapping, and
response serialization. It receives normalization, client authentication,
durability, and observation collaborators from runtime composition.

## AEO Summary

- Package: `tba-router-oauth-pushed-authorization-request`
- Layer: `80-routers`
- Responsibility: RFC 9126 HTTP carrier binding for TBA.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-oauth-pushed-authorization-request/src/tba_router_oauth_pushed_authorization_request/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-router-oauth-pushed-authorization-request` for this responsibility: RFC 9126 HTTP carrier binding for TBA. Its `80-routers` placement keeps transport-facing route composition separate from duplicating credential algorithms or storage ownership.

## Installation

Install the selected PyPI release of `tba-router-oauth-pushed-authorization-request`:

```bash
uv pip install tba-router-oauth-pushed-authorization-request
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/80-routers/tba-router-oauth-pushed-authorization-request
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_router_oauth_pushed_authorization_request import PushedAuthorizationAuthorizer

assert callable(PushedAuthorizationAuthorizer)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-router-oauth-pushed-authorization-request==0.4.0.dev3" python quickstart.py
```

The import and assertion succeed when the PushedAuthorizationAuthorizer entry point is available.

## Usage

The following public-entry-point example belongs to `tba-router-oauth-pushed-authorization-request`. RFC 9126 HTTP carrier binding for TBA. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_router_oauth_pushed_authorization_request import PushedAuthorizationAuthorizer

assert callable(PushedAuthorizationAuthorizer)
```

## Package Boundary

`tba-router-oauth-pushed-authorization-request` belongs to `80-routers` and owns transport-facing route composition: RFC 9126 HTTP carrier binding for TBA.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-oauth-pushed-authorization-request/src/tba_router_oauth_pushed_authorization_request/__init__.py). Public exports include `PushedAuthorizationAuthorizer`, `PushedAuthorizationNormalizer`, `PushedAuthorizationObserver`, `PushedAuthorizationServiceResolver`, `build_pushed_authorization_router`, `include_pushed_authorization_endpoint`, `request_body_data`.

Keep duplicating credential algorithms or storage ownership in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

Explicit construction inputs and collaborators for `tba-router-oauth-pushed-authorization-request`:

- `build_pushed_authorization_router` construction inputs: `service_for_request`, `normalize_request`, `authorize_caller`, `observe_response`, `get_db`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-oauth-pushed-authorization-request/src/tba_router_oauth_pushed_authorization_request/binding.py).
- `include_pushed_authorization_endpoint` construction inputs: `enabled`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-oauth-pushed-authorization-request/src/tba_router_oauth_pushed_authorization_request/binding.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

## Operations and readiness

`tba-router-oauth-pushed-authorization-request` exposes transport-facing route composition. Public operations found in its source:

- `request_body_data` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-oauth-pushed-authorization-request/src/tba_router_oauth_pushed_authorization_request/binding.py).
- `build_pushed_authorization_router` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-oauth-pushed-authorization-request/src/tba_router_oauth_pushed_authorization_request/binding.py).
- `include_pushed_authorization_endpoint` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-oauth-pushed-authorization-request/src/tba_router_oauth_pushed_authorization_request/binding.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-router-oauth-pushed-authorization-request`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

Other direct consumers include [tba-app-backend-core](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-core/README.md), [tba-app-backend-public](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-public/README.md).

## Non-goals

`tba-router-oauth-pushed-authorization-request` does not take ownership of duplicating credential algorithms or storage ownership.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

Declared local runtime dependencies:

- [tba-contracts-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-identity/README.md)
- [tba-protocol-oauth](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-oauth/README.md)

Direct downstream consumers:

- [tba-app-backend-core](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-core/README.md)
- [tba-app-backend-public](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-public/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/80-routers/tba-router-oauth-pushed-authorization-request)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-oauth-pushed-authorization-request/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-oauth-pushed-authorization-request/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-oauth-pushed-authorization-request/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-router-oauth-pushed-authorization-request/)

## Governance

`tba-router-oauth-pushed-authorization-request` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `80-routers` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-oauth-pushed-authorization-request/src/tba_router_oauth_pushed_authorization_request/__init__.py).
