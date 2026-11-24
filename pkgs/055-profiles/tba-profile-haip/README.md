# tba-profile-haip

<!-- readme-standards:begin branding -->
<p align="center"><a href="https://github.com/tigrbl/tigrbl_auth"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="300"></a></p>
<p align="center"><strong>tba-profile-haip</strong></p>
<p align="center">High Assurance Interoperability Profile for digital credentials.</p>
<p align="center">
<a href="https://pypi.org/project/tba-profile-haip/"><img alt="pypi: tba-profile-haip" src="https://img.shields.io/pypi/v/tba-profile-haip?labelColor=1E293B&amp;color=1D4ED8"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-haip/pyproject.toml"><img alt="Source version: 0.4.0.dev3" src="https://img.shields.io/static/v1?label=Source%20version&amp;message=0.4.0.dev3&amp;labelColor=1E293B&amp;color=4338CA"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-haip/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/static/v1?label=Python&amp;message=%3E%3D3.10%2C%3C3.16&amp;labelColor=1E293B&amp;color=0F766E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-haip/pyproject.toml"><img alt="Layer: 055-profiles" src="https://img.shields.io/static/v1?label=Layer&amp;message=055-profiles&amp;labelColor=1E293B&amp;color=6D28D9"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-haip/README.md#lifecycle-and-migration"><img alt="Lifecycle: active" src="https://img.shields.io/static/v1?label=Lifecycle&amp;message=active&amp;labelColor=1E293B&amp;color=166534"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-haip/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/static/v1?label=License&amp;message=Apache-2.0&amp;labelColor=1E293B&amp;color=86198F"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-haip/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/static/v1?label=Notice&amp;message=attribution&amp;labelColor=1E293B&amp;color=86198F"></a>
</p>
<p align="center">
<a href="https://pypi.org/project/tba-profile-haip/"><img alt="Monthly PyPI downloads: tba-profile-haip" src="https://img.shields.io/pypi/dm/tba-profile-haip?labelColor=1E293B&amp;color=0E7490"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-haip/README.md"><img alt="README hits: tba-profile-haip" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/pkgs/055-profiles/tba-profile-haip/README.md.svg?label=README%20hits&amp;labelColor=1E293B&amp;color=0E7490"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="README standards: CI gate" src="https://img.shields.io/static/v1?label=README%20standards&amp;message=CI%20gate&amp;labelColor=1E293B&amp;color=1D4ED8"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-haip/docs/readme/test_examples.py"><img alt="Tests: example source" src="https://img.shields.io/static/v1?label=Tests&amp;message=example%20source&amp;labelColor=1E293B&amp;color=0F766E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-haip/README.md#certification-status"><img alt="Certification: not certified" src="https://img.shields.io/static/v1?label=Certification&amp;message=not%20certified&amp;labelColor=1E293B&amp;color=92400E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/tools/readme/POLICY.md"><img alt="Governance: repository policy" src="https://img.shields.io/static/v1?label=Governance&amp;message=repository%20policy&amp;labelColor=1E293B&amp;color=4338CA"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="Evidence: source and CI" src="https://img.shields.io/static/v1?label=Evidence&amp;message=source%20and%20CI&amp;labelColor=1E293B&amp;color=6D28D9"></a>
</p>
<p align="center"><a href="#overview">Overview</a> · <a href="#installation">Installation</a> · <a href="#quick-start">Quick Start</a> · <a href="#usage">Usage</a> · <a href="#public-api-and-import-surfaces">API</a> · <a href="#contributing">Contributing</a> · <a href="#governance">Governance</a> · <a href="#license">License</a></p>
<!-- readme-standards:end branding -->

---

## Overview

### Summary

Owns versioned protocol composition and compatibility.

- Package: `tba-profile-haip`
- Layer: `055-profiles`
- Responsibility: High Assurance Interoperability Profile for digital credentials.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-haip/src/tba_profile_haip/__init__.py).
- Distribution: Python package on PyPI.

### Why This Package

`tba-profile-haip` isolates this responsibility: High Assurance Interoperability Profile for digital credentials. Its [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-haip/src/tba_profile_haip/__init__.py) exposes `CAPABILITY_REQUIREMENTS`, `COMPATIBILITY_PATHS`, `CURRENT_VERSION`, `FEATURES_BY_VERSION`, `HAIP_CREDENTIAL_FORMATS`, `HAIP_PROOF_CLAIM_CLASSES`, `HaipCompatibility`, `HaipComponentVersionError`, `HaipComponentVersions`, `HaipConfiguration`, `HaipCredentialFormats`, `HaipProfileError`, `HaipTrustBindingError`, `HaipVersion`, `VERSION_HISTORY`, allowing consumers to select this package without treating adjacent packages as part of its public contract.

