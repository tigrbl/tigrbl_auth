# tba-storage-tenancy

<!-- readme-standards:begin branding -->
<p align="center"><a href="https://github.com/tigrbl/tigrbl_auth"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="300"></a></p>
<p align="center"><strong>tba-storage-tenancy</strong></p>
<p align="center">Owned tenancy identity database tables and migrations.</p>
<p align="center">
<a href="https://pypi.org/project/tba-storage-tenancy/"><img alt="pypi: tba-storage-tenancy" src="https://img.shields.io/pypi/v/tba-storage-tenancy?labelColor=1E293B&amp;color=1D4ED8"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-tenancy/pyproject.toml"><img alt="Source version: 0.4.0.dev3" src="https://img.shields.io/static/v1?label=Source%20version&amp;message=0.4.0.dev3&amp;labelColor=1E293B&amp;color=4338CA"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-tenancy/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/static/v1?label=Python&amp;message=%3E%3D3.10%2C%3C3.16&amp;labelColor=1E293B&amp;color=0F766E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-tenancy/pyproject.toml"><img alt="Layer: 001-storage" src="https://img.shields.io/static/v1?label=Layer&amp;message=001-storage&amp;labelColor=1E293B&amp;color=6D28D9"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-tenancy/README.md#lifecycle-and-migration"><img alt="Lifecycle: active" src="https://img.shields.io/static/v1?label=Lifecycle&amp;message=active&amp;labelColor=1E293B&amp;color=166534"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-tenancy/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/static/v1?label=License&amp;message=Apache-2.0&amp;labelColor=1E293B&amp;color=86198F"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-tenancy/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/static/v1?label=Notice&amp;message=attribution&amp;labelColor=1E293B&amp;color=86198F"></a>
</p>
<p align="center">
<a href="https://pypi.org/project/tba-storage-tenancy/"><img alt="Monthly PyPI downloads: tba-storage-tenancy" src="https://img.shields.io/pypi/dm/tba-storage-tenancy?labelColor=1E293B&amp;color=0E7490"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-tenancy/README.md"><img alt="README hits: tba-storage-tenancy" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/pkgs/001-storage/tba-storage-tenancy/README.md.svg?label=README%20hits&amp;labelColor=1E293B&amp;color=0E7490"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="README standards: CI gate" src="https://img.shields.io/static/v1?label=README%20standards&amp;message=CI%20gate&amp;labelColor=1E293B&amp;color=1D4ED8"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-tenancy/docs/readme/test_examples.py"><img alt="Tests: example source" src="https://img.shields.io/static/v1?label=Tests&amp;message=example%20source&amp;labelColor=1E293B&amp;color=0F766E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-tenancy/README.md#certification-status"><img alt="Certification: not certified" src="https://img.shields.io/static/v1?label=Certification&amp;message=not%20certified&amp;labelColor=1E293B&amp;color=92400E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/tools/readme/POLICY.md"><img alt="Governance: repository policy" src="https://img.shields.io/static/v1?label=Governance&amp;message=repository%20policy&amp;labelColor=1E293B&amp;color=4338CA"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="Evidence: source and CI" src="https://img.shields.io/static/v1?label=Evidence&amp;message=source%20and%20CI&amp;labelColor=1E293B&amp;color=6D28D9"></a>
</p>
<p align="center"><a href="#overview">Overview</a> · <a href="#installation">Installation</a> · <a href="#quick-start">Quick Start</a> · <a href="#usage">Usage</a> · <a href="#public-api-and-import-surfaces">API</a> · <a href="#contributing">Contributing</a> · <a href="#governance">Governance</a> · <a href="#license">License</a></p>
<!-- readme-standards:end branding -->

---

## Overview

### Summary

Owns the `tigrbl.identity.storage.tenancy` schema component.

- Package: `tba-storage-tenancy`
- Layer: `001-storage`
- Responsibility: Owned tenancy identity database tables and migrations.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-tenancy/src/tba_storage_tenancy/__init__.py).
- Distribution: Python package on PyPI.

### Why This Package

