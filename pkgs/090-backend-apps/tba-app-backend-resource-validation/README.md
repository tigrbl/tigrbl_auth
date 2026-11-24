# tba-app-backend-resource-validation

<!-- readme-standards:begin branding -->
<p align="center"><a href="https://github.com/tigrbl/tigrbl_auth"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="300"></a></p>
<p align="center"><strong>tba-app-backend-resource-validation</strong></p>
<p align="center">JWKS, introspection, and protected-resource validation backend application for TBA.</p>
<p align="center">
<a href="https://pypi.org/project/tba-app-backend-resource-validation/"><img alt="pypi: tba-app-backend-resource-validation" src="https://img.shields.io/pypi/v/tba-app-backend-resource-validation?labelColor=1E293B&amp;color=1D4ED8"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-resource-validation/pyproject.toml"><img alt="Source version: 0.4.0.dev3" src="https://img.shields.io/static/v1?label=Source%20version&amp;message=0.4.0.dev3&amp;labelColor=1E293B&amp;color=4338CA"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-resource-validation/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/static/v1?label=Python&amp;message=%3E%3D3.10%2C%3C3.16&amp;labelColor=1E293B&amp;color=0F766E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-resource-validation/pyproject.toml"><img alt="Layer: 090-backend-apps" src="https://img.shields.io/static/v1?label=Layer&amp;message=090-backend-apps&amp;labelColor=1E293B&amp;color=6D28D9"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-resource-validation/README.md#lifecycle-and-migration"><img alt="Lifecycle: active" src="https://img.shields.io/static/v1?label=Lifecycle&amp;message=active&amp;labelColor=1E293B&amp;color=166534"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-resource-validation/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/static/v1?label=License&amp;message=Apache-2.0&amp;labelColor=1E293B&amp;color=86198F"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-resource-validation/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/static/v1?label=Notice&amp;message=attribution&amp;labelColor=1E293B&amp;color=86198F"></a>
</p>
<p align="center">
<a href="https://pypi.org/project/tba-app-backend-resource-validation/"><img alt="Monthly PyPI downloads: tba-app-backend-resource-validation" src="https://img.shields.io/pypi/dm/tba-app-backend-resource-validation?labelColor=1E293B&amp;color=0E7490"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-resource-validation/README.md"><img alt="README hits: tba-app-backend-resource-validation" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/pkgs/090-backend-apps/tba-app-backend-resource-validation/README.md.svg?label=README%20hits&amp;labelColor=1E293B&amp;color=0E7490"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="README standards: CI gate" src="https://img.shields.io/static/v1?label=README%20standards&amp;message=CI%20gate&amp;labelColor=1E293B&amp;color=1D4ED8"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-resource-validation/docs/readme/test_examples.py"><img alt="Tests: example source" src="https://img.shields.io/static/v1?label=Tests&amp;message=example%20source&amp;labelColor=1E293B&amp;color=0F766E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-resource-validation/README.md#certification-status"><img alt="Certification: not certified" src="https://img.shields.io/static/v1?label=Certification&amp;message=not%20certified&amp;labelColor=1E293B&amp;color=92400E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/tools/readme/POLICY.md"><img alt="Governance: repository policy" src="https://img.shields.io/static/v1?label=Governance&amp;message=repository%20policy&amp;labelColor=1E293B&amp;color=4338CA"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="Evidence: source and CI" src="https://img.shields.io/static/v1?label=Evidence&amp;message=source%20and%20CI&amp;labelColor=1E293B&amp;color=6D28D9"></a>
</p>
<p align="center"><a href="#overview">Overview</a> · <a href="#installation">Installation</a> · <a href="#quick-start">Quick Start</a> · <a href="#usage">Usage</a> · <a href="#public-api-and-import-surfaces">API</a> · <a href="#contributing">Contributing</a> · <a href="#governance">Governance</a> · <a href="#license">License</a></p>
<!-- readme-standards:end branding -->

---

## Overview

### Summary

Resource-server validation API front door for protected APIs that need issuer metadata.

- Package: `tba-app-backend-resource-validation`
- Layer: `090-backend-apps`
- Responsibility: JWKS, introspection, and protected-resource validation backend application for TBA.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-resource-validation/src/tba_app_backend_resource_validation/__init__.py).
- Distribution: Python package on PyPI.

