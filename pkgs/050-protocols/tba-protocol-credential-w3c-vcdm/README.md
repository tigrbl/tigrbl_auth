# tba-protocol-credential-w3c-vcdm

<!-- readme-standards:begin branding -->
<p align="center"><a href="https://github.com/tigrbl/tigrbl_auth"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="300"></a></p>
<p align="center"><strong>tba-protocol-credential-w3c-vcdm</strong></p>
<p align="center">Version authority, feature selection, compatibility, migration, and semantic object mapping for W3C Verifiable Credentials Data Model revisions.</p>
<p align="center">
<a href="https://pypi.org/project/tba-protocol-credential-w3c-vcdm/"><img alt="pypi: tba-protocol-credential-w3c-vcdm" src="https://img.shields.io/pypi/v/tba-protocol-credential-w3c-vcdm?labelColor=1E293B&amp;color=1D4ED8"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-credential-w3c-vcdm/pyproject.toml"><img alt="Source version: 0.4.0.dev3" src="https://img.shields.io/static/v1?label=Source%20version&amp;message=0.4.0.dev3&amp;labelColor=1E293B&amp;color=4338CA"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-credential-w3c-vcdm/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/static/v1?label=Python&amp;message=%3E%3D3.10%2C%3C3.16&amp;labelColor=1E293B&amp;color=0F766E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-credential-w3c-vcdm/pyproject.toml"><img alt="Layer: 050-protocols" src="https://img.shields.io/static/v1?label=Layer&amp;message=050-protocols&amp;labelColor=1E293B&amp;color=6D28D9"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-credential-w3c-vcdm/README.md#lifecycle-and-migration"><img alt="Lifecycle: active" src="https://img.shields.io/static/v1?label=Lifecycle&amp;message=active&amp;labelColor=1E293B&amp;color=166534"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-credential-w3c-vcdm/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/static/v1?label=License&amp;message=Apache-2.0&amp;labelColor=1E293B&amp;color=86198F"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-credential-w3c-vcdm/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/static/v1?label=Notice&amp;message=attribution&amp;labelColor=1E293B&amp;color=86198F"></a>
</p>
<p align="center">
<a href="https://pypi.org/project/tba-protocol-credential-w3c-vcdm/"><img alt="Monthly PyPI downloads: tba-protocol-credential-w3c-vcdm" src="https://img.shields.io/pypi/dm/tba-protocol-credential-w3c-vcdm?labelColor=1E293B&amp;color=0E7490"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-credential-w3c-vcdm/README.md"><img alt="README hits: tba-protocol-credential-w3c-vcdm" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/pkgs/050-protocols/tba-protocol-credential-w3c-vcdm/README.md.svg?label=README%20hits&amp;labelColor=1E293B&amp;color=0E7490"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="README standards: CI gate" src="https://img.shields.io/static/v1?label=README%20standards&amp;message=CI%20gate&amp;labelColor=1E293B&amp;color=1D4ED8"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-credential-w3c-vcdm/docs/readme/test_examples.py"><img alt="Tests: example source" src="https://img.shields.io/static/v1?label=Tests&amp;message=example%20source&amp;labelColor=1E293B&amp;color=0F766E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-credential-w3c-vcdm/README.md#certification-status"><img alt="Certification: not certified" src="https://img.shields.io/static/v1?label=Certification&amp;message=not%20certified&amp;labelColor=1E293B&amp;color=92400E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/tools/readme/POLICY.md"><img alt="Governance: repository policy" src="https://img.shields.io/static/v1?label=Governance&amp;message=repository%20policy&amp;labelColor=1E293B&amp;color=4338CA"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="Evidence: source and CI" src="https://img.shields.io/static/v1?label=Evidence&amp;message=source%20and%20CI&amp;labelColor=1E293B&amp;color=6D28D9"></a>
</p>
<p align="center"><a href="#overview">Overview</a> · <a href="#installation">Installation</a> · <a href="#quick-start">Quick Start</a> · <a href="#usage">Usage</a> · <a href="#public-api-and-import-surfaces">API</a> · <a href="#contributing">Contributing</a> · <a href="#governance">Governance</a> · <a href="#license">License</a></p>
<!-- readme-standards:end branding -->

---

## Overview

