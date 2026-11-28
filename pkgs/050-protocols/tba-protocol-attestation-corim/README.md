# tba-protocol-attestation-corim

<!-- readme-standards:begin branding -->
<p align="center"><a href="https://github.com/tigrbl/tigrbl_auth"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="300"></a></p>
<p align="center"><strong>tba-protocol-attestation-corim</strong></p>
<p align="center">Versioned CoRIM-family protocol profile and capability mapping.</p>
<p align="center">
<a href="https://pypi.org/project/tba-protocol-attestation-corim/"><img alt="pypi: tba-protocol-attestation-corim" src="https://img.shields.io/pypi/v/tba-protocol-attestation-corim?labelColor=1E293B&amp;color=1D4ED8"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-attestation-corim/pyproject.toml"><img alt="Source version: 0.4.0.dev3" src="https://img.shields.io/static/v1?label=Source%20version&amp;message=0.4.0.dev3&amp;labelColor=1E293B&amp;color=4338CA"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-attestation-corim/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/static/v1?label=Python&amp;message=%3E%3D3.10%2C%3C3.16&amp;labelColor=1E293B&amp;color=0F766E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-attestation-corim/pyproject.toml"><img alt="Layer: 050-protocols" src="https://img.shields.io/static/v1?label=Layer&amp;message=050-protocols&amp;labelColor=1E293B&amp;color=6D28D9"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-attestation-corim/README.md#lifecycle-and-migration"><img alt="Lifecycle: active" src="https://img.shields.io/static/v1?label=Lifecycle&amp;message=active&amp;labelColor=1E293B&amp;color=166534"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-attestation-corim/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/static/v1?label=License&amp;message=Apache-2.0&amp;labelColor=1E293B&amp;color=86198F"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-attestation-corim/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/static/v1?label=Notice&amp;message=attribution&amp;labelColor=1E293B&amp;color=86198F"></a>
</p>
<p align="center">
<a href="https://pypi.org/project/tba-protocol-attestation-corim/"><img alt="Monthly PyPI downloads: tba-protocol-attestation-corim" src="https://img.shields.io/pypi/dm/tba-protocol-attestation-corim?labelColor=1E293B&amp;color=0E7490"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-attestation-corim/README.md"><img alt="README hits: tba-protocol-attestation-corim" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/pkgs/050-protocols/tba-protocol-attestation-corim/README.md.svg?label=README%20hits&amp;labelColor=1E293B&amp;color=0E7490"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="README standards: CI gate" src="https://img.shields.io/static/v1?label=README%20standards&amp;message=CI%20gate&amp;labelColor=1E293B&amp;color=1D4ED8"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-attestation-corim/docs/readme/test_examples.py"><img alt="Tests: example source" src="https://img.shields.io/static/v1?label=Tests&amp;message=example%20source&amp;labelColor=1E293B&amp;color=0F766E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-attestation-corim/README.md#certification-status"><img alt="Certification: not certified" src="https://img.shields.io/static/v1?label=Certification&amp;message=not%20certified&amp;labelColor=1E293B&amp;color=92400E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/tools/readme/POLICY.md"><img alt="Governance: repository policy" src="https://img.shields.io/static/v1?label=Governance&amp;message=repository%20policy&amp;labelColor=1E293B&amp;color=4338CA"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="Evidence: source and CI" src="https://img.shields.io/static/v1?label=Evidence&amp;message=source%20and%20CI&amp;labelColor=1E293B&amp;color=6D28D9"></a>
</p>
<p align="center"><a href="#overview">Overview</a> · <a href="#installation">Installation</a> · <a href="#quick-start">Quick Start</a> · <a href="#usage">Usage</a> · <a href="#public-api-and-import-surfaces">API</a> · <a href="#contributing">Contributing</a> · <a href="#governance">Governance</a> · <a href="#license">License</a></p>
<!-- readme-standards:end branding -->

---

## Overview

### Summary

Owns CoRIM-family revision history, version feature gates, compatibility,
migration guidance, and mappings to normalized attestation capabilities. It
does not own trust selection, appraisal policy, persistence, or key loading.

- Package: `tba-protocol-attestation-corim`
- Layer: `050-protocols`
- Responsibility: Versioned CoRIM-family protocol profile and capability mapping.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-attestation-corim/src/tba_protocol_attestation_corim/__init__.py).
- Distribution: Python package on PyPI.

### Why This Package

