# tba-storage-core

<!-- readme-standards:begin branding -->
<p align="center"><a href="https://github.com/tigrbl/tigrbl_auth"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="300"></a></p>
<p align="center"><strong>tba-storage-core</strong></p>
<p align="center">Tigrbl and SQLAlchemy identity tables, ORM models, migrations, persistence helpers, and table-owned operations for IAM runtimes.</p>
<p align="center">
<a href="https://pypi.org/project/tba-storage-core/"><img alt="pypi: tba-storage-core" src="https://img.shields.io/pypi/v/tba-storage-core"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-core/pyproject.toml"><img alt="Source version: 0.4.0.dev5" src="https://img.shields.io/static/v1?label=Source%20version&amp;message=0.4.0.dev5&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-core/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/static/v1?label=Python&amp;message=%3E%3D3.10%2C%3C3.16&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-core/pyproject.toml"><img alt="Layer: 001-storage" src="https://img.shields.io/static/v1?label=Layer&amp;message=001-storage&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-core/README.md#lifecycle-and-migration"><img alt="Lifecycle: active" src="https://img.shields.io/static/v1?label=Lifecycle&amp;message=active&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-core/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/static/v1?label=License&amp;message=Apache-2.0&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-core/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/static/v1?label=Notice&amp;message=attribution&amp;color=525252"></a>
</p>
<p align="center">
<a href="https://pypi.org/project/tba-storage-core/"><img alt="Monthly PyPI downloads: tba-storage-core" src="https://img.shields.io/pypi/dm/tba-storage-core"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-core/README.md"><img alt="README hits: tba-storage-core" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/pkgs/001-storage/tba-storage-core/README.md.svg?label=README%20hits"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="README standards: CI gate" src="https://img.shields.io/static/v1?label=README%20standards&amp;message=CI%20gate&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-core/docs/readme/test_examples.py"><img alt="Tests: example source" src="https://img.shields.io/static/v1?label=Tests&amp;message=example%20source&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-core/README.md#certification-status"><img alt="Certification: not certified" src="https://img.shields.io/static/v1?label=Certification&amp;message=not%20certified&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/tools/readme/POLICY.md"><img alt="Governance: repository policy" src="https://img.shields.io/static/v1?label=Governance&amp;message=repository%20policy&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="Evidence: source and CI" src="https://img.shields.io/static/v1?label=Evidence&amp;message=source%20and%20CI&amp;color=525252"></a>
</p>
<p align="center"><a href="#overview">Overview</a> · <a href="#installation">Installation</a> · <a href="#quick-start">Quick Start</a> · <a href="#usage">Usage</a> · <a href="#public-api-and-import-surfaces">API</a> · <a href="#contributing">Contributing</a> · <a href="#governance">Governance</a> · <a href="#license">License</a></p>
<!-- readme-standards:end branding -->

---

## Overview

### Summary

Inspect the packaged identity storage migration history and access compatibility imports for domain tables.

- Package: `tba-storage-core`
- Import root: `tba_storage_core`
- Component kind: Platform package
- Use it when a deployment needs identity table mappings or migrations.
- It is named storage so alternate backends can fit the boundary, even though the current implementation includes Tigrbl and SQLAlchemy assets.
- It should not own OAuth, OIDC, admin policy, or ASGI runtime behavior.

### Why This Package

`tba-storage-core` isolates this responsibility: Tigrbl and SQLAlchemy identity tables, ORM models, migrations, persistence helpers, and table-owned operations for IAM runtimes. Its [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-core/src/tba_storage_core/__init__.py) exposes `MigrationContract`, `MigrationRevision`, `build_migration_contract`, `collect_migration_revisions`, `ensure_identity_storage_importable`, allowing consumers to select this package without treating adjacent packages as part of its public contract.

### When to Use

Use this package for the shared migration history and compatibility imports. The domain storage packages own mapped tables, and layer 30 owns executable persistence operations.

### Features

