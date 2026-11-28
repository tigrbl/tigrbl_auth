# tba-app-backend-core

<!-- readme-standards:begin branding -->
<p align="center"><a href="https://github.com/tigrbl/tigrbl_auth"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="300"></a></p>
<p align="center"><strong>tba-app-backend-core</strong></p>
<p align="center">Shared layer-90 ASGI and router composition for TBA backend applications.</p>
<p align="center">
<a href="https://pypi.org/project/tba-app-backend-core/"><img alt="pypi: tba-app-backend-core" src="https://img.shields.io/pypi/v/tba-app-backend-core?labelColor=1E293B&amp;color=1D4ED8"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-core/pyproject.toml"><img alt="Source version: 0.4.0.dev3" src="https://img.shields.io/static/v1?label=Source%20version&amp;message=0.4.0.dev3&amp;labelColor=1E293B&amp;color=4338CA"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-core/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/static/v1?label=Python&amp;message=%3E%3D3.10%2C%3C3.16&amp;labelColor=1E293B&amp;color=0F766E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-core/pyproject.toml"><img alt="Layer: 090-backend-apps" src="https://img.shields.io/static/v1?label=Layer&amp;message=090-backend-apps&amp;labelColor=1E293B&amp;color=6D28D9"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-core/README.md#lifecycle-and-migration"><img alt="Lifecycle: active" src="https://img.shields.io/static/v1?label=Lifecycle&amp;message=active&amp;labelColor=1E293B&amp;color=166534"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-core/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/static/v1?label=License&amp;message=Apache-2.0&amp;labelColor=1E293B&amp;color=86198F"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-core/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/static/v1?label=Notice&amp;message=attribution&amp;labelColor=1E293B&amp;color=86198F"></a>
</p>
<p align="center">
<a href="https://pypi.org/project/tba-app-backend-core/"><img alt="Monthly PyPI downloads: tba-app-backend-core" src="https://img.shields.io/pypi/dm/tba-app-backend-core?labelColor=1E293B&amp;color=0E7490"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-core/README.md"><img alt="README hits: tba-app-backend-core" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/pkgs/090-backend-apps/tba-app-backend-core/README.md.svg?label=README%20hits&amp;labelColor=1E293B&amp;color=0E7490"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="README standards: CI gate" src="https://img.shields.io/static/v1?label=README%20standards&amp;message=CI%20gate&amp;labelColor=1E293B&amp;color=1D4ED8"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-core/docs/readme/test_examples.py"><img alt="Tests: example source" src="https://img.shields.io/static/v1?label=Tests&amp;message=example%20source&amp;labelColor=1E293B&amp;color=0F766E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-core/README.md#certification-status"><img alt="Certification: not certified" src="https://img.shields.io/static/v1?label=Certification&amp;message=not%20certified&amp;labelColor=1E293B&amp;color=92400E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/tools/readme/POLICY.md"><img alt="Governance: repository policy" src="https://img.shields.io/static/v1?label=Governance&amp;message=repository%20policy&amp;labelColor=1E293B&amp;color=4338CA"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="Evidence: source and CI" src="https://img.shields.io/static/v1?label=Evidence&amp;message=source%20and%20CI&amp;labelColor=1E293B&amp;color=6D28D9"></a>
</p>
<p align="center"><a href="#overview">Overview</a> · <a href="#installation">Installation</a> · <a href="#quick-start">Quick Start</a> · <a href="#usage">Usage</a> · <a href="#public-api-and-import-surfaces">API</a> · <a href="#contributing">Contributing</a> · <a href="#governance">Governance</a> · <a href="#license">License</a></p>
<!-- readme-standards:end branding -->

---

## Overview

### Summary

Shared layer-90 composition for deployable TBA backend applications.

This package owns ASGI application construction, layer-80 router closure, HTTP
surface assembly, administrative gate wrapping, and product-surface selection.
Product backend-app packages supply a declared product contract and call the
shared build_product_app factory.

It does not own protocol semantics, capability implementations, durable table
behavior, runtime handlers, or storage. Those remain in layers 50, 40, 30, and
60 and are injected or imported downward.

- Package: `tba-app-backend-core`
- Layer: `090-backend-apps`
- Responsibility: Shared layer-90 ASGI and router composition for TBA backend applications.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-core/src/tba_app_backend_core/__init__.py).
- Distribution: Python package on PyPI.

### Why This Package