### When to Use

Choose `tba-profile-haip` for this responsibility: High Assurance Interoperability Profile for digital credentials. Its `055-profiles` placement keeps focused protocol and credential profiles separate from a universal deployment or implicit trust-policy selection.

### Features

- `HaipCompatibility`: declared in src/tba_profile_haip/compatibility.py
- `HaipProfileError`: Base error for an HAIP configuration or binding failure.
- `HaipComponentVersionError`: Raised when component protocol revisions are not profile-compatible.
- `HaipTrustBindingError`: Raised when required wallet/key/verifier trust evidence is unavailable.
- `HaipConfiguration`: declared in src/tba_profile_haip/profile.py
- `HaipComponentVersions`: declared in src/tba_profile_haip/schemas.py
- `HaipCredentialFormats`: declared in src/tba_profile_haip/schemas.py
- `HaipVersion`: declared in src/tba_profile_haip/versions.py

### Non-Goals

Higher-layer orchestration, lower-layer persistence, and protocol behavior outside this package's declared layer are not owned here.

---

## Getting Started

### Prerequisites

Python `>=3.10,<3.16` is required. The [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-haip/pyproject.toml) declares runtime dependencies including `tba-protocol-oid4vci`, `tba-protocol-oid4vp`, `tba-contracts-identity`. Read the example’s inputs and service requirements before execution.

### Installation

Install the selected PyPI release of `tba-profile-haip`:

```bash
uv pip install tba-profile-haip
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/055-profiles/tba-profile-haip
```

#### uv

<!-- readme-standards:begin installation.uv -->
```bash
uv add tba-profile-haip
```
<!-- readme-standards:end installation.uv -->

#### pip

<!-- readme-standards:begin installation.pip -->
```bash
python -m pip install tba-profile-haip
```
<!-- readme-standards:end installation.pip -->

#### Poetry

<!-- readme-standards:begin installation.poetry -->
```bash
poetry add tba-profile-haip
```
<!-- readme-standards:end installation.poetry -->

### Quick Start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.


```bash
uv run --isolated --no-project --python 3.12 --with "tba-profile-haip==0.4.0.dev3" python quickstart.py
```

The command prints the declared current revision.

#### Example

<!-- readme-standards:begin example.quick-start -->
Source: [docs/readme/quick_start.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-haip/docs/readme/quick_start.py).

```python
from tba_profile_haip import CURRENT_VERSION

assert CURRENT_VERSION is not None
print(CURRENT_VERSION)
```
<!-- readme-standards:end example.quick-start -->

#### Expected Result

The example demonstrates the documented `tba-profile-haip` source boundary or workflow. Complete its required configuration first. README CI checks the maintained source’s syntax and declarations; it does not claim that external services or the application workflow were exercised.

---

## Usage

### Common Workflows

<!-- readme-standards:begin example.usage -->
Source: [docs/readme/usage.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-haip/docs/readme/usage.py).

```python
from tba_profile_haip import CURRENT_VERSION

assert CURRENT_VERSION is not None
print(CURRENT_VERSION)
```
<!-- readme-standards:end example.usage -->

The following public-entry-point example belongs to `tba-profile-haip`. High Assurance Interoperability Profile for digital credentials. Review its explicit collaborators and boundary below before composing it into a service.

### Configuration

Configure `tba-profile-haip` through the APIs in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-haip/src/tba_profile_haip/__init__.py); its [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-haip/pyproject.toml) describes installation requirements, not an implicit service configuration. No additional package-global configuration contract is inferred from dependencies.

### Error Handling

The inspected `tba-profile-haip` source raises `ValueError`. Handle these at the calling boundary and consult the implementation for the triggering conditions.

### Best Practices

