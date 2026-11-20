# tba-durability-authority-graph

<!-- readme-standards:begin branding -->
<p align="center"><a href="https://github.com/tigrbl/tigrbl_auth"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="300"></a></p>
<p align="center"><strong>tba-durability-authority-graph</strong></p>
<p align="center">Durable authority-graph table operations and specifications.</p>
<p align="center">
<a href="https://pypi.org/project/tba-durability-authority-graph/"><img alt="pypi: tba-durability-authority-graph" src="https://img.shields.io/pypi/v/tba-durability-authority-graph"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-durability-authority-graph/pyproject.toml"><img alt="Source version: 0.4.0.dev3" src="https://img.shields.io/static/v1?label=Source%20version&amp;message=0.4.0.dev3&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-durability-authority-graph/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/static/v1?label=Python&amp;message=%3E%3D3.10%2C%3C3.16&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-durability-authority-graph/pyproject.toml"><img alt="Layer: 030-storage-runtime" src="https://img.shields.io/static/v1?label=Layer&amp;message=030-storage-runtime&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-durability-authority-graph/README.md#lifecycle-and-migration"><img alt="Lifecycle: active" src="https://img.shields.io/static/v1?label=Lifecycle&amp;message=active&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-durability-authority-graph/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/static/v1?label=License&amp;message=Apache-2.0&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-durability-authority-graph/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/static/v1?label=Notice&amp;message=attribution&amp;color=525252"></a>
</p>
<p align="center">
<a href="https://pypi.org/project/tba-durability-authority-graph/"><img alt="Monthly PyPI downloads: tba-durability-authority-graph" src="https://img.shields.io/pypi/dm/tba-durability-authority-graph"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-durability-authority-graph/README.md"><img alt="README hits: tba-durability-authority-graph" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/pkgs/030-storage-runtime/tba-durability-authority-graph/README.md.svg?label=README%20hits"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="README standards: CI gate" src="https://img.shields.io/static/v1?label=README%20standards&amp;message=CI%20gate&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-durability-authority-graph/docs/readme/test_examples.py"><img alt="Tests: example source" src="https://img.shields.io/static/v1?label=Tests&amp;message=example%20source&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-durability-authority-graph/README.md#certification-status"><img alt="Certification: not certified" src="https://img.shields.io/static/v1?label=Certification&amp;message=not%20certified&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/tools/readme/POLICY.md"><img alt="Governance: repository policy" src="https://img.shields.io/static/v1?label=Governance&amp;message=repository%20policy&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="Evidence: source and CI" src="https://img.shields.io/static/v1?label=Evidence&amp;message=source%20and%20CI&amp;color=525252"></a>
</p>
<p align="center"><a href="#overview">Overview</a> · <a href="#installation">Installation</a> · <a href="#quick-start">Quick Start</a> · <a href="#usage">Usage</a> · <a href="#public-api-and-import-surfaces">API</a> · <a href="#contributing">Contributing</a> · <a href="#governance">Governance</a> · <a href="#license">License</a></p>
<!-- readme-standards:end branding -->

---

## Overview

### Summary

Durable table operations and derived specifications for authority graphs.

- Package: `tba-durability-authority-graph`
- Layer: `030-storage-runtime`
- Responsibility: Durable authority-graph table operations and specifications.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-durability-authority-graph/src/tba_durability_authority_graph/__init__.py).
- Distribution: Python package on PyPI.

### Why This Package

`tba-durability-authority-graph` isolates this responsibility: Durable authority-graph table operations and specifications. Its [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-durability-authority-graph/src/tba_durability_authority_graph/__init__.py) exposes `AuthorityGraphEdgeTable`, `AuthorityGraphNodeTable`, `AuthorityGraphTable`, `deriveTableSpec`, `makeOp`, `provideTableHandler`, allowing consumers to select this package without treating adjacent packages as part of its public contract.

### When to Use

Choose `tba-durability-authority-graph` for this responsibility: Durable authority-graph table operations and specifications. Its `030-storage-runtime` placement keeps storage-backed runtime adapters separate from protocol wire definitions or standalone application hosting.

### Features

- Public source surface: `AuthorityGraphEdgeTable`, `AuthorityGraphNodeTable`, `AuthorityGraphTable`, `deriveTableSpec`, `makeOp`, `provideTableHandler`.
- Declared responsibility: Durable authority-graph table operations and specifications.
- Versioned package metadata and maintained checkout examples.

### Non-Goals

`tba-durability-authority-graph` does not take ownership of protocol wire definitions or standalone application hosting.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

---

## Getting Started

### Prerequisites

Python `>=3.10,<3.16` is required. The [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-durability-authority-graph/pyproject.toml) declares runtime dependencies including `tigrbl`, `tba-storage-authority-graph`. Read the example’s inputs and service requirements before execution.

### Installation

Install the selected PyPI release of `tba-durability-authority-graph`:

```bash
uv pip install tba-durability-authority-graph
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/030-storage-runtime/tba-durability-authority-graph
```

#### uv

