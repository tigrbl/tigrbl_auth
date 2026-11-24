# tba-tests-scim

<!-- readme-standards:begin branding -->
<p align="center"><a href="https://github.com/tigrbl/tigrbl_auth"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="300"></a></p>
<p align="center"><strong>tba-tests-scim</strong></p>
<p align="center">Schema registration, PATCH operations, and group membership.</p>
<p align="center">
<a href="https://pypi.org/project/tba-tests-scim/"><img alt="pypi: tba-tests-scim unpublished" src="https://img.shields.io/static/v1?label=pypi&amp;message=tba-tests-scim%20unpublished&amp;labelColor=1E293B&amp;color=92400E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-scim/pyproject.toml"><img alt="Source version: 0.4.0.dev2" src="https://img.shields.io/static/v1?label=Source%20version&amp;message=0.4.0.dev2&amp;labelColor=1E293B&amp;color=4338CA"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-scim/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/static/v1?label=Python&amp;message=%3E%3D3.10%2C%3C3.16&amp;labelColor=1E293B&amp;color=0F766E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-scim/pyproject.toml"><img alt="Layer: 120-tests" src="https://img.shields.io/static/v1?label=Layer&amp;message=120-tests&amp;labelColor=1E293B&amp;color=6D28D9"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-scim/README.md#lifecycle-and-migration"><img alt="Lifecycle: active" src="https://img.shields.io/static/v1?label=Lifecycle&amp;message=active&amp;labelColor=1E293B&amp;color=166534"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-scim/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/static/v1?label=License&amp;message=Apache-2.0&amp;labelColor=1E293B&amp;color=86198F"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-scim/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/static/v1?label=Notice&amp;message=attribution&amp;labelColor=1E293B&amp;color=86198F"></a>
</p>
<p align="center">
<a href="https://pypi.org/project/tba-tests-scim/"><img alt="pypi downloads: tba-tests-scim: unpublished" src="https://img.shields.io/static/v1?label=pypi%20downloads&amp;message=tba-tests-scim%3A%20unpublished&amp;labelColor=1E293B&amp;color=92400E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-scim/README.md"><img alt="README hits: tba-tests-scim" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/pkgs/120-tests/tba-tests-scim/README.md.svg?label=README%20hits&amp;labelColor=1E293B&amp;color=0E7490"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="README standards: CI gate" src="https://img.shields.io/static/v1?label=README%20standards&amp;message=CI%20gate&amp;labelColor=1E293B&amp;color=1D4ED8"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-scim/docs/readme/test_examples.py"><img alt="Tests: example source" src="https://img.shields.io/static/v1?label=Tests&amp;message=example%20source&amp;labelColor=1E293B&amp;color=0F766E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-scim/README.md#certification-status"><img alt="Certification: not certified" src="https://img.shields.io/static/v1?label=Certification&amp;message=not%20certified&amp;labelColor=1E293B&amp;color=92400E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/tools/readme/POLICY.md"><img alt="Governance: repository policy" src="https://img.shields.io/static/v1?label=Governance&amp;message=repository%20policy&amp;labelColor=1E293B&amp;color=4338CA"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="Evidence: source and CI" src="https://img.shields.io/static/v1?label=Evidence&amp;message=source%20and%20CI&amp;labelColor=1E293B&amp;color=6D28D9"></a>
</p>
<p align="center"><a href="#overview">Overview</a> · <a href="#installation">Installation</a> · <a href="#quick-start">Quick Start</a> · <a href="#usage">Usage</a> · <a href="#public-api-and-import-surfaces">API</a> · <a href="#contributing">Contributing</a> · <a href="#governance">Governance</a> · <a href="#license">License</a></p>
<!-- readme-standards:end branding -->

---

## Overview

### Summary

Schema registration, PATCH operations, and group membership.

Run from the repository root with
`uv run --extra test pytest --certification-lane all pkgs/120-tests/tba-tests-scim/tests`.

- Package: `tba-tests-scim`
- Layer: `120-tests`
- Responsibility: Schema registration, PATCH operations, and group membership.
- Public surface: [package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-scim/pyproject.toml).
- Distribution: repository development harness.

### Why This Package

`tba-tests-scim` isolates this responsibility: Schema registration, PATCH operations, and group membership. Its [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-scim/pyproject.toml) exposes the checkout commands documented in Quick Start, allowing consumers to select this package without treating adjacent packages as part of its public contract.

### When to Use

Choose `tba-tests-scim` for this responsibility: Schema registration, PATCH operations, and group membership. Its `120-tests` placement keeps test fixtures and executable verification separate from production identity services or deployable policy defaults.

### Features

