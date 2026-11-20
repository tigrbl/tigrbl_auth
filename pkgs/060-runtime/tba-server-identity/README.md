# tba-server-identity

<!-- readme-standards:begin branding -->
<p align="center"><a href="https://github.com/tigrbl/tigrbl_auth"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="300"></a></p>
<p align="center"><strong>tba-server-identity</strong></p>
<p align="center">Carrier-neutral identity runtime handlers, capability assembly, and lifecycle integration.</p>
<p align="center">
<a href="https://pypi.org/project/tba-server-identity/"><img alt="pypi: tba-server-identity" src="https://img.shields.io/pypi/v/tba-server-identity"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-server-identity/pyproject.toml"><img alt="Source version: 0.4.0.dev3" src="https://img.shields.io/static/v1?label=Source%20version&amp;message=0.4.0.dev3&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-server-identity/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/static/v1?label=Python&amp;message=%3E%3D3.10%2C%3C3.16&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-server-identity/pyproject.toml"><img alt="Layer: 060-runtime" src="https://img.shields.io/static/v1?label=Layer&amp;message=060-runtime&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-server-identity/README.md#lifecycle-and-migration"><img alt="Lifecycle: active" src="https://img.shields.io/static/v1?label=Lifecycle&amp;message=active&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-server-identity/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/static/v1?label=License&amp;message=Apache-2.0&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-server-identity/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/static/v1?label=Notice&amp;message=attribution&amp;color=525252"></a>
</p>
<p align="center">
<a href="https://pypi.org/project/tba-server-identity/"><img alt="Monthly PyPI downloads: tba-server-identity" src="https://img.shields.io/pypi/dm/tba-server-identity"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-server-identity/README.md"><img alt="README hits: tba-server-identity" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/pkgs/060-runtime/tba-server-identity/README.md.svg?label=README%20hits"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="README standards: CI gate" src="https://img.shields.io/static/v1?label=README%20standards&amp;message=CI%20gate&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-server-identity/docs/readme/test_examples.py"><img alt="Tests: example source" src="https://img.shields.io/static/v1?label=Tests&amp;message=example%20source&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-server-identity/README.md#certification-status"><img alt="Certification: not certified" src="https://img.shields.io/static/v1?label=Certification&amp;message=not%20certified&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/tools/readme/POLICY.md"><img alt="Governance: repository policy" src="https://img.shields.io/static/v1?label=Governance&amp;message=repository%20policy&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="Evidence: source and CI" src="https://img.shields.io/static/v1?label=Evidence&amp;message=source%20and%20CI&amp;color=525252"></a>
</p>
<p align="center"><a href="#overview">Overview</a> · <a href="#installation">Installation</a> · <a href="#quick-start">Quick Start</a> · <a href="#usage">Usage</a> · <a href="#public-api-and-import-surfaces">API</a> · <a href="#contributing">Contributing</a> · <a href="#governance">Governance</a> · <a href="#license">License</a></p>
<!-- readme-standards:end branding -->

---

## Overview

### Summary

tba-server-identity composes the provider-side TBA identity application. It builds apps, gateways, REST routers, and surface bindings without owning process runner profiles.

- Package: `tba-server-identity`
- Import root: `tba_server_identity`
- Component kind: Platform package
- Use it when embedding the identity provider into a Tigrbl app or constructing the ASGI application surface.
- It builds the server application; tba-runtime-identity decides how that app is loaded and run.
- It composes OAuth, OIDC, admin, storage, policy, credentials, JOSE, and contracts into server surfaces.

### Why This Package

`tba-server-identity` isolates this responsibility: Carrier-neutral identity runtime handlers, capability assembly, and lifecycle integration. Its [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-server-identity/src/tba_server_identity/__init__.py) exposes `AssemblyManifest`, `DEFAULT_ROUTE_SURFACES`, `RouteSurface`, `ServerProfile`, `SurfacePlane`, `assert_public_admin_separation`, `build_route_surface_registry`, `compose_server_manifest`, `provider_server_profile`, allowing consumers to select this package without treating adjacent packages as part of its public contract.

### When to Use

Choose `tba-server-identity` for this responsibility: Carrier-neutral identity runtime handlers, capability assembly, and lifecycle integration. Its `060-runtime` placement keeps runtime composition and operator entry points separate from duplicating protocol grammars, table declarations, or provider implementations.