`tba-storage-tenancy` isolates this responsibility: Owned tenancy identity database tables and migrations. Its [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-tenancy/src/tba_storage_tenancy/__init__.py) exposes `MANIFEST`, `TABLE_MODELS`, `TABLE_MODEL_BY_NAME`, `TABLE_MODEL_BY_TABLENAME`, `load_manifest`, allowing consumers to select this package without treating adjacent packages as part of its public contract.

### When to Use

Choose `tba-storage-tenancy` for this responsibility: Owned tenancy identity database tables and migrations. Its `001-storage` placement keeps storage schema and table declarations separate from protocol endpoints or deployment-specific provider selection.

### Features

- `Realm`: declared in src/tba_storage_tenancy/tables/realm/_table.py
- `Tenant`: declared in src/tba_storage_tenancy/tables/tenant/_table.py

### Non-Goals

`tba-storage-tenancy` does not take ownership of protocol endpoints or deployment-specific provider selection.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

---

## Getting Started

### Prerequisites

Python `>=3.10,<3.16` is required. The [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-tenancy/pyproject.toml) declares runtime dependencies including `tigrbl`, `tigrbl-migrations`, `tba-primitives-identity`. Read the example’s inputs and service requirements before execution.

### Installation

Install the selected PyPI release of `tba-storage-tenancy`:

```bash
uv pip install tba-storage-tenancy
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/001-storage/tba-storage-tenancy
```

#### uv

<!-- readme-standards:begin installation.uv -->
```bash
uv add tba-storage-tenancy
```
<!-- readme-standards:end installation.uv -->

#### pip

<!-- readme-standards:begin installation.pip -->
```bash
python -m pip install tba-storage-tenancy
```
<!-- readme-standards:end installation.pip -->

#### Poetry

<!-- readme-standards:begin installation.poetry -->
```bash
poetry add tba-storage-tenancy
```
<!-- readme-standards:end installation.poetry -->

### Quick Start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.


```bash
uv run --isolated --no-project --python 3.12 --with "tba-storage-tenancy==0.4.0.dev3" python quickstart.py
```

The command prints a positive inventory count.

#### Example

<!-- readme-standards:begin example.quick-start -->
Source: [docs/readme/quick_start.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-tenancy/docs/readme/quick_start.py).

```python
from tba_storage_tenancy import TABLE_MODELS

assert TABLE_MODELS
print(len(TABLE_MODELS))
```
<!-- readme-standards:end example.quick-start -->

#### Expected Result

The example demonstrates the documented `tba-storage-tenancy` source boundary or workflow. Complete its required configuration first. README CI checks the maintained source’s syntax and declarations; it does not claim that external services or the application workflow were exercised.

---

## Usage

### Common Workflows

<!-- readme-standards:begin example.usage -->
Source: [docs/readme/usage.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-tenancy/docs/readme/usage.py).

```python
from tba_storage_tenancy import TABLE_MODELS

assert TABLE_MODELS
print(len(TABLE_MODELS))
```
<!-- readme-standards:end example.usage -->

The following public-entry-point example belongs to `tba-storage-tenancy`. Owned tenancy identity database tables and migrations. Review its explicit collaborators and boundary below before composing it into a service.

### Configuration

Configure `tba-storage-tenancy` through the APIs in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-tenancy/src/tba_storage_tenancy/__init__.py); its [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-tenancy/pyproject.toml) describes installation requirements, not an implicit service configuration. No additional package-global configuration contract is inferred from dependencies.

### Error Handling

The inspected `tba-storage-tenancy` source does not establish a package-wide exception hierarchy. Preserve errors from its declared dependencies and validate inputs using the specific public contract in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-tenancy/src/tba_storage_tenancy/__init__.py).

### Best Practices

Use the explicit `tba-storage-tenancy` imports documented below and keep collaborator configuration with the caller. Run the package’s relevant tests after changing `MANIFEST`, `TABLE_MODELS`, `TABLE_MODEL_BY_NAME`, `TABLE_MODEL_BY_TABLENAME`, `load_manifest`; an import or successful installation alone does not establish its runtime guarantees.