<!-- readme-standards:begin installation.uv -->
```bash
uv add tba-durability-authority-graph
```
<!-- readme-standards:end installation.uv -->

#### pip

<!-- readme-standards:begin installation.pip -->
```bash
python -m pip install tba-durability-authority-graph
```
<!-- readme-standards:end installation.pip -->

#### Poetry

<!-- readme-standards:begin installation.poetry -->
```bash
poetry add tba-durability-authority-graph
```
<!-- readme-standards:end installation.poetry -->

### Quick Start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.


```bash
uv run --isolated --no-project --python 3.12 --with "tba-durability-authority-graph==0.4.0.dev3" python quickstart.py
```

The import and assertion succeed when the AuthorityGraphTable entry point is available.

#### Example

<!-- readme-standards:begin example.quick-start -->
Source: [docs/readme/quick_start.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-durability-authority-graph/docs/readme/quick_start.py).

```python
from tba_durability_authority_graph import AuthorityGraphTable

assert callable(AuthorityGraphTable)
```
<!-- readme-standards:end example.quick-start -->

#### Expected Result

The example demonstrates the documented `tba-durability-authority-graph` source boundary or workflow. Complete its required configuration first. README CI checks the maintained source’s syntax and declarations; it does not claim that external services or the application workflow were exercised.

---

## Usage

### Common Workflows

<!-- readme-standards:begin example.usage -->
Source: [docs/readme/usage.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-durability-authority-graph/docs/readme/usage.py).

```python
from tba_durability_authority_graph import AuthorityGraphTable

assert callable(AuthorityGraphTable)
```
<!-- readme-standards:end example.usage -->

The following public-entry-point example belongs to `tba-durability-authority-graph`. Durable authority-graph table operations and specifications. Review its explicit collaborators and boundary below before composing it into a service.

### Configuration

Configure `tba-durability-authority-graph` through the APIs in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-durability-authority-graph/src/tba_durability_authority_graph/__init__.py); its [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-durability-authority-graph/pyproject.toml) describes installation requirements, not an implicit service configuration. No additional package-global configuration contract is inferred from dependencies.

### Error Handling

The inspected `tba-durability-authority-graph` source does not establish a package-wide exception hierarchy. Preserve errors from its declared dependencies and validate inputs using the specific public contract in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-durability-authority-graph/src/tba_durability_authority_graph/__init__.py).

### Best Practices

Use the explicit `tba-durability-authority-graph` imports documented below and keep collaborator configuration with the caller. Run the package’s relevant tests after changing `AuthorityGraphEdgeTable`, `AuthorityGraphNodeTable`, `AuthorityGraphTable`, `deriveTableSpec`, `makeOp`, `provideTableHandler`; an import or successful installation alone does not establish its runtime guarantees.

---

## Package Boundary

### What It Owns

`tba-durability-authority-graph` belongs to `030-storage-runtime` and owns storage-backed runtime adapters: Durable authority-graph table operations and specifications.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-durability-authority-graph/src/tba_durability_authority_graph/__init__.py).

Keep protocol wire definitions or standalone application hosting in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

### Public API and Import Surfaces

Import namespace: `tba_durability_authority_graph`.

Source-declared exports or types: `AuthorityGraphEdgeTable`, `AuthorityGraphNodeTable`, `AuthorityGraphTable`, `deriveTableSpec`, `makeOp`, `provideTableHandler`.

Inspect [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-durability-authority-graph/src/tba_durability_authority_graph/__init__.py) for exact signatures; this inventory does not designate every internal module as stable.

### Entry Points

<!-- readme-standards:begin entry-points -->
This package declares no command-line, GUI, or plugin entry points in its manifest.
<!-- readme-standards:end entry-points -->

### Injected Dependencies

The [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-durability-authority-graph/src/tba_durability_authority_graph/__init__.py) for `tba-durability-authority-graph` does not declare an explicit service-constructor or keyword-only factory hook in the inspected source. Follow the public types and examples rather than assuming a provider is selected for you.

Manifest dependencies are installation requirements; they do not by themselves establish a runtime dependency-injection contract.

### Protocol Consumers

Direct consumers in this checkout’s package manifests include `tba-durability-authorization-policy-authority-derivation-graph`, `tba-workspace`. These edges describe declared dependencies, not protocol-conformance evidence.

### Extensions

For `tba-durability-authority-graph`, use the source-declared public interfaces (`AuthorityGraphEdgeTable`, `AuthorityGraphNodeTable`, `AuthorityGraphTable`, `deriveTableSpec`, `makeOp`, `provideTableHandler`) when composing or extending behavior. Its entry-point section below is authoritative for registered plugins; no additional extension loader is inferred from the package name.

---

## Operations and Readiness

### Operational Requirements

`tba-durability-authority-graph` exposes storage-backed runtime adapters. Inspect the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-durability-authority-graph/src/tba_durability_authority_graph/__init__.py) for the exported types and composition surface.

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

### Health and Observability

This README does not establish a standalone health endpoint for `tba-durability-authority-graph`. Observe the concrete caller’s results, exceptions, and existing test reports. An application that embeds this package must define its own health and telemetry contract.