`tba-app-backend-core` isolates this responsibility: Shared layer-90 ASGI and router composition for TBA backend applications. Its [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-core/src/tba_app_backend_core/__init__.py) exposes `TbaBackendAppPlugin`, `app`, `build_app`, `build_application_runtime_plan`, `build_product_app`, `install`, `validate_backend_app_contract`, allowing consumers to select this package without treating adjacent packages as part of its public contract.

### When to Use

Choose `tba-app-backend-core` for this responsibility: Shared layer-90 ASGI and router composition for TBA backend applications. Its `090-backend-apps` placement keeps deployable backend composition separate from new protocol grammars or independent persistence implementations.

### Features

- `TbaBackendAppPlugin`: declared in src/tba_app_backend_core/plugin.py
- `TableInitializationScopeError`: Raised when a product surface selects table resources outside its contract.

### Non-Goals

`tba-app-backend-core` does not take ownership of new protocol grammars or independent persistence implementations.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

---

## Getting Started

### Prerequisites

Python `>=3.10,<3.16` is required. The [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-core/pyproject.toml) declares runtime dependencies including `tigrbl`, `tba-protocol-gnap`, `tba-protocol-oauth`, `tba-plugin-tigrbl`, `tba-router-administration-gate`, `tba-router-oauth-authorization`, `tba-router-oauth-authorization-server-metadata`, `tba-router-oauth-device-authorization`, `tba-router-oauth-introspection`, `tba-router-oauth-pushed-authorization-request`, `tba-router-oauth-protected-resource-metadata`, `tba-router-oauth-registration`. Read the example’s inputs and service requirements before execution.

### Installation

Install the selected PyPI release of `tba-app-backend-core`:

```bash
uv pip install tba-app-backend-core
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/090-backend-apps/tba-app-backend-core
```

#### uv

<!-- readme-standards:begin installation.uv -->
```bash
uv add tba-app-backend-core
```
<!-- readme-standards:end installation.uv -->

#### pip

<!-- readme-standards:begin installation.pip -->
```bash
python -m pip install tba-app-backend-core
```
<!-- readme-standards:end installation.pip -->

#### Poetry

<!-- readme-standards:begin installation.poetry -->
```bash
poetry add tba-app-backend-core
```
<!-- readme-standards:end installation.poetry -->

### Quick Start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.


```bash
uv run --isolated --no-project --python 3.12 --with "tba-app-backend-core==0.4.0.dev3" python quickstart.py
```

The import and assertion succeed when the app entry point is available.

#### Example

<!-- readme-standards:begin example.quick-start -->
Source: [docs/readme/quick_start.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-core/docs/readme/quick_start.py).

```python
from tba_app_backend_core import app

assert callable(app)
```
<!-- readme-standards:end example.quick-start -->

#### Expected Result

The example demonstrates the documented `tba-app-backend-core` source boundary or workflow. Complete its required configuration first. README CI checks the maintained source’s syntax and declarations; it does not claim that external services or the application workflow were exercised.

---

## Usage

### Common Workflows

<!-- readme-standards:begin example.usage -->
Source: [docs/readme/usage.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-core/docs/readme/usage.py).

```python
from tba_app_backend_core import app

assert callable(app)
```
<!-- readme-standards:end example.usage -->

The following public-entry-point example belongs to `tba-app-backend-core`. Shared layer-90 ASGI and router composition for TBA backend applications. Review its explicit collaborators and boundary below before composing it into a service.

### Configuration

Configure `tba-app-backend-core` through the APIs in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-core/src/tba_app_backend_core/__init__.py); its [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-core/pyproject.toml) describes installation requirements, not an implicit service configuration. No additional package-global configuration contract is inferred from dependencies.

### Error Handling

The inspected `tba-app-backend-core` source raises `HTTPException`, `TableInitializationScopeError`, `ValueError`. Handle these at the calling boundary and consult the implementation for the triggering conditions.

### Best Practices

Use the explicit `tba-app-backend-core` imports documented below and keep collaborator configuration with the caller. Run the package’s relevant tests after changing `TbaBackendAppPlugin`, `app`, `build_app`, `build_application_runtime_plan`, `build_product_app`, `install`, `validate_backend_app_contract`; an import or successful installation alone does not establish its runtime guarantees.

---

## Package Boundary

### What It Owns

`tba-app-backend-core` belongs to `090-backend-apps` and owns deployable backend composition: Shared layer-90 ASGI and router composition for TBA backend applications.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-core/src/tba_app_backend_core/__init__.py). Public exports include `app`, `build_app`, `build_application_runtime_plan`, `TbaBackendAppPlugin`, `build_product_app`, `install`, `validate_backend_app_contract`.