---

## Package Boundary

### What It Owns

`tba-storage-tenancy` belongs to `001-storage` and owns storage schema and table declarations: Owned tenancy identity database tables and migrations.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-tenancy/src/tba_storage_tenancy/__init__.py).

Keep protocol endpoints or deployment-specific provider selection in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

### Public API and Import Surfaces

Import namespace: `tba_storage_tenancy`.

Source-declared exports or types: `MANIFEST`, `TABLE_MODELS`, `TABLE_MODEL_BY_NAME`, `TABLE_MODEL_BY_TABLENAME`, `load_manifest`.

Inspect [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-tenancy/src/tba_storage_tenancy/__init__.py) for exact signatures; this inventory does not designate every internal module as stable.

### Entry Points

<!-- readme-standards:begin entry-points -->
This package declares no command-line, GUI, or plugin entry points in its manifest.
<!-- readme-standards:end entry-points -->

### Injected Dependencies

The [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-tenancy/src/tba_storage_tenancy/__init__.py) for `tba-storage-tenancy` does not declare an explicit service-constructor or keyword-only factory hook in the inspected source. Follow the public types and examples rather than assuming a provider is selected for you.

Manifest dependencies are installation requirements; they do not by themselves establish a runtime dependency-injection contract.

### Protocol Consumers

Direct consumers in this checkout’s package manifests include `tba-storage-audit`, `tba-storage-claims`, `tba-storage-consent`, `tba-storage-core`, `tba-storage-delegation`, `tba-storage-key-material`, `tba-storage-oauth`, `tba-storage-principals`, `tba-storage-token`, `tba-durability-audit`, `tba-runtime-identity-storage`, `tba-server-identity`, `tba-app-backend-core`, `tba-workspace`. These edges describe declared dependencies, not protocol-conformance evidence.

### Extensions

For `tba-storage-tenancy`, use the source-declared public interfaces (`MANIFEST`, `TABLE_MODELS`, `TABLE_MODEL_BY_NAME`, `TABLE_MODEL_BY_TABLENAME`, `load_manifest`) when composing or extending behavior. Its entry-point section below is authoritative for registered plugins; no additional extension loader is inferred from the package name.

---

## Operations and Readiness

### Operational Requirements

`tba-storage-tenancy` exposes storage schema and table declarations. Inspect the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-tenancy/src/tba_storage_tenancy/__init__.py) for the exported types and composition surface.

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

### Health and Observability

This README does not establish a standalone health endpoint for `tba-storage-tenancy`. Observe the concrete caller’s results, exceptions, and existing test reports. An application that embeds this package must define its own health and telemetry contract.

### Security and Resource Limits

Apply the input, credential, and resource constraints implemented in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-tenancy/src/tba_storage_tenancy/__init__.py). The `tba-storage-tenancy` README gate is a documentation check, not a security review or a substitute for the implementation’s limits and caller authorization.

### Compatibility

This source version of `tba-storage-tenancy` declares Python `>=3.10,<3.16`. Consult its dependency constraints before upgrading. Source-version and registry-version badges have separate meanings; this migration makes no additional platform or interoperability certification claim.

---

## Verification

### Tests

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-tenancy/src/tba_storage_tenancy/__init__.py).

### Certification Status

No external certification is asserted for `tba-storage-tenancy` by this documentation migration. README conformance, example syntax, runtime tests, and protocol or security certification are distinct evidence scopes.

### Evidence

The [README standards CI](https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml) records mechanical documentation results for its tested commit. The [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-tenancy/src/tba_storage_tenancy/__init__.py) and example sources support the package-boundary description; external runtime behavior requires its own test evidence.

---

## FAQ

### Why

**Why select this package?** `tba-storage-tenancy` provides owned tenancy identity database tables and migrations; use its own API boundary rather than assuming neighboring packages are bundled or configured automatically.

### How

**How do I start?** Install or synchronize the environment under Getting Started, follow the maintained example for `tba-storage-tenancy`, and consult [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-tenancy/src/tba_storage_tenancy/__init__.py) for the exact types and signatures involved.