### Summary

Version authority, feature selection, compatibility, migration, and semantic
object mapping for W3C Verifiable Credentials Data Model revisions.

- Package: `tba-protocol-credential-w3c-vcdm`
- Layer: `050-protocols`
- Responsibility: Version authority, feature selection, compatibility, migration, and semantic object mapping for W3C Verifiable Credentials Data Model revisions.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-credential-w3c-vcdm/src/tba_protocol_credential_w3c_vcdm/__init__.py).
- Distribution: Python package on PyPI.

### Why This Package

`tba-protocol-credential-w3c-vcdm` isolates this responsibility: Version authority, feature selection, compatibility, migration, and semantic object mapping for W3C Verifiable Credentials Data Model revisions. Its [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-credential-w3c-vcdm/src/tba_protocol_credential_w3c_vcdm/bindings.py) exposes `CAPABILITY_REQUIREMENTS`, `CURRENT_VERSION`, `CredentialSchemaReference`, `CredentialStatusEntry`, `FEATURES_BY_VERSION`, `VCDM_2_RECOMMENDATION`, `VC_CONTEXT_V2`, `VERSION_HISTORY`, `VcdmCompatibility`, `VcdmProtocolError`, `VcdmVersion`, `VerifiableCredential`, `VerifiablePresentation`, `compatibility`, `credential_subject_claims`, allowing consumers to select this package without treating adjacent packages as part of its public contract.

### When to Use

Choose `tba-protocol-credential-w3c-vcdm` for this responsibility: Version authority, feature selection, compatibility, migration, and semantic object mapping for W3C Verifiable Credentials Data Model revisions. Its `050-protocols` placement keeps protocol semantics and projections separate from deployment hosting or ownership of persistence implementations.

### Features

- `VcdmCompatibility`: declared in src/tba_protocol_credential_w3c_vcdm/compatibility.py
- `VcdmProtocolError`: Raised when a VCDM document violates the selected recommendation.
- `CredentialSchemaReference`: declared in src/tba_protocol_credential_w3c_vcdm/schema_references.py
- `CredentialStatusEntry`: declared in src/tba_protocol_credential_w3c_vcdm/status.py
- `VcdmVersion`: declared in src/tba_protocol_credential_w3c_vcdm/versions.py

### Non-Goals

`tba-protocol-credential-w3c-vcdm` does not take ownership of deployment hosting or ownership of persistence implementations.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

---

## Getting Started

### Prerequisites

Python `>=3.10,<3.16` is required. The [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-credential-w3c-vcdm/pyproject.toml) declares runtime dependencies including `tba-primitives-identity`, `tba-concrete-verifiable-credential`, `tba-concrete-verifiable-presentation`. Read the example’s inputs and service requirements before execution.

### Installation

Install the selected PyPI release of `tba-protocol-credential-w3c-vcdm`:

```bash
uv pip install tba-protocol-credential-w3c-vcdm
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/050-protocols/tba-protocol-credential-w3c-vcdm
```

#### uv

<!-- readme-standards:begin installation.uv -->
```bash
uv add tba-protocol-credential-w3c-vcdm
```
<!-- readme-standards:end installation.uv -->

#### pip

<!-- readme-standards:begin installation.pip -->
```bash
python -m pip install tba-protocol-credential-w3c-vcdm
```
<!-- readme-standards:end installation.pip -->

#### Poetry

<!-- readme-standards:begin installation.poetry -->
```bash
poetry add tba-protocol-credential-w3c-vcdm
```
<!-- readme-standards:end installation.poetry -->

### Quick Start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.


```bash
uv run --isolated --no-project --python 3.12 --with "tba-protocol-credential-w3c-vcdm==0.4.0.dev3" python quickstart.py
```

The command prints the declared current revision.

#### Example

<!-- readme-standards:begin example.quick-start -->
Source: [docs/readme/quick_start.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-credential-w3c-vcdm/docs/readme/quick_start.py).

```python
from tba_protocol_credential_w3c_vcdm import CURRENT_VERSION

assert CURRENT_VERSION is not None
print(CURRENT_VERSION)
```
<!-- readme-standards:end example.quick-start -->

#### Expected Result