Keep new protocol grammars or independent persistence implementations in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

### Public API and Import Surfaces

Import namespace: `tba_app_backend_core`.

Source-declared exports or types: `TbaBackendAppPlugin`, `app`, `build_app`, `build_application_runtime_plan`, `build_product_app`, `install`, `validate_backend_app_contract`.

Inspect [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-core/src/tba_app_backend_core/__init__.py) for exact signatures; this inventory does not designate every internal module as stable.

### Entry Points

<!-- readme-standards:begin entry-points -->
- `tba_auth.app_factories` → `default` → `tba_app_backend_core.app:build_app`
<!-- readme-standards:end entry-points -->

### Injected Dependencies

Explicit construction inputs and collaborators for `tba-app-backend-core`:

- `build_app` construction inputs: `deployment`, `runtime_assembly_factory`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-core/src/tba_app_backend_core/app.py).
- `TbaBackendAppPlugin` construction inputs: `diagnostics_prefix`, `settings`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-core/src/tba_app_backend_core/plugin.py).
- `build_product_app` construction inputs: `contract`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-core/src/tba_app_backend_core/product.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

### Protocol Consumers

Direct consumers in this checkout’s package manifests include `tba-app-backend-developer`, `tba-app-backend-my-account`, `tba-app-backend-platform-administration`, `tba-app-backend-public`, `tba-app-backend-resource-validation`, `tba-app-backend-service-administration`, `tba-app-backend-tenant-administration`, `tba-workspace`. These edges describe declared dependencies, not protocol-conformance evidence.

### Extensions

For `tba-app-backend-core`, use the source-declared public interfaces (`TbaBackendAppPlugin`, `app`, `build_app`, `build_application_runtime_plan`, `build_product_app`, `install`, `validate_backend_app_contract`) when composing or extending behavior. Its entry-point section below is authoritative for registered plugins; no additional extension loader is inferred from the package name.

---

## Operations and Readiness

### Operational Requirements

`tba-app-backend-core` exposes deployable backend composition. Public operations found in its source:

- `build_app` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-core/src/tba_app_backend_core/app.py).
- `build_application_runtime_plan` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-core/src/tba_app_backend_core/app.py).
- `install` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-core/src/tba_app_backend_core/plugin.py).
- `validate_backend_app_contract` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-core/src/tba_app_backend_core/product.py).
- `build_product_app` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-core/src/tba_app_backend_core/product.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

### Health and Observability

This README does not establish a standalone health endpoint for `tba-app-backend-core`. Observe the concrete caller’s results, exceptions, and existing test reports. An application that embeds this package must define its own health and telemetry contract.

### Security and Resource Limits

Apply the input, credential, and resource constraints implemented in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-core/src/tba_app_backend_core/__init__.py). The `tba-app-backend-core` README gate is a documentation check, not a security review or a substitute for the implementation’s limits and caller authorization.

### Compatibility

This source version of `tba-app-backend-core` declares Python `>=3.10,<3.16`. Consult its dependency constraints before upgrading. Source-version and registry-version badges have separate meanings; this migration makes no additional platform or interoperability certification claim.

---

## Verification

### Tests

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-core/src/tba_app_backend_core/__init__.py).

### Certification Status

No external certification is asserted for `tba-app-backend-core` by this documentation migration. README conformance, example syntax, runtime tests, and protocol or security certification are distinct evidence scopes.

### Evidence

The [README standards CI](https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml) records mechanical documentation results for its tested commit. The [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-core/src/tba_app_backend_core/__init__.py) and example sources support the package-boundary description; external runtime behavior requires its own test evidence.

---

## FAQ

### Why

**Why select this package?** `tba-app-backend-core` provides shared layer-90 ASGI and router composition for TBA backend applications; use its own API boundary rather than assuming neighboring packages are bundled or configured automatically.

### How

**How do I start?** Install or synchronize the environment under Getting Started, follow the maintained example for `tba-app-backend-core`, and consult [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-core/src/tba_app_backend_core/__init__.py) for the exact types and signatures involved.

### When

**When should I validate an upgrade?** Recheck `tba-app-backend-core` whenever its source version, declared collaborators, configuration, or caller changes. Run relevant behavioral tests in addition to the README gate before promotion.

---

## Documentation and Related Packages

