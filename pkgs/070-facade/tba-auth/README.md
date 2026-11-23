# tba-auth

<!-- readme-standards:begin branding -->
<p align="center"><a href="https://github.com/tigrbl/tigrbl_auth"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="300"></a></p>
<p align="center"><strong>tba-auth</strong></p>
<p align="center">Compatibility facade for the split TBA identity package suite, preserving legacy app, gateway, plugin, CLI, and RFC imports.</p>
<p align="center">
<a href="https://pypi.org/project/tba-auth/"><img alt="pypi: tba-auth" src="https://img.shields.io/pypi/v/tba-auth"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-auth/pyproject.toml"><img alt="Source version: 0.4.0.dev3" src="https://img.shields.io/static/v1?label=Source%20version&amp;message=0.4.0.dev3&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-auth/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/static/v1?label=Python&amp;message=%3E%3D3.10%2C%3C3.16&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-auth/pyproject.toml"><img alt="Layer: 070-facade" src="https://img.shields.io/static/v1?label=Layer&amp;message=070-facade&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-auth/README.md#lifecycle-and-migration"><img alt="Lifecycle: active" src="https://img.shields.io/static/v1?label=Lifecycle&amp;message=active&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-auth/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/static/v1?label=License&amp;message=Apache-2.0&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-auth/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/static/v1?label=Notice&amp;message=attribution&amp;color=525252"></a>
</p>
<p align="center">
<a href="https://pypi.org/project/tba-auth/"><img alt="Monthly PyPI downloads: tba-auth" src="https://img.shields.io/pypi/dm/tba-auth"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-auth/README.md"><img alt="README hits: tba-auth" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/pkgs/070-facade/tba-auth/README.md.svg?label=README%20hits"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="README standards: CI gate" src="https://img.shields.io/static/v1?label=README%20standards&amp;message=CI%20gate&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-auth/docs/readme/test_examples.py"><img alt="Tests: example source" src="https://img.shields.io/static/v1?label=Tests&amp;message=example%20source&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-auth/README.md#certification-status"><img alt="Certification: not certified" src="https://img.shields.io/static/v1?label=Certification&amp;message=not%20certified&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/tools/readme/POLICY.md"><img alt="Governance: repository policy" src="https://img.shields.io/static/v1?label=Governance&amp;message=repository%20policy&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="Evidence: source and CI" src="https://img.shields.io/static/v1?label=Evidence&amp;message=source%20and%20CI&amp;color=525252"></a>
</p>
<p align="center"><a href="#overview">Overview</a> · <a href="#installation">Installation</a> · <a href="#quick-start">Quick Start</a> · <a href="#usage">Usage</a> · <a href="#public-api-and-import-surfaces">API</a> · <a href="#contributing">Contributing</a> · <a href="#governance">Governance</a> · <a href="#license">License</a></p>
<!-- readme-standards:end branding -->

---

## Overview

### Summary

Keep existing applications working with the compatibility facade for the split TBA identity suite.

- Package: `tba-auth`
- Import root: `tba_auth`
- Component kind: Facade package
- Use it when upgrading existing tba_auth consumers to the split package suite.
- New implementation work should prefer focused packages such as tba-protocol-oauth, tba-protocol-oidc, tba-plugin-tigrbl, tba-server-identity, or tba-runtime-identity.
- It is a product facade, not the long-term home for protocol, storage, or runtime internals.

### Why This Package

`tba-auth` isolates this responsibility: Compatibility facade for the split TBA identity package suite, preserving legacy app, gateway, plugin, CLI, and RFC imports. Its [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-auth/src/tba_auth/__init__.py) exposes `Any`, `FACADE_EXTRAS`, `FacadeImportError`, `STABLE_ENTRYPOINTS`, `StableEntrypoint`, `TbaAuthFacadeWarning`, `annotations`, `extras_for`, `import_module`, `resolve_entrypoint`, `stable_entrypoints`, `warn_legacy_import`, allowing consumers to select this package without treating adjacent packages as part of its public contract.

### When to Use

Use this distribution when maintaining code with `tba_auth` imports. New integrations can use the focused public backend, server, or Tigrbl plugin packages directly. The example plans a local runner without starting it.