### Features

- `CredsIn`: declared in src/tba_server_identity/admin_auth.py
- `AdminPasswordResetRequestIn`: declared in src/tba_server_identity/admin_auth.py
- `AdminPasswordResetCompleteIn`: declared in src/tba_server_identity/admin_auth.py
- `AdminPasswordChangeIn`: declared in src/tba_server_identity/admin_auth.py
- `AdminSessionOut`: declared in src/tba_server_identity/admin_auth.py
- `SurfacePlane`: declared in src/tba_server_identity/assembly.py
- `RouteSurface`: declared in src/tba_server_identity/assembly.py
- `ServerProfile`: declared in src/tba_server_identity/assembly.py

### Non-Goals

`tba-server-identity` does not take ownership of duplicating protocol grammars, table declarations, or provider implementations.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

---

## Getting Started

### Prerequisites

Python `>=3.10,<3.16` is required. The [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-server-identity/pyproject.toml) declares runtime dependencies including `tba-capability-api-key-authentication`, `tba-capability-service-key-authentication`, `tba-capability-account-self-service`, `tba-certification-release`, `tba-protocol-oauth`, `tba-protocol-oidc`, `tba-protocol-gnap`, `tba-contracts-identity`, `tba-capability-identity-administration`, `tba-capability-realm-administration`, `tba-capability-tenant-administration`, `tba-provider-identity-jose`. Read the example’s inputs and service requirements before execution.

### Installation

```bash
pip install tba-server-identity
# or
uv add tba-server-identity
```

Install the current `tba-server-identity` source checkout when working ahead of a PyPI release:

```bash
uv pip install ./pkgs/060-runtime/tba-server-identity
```

#### uv

<!-- readme-standards:begin installation.uv -->
```bash
uv add tba-server-identity
```
<!-- readme-standards:end installation.uv -->

#### pip

<!-- readme-standards:begin installation.pip -->
```bash
python -m pip install tba-server-identity
```
<!-- readme-standards:end installation.pip -->

#### Poetry

<!-- readme-standards:begin installation.poetry -->
```bash
poetry add tba-server-identity
```
<!-- readme-standards:end installation.poetry -->

### Quick Start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.


```bash
uv run --isolated --no-project --python 3.12 --with "tba-server-identity==0.4.0.dev3" python quickstart.py
```

The import and assertion succeed when the AssemblyManifest entry point is available.

#### Example

<!-- readme-standards:begin example.quick-start -->
Source: [docs/readme/quick_start.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-server-identity/docs/readme/quick_start.py).

```python
from tba_server_identity import AssemblyManifest

assert callable(AssemblyManifest)
```
<!-- readme-standards:end example.quick-start -->

#### Expected Result

The example demonstrates the documented `tba-server-identity` source boundary or workflow. Complete its required configuration first. README CI checks the maintained source’s syntax and declarations; it does not claim that external services or the application workflow were exercised.

---

## Usage

### Common Workflows

<!-- readme-standards:begin example.usage -->
Source: [docs/readme/usage.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-server-identity/docs/readme/usage.py).

```python
from tba_server_identity.gateway import build_gateway

gateway = build_gateway()
```
<!-- readme-standards:end example.usage -->

### Configuration

Configure `tba-server-identity` through the APIs in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-server-identity/src/tba_server_identity/__init__.py); its [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-server-identity/pyproject.toml) describes installation requirements, not an implicit service configuration. No additional package-global configuration contract is inferred from dependencies.

### Error Handling

The inspected `tba-server-identity` source raises `AccountAuthenticationError`, `AccountValidationError`, `HTTPException`, `IdentityAdministrationConflictError`, `IdentityAdministrationNotFoundError`, `IdentityAdministrationValidationError`, `InvalidRefreshTokenError`, `RealmAdministrationConflictError`, `RealmAdministrationNotFoundError`, `RealmAdministrationValidationError`. Handle these at the calling boundary and consult the implementation for the triggering conditions.

### Best Practices

Use the explicit `tba-server-identity` imports documented below and keep collaborator configuration with the caller. Run the package’s relevant tests after changing `AssemblyManifest`, `DEFAULT_ROUTE_SURFACES`, `RouteSurface`, `ServerProfile`, `SurfacePlane`, `assert_public_admin_separation`, `build_route_surface_registry`, `compose_server_manifest`, `provider_server_profile`; an import or successful installation alone does not establish its runtime guarantees.