The example demonstrates the documented `tba-protocol-credential-w3c-vcdm` source boundary or workflow. Complete its required configuration first. README CI checks the maintained source’s syntax and declarations; it does not claim that external services or the application workflow were exercised.

---

## Usage

### Common Workflows

<!-- readme-standards:begin example.usage -->
Source: [docs/readme/usage.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-credential-w3c-vcdm/docs/readme/usage.py).

```python
from tba_protocol_credential_w3c_vcdm import CURRENT_VERSION

assert CURRENT_VERSION is not None
print(CURRENT_VERSION)
```
<!-- readme-standards:end example.usage -->

The following public-entry-point example belongs to `tba-protocol-credential-w3c-vcdm`. Version authority, feature selection, compatibility, migration, and semantic object mapping for W3C Verifiable Credentials Data Model revisions. Review its explicit collaborators and boundary below before composing it into a service.

### Configuration

Configure `tba-protocol-credential-w3c-vcdm` through the APIs in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-credential-w3c-vcdm/src/tba_protocol_credential_w3c_vcdm/bindings.py); its [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-credential-w3c-vcdm/pyproject.toml) describes installation requirements, not an implicit service configuration. No additional package-global configuration contract is inferred from dependencies.

### Error Handling

The inspected `tba-protocol-credential-w3c-vcdm` source raises `ValueError`. Handle these at the calling boundary and consult the implementation for the triggering conditions.

### Best Practices

Use the explicit `tba-protocol-credential-w3c-vcdm` imports documented below and keep collaborator configuration with the caller. Run the package’s relevant tests after changing `CAPABILITY_REQUIREMENTS`, `CURRENT_VERSION`, `CredentialSchemaReference`, `CredentialStatusEntry`, `FEATURES_BY_VERSION`, `VCDM_2_RECOMMENDATION`, `VC_CONTEXT_V2`, `VERSION_HISTORY`, `VcdmCompatibility`, `VcdmProtocolError`, `VcdmVersion`, `VerifiableCredential`, `VerifiablePresentation`, `compatibility`, `credential_subject_claims`; an import or successful installation alone does not establish its runtime guarantees.

---

## Package Boundary

### What It Owns

`tba-protocol-credential-w3c-vcdm` belongs to `050-protocols` and owns protocol semantics and projections: Version authority, feature selection, compatibility, migration, and semantic object mapping for W3C Verifiable Credentials Data Model revisions.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-credential-w3c-vcdm/src/tba_protocol_credential_w3c_vcdm/__init__.py). Public exports include `CURRENT_VERSION`, `CAPABILITY_REQUIREMENTS`, `CredentialSchemaReference`, `CredentialStatusEntry`, `FEATURES_BY_VERSION`, `VCDM_2_RECOMMENDATION`, `VC_CONTEXT_V2`, `VERSION_HISTORY`, `VcdmCompatibility`, `VcdmProtocolError`, `VcdmVersion`, `VerifiableCredential`.

Keep deployment hosting or ownership of persistence implementations in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

### Public API and Import Surfaces

Import namespace: `tba_protocol_credential_w3c_vcdm`.

Source-declared exports or types: `CAPABILITY_REQUIREMENTS`, `CURRENT_VERSION`, `CredentialSchemaReference`, `CredentialStatusEntry`, `FEATURES_BY_VERSION`, `VCDM_2_RECOMMENDATION`, `VC_CONTEXT_V2`, `VERSION_HISTORY`, `VcdmCompatibility`, `VcdmProtocolError`, `VcdmVersion`, `VerifiableCredential`, `VerifiablePresentation`, `compatibility`, `credential_subject_claims`.

Inspect [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-credential-w3c-vcdm/src/tba_protocol_credential_w3c_vcdm/bindings.py) for exact signatures; this inventory does not designate every internal module as stable.

### Entry Points

<!-- readme-standards:begin entry-points -->
This package declares no command-line, GUI, or plugin entry points in its manifest.
<!-- readme-standards:end entry-points -->

### Injected Dependencies

Explicit construction inputs and collaborators for `tba-protocol-credential-w3c-vcdm`:

- `migrate_document` construction inputs: `source`, `target`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-credential-w3c-vcdm/src/tba_protocol_credential_w3c_vcdm/migrations.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

### Protocol Consumers