- `MigrationRevision`: declared in src/tba_storage_core/migrations/contract.py
- `MigrationContract`: declared in src/tba_storage_core/migrations/contract.py
- `SupportsTable`: declared in src/tba_storage_core/migrations/helpers.py

### Non-Goals

`tba-storage-core` does not take ownership of protocol endpoints or deployment-specific provider selection.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

---

## Getting Started

### Prerequisites

Python `>=3.10,<3.16` is required. The [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-core/pyproject.toml) declares runtime dependencies including `tigrbl`, `tigrbl-core`, `tba-primitives-identity`, `tba-contracts-security-trust`, `tigrbl-migrations`, `tba-storage-access-governance`, `tba-storage-attestation`, `tba-storage-audit`, `tba-storage-authentication`, `tba-storage-authority-graph`, `tba-storage-authorization-policy`, `tba-storage-certificate`. Read the example’s inputs and service requirements before execution.

### Installation

Install the selected PyPI release of `tba-storage-core`:

```bash
uv pip install tba-storage-core
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/001-storage/tba-storage-core
```

#### uv

<!-- readme-standards:begin installation.uv -->
```bash
uv add tba-storage-core
```
<!-- readme-standards:end installation.uv -->

#### pip

<!-- readme-standards:begin installation.pip -->
```bash
python -m pip install tba-storage-core
```
<!-- readme-standards:end installation.pip -->

#### Poetry

<!-- readme-standards:begin installation.poetry -->
```bash
poetry add tba-storage-core
```
<!-- readme-standards:end installation.poetry -->

### Quick Start

Install the version used by this example.

```bash
python -m pip install "tba-storage-core==0.4.0.dev5"
```

Save the following as `quickstart.py` and run `python quickstart.py`. The assertions should pass.

#### Example

<!-- readme-standards:begin example.quick-start -->
Source: [docs/readme/quick_start.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-core/docs/readme/quick_start.py).

```python
from importlib.resources import files
from pathlib import Path

from tba_storage_core import collect_migration_revisions

versions = Path(str(files("tba_storage_core").joinpath("migrations", "versions")))
revisions = collect_migration_revisions(versions)
assert revisions
print(f"{len(revisions)} packaged revisions")
```
<!-- readme-standards:end example.quick-start -->

#### Expected Result

The example demonstrates the documented `tba-storage-core` source boundary or workflow. Complete its required configuration first. README CI checks the maintained source’s syntax and declarations; it does not claim that external services or the application workflow were exercised.

---

## Usage

### Common Workflows

<!-- readme-standards:begin example.usage -->
Source: [docs/readme/usage.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-core/docs/readme/usage.py).

```python
from importlib.resources import files
from pathlib import Path

from tba_storage_core import collect_migration_revisions

versions = Path(str(files("tba_storage_core").joinpath("migrations", "versions")))
revisions = collect_migration_revisions(versions)
assert revisions
print(f"{len(revisions)} packaged revisions")
```
<!-- readme-standards:end example.usage -->

The following public-entry-point example belongs to `tba-storage-core`. Tigrbl and SQLAlchemy identity tables, ORM models, migrations, persistence helpers, and table-owned operations for IAM runtimes. Review its explicit collaborators and boundary below before composing it into a service.

### Configuration

Configure `tba-storage-core` through the APIs in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-core/src/tba_storage_core/__init__.py); its [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-core/pyproject.toml) describes installation requirements, not an implicit service configuration. No additional package-global configuration contract is inferred from dependencies.

### Error Handling

The inspected `tba-storage-core` source raises `RuntimeError`, `ValueError`. Handle these at the calling boundary and consult the implementation for the triggering conditions.

### Best Practices

Use the explicit `tba-storage-core` imports documented below and keep collaborator configuration with the caller. Run the package’s relevant tests after changing `MigrationContract`, `MigrationRevision`, `build_migration_contract`, `collect_migration_revisions`, `ensure_identity_storage_importable`; an import or successful installation alone does not establish its runtime guarantees.

---

## Package Boundary

### What It Owns

