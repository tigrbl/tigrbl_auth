# tba-tests-interop-jose

<!-- readme-standards:begin branding -->
<p align="center"><a href="https://github.com/tigrbl/tigrbl_auth"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="300"></a></p>
<p align="center"><strong>tba-tests-interop-jose</strong></p>
<p align="center">Bidirectional compact JWE interoperability tests for TbA and Swarmauri</p>
<p align="center">
<a href="https://pypi.org/project/tba-tests-interop-jose/"><img alt="pypi: tba-tests-interop-jose unpublished" src="https://img.shields.io/static/v1?label=pypi&amp;message=tba-tests-interop-jose%20unpublished&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-interop-jose/pyproject.toml"><img alt="Source version: 0.1.0" src="https://img.shields.io/static/v1?label=Source%20version&amp;message=0.1.0&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-interop-jose/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/static/v1?label=Python&amp;message=%3E%3D3.10%2C%3C3.16&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-interop-jose/pyproject.toml"><img alt="Layer: 120-tests" src="https://img.shields.io/static/v1?label=Layer&amp;message=120-tests&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-interop-jose/README.md#lifecycle-and-migration"><img alt="Lifecycle: active" src="https://img.shields.io/static/v1?label=Lifecycle&amp;message=active&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-interop-jose/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/static/v1?label=License&amp;message=Apache-2.0&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-interop-jose/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/static/v1?label=Notice&amp;message=attribution&amp;color=525252"></a>
</p>
<p align="center">
<a href="https://pypi.org/project/tba-tests-interop-jose/"><img alt="pypi downloads: tba-tests-interop-jose: unpublished" src="https://img.shields.io/static/v1?label=pypi%20downloads&amp;message=tba-tests-interop-jose%3A%20unpublished&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-interop-jose/README.md"><img alt="README hits: tba-tests-interop-jose" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/pkgs/120-tests/tba-tests-interop-jose/README.md.svg?label=README%20hits"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="README standards: CI gate" src="https://img.shields.io/static/v1?label=README%20standards&amp;message=CI%20gate&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-interop-jose/docs/readme/test_examples.py"><img alt="Tests: example source" src="https://img.shields.io/static/v1?label=Tests&amp;message=example%20source&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-interop-jose/README.md#certification-status"><img alt="Certification: not certified" src="https://img.shields.io/static/v1?label=Certification&amp;message=not%20certified&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/tools/readme/POLICY.md"><img alt="Governance: repository policy" src="https://img.shields.io/static/v1?label=Governance&amp;message=repository%20policy&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="Evidence: source and CI" src="https://img.shields.io/static/v1?label=Evidence&amp;message=source%20and%20CI&amp;color=525252"></a>
</p>
<p align="center"><a href="#overview">Overview</a> · <a href="#installation">Installation</a> · <a href="#quick-start">Quick Start</a> · <a href="#usage">Usage</a> · <a href="#public-api-and-import-surfaces">API</a> · <a href="#contributing">Contributing</a> · <a href="#governance">Governance</a> · <a href="#license">License</a></p>
<!-- readme-standards:end branding -->

---

## Overview

### Summary

Bidirectional compact JWE interoperability tests for TbA and Swarmauri.

- Package: `tba-tests-interop-jose`
- Layer: `120-tests`
- Responsibility: Bidirectional compact JWE interoperability tests for TbA and Swarmauri.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-interop-jose/src/tba_tests_interop_jose/__init__.py).
- Distribution: test-only Python wheel with a pytest plugin.

### Why This Package

`tba-tests-interop-jose` isolates this responsibility: Bidirectional compact JWE interoperability tests for TbA and Swarmauri. Its [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-interop-jose/src/tba_tests_interop_jose/__init__.py) exposes the checkout commands documented in Quick Start, allowing consumers to select this package without treating adjacent packages as part of its public contract.

### When to Use

Choose `tba-tests-interop-jose` for this responsibility: Bidirectional compact JWE interoperability tests for TbA and Swarmauri. Its `120-tests` placement keeps test fixtures and executable verification separate from production identity services or deployable policy defaults.

### Features

- Public source surface: the checkout commands documented in Quick Start.
- Declared responsibility: Bidirectional compact JWE interoperability tests for TbA and Swarmauri.
- Versioned package metadata and maintained checkout examples.

### Non-Goals

`tba-tests-interop-jose` does not take ownership of production identity services or deployable policy defaults.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

---

## Getting Started

### Prerequisites

Python `>=3.10,<3.16` is required. The [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-interop-jose/pyproject.toml) declares runtime dependencies including `cryptography`, `pytest`, `pytest-asyncio`. Read the example’s inputs and service requirements before execution.

### Installation

Install the selected PyPI release of `tba-tests-interop-jose`:

```bash
uv pip install tba-tests-interop-jose
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/120-tests/tba-tests-interop-jose
```

#### uv