`tba-protocol-attestation-corim` isolates this responsibility: Versioned CoRIM-family protocol profile and capability mapping. Its [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-attestation-corim/src/tba_protocol_attestation_corim/__init__.py) exposes `CAPABILITY_REQUIREMENTS`, `COMPATIBILITY_PATHS`, `CORIM_CARRIERS`, `CORIM_CLAIM_CLASSES`, `CORIM_MAP_FIELDS`, `CORIM_SIGNED_CARRIER`, `CORIM_UNSIGNED_CARRIER`, `CURRENT_VERSION`, `CorimCarrier`, `CorimCompatibility`, `CorimProtocolError`, `CorimReferenceIntegrityError`, `CorimVersion`, `FEATURES_BY_VERSION`, `UnsupportedCorimMediaTypeError`, allowing consumers to select this package without treating adjacent packages as part of its public contract.

### When to Use

Choose `tba-protocol-attestation-corim` for this responsibility: Versioned CoRIM-family protocol profile and capability mapping. Its `050-protocols` placement keeps protocol semantics and projections separate from deployment hosting or ownership of persistence implementations.

### Features

- `CorimCompatibility`: declared in src/tba_protocol_attestation_corim/compatibility.py
- `CorimProtocolError`: Base error for a selected CoRIM draft mapping.
- `UnsupportedCorimMediaTypeError`: Raised when no selected signed/unsigned CoRIM carrier applies.
- `CorimReferenceIntegrityError`: Raised when reference material fails integrity/profile validation.
- `CorimCarrier`: declared in src/tba_protocol_attestation_corim/schemas.py
- `CorimVersion`: declared in src/tba_protocol_attestation_corim/versions.py

### Non-Goals

`tba-protocol-attestation-corim` does not take ownership of deployment hosting or ownership of persistence implementations.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

---

## Getting Started

### Prerequisites

Python `>=3.10,<3.16` is required. The [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-attestation-corim/pyproject.toml) declares runtime dependencies including `tba-concrete-corim`, `tba-contracts-identity`. Read the example’s inputs and service requirements before execution.

### Installation

Install the selected PyPI release of `tba-protocol-attestation-corim`:

```bash
uv pip install tba-protocol-attestation-corim
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/050-protocols/tba-protocol-attestation-corim
```

#### uv

<!-- readme-standards:begin installation.uv -->
```bash
uv add tba-protocol-attestation-corim
```
<!-- readme-standards:end installation.uv -->

#### pip

<!-- readme-standards:begin installation.pip -->
```bash
python -m pip install tba-protocol-attestation-corim
```
<!-- readme-standards:end installation.pip -->

#### Poetry

<!-- readme-standards:begin installation.poetry -->
```bash
poetry add tba-protocol-attestation-corim
```
<!-- readme-standards:end installation.poetry -->

### Quick Start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.


```bash
uv run --isolated --no-project --python 3.12 --with "tba-protocol-attestation-corim==0.4.0.dev3" python quickstart.py
```

The command prints the keys in the package's capability report.

#### Example

<!-- readme-standards:begin example.quick-start -->
Source: [docs/readme/quick_start.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-attestation-corim/docs/readme/quick_start.py).

```python
from tba_protocol_attestation_corim import capability_report

report = capability_report()
assert report
print(sorted(report))
```
<!-- readme-standards:end example.quick-start -->

#### Expected Result

The example demonstrates the documented `tba-protocol-attestation-corim` source boundary or workflow. Complete its required configuration first. README CI checks the maintained source’s syntax and declarations; it does not claim that external services or the application workflow were exercised.

---

## Usage

### Common Workflows

<!-- readme-standards:begin example.usage -->
Source: [docs/readme/usage.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-attestation-corim/docs/readme/usage.py).

```python
from tba_protocol_attestation_corim import capability_report

report = capability_report()
assert report
print(sorted(report))
```
<!-- readme-standards:end example.usage -->

The following public-entry-point example belongs to `tba-protocol-attestation-corim`. Versioned CoRIM-family protocol profile and capability mapping. Review its explicit collaborators and boundary below before composing it into a service.

### Configuration

Configure `tba-protocol-attestation-corim` through the APIs in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-attestation-corim/src/tba_protocol_attestation_corim/__init__.py); its [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-attestation-corim/pyproject.toml) describes installation requirements, not an implicit service configuration. No additional package-global configuration contract is inferred from dependencies.

### Error Handling

The inspected `tba-protocol-attestation-corim` source raises `UnsupportedCorimMediaTypeError`, `ValueError`. Handle these at the calling boundary and consult the implementation for the triggering conditions.

### Best Practices