---

## Package Boundary

### What It Owns

- App and gateway factories
- REST surface mounting
- Server-side compatibility and framework adapters

Plugin installation is owned by `tba-plugin-tigrbl`; `tba_server_identity.plugin` remains a compatibility import for existing callers.

### Public API and Import Surfaces

Import namespace: `tba_server_identity`.

Source-declared exports or types: `AssemblyManifest`, `DEFAULT_ROUTE_SURFACES`, `RouteSurface`, `ServerProfile`, `SurfacePlane`, `assert_public_admin_separation`, `build_route_surface_registry`, `compose_server_manifest`, `provider_server_profile`.

Inspect [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-server-identity/src/tba_server_identity/__init__.py) for exact signatures; this inventory does not designate every internal module as stable.

### Entry Points

<!-- readme-standards:begin entry-points -->
This package declares no command-line, GUI, or plugin entry points in its manifest.
<!-- readme-standards:end entry-points -->

### Injected Dependencies

The [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-server-identity/src/tba_server_identity/__init__.py) for `tba-server-identity` does not declare an explicit service-constructor or keyword-only factory hook in the inspected source. Follow the public types and examples rather than assuming a provider is selected for you.

Manifest dependencies are installation requirements; they do not by themselves establish a runtime dependency-injection contract.

### Protocol Consumers

Direct consumers in this checkout’s package manifests include `tba-plugin-tigrbl`, `tba-runtime-identity-administration`, `tba-auth`, `tba-app-backend-core`, `tba-app-backend-my-account`, `tba-app-backend-platform-administration`, `tba-workspace`. These edges describe declared dependencies, not protocol-conformance evidence.

### Extensions

For `tba-server-identity`, use the source-declared public interfaces (`AssemblyManifest`, `DEFAULT_ROUTE_SURFACES`, `RouteSurface`, `ServerProfile`, `SurfacePlane`, `assert_public_admin_separation`, `build_route_surface_registry`, `compose_server_manifest`, `provider_server_profile`) when composing or extending behavior. Its entry-point section below is authoritative for registered plugins; no additional extension loader is inferred from the package name.

---

## Operations and Readiness

### Operational Requirements

`tba-server-identity` exposes runtime composition and operator entry points. Public operations found in its source:

- `AssemblyManifest.public_routes` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-server-identity/src/tba_server_identity/assembly.py).
- `AssemblyManifest.admin_routes` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-server-identity/src/tba_server_identity/assembly.py).
- `AssemblyManifest.route_names` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-server-identity/src/tba_server_identity/assembly.py).
- `build_route_surface_registry` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-server-identity/src/tba_server_identity/assembly.py).
- `compose_server_manifest` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-server-identity/src/tba_server_identity/assembly.py).
- `assert_public_admin_separation` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-server-identity/src/tba_server_identity/assembly.py).
- `provider_server_profile` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-server-identity/src/tba_server_identity/assembly.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

### Health and Observability

This README does not establish a standalone health endpoint for `tba-server-identity`. Observe the concrete caller’s results, exceptions, and existing test reports. An application that embeds this package must define its own health and telemetry contract.

### Security and Resource Limits

Apply the input, credential, and resource constraints implemented in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-server-identity/src/tba_server_identity/__init__.py). The `tba-server-identity` README gate is a documentation check, not a security review or a substitute for the implementation’s limits and caller authorization.

### Compatibility

This source version of `tba-server-identity` declares Python `>=3.10,<3.16`. Consult its dependency constraints before upgrading. Source-version and registry-version badges have separate meanings; this migration makes no additional platform or interoperability certification claim.

---

## Verification

### Tests

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-server-identity/src/tba_server_identity/__init__.py).

### Certification Status

No external certification is asserted for `tba-server-identity` by this documentation migration. README conformance, example syntax, runtime tests, and protocol or security certification are distinct evidence scopes.

### Evidence

The [README standards CI](https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml) records mechanical documentation results for its tested commit. The [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-server-identity/src/tba_server_identity/__init__.py) and example sources support the package-boundary description; external runtime behavior requires its own test evidence.

---

## FAQ

### Why