### More Documentation

The [repository contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md), [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-core/src/tba_app_backend_core/__init__.py), and [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-core/pyproject.toml) provide the supporting context for `tba-app-backend-core`. The [README policy](https://github.com/groupsum/readme-standards/blob/master/docs/outline.md) defines the common document structure.

### Related Packages

Declared local runtime dependencies:

- [tba-capability-client-secret-authentication](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-client-secret-authentication/README.md)
- [tba-contracts-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-identity/README.md)
- [tba-operator-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-operator-identity/README.md)
- [tba-plugin-tigrbl](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-plugin-tigrbl/README.md)
- [tba-primitives-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/000-primitives/tba-primitives-identity/README.md)
- [tba-protocol-gnap](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-gnap/README.md)
- [tba-protocol-oauth](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oauth/README.md)
- [tba-provider-secret-hashing-bcrypt](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-secret-hashing-bcrypt/README.md)
- [tba-router-administration-gate](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-administration-gate/README.md)
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
- [tba-router-resource-validation-metadata](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-resource-validation-metadata/README.md)
- [tba-router-session-login](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-session-login/README.md)
- [tba-runtime-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity/README.md)
- [tba-runtime-identity-storage](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-runtime-identity-storage/README.md)
- [tba-server-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-server-identity/README.md)
- [tba-storage-core](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-core/README.md)
- [tba-storage-oauth](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-oauth/README.md)
- [tba-storage-tenancy](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-tenancy/README.md)

Direct downstream consumers:

- [tba-app-backend-developer](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-developer/README.md)
- [tba-app-backend-my-account](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-my-account/README.md)
- [tba-app-backend-platform-administration](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-platform-administration/README.md)
- [tba-app-backend-public](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-public/README.md)
- [tba-app-backend-resource-validation](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-resource-validation/README.md)
- [tba-app-backend-service-administration](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-service-administration/README.md)
- [tba-app-backend-tenant-administration](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-tenant-administration/README.md)

### Project Links

<!-- readme-standards:begin project-links -->
- [Documentation](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/090-backend-apps/tba-app-backend-core#readme)
- [Homepage](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/090-backend-apps/tba-app-backend-core#readme)
- [Issues](https://github.com/tigrbl/tigrbl_auth/issues)
- [PyPI](https://pypi.org/project/tba-app-backend-core/)
- [Repository](https://github.com/tigrbl/tigrbl_auth)
- [Source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/090-backend-apps/tba-app-backend-core)
- [pypi: tba-app-backend-core](https://pypi.org/project/tba-app-backend-core/)
<!-- readme-standards:end project-links -->

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/090-backend-apps/tba-app-backend-core)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-core/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-core/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-core/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-app-backend-core/)

---

## Contributing

### How to Contribute

Follow the [contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md) and include a focused example or regression for changes to `tba-app-backend-core`. Keep package behavior, its documented boundary, and its tests aligned.

### Development Setup

Work from the `pkgs/090-backend-apps/tba-app-backend-core` checkout. Synchronize its declared development environment with uv, then run the relevant package tests and `python -m pytest docs/readme/test_examples.py`. The repository’s dedicated README job installs `readme-standards==0.1.3` without resolving unrelated runtime packages.

### Notes for Maintainers

Edit authored prose directly in this `tba-app-backend-core` README. Update source examples in `docs/readme/`, then run `readme-standards render --root . --write` from the package directory and review the diff. Required headings and generated blocks come from package-guide-v1.

---

## Governance

### Ownership and Decision Making

Changes to `tba-app-backend-core` follow the maintainer review process of [tigrbl/tigrbl_auth](https://github.com/tigrbl/tigrbl_auth) and its contribution guide. Author attribution remains in the [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-core/pyproject.toml); this README does not assign new publishing or administrative authority.

### Standards and Policies

`tba-app-backend-core` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `090-backend-apps` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

### Lifecycle and Migration

The `tba-app-backend-core` source version is `0.4.0.dev3`. This change standardizes documentation and adds a development-only gate; it does not publish a new runtime version or declare a previously unpublished package released. Preserve explicit deprecation and replacement instructions where present.

---

## License and Attribution

### License

<!-- readme-standards:begin license -->
Licensed under `Apache-2.0`. See [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-core/LICENSE).
<!-- readme-standards:end license -->

### Notices

<!-- readme-standards:begin notices -->
See [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-core/NOTICE) for attribution.
<!-- readme-standards:end notices -->