<!-- readme-standards:begin installation.uv -->
`tba-tests-interop-jose` is not declared published. From the source checkout:

```bash
uv pip install .
```
<!-- readme-standards:end installation.uv -->

#### pip

<!-- readme-standards:begin installation.pip -->
`tba-tests-interop-jose` is not declared published. From the source checkout:

```bash
python -m pip install .
```
<!-- readme-standards:end installation.pip -->

#### Poetry

<!-- readme-standards:begin installation.poetry -->
`tba-tests-interop-jose` is not declared published. From a separate Poetry project, replace the path with your checkout:

```bash
poetry add /path/to/tba-tests-interop-jose
```
<!-- readme-standards:end installation.poetry -->

### Quick Start

Run both source-checkout directions from the TbA checkout with `SWARMAURI_SDK_ROOT` set to the Swarmauri checkout.

#### Example

<!-- readme-standards:begin example.quick-start -->
Source: [docs/readme/quick_start.sh](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-interop-jose/docs/readme/quick_start.sh).

```bash
uv run --extra test pytest --tba-suite tba-tests-interop-jose --jose-interop-mode source
```
<!-- readme-standards:end example.quick-start -->

#### Expected Result

The example demonstrates the documented `tba-tests-interop-jose` source boundary or workflow. Complete its required configuration first. README CI checks the maintained source’s syntax and declarations; it does not claim that external services or the application workflow were exercised.

---

## Usage

### Common Workflows

<!-- readme-standards:begin example.usage -->
Source: [docs/readme/usage.sh](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-interop-jose/docs/readme/usage.sh).

```bash
python -m pytest --pyargs tba_tests_interop_jose.tests --jose-interop-mode installed
```
<!-- readme-standards:end example.usage -->

For release verification, install this test wheel and pin the peer wheels in
a clean environment. The peer entry points are `swarmauri-crypto-jwe`,
`tba-concrete-jose`, `tba-capability-protected-envelope`,
`tba-protocol-security-jwe`, and `tba-provider-jose-cryptography`.
Run from outside both source checkouts. Installed mode verifies that both
peers resolve to their distribution records.

### Configuration

The [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-interop-jose/src/tba_tests_interop_jose/__init__.py) references configuration keys `SWARMAURI_SDK_ROOT`. Consult the constructor or function signature before supplying them; a referenced key is not necessarily a global environment variable.

### Error Handling

The inspected `tba-tests-interop-jose` source does not establish a package-wide exception hierarchy. Preserve errors from its declared dependencies and validate inputs using the specific public contract in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-interop-jose/src/tba_tests_interop_jose/__init__.py).

### Best Practices

Use the explicit `tba-tests-interop-jose` imports documented below and keep collaborator configuration with the caller. Run the package’s relevant tests after changing the checkout commands documented in Quick Start; an import or successful installation alone does not establish its runtime guarantees.

---

## Package Boundary

### What It Owns

`tba-tests-interop-jose` belongs to `120-tests` and owns test fixtures and executable verification: Bidirectional compact JWE interoperability tests for TbA and Swarmauri.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-interop-jose/src/tba_tests_interop_jose/__init__.py).

Keep production identity services or deployable policy defaults in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

### Public API and Import Surfaces

Import namespace: `tba_tests_interop_jose`.

Source-declared exports or types: the checkout commands documented in Quick Start.

Inspect [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-interop-jose/src/tba_tests_interop_jose/__init__.py) for exact signatures; this inventory does not designate every internal module as stable.

### Entry Points

<!-- readme-standards:begin entry-points -->
- `pytest11` → `tba_tests_interop_jose.pytest_plugin` → `tba_tests_interop_jose.pytest_plugin`
<!-- readme-standards:end entry-points -->

### Injected Dependencies

The [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-interop-jose/src/tba_tests_interop_jose/__init__.py) for `tba-tests-interop-jose` does not declare an explicit service-constructor or keyword-only factory hook in the inspected source. Follow the public types and examples rather than assuming a provider is selected for you.

Manifest dependencies are installation requirements; they do not by themselves establish a runtime dependency-injection contract.

### Protocol Consumers

No direct package-manifest dependency on `tba-tests-interop-jose` was found in the audited three-repository inventory. External consumers may still use its documented imports or commands.

### Extensions

For `tba-tests-interop-jose`, use the source-declared public interfaces (the checkout commands documented in Quick Start) when composing or extending behavior. Its entry-point section below is authoritative for registered plugins; no additional extension loader is inferred from the package name.

---

## Operations and Readiness

### Operational Requirements

`tba-tests-interop-jose` exposes test fixtures and executable verification. Inspect the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-interop-jose/src/tba_tests_interop_jose/__init__.py) for the exported types and composition surface.

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

### Health and Observability

This README does not establish a standalone health endpoint for `tba-tests-interop-jose`. Observe the concrete caller’s results, exceptions, and existing test reports. An application that embeds this package must define its own health and telemetry contract.