Use the explicit `tba-protocol-attestation-corim` imports documented below and keep collaborator configuration with the caller. Run the package’s relevant tests after changing `CAPABILITY_REQUIREMENTS`, `COMPATIBILITY_PATHS`, `CORIM_CARRIERS`, `CORIM_CLAIM_CLASSES`, `CORIM_MAP_FIELDS`, `CORIM_SIGNED_CARRIER`, `CORIM_UNSIGNED_CARRIER`, `CURRENT_VERSION`, `CorimCarrier`, `CorimCompatibility`, `CorimProtocolError`, `CorimReferenceIntegrityError`, `CorimVersion`, `FEATURES_BY_VERSION`, `UnsupportedCorimMediaTypeError`; an import or successful installation alone does not establish its runtime guarantees.

---

## Package Boundary

### What It Owns

`tba-protocol-attestation-corim` belongs to `050-protocols` and owns protocol semantics and projections: Versioned CoRIM-family protocol profile and capability mapping.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-attestation-corim/src/tba_protocol_attestation_corim/__init__.py). Public exports include `CAPABILITY_REQUIREMENTS`, `COMPATIBILITY_PATHS`, `CORIM_CARRIERS`, `CORIM_CLAIM_CLASSES`, `CORIM_MAP_FIELDS`, `CORIM_SIGNED_CARRIER`, `CORIM_UNSIGNED_CARRIER`, `CURRENT_VERSION`, `FEATURES_BY_VERSION`, `VERSION_HISTORY`, `CorimCarrier`, `CorimCompatibility`.

Keep deployment hosting or ownership of persistence implementations in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

### Public API and Import Surfaces

Import namespace: `tba_protocol_attestation_corim`.

Source-declared exports or types: `CAPABILITY_REQUIREMENTS`, `COMPATIBILITY_PATHS`, `CORIM_CARRIERS`, `CORIM_CLAIM_CLASSES`, `CORIM_MAP_FIELDS`, `CORIM_SIGNED_CARRIER`, `CORIM_UNSIGNED_CARRIER`, `CURRENT_VERSION`, `CorimCarrier`, `CorimCompatibility`, `CorimProtocolError`, `CorimReferenceIntegrityError`, `CorimVersion`, `FEATURES_BY_VERSION`, `UnsupportedCorimMediaTypeError`.

Inspect [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-attestation-corim/src/tba_protocol_attestation_corim/__init__.py) for exact signatures; this inventory does not designate every internal module as stable.

### Entry Points

<!-- readme-standards:begin entry-points -->
This package declares no command-line, GUI, or plugin entry points in its manifest.
<!-- readme-standards:end entry-points -->

### Injected Dependencies

Explicit construction inputs and collaborators for `tba-protocol-attestation-corim`:

- `migrate_document` construction inputs: `from_version`, `to_version`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-attestation-corim/src/tba_protocol_attestation_corim/migrations.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

### Protocol Consumers

Direct consumers in this checkout’s package manifests include `tba-workspace`. These edges describe declared dependencies, not protocol-conformance evidence.

### Extensions

For `tba-protocol-attestation-corim`, use the source-declared public interfaces (`CAPABILITY_REQUIREMENTS`, `COMPATIBILITY_PATHS`, `CORIM_CARRIERS`, `CORIM_CLAIM_CLASSES`, `CORIM_MAP_FIELDS`, `CORIM_SIGNED_CARRIER`, `CORIM_UNSIGNED_CARRIER`, `CURRENT_VERSION`, `CorimCarrier`, `CorimCompatibility`, `CorimProtocolError`, `CorimReferenceIntegrityError`, `CorimVersion`, `FEATURES_BY_VERSION`, `UnsupportedCorimMediaTypeError`) when composing or extending behavior. Its entry-point section below is authoritative for registered plugins; no additional extension loader is inferred from the package name.

---

## Operations and Readiness

### Operational Requirements

`tba-protocol-attestation-corim` exposes protocol semantics and projections. Public operations found in its source:

- `capability_report` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-attestation-corim/src/tba_protocol_attestation_corim/__init__.py).
- `compatibility` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-attestation-corim/src/tba_protocol_attestation_corim/compatibility.py).
- `supports` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-attestation-corim/src/tba_protocol_attestation_corim/features.py).
- `migrate_document` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-attestation-corim/src/tba_protocol_attestation_corim/migrations.py).
- `select_carrier` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-attestation-corim/src/tba_protocol_attestation_corim/schemas.py).
- `select_version` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-attestation-corim/src/tba_protocol_attestation_corim/versions.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

### Health and Observability

This README does not establish a standalone health endpoint for `tba-protocol-attestation-corim`. Observe the concrete caller’s results, exceptions, and existing test reports. An application that embeds this package must define its own health and telemetry contract.

### Security and Resource Limits

Apply the input, credential, and resource constraints implemented in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-attestation-corim/src/tba_protocol_attestation_corim/__init__.py). The `tba-protocol-attestation-corim` README gate is a documentation check, not a security review or a substitute for the implementation’s limits and caller authorization.