### Features

- `BackendAppCompositionMovedError`: Raised when the retired layer-70 backend-app factory is called.
- `TbaAuthFacadeWarning`: Warning emitted when a legacy ``tba_auth`` compatibility surface is used.
- `FacadeImportError`: Raised when a facade target is unavailable in the installed package set.
- `StableEntrypoint`: declared in src/tba_auth/compat.py
- `LazyCompatEntrypoint`: declared in src/tba_auth/compat.py

### Non-Goals

`tba-auth` does not take ownership of moving implementation ownership out of focused packages.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

---

## Getting Started

### Prerequisites

Python `>=3.10,<3.16` is required. The [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-auth/pyproject.toml) declares runtime dependencies including `tba-concrete-authorization-policy-rules`, `tba-concrete-authorization-policy-combiner-default`, `tba-concrete-authorization-policy-evaluators-default`, `tba-concrete-authorization-policy-attributes-mapping`, `tba-concrete-authorization-policy-obligations`, `tba-provider-security-authorization-provenance-builder`, `tba-runtime-identity-administration`, `tba-runtime-identity-authoring`, `tba-cli-identity`, `tba-contracts-identity`, `tba-primitives-identity`, `tba-credentials`. Read the example’s inputs and service requirements before execution.

### Installation

Install the selected PyPI release of `tba-auth`:

```bash
uv pip install tba-auth
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/070-facade/tba-auth
```

#### uv

<!-- readme-standards:begin installation.uv -->
```bash
uv add tba-auth
```
<!-- readme-standards:end installation.uv -->

#### pip

<!-- readme-standards:begin installation.pip -->
```bash
python -m pip install tba-auth
```
<!-- readme-standards:end installation.pip -->

#### Poetry

<!-- readme-standards:begin installation.poetry -->
```bash
poetry add tba-auth
```
<!-- readme-standards:end installation.poetry -->

### Quick Start

Install the version used by this example.

```bash
python -m pip install "tba-auth==0.4.0.dev3"
```

Save the following as `quickstart.py` and run `python quickstart.py`. The assertions should pass.

#### Example

<!-- readme-standards:begin example.quick-start -->
Source: [docs/readme/quick_start.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-auth/docs/readme/quick_start.py).

```python
from tba_auth.app import build_application_runtime_plan

plan = build_application_runtime_plan(runner="uvicorn", host="127.0.0.1", port=8000)
assert plan.runner == "uvicorn"
assert plan.port == 8000
```
<!-- readme-standards:end example.quick-start -->

#### Expected Result

The example demonstrates the documented `tba-auth` source boundary or workflow. Complete its required configuration first. README CI checks the maintained source’s syntax and declarations; it does not claim that external services or the application workflow were exercised.

---

## Usage

### Common Workflows

<!-- readme-standards:begin example.usage -->
Source: [docs/readme/usage.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-auth/docs/readme/usage.py).

```python
from tba_auth.app import build_application_runtime_plan

plan = build_application_runtime_plan(runner="uvicorn", host="127.0.0.1", port=8000)
assert plan.runner == "uvicorn"
assert plan.port == 8000
```
<!-- readme-standards:end example.usage -->

The following public-entry-point example belongs to `tba-auth`. Compatibility facade for the split TBA identity package suite, preserving legacy app, gateway, plugin, CLI, and RFC imports. Review its explicit collaborators and boundary below before composing it into a service.

### Configuration

Configure `tba-auth` through the APIs in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-auth/src/tba_auth/__init__.py); its [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-auth/pyproject.toml) describes installation requirements, not an implicit service configuration. No additional package-global configuration contract is inferred from dependencies.

### Error Handling

The inspected `tba-auth` source raises `AttributeError`, `BackendAppCompositionMovedError`, `FacadeImportError`, `RuntimeError`. Handle these at the calling boundary and consult the implementation for the triggering conditions.

### Best Practices