### Security and Resource Limits

Apply the input, credential, and resource constraints implemented in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-durability-authority-graph/src/tba_durability_authority_graph/__init__.py). The `tba-durability-authority-graph` README gate is a documentation check, not a security review or a substitute for the implementation’s limits and caller authorization.

### Compatibility

This source version of `tba-durability-authority-graph` declares Python `>=3.10,<3.16`. Consult its dependency constraints before upgrading. Source-version and registry-version badges have separate meanings; this migration makes no additional platform or interoperability certification claim.

---

## Verification

### Tests

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-durability-authority-graph/src/tba_durability_authority_graph/__init__.py).

### Certification Status

No external certification is asserted for `tba-durability-authority-graph` by this documentation migration. README conformance, example syntax, runtime tests, and protocol or security certification are distinct evidence scopes.

### Evidence

The [README standards CI](https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml) records mechanical documentation results for its tested commit. The [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-durability-authority-graph/src/tba_durability_authority_graph/__init__.py) and example sources support the package-boundary description; external runtime behavior requires its own test evidence.

---

## FAQ

### Why

**Why select this package?** `tba-durability-authority-graph` provides durable authority-graph table operations and specifications; use its own API boundary rather than assuming neighboring packages are bundled or configured automatically.

### How

**How do I start?** Install or synchronize the environment under Getting Started, follow the maintained example for `tba-durability-authority-graph`, and consult [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-durability-authority-graph/src/tba_durability_authority_graph/__init__.py) for the exact types and signatures involved.

### When

**When should I validate an upgrade?** Recheck `tba-durability-authority-graph` whenever its source version, declared collaborators, configuration, or caller changes. Run relevant behavioral tests in addition to the README gate before promotion.

---

## Documentation and Related Packages

### More Documentation

The [repository contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md), [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-durability-authority-graph/src/tba_durability_authority_graph/__init__.py), and [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-durability-authority-graph/pyproject.toml) provide the supporting context for `tba-durability-authority-graph`. The [README policy](https://github.com/groupsum/readme-standards/blob/master/docs/outline.md) defines the common document structure.

### Related Packages

Declared local runtime dependencies:

- [tba-storage-authority-graph](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-authority-graph/README.md)

Direct downstream consumers:

- [tba-durability-authorization-policy-authority-derivation-graph](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-durability-authorization-policy-authority-derivation-graph/README.md)

### Project Links

<!-- readme-standards:begin project-links -->
- [Documentation](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/030-storage-runtime/tba-durability-authority-graph#readme)
- [Homepage](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/030-storage-runtime/tba-durability-authority-graph#readme)
- [Issues](https://github.com/tigrbl/tigrbl_auth/issues)
- [PyPI](https://pypi.org/project/tba-durability-authority-graph/)
- [Repository](https://github.com/tigrbl/tigrbl_auth)
- [Source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/030-storage-runtime/tba-durability-authority-graph)
- [pypi: tba-durability-authority-graph](https://pypi.org/project/tba-durability-authority-graph/)
<!-- readme-standards:end project-links -->

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/030-storage-runtime/tba-durability-authority-graph)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-durability-authority-graph/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-durability-authority-graph/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-durability-authority-graph/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-durability-authority-graph/)

---

## Contributing

### How to Contribute

Follow the [contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md) and include a focused example or regression for changes to `tba-durability-authority-graph`. Keep package behavior, its documented boundary, and its tests aligned.

### Development Setup

Work from the `pkgs/030-storage-runtime/tba-durability-authority-graph` checkout. Synchronize its declared development environment with uv, then run the relevant package tests and `python -m pytest docs/readme/test_examples.py`. The repository’s dedicated README job installs `readme-standards==0.1.1` without resolving unrelated runtime packages.

### Notes for Maintainers

Edit authored prose directly in this `tba-durability-authority-graph` README. Update source examples in `docs/readme/`, then run `readme-standards render --root . --write` from the package directory and review the diff. Required headings and generated blocks come from package-guide-v1.

---

## Governance

### Ownership and Decision Making

Changes to `tba-durability-authority-graph` follow the maintainer review process of [tigrbl/tigrbl_auth](https://github.com/tigrbl/tigrbl_auth) and its contribution guide. Author attribution remains in the [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-durability-authority-graph/pyproject.toml); this README does not assign new publishing or administrative authority.

### Standards and Policies

`tba-durability-authority-graph` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `030-storage-runtime` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

### Lifecycle and Migration

The `tba-durability-authority-graph` source version is `0.4.0.dev3`. This change standardizes documentation and adds a development-only gate; it does not publish a new runtime version or declare a previously unpublished package released. Preserve explicit deprecation and replacement instructions where present.

---

## License and Attribution

### License

<!-- readme-standards:begin license -->
Licensed under `Apache-2.0`. See [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-durability-authority-graph/LICENSE).
<!-- readme-standards:end license -->

### Notices

<!-- readme-standards:begin notices -->
See [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-durability-authority-graph/NOTICE) for attribution.
<!-- readme-standards:end notices -->
