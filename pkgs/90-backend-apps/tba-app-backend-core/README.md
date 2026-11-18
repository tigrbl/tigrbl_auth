# tba-app-backend-core

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-core/pyproject.toml"><img alt="Checkout: 0.4.0.dev4" src="https://img.shields.io/badge/Checkout-0.4.0.dev4-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-core/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-app-backend-core%3D%3D0.4.0.dev4/pkgs/90-backend-apps/tba-app-backend-core/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-app-backend-core%3D%3D0.4.0.dev4/pkgs/90-backend-apps/tba-app-backend-core/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/90-backend-apps"><img alt="Layer: 90 backend apps" src="https://img.shields.io/badge/Layer-90%20backend%20apps-0a7f5a"></a>
<a href="https://pypi.org/project/tba-app-backend-core/"><img alt="PyPI version for tba-app-backend-core" src="https://img.shields.io/pypi/v/tba-app-backend-core?label=tba-app-backend-core%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-app-backend-core"><img alt="Monthly PyPI downloads for tba-app-backend-core" src="https://static.pepy.tech/badge/tba-app-backend-core/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-core/README.md"><img alt="README hits for tba-app-backend-core" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-core/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-core/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Shared layer-90 composition for deployable TBA backend applications.

This package owns ASGI application construction, layer-80 router closure, HTTP
surface assembly, administrative gate wrapping, and product-surface selection.
Product backend-app packages supply a declared product contract and call the
shared build_product_app factory.

It does not own protocol semantics, capability implementations, durable table
behavior, runtime handlers, or storage. Those remain in layers 50, 40, 30, and
60 and are injected or imported downward.

## AEO Summary

- Package: `tba-app-backend-core`
- Layer: `90-backend-apps`
- Responsibility: Shared layer-90 ASGI and router composition for TBA backend applications.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-core/src/tba_app_backend_core/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-app-backend-core` for this responsibility: Shared layer-90 ASGI and router composition for TBA backend applications. Its `90-backend-apps` placement keeps deployable backend composition separate from new protocol grammars or independent persistence implementations.

## Installation

Install the selected PyPI release of `tba-app-backend-core`:

```bash
uv pip install tba-app-backend-core
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/90-backend-apps/tba-app-backend-core
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_app_backend_core import app

assert callable(app)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-app-backend-core==0.4.0.dev4" python quickstart.py
```

The import and assertion succeed when the app entry point is available.

## Usage

The following public-entry-point example belongs to `tba-app-backend-core`. Shared layer-90 ASGI and router composition for TBA backend applications. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_app_backend_core import app

assert callable(app)
```

## Package Boundary

`tba-app-backend-core` belongs to `90-backend-apps` and owns deployable backend composition: Shared layer-90 ASGI and router composition for TBA backend applications.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-core/src/tba_app_backend_core/__init__.py). Public exports include `app`, `build_app`, `build_application_runtime_plan`, `TbaBackendAppPlugin`, `build_product_app`, `install`, `validate_backend_app_contract`.

Keep new protocol grammars or independent persistence implementations in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

Explicit construction inputs and collaborators for `tba-app-backend-core`:

- `build_app` construction inputs: `deployment`, `runtime_assembly_factory`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-core/src/tba_app_backend_core/app.py).
- `TbaBackendAppPlugin` construction inputs: `diagnostics_prefix`, `settings`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-core/src/tba_app_backend_core/plugin.py).
- `build_product_app` construction inputs: `contract`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-core/src/tba_app_backend_core/product.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

## Operations and readiness

`tba-app-backend-core` exposes deployable backend composition. Public operations found in its source:

- `build_app` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-core/src/tba_app_backend_core/app.py).
- `build_application_runtime_plan` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-core/src/tba_app_backend_core/app.py).
- `install` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-core/src/tba_app_backend_core/plugin.py).
- `validate_backend_app_contract` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-core/src/tba_app_backend_core/product.py).
- `build_product_app` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-core/src/tba_app_backend_core/product.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-app-backend-core`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

Other direct consumers include [tba-app-backend-developer](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-developer/README.md), [tba-app-backend-my-account](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-my-account/README.md), [tba-app-backend-platform-administration](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-platform-administration/README.md), [tba-app-backend-public](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-public/README.md), [tba-app-backend-resource-validation](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-resource-validation/README.md), [tba-app-backend-service-administration](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-service-administration/README.md), [tba-app-backend-tenant-administration](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-tenant-administration/README.md).

## Non-goals

`tba-app-backend-core` does not take ownership of new protocol grammars or independent persistence implementations.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

Declared local runtime dependencies:

- [tba-capability-client-secret-authentication](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-client-secret-authentication/README.md)
- [tba-contracts-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-identity/README.md)
- [tba-operator-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-operator-identity/README.md)
- [tba-plugin-tigrbl](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-plugin-tigrbl/README.md)
- [tba-primitives-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/00-primitives/tba-primitives-identity/README.md)
- [tba-protocol-gnap](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-gnap/README.md)
- [tba-protocol-oauth](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-oauth/README.md)
- [tba-provider-secret-hashing-bcrypt](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-secret-hashing-bcrypt/README.md)
- [tba-router-administration-gate](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-administration-gate/README.md)
- [tba-router-oauth-authorization](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-oauth-authorization/README.md)
- [tba-router-oauth-authorization-server-metadata](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-oauth-authorization-server-metadata/README.md)
- [tba-router-oauth-device-authorization](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-oauth-device-authorization/README.md)
- [tba-router-oauth-introspection](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-oauth-introspection/README.md)
- [tba-router-oauth-protected-resource-metadata](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-oauth-protected-resource-metadata/README.md)
- [tba-router-oauth-pushed-authorization-request](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-oauth-pushed-authorization-request/README.md)
- [tba-router-oauth-registration](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-oauth-registration/README.md)
- [tba-router-oauth-revocation](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-oauth-revocation/README.md)
- [tba-router-oauth-token](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-oauth-token/README.md)
- [tba-router-oauth-token-exchange](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-oauth-token-exchange/README.md)
- [tba-router-oidc-discovery](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-oidc-discovery/README.md)
- [tba-router-oidc-logout](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-oidc-logout/README.md)
- [tba-router-oidc-userinfo](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-oidc-userinfo/README.md)
- [tba-router-resource-validation-metadata](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-resource-validation-metadata/README.md)
- [tba-router-session-login](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-session-login/README.md)
- [tba-runtime-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-runtime-identity/README.md)
- [tba-runtime-identity-storage](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/30-storage-runtime/tba-runtime-identity-storage/README.md)
- [tba-server-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-server-identity/README.md)
- [tba-storage-core](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/01-storage/tba-storage-core/README.md)
- [tba-storage-oauth](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/01-storage/tba-storage-oauth/README.md)
- [tba-storage-tenancy](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/01-storage/tba-storage-tenancy/README.md)

Direct downstream consumers:

- [tba-app-backend-developer](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-developer/README.md)
- [tba-app-backend-my-account](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-my-account/README.md)
- [tba-app-backend-platform-administration](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-platform-administration/README.md)
- [tba-app-backend-public](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-public/README.md)
- [tba-app-backend-resource-validation](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-resource-validation/README.md)
- [tba-app-backend-service-administration](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-service-administration/README.md)
- [tba-app-backend-tenant-administration](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-tenant-administration/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/90-backend-apps/tba-app-backend-core)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-core/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-core/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-core/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-app-backend-core/)

## Governance

`tba-app-backend-core` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `90-backend-apps` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-core/src/tba_app_backend_core/__init__.py).