Use the explicit `tba-auth` imports documented below and keep collaborator configuration with the caller. Run the package’s relevant tests after changing `Any`, `FACADE_EXTRAS`, `FacadeImportError`, `STABLE_ENTRYPOINTS`, `StableEntrypoint`, `TbaAuthFacadeWarning`, `annotations`, `extras_for`, `import_module`, `resolve_entrypoint`, `stable_entrypoints`, `warn_legacy_import`; an import or successful installation alone does not establish its runtime guarantees.

---

## Package Boundary

### What It Owns

- Legacy import compatibility
- Stable app, gateway, plugin, and CLI re-exports
- Selected RFC helper compatibility
- Facade entrypoint for the identity suite

### Public API and Import Surfaces

Import namespace: `tba_auth`.

Source-declared exports or types: `Any`, `FACADE_EXTRAS`, `FacadeImportError`, `STABLE_ENTRYPOINTS`, `StableEntrypoint`, `TbaAuthFacadeWarning`, `annotations`, `extras_for`, `import_module`, `resolve_entrypoint`, `stable_entrypoints`, `warn_legacy_import`.

Inspect [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-auth/src/tba_auth/__init__.py) for exact signatures; this inventory does not designate every internal module as stable.

### Entry Points

<!-- readme-standards:begin entry-points -->
This package declares no command-line, GUI, or plugin entry points in its manifest.
<!-- readme-standards:end entry-points -->

### Injected Dependencies

The [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-auth/src/tba_auth/__init__.py) for `tba-auth` does not declare an explicit service-constructor or keyword-only factory hook in the inspected source. Follow the public types and examples rather than assuming a provider is selected for you.

Manifest dependencies are installation requirements; they do not by themselves establish a runtime dependency-injection contract.

### Protocol Consumers

Direct consumers in this checkout’s package manifests include `tba-app-backend-developer`, `tba-app-backend-my-account`, `tba-app-backend-platform-administration`, `tba-app-backend-public`, `tba-app-backend-resource-validation`, `tba-app-backend-service-administration`, `tba-app-backend-tenant-administration`, `tba-workspace`. These edges describe declared dependencies, not protocol-conformance evidence.

### Extensions

For `tba-auth`, use the source-declared public interfaces (`Any`, `FACADE_EXTRAS`, `FacadeImportError`, `STABLE_ENTRYPOINTS`, `StableEntrypoint`, `TbaAuthFacadeWarning`, `annotations`, `extras_for`, `import_module`, `resolve_entrypoint`, `stable_entrypoints`, `warn_legacy_import`) when composing or extending behavior. Its entry-point section below is authoritative for registered plugins; no additional extension loader is inferred from the package name.

---

## Operations and Readiness

### Operational Requirements

`tba-auth` exposes curated public entry points. Inspect the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-auth/src/tba_auth/__init__.py) for the exported types and composition surface.

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

### Health and Observability

This README does not establish a standalone health endpoint for `tba-auth`. Observe the concrete caller’s results, exceptions, and existing test reports. An application that embeds this package must define its own health and telemetry contract.

### Security and Resource Limits

Apply the input, credential, and resource constraints implemented in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-auth/src/tba_auth/__init__.py). The `tba-auth` README gate is a documentation check, not a security review or a substitute for the implementation’s limits and caller authorization.

### Compatibility

This source version of `tba-auth` declares Python `>=3.10,<3.16`. Consult its dependency constraints before upgrading. Source-version and registry-version badges have separate meanings; this migration makes no additional platform or interoperability certification claim.

---

## Verification

### Tests

See the [related repository tests](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-architecture/tests/unit/test_facade_compatibility_boundary.py) for the implementation scope covered by this example.