### When

**When should I validate an upgrade?** Recheck `tba-storage-tenancy` whenever its source version, declared collaborators, configuration, or caller changes. Run relevant behavioral tests in addition to the README gate before promotion.

---

## Documentation and Related Packages

### More Documentation

The [repository contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md), [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-tenancy/src/tba_storage_tenancy/__init__.py), and [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-tenancy/pyproject.toml) provide the supporting context for `tba-storage-tenancy`. The [README policy](https://github.com/groupsum/readme-standards/blob/master/docs/outline.md) defines the common document structure.

### Related Packages

Declared local runtime dependencies:

- [tba-primitives-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/000-primitives/tba-primitives-identity/README.md)

Direct downstream consumers:

- [tba-app-backend-core](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-core/README.md)
- [tba-durability-audit](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-durability-audit/README.md)
- [tba-runtime-identity-storage](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-runtime-identity-storage/README.md)
- [tba-server-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-server-identity/README.md)
- [tba-storage-audit](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-audit/README.md)
- [tba-storage-claims](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-claims/README.md)
- [tba-storage-consent](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-consent/README.md)
- [tba-storage-core](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-core/README.md)
- [tba-storage-delegation](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-delegation/README.md)
- [tba-storage-key-material](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-key-material/README.md)
- [tba-storage-oauth](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-oauth/README.md)
- [tba-storage-principals](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-principals/README.md)

13 packages directly declare this dependency; the [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records the complete graph.

### Project Links

<!-- readme-standards:begin project-links -->
- [Documentation](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/001-storage/tba-storage-tenancy#readme)
- [Homepage](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/001-storage/tba-storage-tenancy#readme)
- [Issues](https://github.com/tigrbl/tigrbl_auth/issues)
- [PyPI](https://pypi.org/project/tba-storage-tenancy/)
- [Repository](https://github.com/tigrbl/tigrbl_auth)
- [Source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/001-storage/tba-storage-tenancy)
- [pypi: tba-storage-tenancy](https://pypi.org/project/tba-storage-tenancy/)
<!-- readme-standards:end project-links -->

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/001-storage/tba-storage-tenancy)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-tenancy/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-tenancy/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-tenancy/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-storage-tenancy/)

---

## Contributing

### How to Contribute

Follow the [contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md) and include a focused example or regression for changes to `tba-storage-tenancy`. Keep package behavior, its documented boundary, and its tests aligned.

### Development Setup

Work from the `pkgs/001-storage/tba-storage-tenancy` checkout. Synchronize its declared development environment with uv, then run the relevant package tests and `python -m pytest docs/readme/test_examples.py`. The repository’s dedicated README job installs `readme-standards==0.1.3` without resolving unrelated runtime packages.

### Notes for Maintainers

Edit authored prose directly in this `tba-storage-tenancy` README. Update source examples in `docs/readme/`, then run `readme-standards render --root . --write` from the package directory and review the diff. Required headings and generated blocks come from package-guide-v1.

---

## Governance

### Ownership and Decision Making

Changes to `tba-storage-tenancy` follow the maintainer review process of [tigrbl/tigrbl_auth](https://github.com/tigrbl/tigrbl_auth) and its contribution guide. Author attribution remains in the [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-tenancy/pyproject.toml); this README does not assign new publishing or administrative authority.

### Standards and Policies

`tba-storage-tenancy` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `001-storage` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

### Lifecycle and Migration

The `tba-storage-tenancy` source version is `0.4.0.dev3`. This change standardizes documentation and adds a development-only gate; it does not publish a new runtime version or declare a previously unpublished package released. Preserve explicit deprecation and replacement instructions where present.

---

## License and Attribution

### License

<!-- readme-standards:begin license -->
Licensed under `Apache-2.0`. See [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-tenancy/LICENSE).
<!-- readme-standards:end license -->

### Notices

<!-- readme-standards:begin notices -->
See [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-tenancy/NOTICE) for attribution.
<!-- readme-standards:end notices -->