- Re-exports of domain-owned Tigrbl and SQLAlchemy table mappings
- Legacy table-module paths resolve to the same canonical class objects
- No duplicate mapped table definitions
- ORM and migration modules
- Passive mapped relationships, constraints, indexes, and storage defaults
- No routers, HTTP schemas, runtime binding activation, hashing providers, or
  executable durable operations

### Public API and Import Surfaces

Import namespace: `tba_storage_core`.

Source-declared exports or types: `MigrationContract`, `MigrationRevision`, `build_migration_contract`, `collect_migration_revisions`, `ensure_identity_storage_importable`.

Inspect [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-core/src/tba_storage_core/__init__.py) for exact signatures; this inventory does not designate every internal module as stable.

### Entry Points

<!-- readme-standards:begin entry-points -->
This package declares no command-line, GUI, or plugin entry points in its manifest.
<!-- readme-standards:end entry-points -->

### Injected Dependencies

Explicit construction inputs and collaborators for `tba-storage-core`:

- `build_migration_contract` construction inputs: `versions_dir`, `required_collections`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-core/src/tba_storage_core/migrations/contract.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

### Protocol Consumers

Direct consumers in this checkout’s package manifests include `tba-runtime-identity-storage`, `tba-runtime-identity`, `tba-auth`, `tba-app-backend-core`, `tba-workspace`. These edges describe declared dependencies, not protocol-conformance evidence.

### Extensions

For `tba-storage-core`, use the source-declared public interfaces (`MigrationContract`, `MigrationRevision`, `build_migration_contract`, `collect_migration_revisions`, `ensure_identity_storage_importable`) when composing or extending behavior. Its entry-point section below is authoritative for registered plugins; no additional extension loader is inferred from the package name.

---

## Operations and Readiness

### Operational Requirements

`tba-storage-core` exposes storage schema and table declarations. Public operations found in its source:

- `ensure_identity_storage_importable` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-core/src/tba_storage_core/__init__.py).
- `MigrationContract.is_ordered` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-core/src/tba_storage_core/migrations/contract.py).
- `MigrationContract.latest_revision` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-core/src/tba_storage_core/migrations/contract.py).
- `MigrationContract.assert_complete` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-core/src/tba_storage_core/migrations/contract.py).
- `collect_migration_revisions` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-core/src/tba_storage_core/migrations/contract.py).
- `build_migration_contract` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-core/src/tba_storage_core/migrations/contract.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

### Health and Observability

This README does not establish a standalone health endpoint for `tba-storage-core`. Observe the concrete caller’s results, exceptions, and existing test reports. An application that embeds this package must define its own health and telemetry contract.

### Security and Resource Limits

Apply the input, credential, and resource constraints implemented in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-core/src/tba_storage_core/__init__.py). The `tba-storage-core` README gate is a documentation check, not a security review or a substitute for the implementation’s limits and caller authorization.

### Compatibility

This source version of `tba-storage-core` declares Python `>=3.10,<3.16`. Consult its dependency constraints before upgrading. Source-version and registry-version badges have separate meanings; this migration makes no additional platform or interoperability certification claim.

---

## Verification

### Tests