[Workspace and package catalog](https://github.com/tigrbl/tigrbl_auth#package-catalog) · [tba-app-backend-public](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/090-backend-apps/tba-app-backend-public#readme) · [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues) · [Repository license](https://github.com/tigrbl/tigrbl_auth/blob/master/LICENSE)

### Certification Status

No external certification is asserted for `tba-auth` by this documentation migration. README conformance, example syntax, runtime tests, and protocol or security certification are distinct evidence scopes.

### Evidence

The [README standards CI](https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml) records mechanical documentation results for its tested commit. The [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-auth/src/tba_auth/__init__.py) and example sources support the package-boundary description; external runtime behavior requires its own test evidence.

---

## FAQ

### Why

**Why select this package?** `tba-auth` provides compatibility facade for the split TBA identity package suite, preserving legacy app, gateway, plugin, CLI, and RFC imports; use its own API boundary rather than assuming neighboring packages are bundled or configured automatically.

### How

**How do I start?** Install or synchronize the environment under Getting Started, follow the maintained example for `tba-auth`, and consult [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-auth/src/tba_auth/__init__.py) for the exact types and signatures involved.

### When

**When should I validate an upgrade?** Recheck `tba-auth` whenever its source version, declared collaborators, configuration, or caller changes. Run relevant behavioral tests in addition to the README gate before promotion.

---

## Documentation and Related Packages

### More Documentation

The [repository contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md), [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-auth/src/tba_auth/__init__.py), and [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-auth/pyproject.toml) provide the supporting context for `tba-auth`. The [README policy](https://github.com/groupsum/readme-standards/blob/master/docs/outline.md) defines the common document structure.

### Related Packages

- [tba-auth](https://pypi.org/project/tba-auth/)
- [tba-plugin-tigrbl](https://pypi.org/project/tba-plugin-tigrbl/)
- [tba-server-identity](https://pypi.org/project/tba-server-identity/)
- [tba-runtime-identity](https://pypi.org/project/tba-runtime-identity/)
- [tba-operator-identity](https://pypi.org/project/tba-operator-identity/)
- [tba-protocol-oauth](https://pypi.org/project/tba-protocol-oauth/)
- [tba-protocol-oidc](https://pypi.org/project/tba-protocol-oidc/)

### Project Links

<!-- readme-standards:begin project-links -->
- [Documentation](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/070-facade/tba-auth#readme)
- [Homepage](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/070-facade/tba-auth#readme)
- [Issues](https://github.com/tigrbl/tigrbl_auth/issues)
- [PyPI](https://pypi.org/project/tba-auth/)
- [Repository](https://github.com/tigrbl/tigrbl_auth)
- [SSOT](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [Source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/070-facade/tba-auth)
- [pypi: tba-auth](https://pypi.org/project/tba-auth/)
<!-- readme-standards:end project-links -->

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/070-facade/tba-auth)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-auth/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-auth/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-auth/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-auth/)

---

## Contributing

### How to Contribute

Follow the [contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md) and include a focused example or regression for changes to `tba-auth`. Keep package behavior, its documented boundary, and its tests aligned.

### Development Setup

Work from the `pkgs/070-facade/tba-auth` checkout. Synchronize its declared development environment with uv, then run the relevant package tests and `python -m pytest docs/readme/test_examples.py`. The repository’s dedicated README job installs `readme-standards==0.1.1` without resolving unrelated runtime packages.

### Notes for Maintainers

Edit authored prose directly in this `tba-auth` README. Update source examples in `docs/readme/`, then run `readme-standards render --root . --write` from the package directory and review the diff. Required headings and generated blocks come from package-guide-v1.

---

## Governance

### Ownership and Decision Making

Changes to `tba-auth` follow the maintainer review process of [tigrbl/tigrbl_auth](https://github.com/tigrbl/tigrbl_auth) and its contribution guide. Author attribution remains in the [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-auth/pyproject.toml); this README does not assign new publishing or administrative authority.

### Standards and Policies

This package is part of the SSOT-governed TBA identity package suite. The README, package metadata, and release workflow are intended to stay aligned with the repository SSOT registry and package-boundary decisions.

`tba-auth` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `070-facade` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

### Lifecycle and Migration

The `tba-auth` source version is `0.4.0.dev3`. This change standardizes documentation and adds a development-only gate; it does not publish a new runtime version or declare a previously unpublished package released. Preserve explicit deprecation and replacement instructions where present.

---

## License and Attribution

### License

<!-- readme-standards:begin license -->
Licensed under `Apache-2.0`. See [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-auth/LICENSE).
<!-- readme-standards:end license -->

### Notices

<!-- readme-standards:begin notices -->
See [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-auth/NOTICE) for attribution.
<!-- readme-standards:end notices -->