### Why This Package

`tba-app-backend-resource-validation` isolates this responsibility: JWKS, introspection, and protected-resource validation backend application for TBA. Its [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-resource-validation/src/tba_app_backend_resource_validation/__init__.py) exposes `PRODUCT_SURFACE`, `RESOURCE_VALIDATION_BACKEND_APP_CONTRACT`, `ResourceValidationBackendAppContract`, `app`, `build_app`, allowing consumers to select this package without treating adjacent packages as part of its public contract.

### When to Use

Choose `tba-app-backend-resource-validation` for this responsibility: JWKS, introspection, and protected-resource validation backend application for TBA. Its `090-backend-apps` placement keeps deployable backend composition separate from new protocol grammars or independent persistence implementations.

### Features

- `ResourceValidationBackendAppContract`: Machine-readable boundary for resource-server validation metadata.
- `ResourceValidationOpenAPIGate`: ASGI wrapper that serves the patched validation OpenAPI document.

### Non-Goals

`tba-app-backend-resource-validation` does not take ownership of new protocol grammars or independent persistence implementations.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

---

## Getting Started

### Prerequisites

Python `>=3.10,<3.16` is required. The [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-resource-validation/pyproject.toml) declares runtime dependencies including `tba-auth`, `tba-app-backend-core`, `tba-router-oauth-introspection`, `tba-router-oauth-protected-resource-metadata`, `tba-router-oidc-discovery`, `tba-router-resource-validation-metadata`. Read the example’s inputs and service requirements before execution.

### Installation

Install the selected PyPI release of `tba-app-backend-resource-validation`:

```bash
uv pip install tba-app-backend-resource-validation
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/090-backend-apps/tba-app-backend-resource-validation
```

#### uv

<!-- readme-standards:begin installation.uv -->
```bash
uv add tba-app-backend-resource-validation
```
<!-- readme-standards:end installation.uv -->

#### pip

<!-- readme-standards:begin installation.pip -->
```bash
python -m pip install tba-app-backend-resource-validation
```
<!-- readme-standards:end installation.pip -->

#### Poetry

<!-- readme-standards:begin installation.poetry -->
```bash
poetry add tba-app-backend-resource-validation
```
<!-- readme-standards:end installation.poetry -->

### Quick Start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.


```bash
uv run --isolated --no-project --python 3.12 --with "tba-app-backend-resource-validation==0.4.0.dev3" python quickstart.py
```

The import and assertion succeed when the ResourceValidationBackendAppContract entry point is available.

#### Example

<!-- readme-standards:begin example.quick-start -->
Source: [docs/readme/quick_start.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-resource-validation/docs/readme/quick_start.py).

```python
from tba_app_backend_resource_validation import ResourceValidationBackendAppContract

assert callable(ResourceValidationBackendAppContract)
```
<!-- readme-standards:end example.quick-start -->

#### Expected Result

The example demonstrates the documented `tba-app-backend-resource-validation` source boundary or workflow. Complete its required configuration first. README CI checks the maintained source’s syntax and declarations; it does not claim that external services or the application workflow were exercised.

---

## Usage

### Common Workflows

<!-- readme-standards:begin example.usage -->
Source: [docs/readme/usage.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-resource-validation/docs/readme/usage.py).

```python
from tba_app_backend_resource_validation import ResourceValidationBackendAppContract

assert callable(ResourceValidationBackendAppContract)
```
<!-- readme-standards:end example.usage -->

The following public-entry-point example belongs to `tba-app-backend-resource-validation`. JWKS, introspection, and protected-resource validation backend application for TBA. Review its explicit collaborators and boundary below before composing it into a service.

### Configuration

The [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-resource-validation/src/tba_app_backend_resource_validation/__init__.py) references configuration keys `AUTHN_ISSUER`, `TBA_AUTH_ENABLE_RFC9207`, `TBA_AUTH_PROFILE`, `TBA_AUTH_PROTECTED_RESOURCE_IDENTIFIER`, `TBA_AUTH_REQUIRE_TLS`, `TBA_AUTH_SESSION_COOKIE_FORCE_SECURE`. Consult the constructor or function signature before supplying them; a referenced key is not necessarily a global environment variable.

### Error Handling