### Security and Resource Limits

Apply the input, credential, and resource constraints implemented in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-interop-jose/src/tba_tests_interop_jose/__init__.py). The `tba-tests-interop-jose` README gate is a documentation check, not a security review or a substitute for the implementation’s limits and caller authorization.

### Compatibility

This source version of `tba-tests-interop-jose` declares Python `>=3.10,<3.16`. Consult its dependency constraints before upgrading. Source-version and registry-version badges have separate meanings; this migration makes no additional platform or interoperability certification claim.

---

## Verification

### Tests

Run the README and package-standard checks from the repository root:

```bash
uv run --no-project python scripts/verify_readme_standards.py
uv run --no-project python scripts/verify_package_standards.py
```

These checks validate documentation structure, metadata, and branding for `tba-tests-interop-jose`. Behavioral and integration assertions require the package's own tests and their recorded evidence.

### Certification Status

No external certification is asserted for `tba-tests-interop-jose` by this documentation migration. README conformance, example syntax, runtime tests, and protocol or security certification are distinct evidence scopes.

### Evidence

The [README standards CI](https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml) records mechanical documentation results for its tested commit. The [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-interop-jose/src/tba_tests_interop_jose/__init__.py) and example sources support the package-boundary description; external runtime behavior requires its own test evidence.

---

## FAQ

### Why

**Why select this package?** `tba-tests-interop-jose` provides bidirectional compact JWE interoperability tests for TbA and Swarmauri; use its own API boundary rather than assuming neighboring packages are bundled or configured automatically.

### How

**How do I start?** Install or synchronize the environment under Getting Started, follow the maintained example for `tba-tests-interop-jose`, and consult [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-interop-jose/src/tba_tests_interop_jose/__init__.py) for the exact types and signatures involved.

### When

**When should I validate an upgrade?** Recheck `tba-tests-interop-jose` whenever its source version, declared collaborators, configuration, or caller changes. Run relevant behavioral tests in addition to the README gate before promotion.

---

## Documentation and Related Packages

### More Documentation

The [repository contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md), [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-interop-jose/src/tba_tests_interop_jose/__init__.py), and [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-interop-jose/pyproject.toml) provide the supporting context for `tba-tests-interop-jose`. The [README policy](https://github.com/groupsum/readme-standards/blob/master/docs/outline.md) defines the common document structure.

### Related Packages

`tba-tests-interop-jose` declares no local runtime dependency and has no direct consumer in the active manifest graph. Browse the [120-tests layer](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/120-tests) for adjacent package responsibilities; adjacency does not imply a dependency.

### Project Links

<!-- readme-standards:begin project-links -->
- [PyPI](https://pypi.org/project/tba-tests-interop-jose/)
- [Source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/120-tests/tba-tests-interop-jose)
- [pypi: tba-tests-interop-jose](https://pypi.org/project/tba-tests-interop-jose/)
<!-- readme-standards:end project-links -->

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/120-tests/tba-tests-interop-jose)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-interop-jose/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-interop-jose/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-interop-jose/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-tests-interop-jose/)

---

## Contributing

### How to Contribute

Follow the [contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md) and include a focused example or regression for changes to `tba-tests-interop-jose`. Keep package behavior, its documented boundary, and its tests aligned.

### Development Setup

Work from the `pkgs/120-tests/tba-tests-interop-jose` checkout. Synchronize its declared development environment with uv, then run the relevant package tests and `python -m pytest docs/readme/test_examples.py`. The repository’s dedicated README job installs `readme-standards==0.1.1` without resolving unrelated runtime packages.

### Notes for Maintainers

Edit authored prose directly in this `tba-tests-interop-jose` README. Update source examples in `docs/readme/`, then run `readme-standards render --root . --write` from the package directory and review the diff. Required headings and generated blocks come from package-guide-v1.

---

## Governance

### Ownership and Decision Making

Changes to `tba-tests-interop-jose` follow the maintainer review process of [tigrbl/tigrbl_auth](https://github.com/tigrbl/tigrbl_auth) and its contribution guide. Author attribution remains in the [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-interop-jose/pyproject.toml); this README does not assign new publishing or administrative authority.

### Standards and Policies

`tba-tests-interop-jose` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `120-tests` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

### Lifecycle and Migration

The `tba-tests-interop-jose` source version is `0.1.0`. This change standardizes documentation and adds a development-only gate; it does not publish a new runtime version or declare a previously unpublished package released. Preserve explicit deprecation and replacement instructions where present.

---

## License and Attribution

### License

<!-- readme-standards:begin license -->
Licensed under `Apache-2.0`. See [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-interop-jose/LICENSE).
<!-- readme-standards:end license -->

### Notices

<!-- readme-standards:begin notices -->
See [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-interop-jose/NOTICE) for attribution.
<!-- readme-standards:end notices -->
