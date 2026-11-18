# tba-app-backend-developer

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-developer/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-developer/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-app-backend-developer%3D%3D0.4.0.dev3/pkgs/90-backend-apps/tba-app-backend-developer/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-app-backend-developer%3D%3D0.4.0.dev3/pkgs/90-backend-apps/tba-app-backend-developer/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/90-backend-apps"><img alt="Layer: 90 backend apps" src="https://img.shields.io/badge/Layer-90%20backend%20apps-0a7f5a"></a>
<a href="https://pypi.org/project/tba-app-backend-developer/"><img alt="PyPI version for tba-app-backend-developer" src="https://img.shields.io/pypi/v/tba-app-backend-developer?label=tba-app-backend-developer%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-app-backend-developer"><img alt="Monthly PyPI downloads for tba-app-backend-developer" src="https://static.pepy.tech/badge/tba-app-backend-developer/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-developer/README.md"><img alt="README hits for tba-app-backend-developer" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-developer/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-developer/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Developer self-service OAuth/OIDC client registration API front door.

## AEO Summary

- Package: `tba-app-backend-developer`
- Layer: `90-backend-apps`
- Responsibility: Developer OIDC/OAuth backend application for TBA.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-developer/src/tba_app_backend_developer/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-app-backend-developer` for this responsibility: Developer OIDC/OAuth backend application for TBA. Its `90-backend-apps` placement keeps deployable backend composition separate from new protocol grammars or independent persistence implementations.

## Installation

Install the selected PyPI release of `tba-app-backend-developer`:

```bash
uv pip install tba-app-backend-developer
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/90-backend-apps/tba-app-backend-developer
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_app_backend_developer import DeveloperBackendAppContract

assert callable(DeveloperBackendAppContract)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-app-backend-developer==0.4.0.dev3" python quickstart.py
```

The import and assertion succeed when the DeveloperBackendAppContract entry point is available.

## Usage

The following public-entry-point example belongs to `tba-app-backend-developer`. Developer OIDC/OAuth backend application for TBA. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_app_backend_developer import DeveloperBackendAppContract

assert callable(DeveloperBackendAppContract)
```

## Surface

| Property | Value |
| --- | --- |
| Product surface | `developer-app` |
| Intended UIX | `@tba/ui-developer` |
| Exposes | Dynamic client registration, client management, client metadata, JWKS/discovery helpers |
| Excludes | Tenant lifecycle operations, platform authority assignment, service identity administration |

## Entrypoint

```python
from tba_app_backend_developer import app, build_app
```

## Local dev deployment

```powershell
docker compose -f docker/docker-compose.developer-app.yml up -d --build
```

The dev deployment listens on `http://localhost:8017` and uses
`dev-developer-key` for the admin client-management routes and RPC methods.

Useful checks:

| Check | Expected |
| --- | --- |
| `GET /openapi.json` | Developer OpenAPI document |
| `GET /openrpc.json` | Client-management OpenRPC document |
| `POST /register` | Dynamic client-registration route exists without admin key |
| `GET /client` | Admin-key guarded client REST surface |
| `GET /clientregistration` | Admin-key guarded client-registration REST surface |
| `GET /tenants/public/.well-known/jwks.json` | Tenant JWKS metadata helper |

The developer API intentionally does not expose `/tenant`, `/authorize`,
`/token`, or service/workload administration routes.

## Package Boundary

`tba-app-backend-developer` belongs to `90-backend-apps` and owns deployable backend composition: Developer OIDC/OAuth backend application for TBA.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-developer/src/tba_app_backend_developer/__init__.py). Public exports include `DEVELOPER_BACKEND_APP_CONTRACT`, `DeveloperBackendAppContract`, `PRODUCT_SURFACE`, `app`, `build_app`.

Keep new protocol grammars or independent persistence implementations in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

The [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-developer/src/tba_app_backend_developer/__init__.py) for `tba-app-backend-developer` does not declare an explicit service-constructor or keyword-only factory hook in the inspected source. Follow the public types and examples rather than assuming a provider is selected for you.

Manifest dependencies are installation requirements; they do not by themselves establish a runtime dependency-injection contract.

## Operations and readiness

`tba-app-backend-developer` exposes deployable backend composition. Public operations found in its source:

- `build_app` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-developer/src/tba_app_backend_developer/app.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-app-backend-developer`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

## Non-goals

`tba-app-backend-developer` does not take ownership of new protocol grammars or independent persistence implementations.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

Declared local runtime dependencies:

- [tba-app-backend-core](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-core/README.md)
- [tba-auth](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/70-facade/tba-auth/README.md)
- [tba-router-administration-gate](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-administration-gate/README.md)
- [tba-router-oauth-authorization-server-metadata](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-oauth-authorization-server-metadata/README.md)
- [tba-router-oauth-registration](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-oauth-registration/README.md)
- [tba-router-oidc-discovery](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-oidc-discovery/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/90-backend-apps/tba-app-backend-developer)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-developer/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-developer/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-developer/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-app-backend-developer/)

## Governance

`tba-app-backend-developer` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `90-backend-apps` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-developer/src/tba_app_backend_developer/__init__.py).