- Public source surface: the checkout commands documented in Quick Start.
- Declared responsibility: Schema registration, PATCH operations, and group membership.
- Versioned package metadata and maintained checkout examples.

### Non-Goals

`tba-tests-scim` does not take ownership of production identity services or deployable policy defaults.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

---

## Getting Started

### Prerequisites

Python `>=3.10,<3.16` is required. The [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-scim/pyproject.toml) declares no direct runtime dependencies. Use the source-checkout workflow for this workspace or test harness.

### Installation

`tba-tests-scim` is a workspace-only harness (`tool.uv.package = false`), so install the repository development environment rather than a nonexistent wheel:

```bash
uv sync --group dev
```

Run the package's verification commands from the repository root.

#### uv

<!-- readme-standards:begin installation.uv -->
This is a source-only workspace or test harness, not an installable distribution. From its checkout, synchronize the declared environment:

```bash
uv sync
```
<!-- readme-standards:end installation.uv -->

#### pip

<!-- readme-standards:begin installation.pip -->
This is a source-only workspace or test harness, not an installable distribution. Use the uv checkout workflow above; this installer does not install the harness itself.
<!-- readme-standards:end installation.pip -->

#### Poetry

<!-- readme-standards:begin installation.poetry -->
This is a source-only workspace or test harness, not an installable distribution. Use the uv checkout workflow above; this installer does not install the harness itself.
<!-- readme-standards:end installation.poetry -->

### Quick Start

`tba-tests-scim` is a workspace-only harness (`tool.uv.package = false`), so install the repository development environment rather than a nonexistent wheel:


Run the package's verification commands from the repository root.

#### Example

<!-- readme-standards:begin example.quick-start -->
Source: [docs/readme/quick_start.sh](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-scim/docs/readme/quick_start.sh).

```bash
uv sync --group dev
```
<!-- readme-standards:end example.quick-start -->

#### Expected Result

The example demonstrates the documented `tba-tests-scim` source boundary or workflow. Complete its required configuration first. README CI checks the maintained source’s syntax and declarations; it does not claim that external services or the application workflow were exercised.

---

## Usage

### Common Workflows

<!-- readme-standards:begin example.usage -->
Source: [docs/readme/usage.sh](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-scim/docs/readme/usage.sh).

```bash
uv run pytest pkgs/120-tests/tba-tests-scim
```
<!-- readme-standards:end example.usage -->

Use `tba-tests-scim` through its repository test harness rather than as a production runtime import:


Its fixtures and checks support the integration workflow documented in Quick start.

### Configuration

Configure `tba-tests-scim` through the APIs in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-scim/pyproject.toml); its [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-scim/pyproject.toml) describes installation requirements, not an implicit service configuration. No additional package-global configuration contract is inferred from dependencies.

### Error Handling

The inspected `tba-tests-scim` source does not establish a package-wide exception hierarchy. Preserve errors from its declared dependencies and validate inputs using the specific public contract in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-scim/pyproject.toml).

### Best Practices

Use the explicit `tba-tests-scim` imports documented below and keep collaborator configuration with the caller. Run the package’s relevant tests after changing the checkout commands documented in Quick Start; an import or successful installation alone does not establish its runtime guarantees.

---

## Package Boundary

### What It Owns

`tba-tests-scim` belongs to `120-tests` and owns test fixtures and executable verification: Schema registration, PATCH operations, and group membership.

Its implementation surface is the [package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-scim/pyproject.toml).

Keep production identity services or deployable policy defaults in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

### Public API and Import Surfaces

`tba-tests-scim` is a source-checkout harness. No installable Python namespace was found in the package layout; use its documented commands and test files.

### Entry Points

<!-- readme-standards:begin entry-points -->
This package declares no command-line, GUI, or plugin entry points in its manifest.
<!-- readme-standards:end entry-points -->

### Injected Dependencies

The [package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-scim/pyproject.toml) for `tba-tests-scim` does not declare an explicit service-constructor or keyword-only factory hook in the inspected source. Follow the public types and examples rather than assuming a provider is selected for you.

Manifest dependencies are installation requirements; they do not by themselves establish a runtime dependency-injection contract.

### Protocol Consumers

No direct package-manifest dependency on `tba-tests-scim` was found in the audited three-repository inventory. External consumers may still use its documented imports or commands.

### Extensions

For `tba-tests-scim`, use the source-declared public interfaces (the checkout commands documented in Quick Start) when composing or extending behavior. Its entry-point section below is authoritative for registered plugins; no additional extension loader is inferred from the package name.

---

## Operations and Readiness

### Operational Requirements

