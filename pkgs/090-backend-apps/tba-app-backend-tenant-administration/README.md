# tba-app-backend-tenant-administration

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-tenant-administration/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-tenant-administration/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-app-backend-tenant-administration%3D%3D0.4.0.dev3/pkgs/090-backend-apps/tba-app-backend-tenant-administration/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-app-backend-tenant-administration%3D%3D0.4.0.dev3/pkgs/090-backend-apps/tba-app-backend-tenant-administration/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/090-backend-apps"><img alt="Layer: 090 backend apps" src="https://img.shields.io/badge/Layer-090%20backend%20apps-0a7f5a"></a>
<a href="https://pypi.org/project/tba-app-backend-tenant-administration/"><img alt="PyPI version for tba-app-backend-tenant-administration" src="https://img.shields.io/pypi/v/tba-app-backend-tenant-administration?label=tba-app-backend-tenant-administration%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-app-backend-tenant-administration"><img alt="Monthly PyPI downloads for tba-app-backend-tenant-administration" src="https://static.pepy.tech/badge/tba-app-backend-tenant-administration/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-tenant-administration/README.md"><img alt="README hits for tba-app-backend-tenant-administration" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-tenant-administration/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-tenant-administration/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Tenant-scoped identity, admin delegation, JWKS, and local policy API front door.

## AEO Summary

- Package: `tba-app-backend-tenant-administration`
- Layer: `090-backend-apps`
- Responsibility: Tenant-scoped administration backend application for TBA.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-tenant-administration/src/tba_app_backend_tenant_administration/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-app-backend-tenant-administration` for this responsibility: Tenant-scoped administration backend application for TBA. Its `090-backend-apps` placement keeps deployable backend composition separate from new protocol grammars or independent persistence implementations.

## Installation

Install the selected PyPI release of `tba-app-backend-tenant-administration`:

```bash
uv pip install tba-app-backend-tenant-administration
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/090-backend-apps/tba-app-backend-tenant-administration
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_app_backend_tenant_administration import TenantAdminBackendAppContract

assert callable(TenantAdminBackendAppContract)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-app-backend-tenant-administration==0.4.0.dev3" python quickstart.py
```

The import and assertion succeed when the TenantAdminBackendAppContract entry point is available.

## Usage

The following public-entry-point example belongs to `tba-app-backend-tenant-administration`. Tenant-scoped administration backend application for TBA. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_app_backend_tenant_administration import TenantAdminBackendAppContract

assert callable(TenantAdminBackendAppContract)
```

## Surface

| Property | Value |
| --- | --- |
| Product surface | `tenant-admin-app` |
| Intended UIX | `@tba/ui-tenant-administration` |
| Exposes | Tenant identities, clients, consents, sessions, tenant keys/JWKS, tenant-local audit |
| Excludes | Platform tenant creation/deletion and cross-tenant authority assignment |

## Entrypoint

```python
from tba_app_backend_tenant_administration import app, build_app
```

## Local Dev Deployment

The Docker dev surface listens on `http://localhost:8016` and uses the
admin API key `dev-tenant-admin-key` unless overridden.

```bash
docker compose -f docker/docker-compose.tenant-admin-app.yml up -d --build
```

Useful checks:

- `GET /openapi.json`
- `GET /openrpc.json`
- `POST /rpc` with `X-API-Key: dev-tenant-admin-key`
- `GET /user`, `/client`, `/clientregistration`, `/consent`

The tenant-admin surface intentionally does not expose `/tenant`, public
OAuth/OIDC routes, platform tenant lifecycle RPC, or service/workload admin
resources.

## Package Boundary

`tba-app-backend-tenant-administration` belongs to `090-backend-apps` and owns deployable backend composition: Tenant-scoped administration backend application for TBA.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-tenant-administration/src/tba_app_backend_tenant_administration/__init__.py). Public exports include `PRODUCT_SURFACE`, `TENANT_ADMIN_BACKEND_APP_CONTRACT`, `TenantAdminBackendAppContract`, `app`, `build_app`.

Keep new protocol grammars or independent persistence implementations in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

The [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-tenant-administration/src/tba_app_backend_tenant_administration/__init__.py) for `tba-app-backend-tenant-administration` does not declare an explicit service-constructor or keyword-only factory hook in the inspected source. Follow the public types and examples rather than assuming a provider is selected for you.

Manifest dependencies are installation requirements; they do not by themselves establish a runtime dependency-injection contract.

## Operations and readiness

`tba-app-backend-tenant-administration` exposes deployable backend composition. Public operations found in its source:

- `build_app` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-tenant-administration/src/tba_app_backend_tenant_administration/app.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-app-backend-tenant-administration`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

## Non-goals

`tba-app-backend-tenant-administration` does not take ownership of new protocol grammars or independent persistence implementations.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

Declared local runtime dependencies:

- [tba-app-backend-core](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-core/README.md)
- [tba-auth](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-auth/README.md)
- [tba-router-administration-gate](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-administration-gate/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/090-backend-apps/tba-app-backend-tenant-administration)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-tenant-administration/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-tenant-administration/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-tenant-administration/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-app-backend-tenant-administration/)

## Governance

`tba-app-backend-tenant-administration` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `090-backend-apps` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-tenant-administration/src/tba_app_backend_tenant_administration/__init__.py).