Use the explicit `tba-profile-haip` imports documented below and keep collaborator configuration with the caller. Run the package’s relevant tests after changing `CAPABILITY_REQUIREMENTS`, `COMPATIBILITY_PATHS`, `CURRENT_VERSION`, `FEATURES_BY_VERSION`, `HAIP_CREDENTIAL_FORMATS`, `HAIP_PROOF_CLAIM_CLASSES`, `HaipCompatibility`, `HaipComponentVersionError`, `HaipComponentVersions`, `HaipConfiguration`, `HaipCredentialFormats`, `HaipProfileError`, `HaipTrustBindingError`, `HaipVersion`, `VERSION_HISTORY`; an import or successful installation alone does not establish its runtime guarantees.

---

## Package Boundary

### What It Owns

`tba-profile-haip` belongs to `055-profiles` and owns focused protocol and credential profiles: High Assurance Interoperability Profile for digital credentials.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-haip/src/tba_profile_haip/__init__.py). Public exports include `CAPABILITY_REQUIREMENTS`, `COMPATIBILITY_PATHS`, `CURRENT_VERSION`, `FEATURES_BY_VERSION`, `HAIP_CREDENTIAL_FORMATS`, `HAIP_PROOF_CLAIM_CLASSES`, `VERSION_HISTORY`, `HaipCompatibility`, `HaipComponentVersionError`, `HaipComponentVersions`, `HaipConfiguration`, `HaipCredentialFormats`.

Keep a universal deployment or implicit trust-policy selection in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

### Public API and Import Surfaces

Import namespace: `tba_profile_haip`.

Source-declared exports or types: `CAPABILITY_REQUIREMENTS`, `COMPATIBILITY_PATHS`, `CURRENT_VERSION`, `FEATURES_BY_VERSION`, `HAIP_CREDENTIAL_FORMATS`, `HAIP_PROOF_CLAIM_CLASSES`, `HaipCompatibility`, `HaipComponentVersionError`, `HaipComponentVersions`, `HaipConfiguration`, `HaipCredentialFormats`, `HaipProfileError`, `HaipTrustBindingError`, `HaipVersion`, `VERSION_HISTORY`.

Inspect [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-haip/src/tba_profile_haip/__init__.py) for exact signatures; this inventory does not designate every internal module as stable.

### Entry Points

<!-- readme-standards:begin entry-points -->
This package declares no command-line, GUI, or plugin entry points in its manifest.
<!-- readme-standards:end entry-points -->

### Injected Dependencies

Explicit construction inputs and collaborators for `tba-profile-haip`:

- `migrate_configuration` construction inputs: `source`, `target`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-haip/src/tba_profile_haip/migrations.py).
- `configure_haip` construction inputs: `credential_formats`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-haip/src/tba_profile_haip/profile.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

### Protocol Consumers

Direct consumers in this checkout’s package manifests include `tba-workspace`. These edges describe declared dependencies, not protocol-conformance evidence.

### Extensions

For `tba-profile-haip`, use the source-declared public interfaces (`CAPABILITY_REQUIREMENTS`, `COMPATIBILITY_PATHS`, `CURRENT_VERSION`, `FEATURES_BY_VERSION`, `HAIP_CREDENTIAL_FORMATS`, `HAIP_PROOF_CLAIM_CLASSES`, `HaipCompatibility`, `HaipComponentVersionError`, `HaipComponentVersions`, `HaipConfiguration`, `HaipCredentialFormats`, `HaipProfileError`, `HaipTrustBindingError`, `HaipVersion`, `VERSION_HISTORY`) when composing or extending behavior. Its entry-point section below is authoritative for registered plugins; no additional extension loader is inferred from the package name.

---

## Operations and Readiness

### Operational Requirements

`tba-profile-haip` exposes focused protocol and credential profiles. Public operations found in its source:

- `capability_report` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-haip/src/tba_profile_haip/__init__.py).
- `compatibility` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-haip/src/tba_profile_haip/compatibility.py).
- `supports` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-haip/src/tba_profile_haip/features.py).
- `migrate_configuration` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-haip/src/tba_profile_haip/migrations.py).
- `HaipConfiguration.validate` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-haip/src/tba_profile_haip/profile.py).
- `configure_haip` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-haip/src/tba_profile_haip/profile.py).
- `select_version` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-haip/src/tba_profile_haip/versions.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

### Health and Observability

This README does not establish a standalone health endpoint for `tba-profile-haip`. Observe the concrete caller’s results, exceptions, and existing test reports. An application that embeds this package must define its own health and telemetry contract.

### Security and Resource Limits

Apply the input, credential, and resource constraints implemented in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-haip/src/tba_profile_haip/__init__.py). The `tba-profile-haip` README gate is a documentation check, not a security review or a substitute for the implementation’s limits and caller authorization.

