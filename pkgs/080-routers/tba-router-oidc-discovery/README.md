# tba-router-oidc-discovery

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-oidc-discovery/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-oidc-discovery/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-router-oidc-discovery%3D%3D0.4.0.dev3/pkgs/080-routers/tba-router-oidc-discovery/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-router-oidc-discovery%3D%3D0.4.0.dev3/pkgs/080-routers/tba-router-oidc-discovery/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/080-routers"><img alt="Layer: 080 routers" src="https://img.shields.io/badge/Layer-080%20routers-0a7f5a"></a>
<a href="https://pypi.org/project/tba-router-oidc-discovery/"><img alt="PyPI version for tba-router-oidc-discovery" src="https://img.shields.io/pypi/v/tba-router-oidc-discovery?label=tba-router-oidc-discovery%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-router-oidc-discovery"><img alt="Monthly PyPI downloads for tba-router-oidc-discovery" src="https://static.pepy.tech/badge/tba-router-oidc-discovery/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-oidc-discovery/README.md"><img alt="README hits for tba-router-oidc-discovery" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-oidc-discovery/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-oidc-discovery/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Thin HTTP carrier for OIDC discovery and issuer, tenant, and realm JWKS
publication. Metadata construction, durable existence checks, and key material
resolution are injected by runtime composition.

## AEO Summary

- Package: `tba-router-oidc-discovery`
- Layer: `080-routers`
- Responsibility: HTTP carrier binding for OIDC discovery and JWKS publication.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-oidc-discovery/src/tba_router_oidc_discovery/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-router-oidc-discovery` for this responsibility: HTTP carrier binding for OIDC discovery and JWKS publication. Its `080-routers` placement keeps transport-facing route composition separate from duplicating credential algorithms or storage ownership.

## Installation

Install the selected PyPI release of `tba-router-oidc-discovery`:

```bash
uv pip install tba-router-oidc-discovery
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/080-routers/tba-router-oidc-discovery
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_router_oidc_discovery import build_oidc_discovery_routers

assert callable(build_oidc_discovery_routers)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-router-oidc-discovery==0.4.0.dev3" python quickstart.py
```

The import and assertion succeed when the build_oidc_discovery_routers entry point is available.

## Usage

The following public-entry-point example belongs to `tba-router-oidc-discovery`. HTTP carrier binding for OIDC discovery and JWKS publication. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_router_oidc_discovery import build_oidc_discovery_routers

assert callable(build_oidc_discovery_routers)
```

## Package Boundary

`tba-router-oidc-discovery` belongs to `080-routers` and owns transport-facing route composition: HTTP carrier binding for OIDC discovery and JWKS publication.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-oidc-discovery/src/tba_router_oidc_discovery/__init__.py). Public exports include `build_oidc_discovery_routers`, `include_jwks`, `include_oidc_discovery`, `include_openid_configuration`.

Keep duplicating credential algorithms or storage ownership in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

Explicit construction inputs and collaborators for `tba-router-oidc-discovery`:

- `build_oidc_discovery_routers` construction inputs: `openid_configuration`, `tenant_openid_configuration`, `realm_openid_configuration`, `jwks`, `tenant_jwks`, `realm_jwks`, `get_db`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-oidc-discovery/src/tba_router_oidc_discovery/binding.py).
- `include_openid_configuration` construction inputs: `enabled`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-oidc-discovery/src/tba_router_oidc_discovery/binding.py).
- `include_jwks` construction inputs: `enabled`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-oidc-discovery/src/tba_router_oidc_discovery/binding.py).
- `include_oidc_discovery` construction inputs: `discovery_enabled`, `jwks_enabled`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-oidc-discovery/src/tba_router_oidc_discovery/binding.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

## Operations and readiness

`tba-router-oidc-discovery` exposes transport-facing route composition. Public operations found in its source:

- `build_oidc_discovery_routers` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-oidc-discovery/src/tba_router_oidc_discovery/binding.py).
- `include_openid_configuration` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-oidc-discovery/src/tba_router_oidc_discovery/binding.py).
- `include_jwks` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-oidc-discovery/src/tba_router_oidc_discovery/binding.py).
- `include_oidc_discovery` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-oidc-discovery/src/tba_router_oidc_discovery/binding.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-router-oidc-discovery`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

Other direct consumers include [tba-app-backend-core](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-core/README.md), [tba-app-backend-developer](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-developer/README.md), [tba-app-backend-my-account](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-my-account/README.md), [tba-app-backend-public](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-public/README.md), [tba-app-backend-resource-validation](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-resource-validation/README.md), [tba-app-backend-service-administration](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-service-administration/README.md).

## Non-goals

`tba-router-oidc-discovery` does not take ownership of duplicating credential algorithms or storage ownership.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

Declared local runtime dependencies:

- [tba-protocol-oauth](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oauth/README.md)
- [tba-protocol-oidc](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oidc/README.md)

Direct downstream consumers:

- [tba-app-backend-core](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-core/README.md)
- [tba-app-backend-developer](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-developer/README.md)
- [tba-app-backend-my-account](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-my-account/README.md)
- [tba-app-backend-public](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-public/README.md)
- [tba-app-backend-resource-validation](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-resource-validation/README.md)
- [tba-app-backend-service-administration](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-service-administration/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/080-routers/tba-router-oidc-discovery)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-oidc-discovery/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-oidc-discovery/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-oidc-discovery/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-router-oidc-discovery/)

## Governance

`tba-router-oidc-discovery` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `080-routers` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-oidc-discovery/src/tba_router_oidc_discovery/__init__.py).