**Why select this package?** `tba-server-identity` provides carrier-neutral identity runtime handlers, capability assembly, and lifecycle integration; use its own API boundary rather than assuming neighboring packages are bundled or configured automatically.

### How

**How do I start?** Install or synchronize the environment under Getting Started, follow the maintained example for `tba-server-identity`, and consult [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-server-identity/src/tba_server_identity/__init__.py) for the exact types and signatures involved.

### When

**When should I validate an upgrade?** Recheck `tba-server-identity` whenever its source version, declared collaborators, configuration, or caller changes. Run relevant behavioral tests in addition to the README gate before promotion.

---

## Documentation and Related Packages

### More Documentation

The [repository contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md), [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-server-identity/src/tba_server_identity/__init__.py), and [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-server-identity/pyproject.toml) provide the supporting context for `tba-server-identity`. The [README policy](https://github.com/groupsum/readme-standards/blob/master/docs/outline.md) defines the common document structure.

### Related Packages

- [tba-runtime-identity-administration](https://pypi.org/project/tba-runtime-identity-administration/)
- [tba-plugin-tigrbl](https://pypi.org/project/tba-plugin-tigrbl/)
- [tba-storage-core](https://pypi.org/project/tba-storage-core/)
- [tba-server-identity](https://pypi.org/project/tba-server-identity/)
- [tba-runtime-identity](https://pypi.org/project/tba-runtime-identity/)
- [tba-operator-identity](https://pypi.org/project/tba-operator-identity/)
- [tba-tests-identity](https://pypi.org/project/tba-tests-identity/)

### Project Links

<!-- readme-standards:begin project-links -->
- [Documentation](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/060-runtime/tba-server-identity#readme)
- [Homepage](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/060-runtime/tba-server-identity#readme)
- [Issues](https://github.com/tigrbl/tigrbl_auth/issues)
- [PyPI](https://pypi.org/project/tba-server-identity/)
- [Repository](https://github.com/tigrbl/tigrbl_auth)
- [SSOT](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [Source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/060-runtime/tba-server-identity)
- [pypi: tba-server-identity](https://pypi.org/project/tba-server-identity/)
<!-- readme-standards:end project-links -->

- [PyPI package](https://pypi.org/project/tba-server-identity/)
- [Source repository](https://github.com/tigrbl/tigrbl_auth)
- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/060-runtime/tba-server-identity)
- [SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/060-runtime/tba-server-identity)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-server-identity/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-server-identity/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-server-identity/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-server-identity/)

---

## Contributing

### How to Contribute

Follow the [contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md) and include a focused example or regression for changes to `tba-server-identity`. Keep package behavior, its documented boundary, and its tests aligned.

### Development Setup

Work from the `pkgs/060-runtime/tba-server-identity` checkout. Synchronize its declared development environment with uv, then run the relevant package tests and `python -m pytest docs/readme/test_examples.py`. The repository’s dedicated README job installs `readme-standards==0.1.1` without resolving unrelated runtime packages.

### Notes for Maintainers

Edit authored prose directly in this `tba-server-identity` README. Update source examples in `docs/readme/`, then run `readme-standards render --root . --write` from the package directory and review the diff. Required headings and generated blocks come from package-guide-v1.

---

## Governance

### Ownership and Decision Making

Changes to `tba-server-identity` follow the maintainer review process of [tigrbl/tigrbl_auth](https://github.com/tigrbl/tigrbl_auth) and its contribution guide. Author attribution remains in the [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-server-identity/pyproject.toml); this README does not assign new publishing or administrative authority.

### Standards and Policies

This package is part of the SSOT-governed TBA identity package suite. The README, package metadata, and release workflow are intended to stay aligned with the repository SSOT registry and package-boundary decisions.

`tba-server-identity` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `060-runtime` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

### Lifecycle and Migration

The `tba-server-identity` source version is `0.4.0.dev3`. This change standardizes documentation and adds a development-only gate; it does not publish a new runtime version or declare a previously unpublished package released. Preserve explicit deprecation and replacement instructions where present.

---

## License and Attribution

### License

<!-- readme-standards:begin license -->
Licensed under `Apache-2.0`. See [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-server-identity/LICENSE).
<!-- readme-standards:end license -->

### Notices

<!-- readme-standards:begin notices -->
See [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-server-identity/NOTICE) for attribution.
<!-- readme-standards:end notices -->