`tba-tests-scim` exposes test fixtures and executable verification. Inspect the [package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-scim/pyproject.toml) for the exported types and composition surface.

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

### Health and Observability

This README does not establish a standalone health endpoint for `tba-tests-scim`. Observe the concrete caller’s results, exceptions, and existing test reports. An application that embeds this package must define its own health and telemetry contract.

### Security and Resource Limits

Apply the input, credential, and resource constraints implemented in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-scim/pyproject.toml). The `tba-tests-scim` README gate is a documentation check, not a security review or a substitute for the implementation’s limits and caller authorization.

### Compatibility

This source version of `tba-tests-scim` declares Python `>=3.10,<3.16`. Consult its dependency constraints before upgrading. Source-version and registry-version badges have separate meanings; this migration makes no additional platform or interoperability certification claim.

---

## Verification

### Tests

Run the README and package-standard checks from the repository root:

```bash
uv run --no-project python scripts/verify_readme_standards.py
uv run --no-project python scripts/verify_package_standards.py
```

These checks validate documentation structure, metadata, and branding for `tba-tests-scim`. Behavioral and integration assertions require the package's own tests and their recorded evidence.

### Certification Status

No external certification is asserted for `tba-tests-scim` by this documentation migration. README conformance, example syntax, runtime tests, and protocol or security certification are distinct evidence scopes.

### Evidence

The [README standards CI](https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml) records mechanical documentation results for its tested commit. The [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-scim/pyproject.toml) and example sources support the package-boundary description; external runtime behavior requires its own test evidence.

---

## FAQ

### Why

**Why select this package?** `tba-tests-scim` provides schema registration, PATCH operations, and group membership; use its own API boundary rather than assuming neighboring packages are bundled or configured automatically.

### How

**How do I start?** Install or synchronize the environment under Getting Started, follow the maintained example for `tba-tests-scim`, and consult [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-scim/pyproject.toml) for the exact types and signatures involved.

### When

**When should I validate an upgrade?** Recheck `tba-tests-scim` whenever its source version, declared collaborators, configuration, or caller changes. Run relevant behavioral tests in addition to the README gate before promotion.

---

## Documentation and Related Packages

### More Documentation

The [repository contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md), [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-scim/pyproject.toml), and [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-scim/pyproject.toml) provide the supporting context for `tba-tests-scim`. The [README policy](https://github.com/groupsum/readme-standards/blob/master/docs/outline.md) defines the common document structure.

### Related Packages

`tba-tests-scim` declares no local runtime dependency and has no direct consumer in the active manifest graph. Browse the [120-tests layer](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/120-tests) for adjacent package responsibilities; adjacency does not imply a dependency.

### Project Links

<!-- readme-standards:begin project-links -->
- [Source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/120-tests/tba-tests-scim)
- [pypi: tba-tests-scim](https://pypi.org/project/tba-tests-scim/)
<!-- readme-standards:end project-links -->

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/120-tests/tba-tests-scim)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-scim/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-scim/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-scim/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

---

## Contributing

### How to Contribute

Follow the [contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md) and include a focused example or regression for changes to `tba-tests-scim`. Keep package behavior, its documented boundary, and its tests aligned.

### Development Setup

Work from the `pkgs/120-tests/tba-tests-scim` checkout. Synchronize its declared development environment with uv, then run the relevant package tests and `python -m pytest docs/readme/test_examples.py`. The repository’s dedicated README job installs `readme-standards==0.1.3` without resolving unrelated runtime packages.

### Notes for Maintainers

Edit authored prose directly in this `tba-tests-scim` README. Update source examples in `docs/readme/`, then run `readme-standards render --root . --write` from the package directory and review the diff. Required headings and generated blocks come from package-guide-v1.

---

## Governance

### Ownership and Decision Making

Changes to `tba-tests-scim` follow the maintainer review process of [tigrbl/tigrbl_auth](https://github.com/tigrbl/tigrbl_auth) and its contribution guide. Author attribution remains in the [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-scim/pyproject.toml); this README does not assign new publishing or administrative authority.

### Standards and Policies

`tba-tests-scim` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `120-tests` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

### Lifecycle and Migration

The `tba-tests-scim` source version is `0.4.0.dev2`. This change standardizes documentation and adds a development-only gate; it does not publish a new runtime version or declare a previously unpublished package released. Preserve explicit deprecation and replacement instructions where present.

---

## License and Attribution

### License

<!-- readme-standards:begin license -->
Licensed under `Apache-2.0`. See [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-scim/LICENSE).
<!-- readme-standards:end license -->

### Notices

<!-- readme-standards:begin notices -->
See [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-scim/NOTICE) for attribution.
<!-- readme-standards:end notices -->
