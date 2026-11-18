# tba-app-backend-platform-administration

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-platform-administration/pyproject.toml"><img alt="Checkout: 0.4.0.dev4" src="https://img.shields.io/badge/Checkout-0.4.0.dev4-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-platform-administration/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-app-backend-platform-administration%3D%3D0.4.0.dev4/pkgs/90-backend-apps/tba-app-backend-platform-administration/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-app-backend-platform-administration%3D%3D0.4.0.dev4/pkgs/90-backend-apps/tba-app-backend-platform-administration/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/90-backend-apps"><img alt="Layer: 90 backend apps" src="https://img.shields.io/badge/Layer-90%20backend%20apps-0a7f5a"></a>
<a href="https://pypi.org/project/tba-app-backend-platform-administration/"><img alt="PyPI version for tba-app-backend-platform-administration" src="https://img.shields.io/pypi/v/tba-app-backend-platform-administration?label=tba-app-backend-platform-administration%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-app-backend-platform-administration"><img alt="Monthly PyPI downloads for tba-app-backend-platform-administration" src="https://static.pepy.tech/badge/tba-app-backend-platform-administration/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-platform-administration/README.md"><img alt="README hits for tba-app-backend-platform-administration" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-platform-administration/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-platform-administration/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Platform-scoped tenant lifecycle and authority-assignment API front door.

## AEO Summary

- Package: `tba-app-backend-platform-administration`
- Layer: `90-backend-apps`
- Responsibility: Platform owner and operator control-plane backend application for TBA.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-platform-administration/src/tba_app_backend_platform_administration/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-app-backend-platform-administration` for this responsibility: Platform owner and operator control-plane backend application for TBA. Its `90-backend-apps` placement keeps deployable backend composition separate from new protocol grammars or independent persistence implementations.

## Installation

Install the selected PyPI release of `tba-app-backend-platform-administration`:

```bash
uv pip install tba-app-backend-platform-administration
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/90-backend-apps/tba-app-backend-platform-administration
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_app_backend_platform_administration import AdminIdentityOut

assert callable(AdminIdentityOut)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-app-backend-platform-administration==0.4.0.dev4" python quickstart.py
```

The import and assertion succeed when the AdminIdentityOut entry point is available.

## Usage

The following public-entry-point example belongs to `tba-app-backend-platform-administration`. Platform owner and operator control-plane backend application for TBA. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_app_backend_platform_administration import AdminIdentityOut

assert callable(AdminIdentityOut)
```

## Surface

| Property | Value |
| --- | --- |
| Product surface | `platform-admin-app` |

The backend app owns HTTP schemas and routes only. Tenant, realm, and identity
administration are invoked through request-scoped layer-40 capabilities composed
by `tba-server-identity`; durable table operations and secret hashing remain
in the layer-60 runtime adapters and their lower-layer providers.
| Intended UIX | `@tba/ui-platform-administration` |
| Exposes | Tenant lifecycle, platform authority assignment, admin identity lookup, audit/session/profile RPC |
| Excludes | Public login/consent pages, tenant self-service-only workflows, developer app registration surface |

## Entrypoint

```python
from tba_app_backend_platform_administration import app, build_app
```

## Local dev deployment

Run the isolated platform control-plane front door on port `8015`:

```bash
docker compose -f docker/docker-compose.platform-admin-app.yml up -d --build
```

The dev API key defaults to `dev-platform-admin-key`.

Useful endpoints:

| Endpoint | Purpose |
| --- | --- |
| `/openapi.json` | Platform-admin REST/control-plane contract. |
| `/openrpc.json` | Platform-admin JSON-RPC method contract. |
| `/rpc` | API-key-protected JSON-RPC dispatch. |
| `/tenant` | API-key-protected platform tenant lifecycle resource. |

## Package Boundary

`tba-app-backend-platform-administration` belongs to `90-backend-apps` and owns deployable backend composition: Platform owner and operator control-plane backend application for TBA.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-platform-administration/src/tba_app_backend_platform_administration/__init__.py). Public exports include `AdminIdentityOut`, `AdminIdentityProvisionIn`, `AdminIdentityUpdateIn`, `AdminRealmOut`, `AdminRealmProvisionIn`, `AdminRealmUpdateIn`, `AdminTenantOut`, `AdminTenantProvisionIn`, `AdminTenantUpdateIn`, `PRODUCT_SURFACE`, `PLATFORM_ADMIN_BACKEND_APP_CONTRACT`, `PlatformAdminBackendAppContract`.

Keep new protocol grammars or independent persistence implementations in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

The [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-platform-administration/src/tba_app_backend_platform_administration/__init__.py) for `tba-app-backend-platform-administration` does not declare an explicit service-constructor or keyword-only factory hook in the inspected source. Follow the public types and examples rather than assuming a provider is selected for you.

Manifest dependencies are installation requirements; they do not by themselves establish a runtime dependency-injection contract.

## Operations and readiness

`tba-app-backend-platform-administration` exposes deployable backend composition. Public operations found in its source:

- `build_app` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-platform-administration/src/tba_app_backend_platform_administration/app.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-app-backend-platform-administration`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

## Non-goals

`tba-app-backend-platform-administration` does not take ownership of new protocol grammars or independent persistence implementations.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

Declared local runtime dependencies:

- [tba-app-backend-core](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-core/README.md)
- [tba-auth](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/70-facade/tba-auth/README.md)
- [tba-contracts-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-identity/README.md)
- [tba-router-administration-gate](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-administration-gate/README.md)
- [tba-server-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-server-identity/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/90-backend-apps/tba-app-backend-platform-administration)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-platform-administration/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-platform-administration/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-platform-administration/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-app-backend-platform-administration/)

## Governance

`tba-app-backend-platform-administration` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `90-backend-apps` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-platform-administration/src/tba_app_backend_platform_administration/__init__.py).