Direct consumers in this checkout’s package manifests include `tba-workspace`. These edges describe declared dependencies, not protocol-conformance evidence.

### Extensions

For `tba-protocol-credential-w3c-vcdm`, use the source-declared public interfaces (`CAPABILITY_REQUIREMENTS`, `CURRENT_VERSION`, `CredentialSchemaReference`, `CredentialStatusEntry`, `FEATURES_BY_VERSION`, `VCDM_2_RECOMMENDATION`, `VC_CONTEXT_V2`, `VERSION_HISTORY`, `VcdmCompatibility`, `VcdmProtocolError`, `VcdmVersion`, `VerifiableCredential`, `VerifiablePresentation`, `compatibility`, `credential_subject_claims`) when composing or extending behavior. Its entry-point section below is authoritative for registered plugins; no additional extension loader is inferred from the package name.

---

## Operations and Readiness

### Operational Requirements

`tba-protocol-credential-w3c-vcdm` exposes protocol semantics and projections. Public operations found in its source:

- `credential_subject_claims` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-credential-w3c-vcdm/src/tba_protocol_credential_w3c_vcdm/claims.py).
- `compatibility` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-credential-w3c-vcdm/src/tba_protocol_credential_w3c_vcdm/compatibility.py).
- `validate_contexts` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-credential-w3c-vcdm/src/tba_protocol_credential_w3c_vcdm/contexts.py).
- `supports` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-credential-w3c-vcdm/src/tba_protocol_credential_w3c_vcdm/features.py).
- `migrate_document` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-credential-w3c-vcdm/src/tba_protocol_credential_w3c_vcdm/migrations.py).
- `parse_credential_schema` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-credential-w3c-vcdm/src/tba_protocol_credential_w3c_vcdm/schema_references.py).
- `parse_verifiable_credential` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-credential-w3c-vcdm/src/tba_protocol_credential_w3c_vcdm/schemas.py).
- `parse_verifiable_presentation` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-credential-w3c-vcdm/src/tba_protocol_credential_w3c_vcdm/schemas.py).
- `parse_credential_status` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-credential-w3c-vcdm/src/tba_protocol_credential_w3c_vcdm/status.py).
- `validate_verifiable_credential` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-credential-w3c-vcdm/src/tba_protocol_credential_w3c_vcdm/validation.py).
- `validate_verifiable_presentation` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-credential-w3c-vcdm/src/tba_protocol_credential_w3c_vcdm/validation.py).
- `select_version` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-credential-w3c-vcdm/src/tba_protocol_credential_w3c_vcdm/versions.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

### Health and Observability

This README does not establish a standalone health endpoint for `tba-protocol-credential-w3c-vcdm`. Observe the concrete caller’s results, exceptions, and existing test reports. An application that embeds this package must define its own health and telemetry contract.

### Security and Resource Limits

Apply the input, credential, and resource constraints implemented in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-credential-w3c-vcdm/src/tba_protocol_credential_w3c_vcdm/bindings.py). The `tba-protocol-credential-w3c-vcdm` README gate is a documentation check, not a security review or a substitute for the implementation’s limits and caller authorization.

### Compatibility

This source version of `tba-protocol-credential-w3c-vcdm` declares Python `>=3.10,<3.16`. Consult its dependency constraints before upgrading. Source-version and registry-version badges have separate meanings; this migration makes no additional platform or interoperability certification claim.

---

## Verification

### Tests

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-credential-w3c-vcdm/src/tba_protocol_credential_w3c_vcdm/__init__.py).

### Certification Status

No external certification is asserted for `tba-protocol-credential-w3c-vcdm` by this documentation migration. README conformance, example syntax, runtime tests, and protocol or security certification are distinct evidence scopes.

### Evidence

The [README standards CI](https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml) records mechanical documentation results for its tested commit. The [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-credential-w3c-vcdm/src/tba_protocol_credential_w3c_vcdm/bindings.py) and example sources support the package-boundary description; external runtime behavior requires its own test evidence.

---

## FAQ

### Why

**Why select this package?** `tba-protocol-credential-w3c-vcdm` provides version authority, feature selection, compatibility, migration, and semantic object mapping for W3C Verifiable Credentials Data Model revisions; use its own API boundary rather than assuming neighboring packages are bundled or configured automatically.

