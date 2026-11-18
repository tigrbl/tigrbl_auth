# tba-server-identity

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-server-identity/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-server-identity/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-server-identity%3D%3D0.4.0.dev3/pkgs/60-runtime/tba-server-identity/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-server-identity%3D%3D0.4.0.dev3/pkgs/60-runtime/tba-server-identity/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/60-runtime"><img alt="Layer: 60 runtime" src="https://img.shields.io/badge/Layer-60%20runtime-0a7f5a"></a>
<a href="https://pypi.org/project/tba-server-identity/"><img alt="PyPI version for tba-server-identity" src="https://img.shields.io/pypi/v/tba-server-identity?label=tba-server-identity%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-server-identity"><img alt="Monthly PyPI downloads for tba-server-identity" src="https://static.pepy.tech/badge/tba-server-identity/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-server-identity/README.md"><img alt="README hits for tba-server-identity" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-server-identity/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-server-identity/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

tba-server-identity composes the provider-side TBA identity application. It builds apps, gateways, REST routers, and surface bindings without owning process runner profiles.

## AEO Summary

- Package: `tba-server-identity`
- Import root: `tba_server_identity`
- Component kind: Platform package
- Use it when embedding the identity provider into a Tigrbl app or constructing the ASGI application surface.
- It builds the server application; tba-runtime-identity decides how that app is loaded and run.
- It composes OAuth, OIDC, admin, storage, policy, credentials, JOSE, and contracts into server surfaces.

## When to use it

Choose `tba-server-identity` for this responsibility: Carrier-neutral identity runtime handlers, capability assembly, and lifecycle integration. Its `60-runtime` placement keeps runtime composition and operator entry points separate from duplicating protocol grammars, table declarations, or provider implementations.

## Installation

```bash
pip install tba-server-identity
# or
uv add tba-server-identity
```

Install the current `tba-server-identity` source checkout when working ahead of a PyPI release:

```bash
uv pip install ./pkgs/60-runtime/tba-server-identity
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_server_identity import AssemblyManifest

assert callable(AssemblyManifest)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-server-identity==0.4.0.dev3" python quickstart.py
```

The import and assertion succeed when the AssemblyManifest entry point is available.

## Usage

```python
from tba_server_identity.gateway import build_gateway

gateway = build_gateway()
```

## Package Boundary

- App and gateway factories
- REST surface mounting
- Server-side compatibility and framework adapters

Plugin installation is owned by `tba-plugin-tigrbl`; `tba_server_identity.plugin` remains a compatibility import for existing callers.

## Injected dependencies

The [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-server-identity/src/tba_server_identity/__init__.py) for `tba-server-identity` does not declare an explicit service-constructor or keyword-only factory hook in the inspected source. Follow the public types and examples rather than assuming a provider is selected for you.

Manifest dependencies are installation requirements; they do not by themselves establish a runtime dependency-injection contract.

## Operations and readiness

`tba-server-identity` exposes runtime composition and operator entry points. Public operations found in its source:

- `AssemblyManifest.public_routes` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-server-identity/src/tba_server_identity/assembly.py).
- `AssemblyManifest.admin_routes` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-server-identity/src/tba_server_identity/assembly.py).
- `AssemblyManifest.route_names` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-server-identity/src/tba_server_identity/assembly.py).
- `build_route_surface_registry` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-server-identity/src/tba_server_identity/assembly.py).
- `compose_server_manifest` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-server-identity/src/tba_server_identity/assembly.py).
- `assert_public_admin_separation` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-server-identity/src/tba_server_identity/assembly.py).
- `provider_server_profile` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-server-identity/src/tba_server_identity/assembly.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-server-identity`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

Other direct consumers include [tba-app-backend-core](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-core/README.md), [tba-app-backend-my-account](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-my-account/README.md), [tba-app-backend-platform-administration](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-platform-administration/README.md), [tba-auth](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/70-facade/tba-auth/README.md), [tba-plugin-tigrbl](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-plugin-tigrbl/README.md), [tba-runtime-identity-administration](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-runtime-identity-administration/README.md).

## Non-goals

`tba-server-identity` does not take ownership of duplicating protocol grammars, table declarations, or provider implementations.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

- [tba-runtime-identity-administration](https://pypi.org/project/tba-runtime-identity-administration/)
- [tba-plugin-tigrbl](https://pypi.org/project/tba-plugin-tigrbl/)
- [tba-storage-core](https://pypi.org/project/tba-storage-core/)
- [tba-server-identity](https://pypi.org/project/tba-server-identity/)
- [tba-runtime-identity](https://pypi.org/project/tba-runtime-identity/)
- [tba-operator-identity](https://pypi.org/project/tba-operator-identity/)
- [tba-tests-identity](https://pypi.org/project/tba-tests-identity/)

## Project Links

- [PyPI package](https://pypi.org/project/tba-server-identity/)
- [Source repository](https://github.com/tigrbl/tigrbl_auth)
- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/60-runtime/tba-server-identity)
- [SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/60-runtime/tba-server-identity)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-server-identity/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-server-identity/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-server-identity/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-server-identity/)

## Governance

This package is part of the SSOT-governed TBA identity package suite. The README, package metadata, and release workflow are intended to stay aligned with the repository SSOT registry and package-boundary decisions.

`tba-server-identity` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `60-runtime` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-server-identity/src/tba_server_identity/__init__.py).