The inspected `tba-app-backend-resource-validation` source does not establish a package-wide exception hierarchy. Preserve errors from its declared dependencies and validate inputs using the specific public contract in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-resource-validation/src/tba_app_backend_resource_validation/__init__.py).

### Best Practices

Use the explicit `tba-app-backend-resource-validation` imports documented below and keep collaborator configuration with the caller. Run the package’s relevant tests after changing `PRODUCT_SURFACE`, `RESOURCE_VALIDATION_BACKEND_APP_CONTRACT`, `ResourceValidationBackendAppContract`, `app`, `build_app`; an import or successful installation alone does not establish its runtime guarantees.

---

## Package Boundary

### What It Owns

`tba-app-backend-resource-validation` belongs to `090-backend-apps` and owns deployable backend composition: JWKS, introspection, and protected-resource validation backend application for TBA.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-resource-validation/src/tba_app_backend_resource_validation/__init__.py). Public exports include `PRODUCT_SURFACE`, `RESOURCE_VALIDATION_BACKEND_APP_CONTRACT`, `ResourceValidationBackendAppContract`, `app`, `build_app`.

Keep new protocol grammars or independent persistence implementations in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

### Public API and Import Surfaces

Import namespace: `tba_app_backend_resource_validation`.

Source-declared exports or types: `PRODUCT_SURFACE`, `RESOURCE_VALIDATION_BACKEND_APP_CONTRACT`, `ResourceValidationBackendAppContract`, `app`, `build_app`.

Inspect [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-resource-validation/src/tba_app_backend_resource_validation/__init__.py) for exact signatures; this inventory does not designate every internal module as stable.

### Entry Points

<!-- readme-standards:begin entry-points -->
This package declares no command-line, GUI, or plugin entry points in its manifest.
<!-- readme-standards:end entry-points -->

```python
from tba_app_backend_resource_validation import app, build_app
```

### Injected Dependencies

The [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-resource-validation/src/tba_app_backend_resource_validation/__init__.py) for `tba-app-backend-resource-validation` does not declare an explicit service-constructor or keyword-only factory hook in the inspected source. Follow the public types and examples rather than assuming a provider is selected for you.

Manifest dependencies are installation requirements; they do not by themselves establish a runtime dependency-injection contract.

### Protocol Consumers

Direct consumers in this checkout’s package manifests include `tba-workspace`. These edges describe declared dependencies, not protocol-conformance evidence.

### Extensions

For `tba-app-backend-resource-validation`, use the source-declared public interfaces (`PRODUCT_SURFACE`, `RESOURCE_VALIDATION_BACKEND_APP_CONTRACT`, `ResourceValidationBackendAppContract`, `app`, `build_app`) when composing or extending behavior. Its entry-point section below is authoritative for registered plugins; no additional extension loader is inferred from the package name.

---

## Operations and Readiness

### Operational Requirements

`tba-app-backend-resource-validation` exposes deployable backend composition. Public operations found in its source:

- `build_app` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-resource-validation/src/tba_app_backend_resource_validation/app.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

### Health and Observability

This README does not establish a standalone health endpoint for `tba-app-backend-resource-validation`. Observe the concrete caller’s results, exceptions, and existing test reports. An application that embeds this package must define its own health and telemetry contract.

### Security and Resource Limits

Apply the input, credential, and resource constraints implemented in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-resource-validation/src/tba_app_backend_resource_validation/__init__.py). The `tba-app-backend-resource-validation` README gate is a documentation check, not a security review or a substitute for the implementation’s limits and caller authorization.

### Compatibility

This source version of `tba-app-backend-resource-validation` declares Python `>=3.10,<3.16`. Consult its dependency constraints before upgrading. Source-version and registry-version badges have separate meanings; this migration makes no additional platform or interoperability certification claim.

---

## Verification

### Tests

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-resource-validation/src/tba_app_backend_resource_validation/__init__.py).

### Certification Status

No external certification is asserted for `tba-app-backend-resource-validation` by this documentation migration. README conformance, example syntax, runtime tests, and protocol or security certification are distinct evidence scopes.

### Evidence

The [README standards CI](https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml) records mechanical documentation results for its tested commit. The [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-resource-validation/src/tba_app_backend_resource_validation/__init__.py) and example sources support the package-boundary description; external runtime behavior requires its own test evidence.

---

## FAQ

### Why