See the [related repository tests](https://github.com/tigrbl/tigrbl_auth/blob/master/tests/unit/test_registry_state_table_ownership.py) for the implementation scope covered by this example.

[Workspace and package catalog](https://github.com/tigrbl/tigrbl_auth#package-catalog) · [tba-durability-replay-protection](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/030-storage-runtime/tba-durability-replay-protection#readme) · [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues) · [Repository license](https://github.com/tigrbl/tigrbl_auth/blob/master/LICENSE)

### Certification Status

No external certification is asserted for `tba-storage-core` by this documentation migration. README conformance, example syntax, runtime tests, and protocol or security certification are distinct evidence scopes.

### Evidence

The [README standards CI](https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml) records mechanical documentation results for its tested commit. The [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-core/src/tba_storage_core/__init__.py) and example sources support the package-boundary description; external runtime behavior requires its own test evidence.

---

## FAQ

### Why

**Why select this package?** `tba-storage-core` provides tigrbl and SQLAlchemy identity tables, ORM models, migrations, persistence helpers, and table-owned operations for IAM runtimes; use its own API boundary rather than assuming neighboring packages are bundled or configured automatically.

### How

**How do I start?** Install or synchronize the environment under Getting Started, follow the maintained example for `tba-storage-core`, and consult [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-core/src/tba_storage_core/__init__.py) for the exact types and signatures involved.

### When

**When should I validate an upgrade?** Recheck `tba-storage-core` whenever its source version, declared collaborators, configuration, or caller changes. Run relevant behavioral tests in addition to the README gate before promotion.

---

## Documentation and Related Packages

### More Documentation

The [repository contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md), [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-core/src/tba_storage_core/__init__.py), and [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-core/pyproject.toml) provide the supporting context for `tba-storage-core`. The [README policy](https://github.com/groupsum/readme-standards/blob/master/docs/outline.md) defines the common document structure.

### Related Packages

- [tba-runtime-identity-administration](https://pypi.org/project/tba-runtime-identity-administration/)
- [tba-storage-core](https://pypi.org/project/tba-storage-core/)
- [tba-server-identity](https://pypi.org/project/tba-server-identity/)
- [tba-runtime-identity](https://pypi.org/project/tba-runtime-identity/)
- [tba-operator-identity](https://pypi.org/project/tba-operator-identity/)
- [tba-testkit-identity](https://pypi.org/project/tba-testkit-identity/)

### Project Links

<!-- readme-standards:begin project-links -->
- [Documentation](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/001-storage/tba-storage-core#readme)
- [Homepage](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/001-storage/tba-storage-core#readme)
- [Issues](https://github.com/tigrbl/tigrbl_auth/issues)
- [PyPI](https://pypi.org/project/tba-storage-core/)
- [Repository](https://github.com/tigrbl/tigrbl_auth)
- [SSOT](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [Source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/001-storage/tba-storage-core)
- [pypi: tba-storage-core](https://pypi.org/project/tba-storage-core/)
<!-- readme-standards:end project-links -->

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/001-storage/tba-storage-core)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-core/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-core/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-core/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-storage-core/)

---

## Contributing

### How to Contribute

Follow the [contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md) and include a focused example or regression for changes to `tba-storage-core`. Keep package behavior, its documented boundary, and its tests aligned.

### Development Setup

Work from the `pkgs/001-storage/tba-storage-core` checkout. Synchronize its declared development environment with uv, then run the relevant package tests and `python -m pytest docs/readme/test_examples.py`. The repository’s dedicated README job installs `readme-standards==0.1.1` without resolving unrelated runtime packages.

### Notes for Maintainers

Edit authored prose directly in this `tba-storage-core` README. Update source examples in `docs/readme/`, then run `readme-standards render --root . --write` from the package directory and review the diff. Required headings and generated blocks come from package-guide-v1.

---

## Governance

### Ownership and Decision Making

Changes to `tba-storage-core` follow the maintainer review process of [tigrbl/tigrbl_auth](https://github.com/tigrbl/tigrbl_auth) and its contribution guide. Author attribution remains in the [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-core/pyproject.toml); this README does not assign new publishing or administrative authority.

### Standards and Policies

This package is part of the SSOT-governed TBA identity package suite. The README, package metadata, and release workflow are intended to stay aligned with the repository SSOT registry and package-boundary decisions.

`tba-storage-core` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `001-storage` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

### Lifecycle and Migration

The `tba-storage-core` source version is `0.4.0.dev5`. This change standardizes documentation and adds a development-only gate; it does not publish a new runtime version or declare a previously unpublished package released. Preserve explicit deprecation and replacement instructions where present.

---

## License and Attribution

### License

<!-- readme-standards:begin license -->
Licensed under `Apache-2.0`. See [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-core/LICENSE).
<!-- readme-standards:end license -->

### Notices

<!-- readme-standards:begin notices -->
See [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-core/NOTICE) for attribution.
<!-- readme-standards:end notices -->
