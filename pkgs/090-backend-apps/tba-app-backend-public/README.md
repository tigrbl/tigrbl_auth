# tba-app-backend-public

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-public/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-public/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-app-backend-public%3D%3D0.4.0.dev3/pkgs/090-backend-apps/tba-app-backend-public/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-app-backend-public%3D%3D0.4.0.dev3/pkgs/090-backend-apps/tba-app-backend-public/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/090-backend-apps"><img alt="Layer: 090 backend apps" src="https://img.shields.io/badge/Layer-090%20backend%20apps-0a7f5a"></a>
<a href="https://pypi.org/project/tba-app-backend-public/"><img alt="PyPI version for tba-app-backend-public" src="https://img.shields.io/pypi/v/tba-app-backend-public?label=tba-app-backend-public%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-app-backend-public"><img alt="Monthly PyPI downloads for tba-app-backend-public" src="https://static.pepy.tech/badge/tba-app-backend-public/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-public/README.md"><img alt="README hits for tba-app-backend-public" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-public/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-public/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Expose the public TBA OAuth and OpenID Connect API and login surface.

## AEO Summary

- Package: `tba-app-backend-public`
- Layer: `090-backend-apps`
- Responsibility: Public OAuth/OIDC and human-login backend application for TBA.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-public/src/tba_app_backend_public/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Use `tba_app_backend_public:app` for ASGI serving or `build_app` for explicit composition. The public backend pairs with `@tba/ui-public`. It assembles discovery, authorization, and token routes from the protocol and runtime packages. Tenant and platform administration use separate backends.

## Installation

Install the selected PyPI release of `tba-app-backend-public`:

```bash
uv pip install tba-app-backend-public
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/090-backend-apps/tba-app-backend-public
```

## Quick start

Install the version used by this example.

```bash
python -m pip install "tba-app-backend-public==0.4.0.dev3"
```

Save the following as `quickstart.py` and run `python quickstart.py`. This checks the exported ASGI callable and its declared surface without launching a runner or opening a database.

```python
from tba_app_backend_public import PUBLIC_BACKEND_APP_CONTRACT, app

assert callable(app)
assert PUBLIC_BACKEND_APP_CONTRACT.product_surface == "public-app"
assert "openid-configuration" in PUBLIC_BACKEND_APP_CONTRACT.production_capabilities
```

For a local API deployment, see the [Docker Compose configuration](https://github.com/tigrbl/tigrbl_auth/blob/master/docker/docker-compose.public-app.yml). It exposes discovery and JWKS at `http://localhost:8013` with TLS disabled for loopback development. The Compose deployment is separate from the quick start above.

## Usage

The following public-entry-point example belongs to `tba-app-backend-public`. Public OAuth/OIDC and human-login backend application for TBA. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_app_backend_public import PUBLIC_BACKEND_APP_CONTRACT, app

assert callable(app)
assert PUBLIC_BACKEND_APP_CONTRACT.product_surface == "public-app"
assert "openid-configuration" in PUBLIC_BACKEND_APP_CONTRACT.production_capabilities
```

## Package Boundary

`tba-app-backend-public` belongs to `090-backend-apps` and owns deployable backend composition: Public OAuth/OIDC and human-login backend application for TBA.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-public/src/tba_app_backend_public/__init__.py). Public exports include `PRODUCT_SURFACE`, `PUBLIC_BACKEND_APP_CONTRACT`, `PublicBackendAppContract`, `app`, `build_app`.

Keep new protocol grammars or independent persistence implementations in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

The [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-public/src/tba_app_backend_public/__init__.py) for `tba-app-backend-public` does not declare an explicit service-constructor or keyword-only factory hook in the inspected source. Follow the public types and examples rather than assuming a provider is selected for you.

Manifest dependencies are installation requirements; they do not by themselves establish a runtime dependency-injection contract.

## Operations and readiness

`tba-app-backend-public` exposes deployable backend composition. Public operations found in its source:

- `build_app` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-public/src/tba_app_backend_public/app.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-app-backend-public`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

## Non-goals

`tba-app-backend-public` does not take ownership of new protocol grammars or independent persistence implementations.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

Declared local runtime dependencies:

- [tba-app-backend-core](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-core/README.md)
- [tba-auth](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-auth/README.md)
- [tba-router-oauth-authorization](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-oauth-authorization/README.md)
- [tba-router-oauth-authorization-server-metadata](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-oauth-authorization-server-metadata/README.md)
- [tba-router-oauth-device-authorization](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-oauth-device-authorization/README.md)
- [tba-router-oauth-introspection](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-oauth-introspection/README.md)
- [tba-router-oauth-protected-resource-metadata](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-oauth-protected-resource-metadata/README.md)
- [tba-router-oauth-pushed-authorization-request](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-oauth-pushed-authorization-request/README.md)
- [tba-router-oauth-registration](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-oauth-registration/README.md)
- [tba-router-oauth-revocation](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-oauth-revocation/README.md)
- [tba-router-oauth-token](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-oauth-token/README.md)
- [tba-router-oauth-token-exchange](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-oauth-token-exchange/README.md)
- [tba-router-oidc-discovery](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-oidc-discovery/README.md)
- [tba-router-oidc-logout](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-oidc-logout/README.md)
- [tba-router-oidc-userinfo](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-oidc-userinfo/README.md)
- [tba-router-session-login](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-session-login/README.md)
- [tba-router-webauthn](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-webauthn/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/090-backend-apps/tba-app-backend-public)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-public/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-public/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-public/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-app-backend-public/)

## Governance

`tba-app-backend-public` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `090-backend-apps` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

See the [related repository tests](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-backend-apps/tests/packages/tba-app-backend-public/test_public_backend_app_package.py) for the implementation scope covered by this example.

[Workspace and package catalog](https://github.com/tigrbl/tigrbl_auth#package-catalog) · [tba-cli-identity](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/060-runtime/tba-cli-identity#readme) · [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues) · [Repository license](https://github.com/tigrbl/tigrbl_auth/blob/master/LICENSE)