### Compatibility

This source version of `tba-profile-haip` declares Python `>=3.10,<3.16`. Consult its dependency constraints before upgrading. Source-version and registry-version badges have separate meanings; this migration makes no additional platform or interoperability certification claim.

---

## Verification

### Tests

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-haip/src/tba_profile_haip/__init__.py).

### Certification Status

No external certification is asserted for `tba-profile-haip` by this documentation migration. README conformance, example syntax, runtime tests, and protocol or security certification are distinct evidence scopes.

### Evidence

The [README standards CI](https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml) records mechanical documentation results for its tested commit. The [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-haip/src/tba_profile_haip/__init__.py) and example sources support the package-boundary description; external runtime behavior requires its own test evidence.

---

## FAQ

### Why

**Why select this package?** `tba-profile-haip` provides high Assurance Interoperability Profile for digital credentials; use its own API boundary rather than assuming neighboring packages are bundled or configured automatically.

### How

**How do I start?** Install or synchronize the environment under Getting Started, follow the maintained example for `tba-profile-haip`, and consult [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-haip/src/tba_profile_haip/__init__.py) for the exact types and signatures involved.

### When

**When should I validate an upgrade?** Recheck `tba-profile-haip` whenever its source version, declared collaborators, configuration, or caller changes. Run relevant behavioral tests in addition to the README gate before promotion.

---

## Documentation and Related Packages

### More Documentation

The [repository contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md), [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-haip/src/tba_profile_haip/__init__.py), and [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-haip/pyproject.toml) provide the supporting context for `tba-profile-haip`. The [README policy](https://github.com/groupsum/readme-standards/blob/master/docs/outline.md) defines the common document structure.

### Related Packages

Declared local runtime dependencies:

- [tba-contracts-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-identity/README.md)
- [tba-protocol-oid4vci](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oid4vci/README.md)
- [tba-protocol-oid4vp](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oid4vp/README.md)

### Project Links

<!-- readme-standards:begin project-links -->
- [Documentation](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/055-profiles/tba-profile-haip#readme)
- [Homepage](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/055-profiles/tba-profile-haip#readme)
- [Issues](https://github.com/tigrbl/tigrbl_auth/issues)
- [PyPI](https://pypi.org/project/tba-profile-haip/)
- [Repository](https://github.com/tigrbl/tigrbl_auth)
- [Source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/055-profiles/tba-profile-haip)
- [pypi: tba-profile-haip](https://pypi.org/project/tba-profile-haip/)
<!-- readme-standards:end project-links -->

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/055-profiles/tba-profile-haip)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-haip/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-haip/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-haip/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-profile-haip/)

---

## Contributing

### How to Contribute

Follow the [contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md) and include a focused example or regression for changes to `tba-profile-haip`. Keep package behavior, its documented boundary, and its tests aligned.

### Development Setup

Work from the `pkgs/055-profiles/tba-profile-haip` checkout. Synchronize its declared development environment with uv, then run the relevant package tests and `python -m pytest docs/readme/test_examples.py`. The repository’s dedicated README job installs `readme-standards==0.1.3` without resolving unrelated runtime packages.

### Notes for Maintainers

Edit authored prose directly in this `tba-profile-haip` README. Update source examples in `docs/readme/`, then run `readme-standards render --root . --write` from the package directory and review the diff. Required headings and generated blocks come from package-guide-v1.

---

## Governance

### Ownership and Decision Making

Changes to `tba-profile-haip` follow the maintainer review process of [tigrbl/tigrbl_auth](https://github.com/tigrbl/tigrbl_auth) and its contribution guide. Author attribution remains in the [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-haip/pyproject.toml); this README does not assign new publishing or administrative authority.

### Standards and Policies

`tba-profile-haip` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `055-profiles` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

### Lifecycle and Migration

The `tba-profile-haip` source version is `0.4.0.dev3`. This change standardizes documentation and adds a development-only gate; it does not publish a new runtime version or declare a previously unpublished package released. Preserve explicit deprecation and replacement instructions where present.

---

## License and Attribution

### License

<!-- readme-standards:begin license -->
Licensed under `Apache-2.0`. See [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-haip/LICENSE).
<!-- readme-standards:end license -->

### Notices

<!-- readme-standards:begin notices -->
See [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-haip/NOTICE) for attribution.
<!-- readme-standards:end notices -->