### Compatibility

This source version of `tba-protocol-attestation-corim` declares Python `>=3.10,<3.16`. Consult its dependency constraints before upgrading. Source-version and registry-version badges have separate meanings; this migration makes no additional platform or interoperability certification claim.

---

## Verification

### Tests

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-attestation-corim/src/tba_protocol_attestation_corim/__init__.py).

### Certification Status

No external certification is asserted for `tba-protocol-attestation-corim` by this documentation migration. README conformance, example syntax, runtime tests, and protocol or security certification are distinct evidence scopes.

### Evidence

The [README standards CI](https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml) records mechanical documentation results for its tested commit. The [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-attestation-corim/src/tba_protocol_attestation_corim/__init__.py) and example sources support the package-boundary description; external runtime behavior requires its own test evidence.

---

## FAQ

### Why

**Why select this package?** `tba-protocol-attestation-corim` provides versioned CoRIM-family protocol profile and capability mapping; use its own API boundary rather than assuming neighboring packages are bundled or configured automatically.

### How

**How do I start?** Install or synchronize the environment under Getting Started, follow the maintained example for `tba-protocol-attestation-corim`, and consult [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-attestation-corim/src/tba_protocol_attestation_corim/__init__.py) for the exact types and signatures involved.

### When

**When should I validate an upgrade?** Recheck `tba-protocol-attestation-corim` whenever its source version, declared collaborators, configuration, or caller changes. Run relevant behavioral tests in addition to the README gate before promotion.

---

## Documentation and Related Packages

### More Documentation

The [repository contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md), [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-attestation-corim/src/tba_protocol_attestation_corim/__init__.py), and [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-attestation-corim/pyproject.toml) provide the supporting context for `tba-protocol-attestation-corim`. The [README policy](https://github.com/groupsum/readme-standards/blob/master/docs/outline.md) defines the common document structure.

### Related Packages

Declared local runtime dependencies:

- [tba-concrete-corim](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-corim/README.md)
- [tba-contracts-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-identity/README.md)

### Project Links

<!-- readme-standards:begin project-links -->
- [Documentation](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/050-protocols/tba-protocol-attestation-corim#readme)
- [Homepage](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/050-protocols/tba-protocol-attestation-corim#readme)
- [Issues](https://github.com/tigrbl/tigrbl_auth/issues)
- [PyPI](https://pypi.org/project/tba-protocol-attestation-corim/)
- [Repository](https://github.com/tigrbl/tigrbl_auth)
- [Source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/050-protocols/tba-protocol-attestation-corim)
- [pypi: tba-protocol-attestation-corim](https://pypi.org/project/tba-protocol-attestation-corim/)
<!-- readme-standards:end project-links -->

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/050-protocols/tba-protocol-attestation-corim)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-attestation-corim/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-attestation-corim/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-attestation-corim/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-protocol-attestation-corim/)

---

## Contributing

### How to Contribute

Follow the [contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md) and include a focused example or regression for changes to `tba-protocol-attestation-corim`. Keep package behavior, its documented boundary, and its tests aligned.

### Development Setup

Work from the `pkgs/050-protocols/tba-protocol-attestation-corim` checkout. Synchronize its declared development environment with uv, then run the relevant package tests and `python -m pytest docs/readme/test_examples.py`. The repository’s dedicated README job installs `readme-standards==0.1.3` without resolving unrelated runtime packages.

### Notes for Maintainers

Edit authored prose directly in this `tba-protocol-attestation-corim` README. Update source examples in `docs/readme/`, then run `readme-standards render --root . --write` from the package directory and review the diff. Required headings and generated blocks come from package-guide-v1.

---

## Governance

### Ownership and Decision Making

Changes to `tba-protocol-attestation-corim` follow the maintainer review process of [tigrbl/tigrbl_auth](https://github.com/tigrbl/tigrbl_auth) and its contribution guide. Author attribution remains in the [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-attestation-corim/pyproject.toml); this README does not assign new publishing or administrative authority.

### Standards and Policies

`tba-protocol-attestation-corim` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `050-protocols` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

### Lifecycle and Migration

The `tba-protocol-attestation-corim` source version is `0.4.0.dev3`. This change standardizes documentation and adds a development-only gate; it does not publish a new runtime version or declare a previously unpublished package released. Preserve explicit deprecation and replacement instructions where present.

---

## License and Attribution

### License

<!-- readme-standards:begin license -->
Licensed under `Apache-2.0`. See [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-attestation-corim/LICENSE).
<!-- readme-standards:end license -->

### Notices

<!-- readme-standards:begin notices -->
See [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-attestation-corim/NOTICE) for attribution.
<!-- readme-standards:end notices -->
