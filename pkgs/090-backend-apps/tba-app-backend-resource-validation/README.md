# tba-app-backend-resource-validation

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-resource-validation/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-resource-validation/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-app-backend-resource-validation%3D%3D0.4.0.dev3/pkgs/090-backend-apps/tba-app-backend-resource-validation/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-app-backend-resource-validation%3D%3D0.4.0.dev3/pkgs/090-backend-apps/tba-app-backend-resource-validation/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/090-backend-apps"><img alt="Layer: 090 backend apps" src="https://img.shields.io/badge/Layer-090%20backend%20apps-0a7f5a"></a>
<a href="https://pypi.org/project/tba-app-backend-resource-validation/"><img alt="PyPI version for tba-app-backend-resource-validation" src="https://img.shields.io/pypi/v/tba-app-backend-resource-validation?label=tba-app-backend-resource-validation%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-app-backend-resource-validation"><img alt="Monthly PyPI downloads for tba-app-backend-resource-validation" src="https://static.pepy.tech/badge/tba-app-backend-resource-validation/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-resource-validation/README.md"><img alt="README hits for tba-app-backend-resource-validation" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-resource-validation/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-resource-validation/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Resource-server validation API front door for protected APIs that need issuer metadata.

## AEO Summary

- Package: `tba-app-backend-resource-validation`
- Layer: `090-backend-apps`
- Responsibility: JWKS, introspection, and protected-resource validation backend application for TBA.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-resource-validation/src/tba_app_backend_resource_validation/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-app-backend-resource-validation` for this responsibility: JWKS, introspection, and protected-resource validation backend application for TBA. Its `090-backend-apps` placement keeps deployable backend composition separate from new protocol grammars or independent persistence implementations.

## Installation

Install the selected PyPI release of `tba-app-backend-resource-validation`:

```bash
uv pip install tba-app-backend-resource-validation
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/090-backend-apps/tba-app-backend-resource-validation
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_app_backend_resource_validation import ResourceValidationBackendAppContract

assert callable(ResourceValidationBackendAppContract)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-app-backend-resource-validation==0.4.0.dev3" python quickstart.py
```

The import and assertion succeed when the ResourceValidationBackendAppContract entry point is available.

## Usage

The following public-entry-point example belongs to `tba-app-backend-resource-validation`. JWKS, introspection, and protected-resource validation backend application for TBA. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_app_backend_resource_validation import ResourceValidationBackendAppContract

assert callable(ResourceValidationBackendAppContract)
```

## Surface

| Property | Value |
| --- | --- |
| Product surface | `resource-validation-app` |
| Intended consumers | Resource servers, API gateways, validation middleware |
| Exposes | JWKS, tenant JWKS, introspection, OIDC discovery, protected-resource metadata |
| Excludes | Public human login/consent pages, dynamic client registration, admin resources, `/rpc` |

## Entrypoint

```python
from tba_app_backend_resource_validation import app, build_app
```

## Local dev deployment

Run the isolated validation front door on port `8014`:

```bash
docker compose -f docker/docker-compose.resource-validation-app.yml up -d --build
```

Useful endpoints:

| Endpoint | Purpose |
| --- | --- |
| `/.well-known/openid-configuration` | Issuer metadata needed by validators. |
| `/.well-known/oauth-protected-resource` | Protected-resource metadata and verifier contract projection. |
| `/.well-known/jwks.json` | Issuer key set for local JWT validation. |
| `/tenants/{tenant_slug}/.well-known/jwks.json` | Tenant-scoped key set. |
| `/introspect` | RFC 7662 token status checks for authorized callers. |

## Package Boundary

`tba-app-backend-resource-validation` belongs to `090-backend-apps` and owns deployable backend composition: JWKS, introspection, and protected-resource validation backend application for TBA.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-resource-validation/src/tba_app_backend_resource_validation/__init__.py). Public exports include `PRODUCT_SURFACE`, `RESOURCE_VALIDATION_BACKEND_APP_CONTRACT`, `ResourceValidationBackendAppContract`, `app`, `build_app`.

Keep new protocol grammars or independent persistence implementations in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

The [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-resource-validation/src/tba_app_backend_resource_validation/__init__.py) for `tba-app-backend-resource-validation` does not declare an explicit service-constructor or keyword-only factory hook in the inspected source. Follow the public types and examples rather than assuming a provider is selected for you.

Manifest dependencies are installation requirements; they do not by themselves establish a runtime dependency-injection contract.

## Operations and readiness

`tba-app-backend-resource-validation` exposes deployable backend composition. Public operations found in its source:

- `build_app` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-resource-validation/src/tba_app_backend_resource_validation/app.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-app-backend-resource-validation`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

## Non-goals

`tba-app-backend-resource-validation` does not take ownership of new protocol grammars or independent persistence implementations.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

Declared local runtime dependencies:

- [tba-app-backend-core](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-core/README.md)
- [tba-auth](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-auth/README.md)
- [tba-router-oauth-introspection](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-oauth-introspection/README.md)
- [tba-router-oauth-protected-resource-metadata](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-oauth-protected-resource-metadata/README.md)
- [tba-router-oidc-discovery](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-oidc-discovery/README.md)
- [tba-router-resource-validation-metadata](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-resource-validation-metadata/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/090-backend-apps/tba-app-backend-resource-validation)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-resource-validation/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-resource-validation/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-resource-validation/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-app-backend-resource-validation/)

## Governance

`tba-app-backend-resource-validation` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `090-backend-apps` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-resource-validation/src/tba_app_backend_resource_validation/__init__.py).