### How

**How do I start?** Install or synchronize the environment under Getting Started, follow the maintained example for `tba-protocol-credential-w3c-vcdm`, and consult [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-credential-w3c-vcdm/src/tba_protocol_credential_w3c_vcdm/bindings.py) for the exact types and signatures involved.

### When

**When should I validate an upgrade?** Recheck `tba-protocol-credential-w3c-vcdm` whenever its source version, declared collaborators, configuration, or caller changes. Run relevant behavioral tests in addition to the README gate before promotion.

---

## Documentation and Related Packages

### More Documentation

The [repository contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md), [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-credential-w3c-vcdm/src/tba_protocol_credential_w3c_vcdm/bindings.py), and [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-credential-w3c-vcdm/pyproject.toml) provide the supporting context for `tba-protocol-credential-w3c-vcdm`. The [README policy](https://github.com/groupsum/readme-standards/blob/master/docs/outline.md) defines the common document structure.

### Related Packages

Declared local runtime dependencies:

- [tba-concrete-verifiable-credential](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-verifiable-credential/README.md)
- [tba-concrete-verifiable-presentation](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-verifiable-presentation/README.md)
- [tba-primitives-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/000-primitives/tba-primitives-identity/README.md)

### Project Links

<!-- readme-standards:begin project-links -->
- [Documentation](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/050-protocols/tba-protocol-credential-w3c-vcdm#readme)
- [Homepage](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/050-protocols/tba-protocol-credential-w3c-vcdm#readme)
- [Issues](https://github.com/tigrbl/tigrbl_auth/issues)
- [PyPI](https://pypi.org/project/tba-protocol-credential-w3c-vcdm/)
- [Repository](https://github.com/tigrbl/tigrbl_auth)
- [Source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/050-protocols/tba-protocol-credential-w3c-vcdm)
- [pypi: tba-protocol-credential-w3c-vcdm](https://pypi.org/project/tba-protocol-credential-w3c-vcdm/)
<!-- readme-standards:end project-links -->

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/050-protocols/tba-protocol-credential-w3c-vcdm)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-credential-w3c-vcdm/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-credential-w3c-vcdm/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-credential-w3c-vcdm/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-protocol-credential-w3c-vcdm/)

---

## Contributing

### How to Contribute

Follow the [contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md) and include a focused example or regression for changes to `tba-protocol-credential-w3c-vcdm`. Keep package behavior, its documented boundary, and its tests aligned.

### Development Setup

Work from the `pkgs/050-protocols/tba-protocol-credential-w3c-vcdm` checkout. Synchronize its declared development environment with uv, then run the relevant package tests and `python -m pytest docs/readme/test_examples.py`. The repository’s dedicated README job installs `readme-standards==0.1.3` without resolving unrelated runtime packages.

### Notes for Maintainers

Edit authored prose directly in this `tba-protocol-credential-w3c-vcdm` README. Update source examples in `docs/readme/`, then run `readme-standards render --root . --write` from the package directory and review the diff. Required headings and generated blocks come from package-guide-v1.

---

## Governance

### Ownership and Decision Making

Changes to `tba-protocol-credential-w3c-vcdm` follow the maintainer review process of [tigrbl/tigrbl_auth](https://github.com/tigrbl/tigrbl_auth) and its contribution guide. Author attribution remains in the [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-credential-w3c-vcdm/pyproject.toml); this README does not assign new publishing or administrative authority.

### Standards and Policies

`tba-protocol-credential-w3c-vcdm` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `050-protocols` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

### Lifecycle and Migration

The `tba-protocol-credential-w3c-vcdm` source version is `0.4.0.dev3`. This change standardizes documentation and adds a development-only gate; it does not publish a new runtime version or declare a previously unpublished package released. Preserve explicit deprecation and replacement instructions where present.

---

## License and Attribution

### License

<!-- readme-standards:begin license -->
Licensed under `Apache-2.0`. See [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-credential-w3c-vcdm/LICENSE).
<!-- readme-standards:end license -->

### Notices

<!-- readme-standards:begin notices -->
See [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-credential-w3c-vcdm/NOTICE) for attribution.
<!-- readme-standards:end notices -->