**Why select this package?** `tba-app-backend-resource-validation` provides jWKS, introspection, and protected-resource validation backend application for TBA; use its own API boundary rather than assuming neighboring packages are bundled or configured automatically.

### How

**How do I start?** Install or synchronize the environment under Getting Started, follow the maintained example for `tba-app-backend-resource-validation`, and consult [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-resource-validation/src/tba_app_backend_resource_validation/__init__.py) for the exact types and signatures involved.

### When

**When should I validate an upgrade?** Recheck `tba-app-backend-resource-validation` whenever its source version, declared collaborators, configuration, or caller changes. Run relevant behavioral tests in addition to the README gate before promotion.

---

## Documentation and Related Packages

### More Documentation

The [repository contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md), [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-resource-validation/src/tba_app_backend_resource_validation/__init__.py), and [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-resource-validation/pyproject.toml) provide the supporting context for `tba-app-backend-resource-validation`. The [README policy](https://github.com/groupsum/readme-standards/blob/master/docs/outline.md) defines the common document structure.

### Related Packages

Declared local runtime dependencies:

- [tba-app-backend-core](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-core/README.md)
- [tba-auth](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-auth/README.md)
- [tba-router-oauth-introspection](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-oauth-introspection/README.md)
- [tba-router-oauth-protected-resource-metadata](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-oauth-protected-resource-metadata/README.md)
- [tba-router-oidc-discovery](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-oidc-discovery/README.md)
- [tba-router-resource-validation-metadata](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-resource-validation-metadata/README.md)

### Project Links

<!-- readme-standards:begin project-links -->
- [Documentation](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/090-backend-apps/tba-app-backend-resource-validation#readme)
- [Homepage](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/090-backend-apps/tba-app-backend-resource-validation#readme)
- [Issues](https://github.com/tigrbl/tigrbl_auth/issues)
- [PyPI](https://pypi.org/project/tba-app-backend-resource-validation/)
- [Repository](https://github.com/tigrbl/tigrbl_auth)
- [Source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/090-backend-apps/tba-app-backend-resource-validation)
- [pypi: tba-app-backend-resource-validation](https://pypi.org/project/tba-app-backend-resource-validation/)
<!-- readme-standards:end project-links -->

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/090-backend-apps/tba-app-backend-resource-validation)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-resource-validation/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-resource-validation/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-resource-validation/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-app-backend-resource-validation/)

---

## Contributing

### How to Contribute

Follow the [contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md) and include a focused example or regression for changes to `tba-app-backend-resource-validation`. Keep package behavior, its documented boundary, and its tests aligned.

### Development Setup

Work from the `pkgs/090-backend-apps/tba-app-backend-resource-validation` checkout. Synchronize its declared development environment with uv, then run the relevant package tests and `python -m pytest docs/readme/test_examples.py`. The repository’s dedicated README job installs `readme-standards==0.1.3` without resolving unrelated runtime packages.

### Notes for Maintainers

**Surface**

| Property | Value |
| --- | --- |
| Product surface | `resource-validation-app` |
| Intended consumers | Resource servers, API gateways, validation middleware |
| Exposes | JWKS, tenant JWKS, introspection, OIDC discovery, protected-resource metadata |
| Excludes | Public human login/consent pages, dynamic client registration, admin resources, `/rpc` |

**Local dev deployment**

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

---

## Governance

### Ownership and Decision Making

Changes to `tba-app-backend-resource-validation` follow the maintainer review process of [tigrbl/tigrbl_auth](https://github.com/tigrbl/tigrbl_auth) and its contribution guide. Author attribution remains in the [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-resource-validation/pyproject.toml); this README does not assign new publishing or administrative authority.

### Standards and Policies

`tba-app-backend-resource-validation` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `090-backend-apps` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

### Lifecycle and Migration

The `tba-app-backend-resource-validation` source version is `0.4.0.dev3`. This change standardizes documentation and adds a development-only gate; it does not publish a new runtime version or declare a previously unpublished package released. Preserve explicit deprecation and replacement instructions where present.

---

## License and Attribution

### License

<!-- readme-standards:begin license -->
Licensed under `Apache-2.0`. See [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-resource-validation/LICENSE).
<!-- readme-standards:end license -->

### Notices

<!-- readme-standards:begin notices -->
See [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-resource-validation/NOTICE) for attribution.
<!-- readme-standards:end notices -->
