# tba-bases-replay

<!-- readme-standards:begin branding -->
<p align="center"><a href="https://github.com/tigrbl/tigrbl_auth"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="300"></a></p>
<p align="center"><strong>tba-bases-replay</strong></p>
<p align="center">Protocol-neutral replay reservation bases.</p>
<p align="center">
<a href="https://pypi.org/project/tba-bases-replay/"><img alt="pypi: tba-bases-replay" src="https://img.shields.io/pypi/v/tba-bases-replay"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-replay/pyproject.toml"><img alt="Source version: 0.4.0.dev3" src="https://img.shields.io/static/v1?label=Source%20version&amp;message=0.4.0.dev3&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-replay/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/static/v1?label=Python&amp;message=%3E%3D3.10%2C%3C3.16&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-replay/pyproject.toml"><img alt="Layer: 005-bases" src="https://img.shields.io/static/v1?label=Layer&amp;message=005-bases&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-replay/README.md#lifecycle-and-migration"><img alt="Lifecycle: active" src="https://img.shields.io/static/v1?label=Lifecycle&amp;message=active&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-replay/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/static/v1?label=License&amp;message=Apache-2.0&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-replay/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/static/v1?label=Notice&amp;message=attribution&amp;color=525252"></a>
</p>
<p align="center">
<a href="https://pypi.org/project/tba-bases-replay/"><img alt="Monthly PyPI downloads: tba-bases-replay" src="https://img.shields.io/pypi/dm/tba-bases-replay"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-replay/README.md"><img alt="README hits: tba-bases-replay" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/pkgs/005-bases/tba-bases-replay/README.md.svg?label=README%20hits"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="README standards: CI gate" src="https://img.shields.io/static/v1?label=README%20standards&amp;message=CI%20gate&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-replay/docs/readme/test_examples.py"><img alt="Tests: example source" src="https://img.shields.io/static/v1?label=Tests&amp;message=example%20source&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-replay/README.md#certification-status"><img alt="Certification: not certified" src="https://img.shields.io/static/v1?label=Certification&amp;message=not%20certified&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/tools/readme/POLICY.md"><img alt="Governance: repository policy" src="https://img.shields.io/static/v1?label=Governance&amp;message=repository%20policy&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="Evidence: source and CI" src="https://img.shields.io/static/v1?label=Evidence&amp;message=source%20and%20CI&amp;color=525252"></a>
</p>
<p align="center"><a href="#overview">Overview</a> · <a href="#installation">Installation</a> · <a href="#quick-start">Quick Start</a> · <a href="#usage">Usage</a> · <a href="#public-api-and-import-surfaces">API</a> · <a href="#contributing">Contributing</a> · <a href="#governance">Governance</a> · <a href="#license">License</a></p>
<!-- readme-standards:end branding -->

---

## Overview

### Summary

Shared protocol-neutral replay reservation behavior. Implementations must make
check-and-reserve atomic; the base does not select persistence or networking.

- Package: `tba-bases-replay`
- Layer: `005-bases`
- Responsibility: Protocol-neutral replay reservation bases.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-replay/src/tba_bases_replay/__init__.py).
- Distribution: Python package on PyPI.

### Why This Package

`tba-bases-replay` isolates this responsibility: Protocol-neutral replay reservation bases. Its [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-replay/src/tba_bases_replay/__init__.py) exposes `ReplayReservationBase`, allowing consumers to select this package without treating adjacent packages as part of its public contract.

### When to Use

Choose `tba-bases-replay` for this responsibility: Protocol-neutral replay reservation bases. Its `005-bases` placement keeps reusable component bases separate from deployment composition or implicit provider selection.

### Features

- `ReplayReservationBase`: declared in src/tba_bases_replay/__init__.py

### Non-Goals

`tba-bases-replay` does not take ownership of deployment composition or implicit provider selection.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

---

## Getting Started

### Prerequisites

Python `>=3.10,<3.16` is required. The [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-replay/pyproject.toml) declares runtime dependencies including `tba-contracts-replay`. Read the example’s inputs and service requirements before execution.

### Installation

Install the selected PyPI release of `tba-bases-replay`:

```bash
uv pip install tba-bases-replay
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/005-bases/tba-bases-replay
```

#### uv

<!-- readme-standards:begin installation.uv -->
```bash
uv add tba-bases-replay
```
<!-- readme-standards:end installation.uv -->

#### pip

<!-- readme-standards:begin installation.pip -->
```bash
python -m pip install tba-bases-replay
```
<!-- readme-standards:end installation.pip -->

#### Poetry

<!-- readme-standards:begin installation.poetry -->
```bash
poetry add tba-bases-replay
```
<!-- readme-standards:end installation.poetry -->

### Quick Start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.


```bash
uv run --isolated --no-project --python 3.12 --with "tba-bases-replay==0.4.0.dev3" python quickstart.py
```

The import and assertion succeed when the ReplayReservationBase entry point is available.

#### Example

<!-- readme-standards:begin example.quick-start -->
Source: [docs/readme/quick_start.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-replay/docs/readme/quick_start.py).

```python
from tba_bases_replay import ReplayReservationBase

assert callable(ReplayReservationBase)
```
<!-- readme-standards:end example.quick-start -->

#### Expected Result

The example demonstrates the documented `tba-bases-replay` source boundary or workflow. Complete its required configuration first. README CI checks the maintained source’s syntax and declarations; it does not claim that external services or the application workflow were exercised.

---

## Usage

### Common Workflows

<!-- readme-standards:begin example.usage -->
Source: [docs/readme/usage.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-replay/docs/readme/usage.py).

```python
from tba_bases_replay import ReplayReservationBase

assert callable(ReplayReservationBase)
```
<!-- readme-standards:end example.usage -->

The following public-entry-point example belongs to `tba-bases-replay`. Protocol-neutral replay reservation bases. Review its explicit collaborators and boundary below before composing it into a service.

### Configuration

Configure `tba-bases-replay` through the APIs in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-replay/src/tba_bases_replay/__init__.py); its [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-replay/pyproject.toml) describes installation requirements, not an implicit service configuration. No additional package-global configuration contract is inferred from dependencies.

### Error Handling

The inspected `tba-bases-replay` source does not establish a package-wide exception hierarchy. Preserve errors from its declared dependencies and validate inputs using the specific public contract in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-replay/src/tba_bases_replay/__init__.py).

### Best Practices

Use the explicit `tba-bases-replay` imports documented below and keep collaborator configuration with the caller. Run the package’s relevant tests after changing `ReplayReservationBase`; an import or successful installation alone does not establish its runtime guarantees.

---

## Package Boundary

### What It Owns

`tba-bases-replay` belongs to `005-bases` and owns reusable component bases: Protocol-neutral replay reservation bases.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-replay/src/tba_bases_replay/__init__.py). Public exports include `ReplayReservationBase`.

Keep deployment composition or implicit provider selection in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

### Public API and Import Surfaces

Import namespace: `tba_bases_replay`.

Source-declared exports or types: `ReplayReservationBase`.

Inspect [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-replay/src/tba_bases_replay/__init__.py) for exact signatures; this inventory does not designate every internal module as stable.

### Entry Points

<!-- readme-standards:begin entry-points -->
This package declares no command-line, GUI, or plugin entry points in its manifest.
<!-- readme-standards:end entry-points -->

### Injected Dependencies

The [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-replay/src/tba_bases_replay/__init__.py) for `tba-bases-replay` does not declare an explicit service-constructor or keyword-only factory hook in the inspected source. Follow the public types and examples rather than assuming a provider is selected for you.

Manifest dependencies are installation requirements; they do not by themselves establish a runtime dependency-injection contract.

### Protocol Consumers

Direct consumers in this checkout’s package manifests include `tba-provider-replay-memory`, `tba-durability-attestation`, `tba-durability-audit`, `tba-durability-authorization-policy`, `tba-durability-consent`, `tba-durability-delegation`, `tba-durability-digital-credential`, `tba-durability-gnap-state`, `tba-durability-identity`, `tba-durability-oauth-state`, `tba-durability-oidc-state`, `tba-durability-presentation`, `tba-durability-replay-protection`, `tba-durability-security-event`, `tba-durability-session`. These edges describe declared dependencies, not protocol-conformance evidence.

### Extensions

For `tba-bases-replay`, use the source-declared public interfaces (`ReplayReservationBase`) when composing or extending behavior. Its entry-point section below is authoritative for registered plugins; no additional extension loader is inferred from the package name.

---

## Operations and Readiness

### Operational Requirements

`tba-bases-replay` exposes reusable component bases. Public operations found in its source:

- `ReplayReservationBase.digest_key` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-replay/src/tba_bases_replay/__init__.py).
- `ReplayReservationBase.check_and_reserve` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-replay/src/tba_bases_replay/__init__.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

### Health and Observability

This README does not establish a standalone health endpoint for `tba-bases-replay`. Observe the concrete caller’s results, exceptions, and existing test reports. An application that embeds this package must define its own health and telemetry contract.

### Security and Resource Limits

Apply the input, credential, and resource constraints implemented in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-replay/src/tba_bases_replay/__init__.py). The `tba-bases-replay` README gate is a documentation check, not a security review or a substitute for the implementation’s limits and caller authorization.

### Compatibility

This source version of `tba-bases-replay` declares Python `>=3.10,<3.16`. Consult its dependency constraints before upgrading. Source-version and registry-version badges have separate meanings; this migration makes no additional platform or interoperability certification claim.

---

## Verification

### Tests

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-replay/src/tba_bases_replay/__init__.py).

### Certification Status

No external certification is asserted for `tba-bases-replay` by this documentation migration. README conformance, example syntax, runtime tests, and protocol or security certification are distinct evidence scopes.

### Evidence

The [README standards CI](https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml) records mechanical documentation results for its tested commit. The [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-replay/src/tba_bases_replay/__init__.py) and example sources support the package-boundary description; external runtime behavior requires its own test evidence.

---

## FAQ

### Why

**Why select this package?** `tba-bases-replay` provides protocol-neutral replay reservation bases; use its own API boundary rather than assuming neighboring packages are bundled or configured automatically.

### How

**How do I start?** Install or synchronize the environment under Getting Started, follow the maintained example for `tba-bases-replay`, and consult [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-replay/src/tba_bases_replay/__init__.py) for the exact types and signatures involved.

### When

**When should I validate an upgrade?** Recheck `tba-bases-replay` whenever its source version, declared collaborators, configuration, or caller changes. Run relevant behavioral tests in addition to the README gate before promotion.

---

## Documentation and Related Packages

### More Documentation

The [repository contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md), [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-replay/src/tba_bases_replay/__init__.py), and [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-replay/pyproject.toml) provide the supporting context for `tba-bases-replay`. The [README policy](https://github.com/groupsum/readme-standards/blob/master/docs/outline.md) defines the common document structure.

### Related Packages

Declared local runtime dependencies:

- [tba-contracts-replay](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-replay/README.md)

Direct downstream consumers:

- [tba-durability-attestation](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-durability-attestation/README.md)
- [tba-durability-audit](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-durability-audit/README.md)
- [tba-durability-authorization-policy](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-durability-authorization-policy/README.md)
- [tba-durability-consent](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-durability-consent/README.md)
- [tba-durability-delegation](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-durability-delegation/README.md)
- [tba-durability-digital-credential](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-durability-digital-credential/README.md)
- [tba-durability-gnap-state](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-durability-gnap-state/README.md)
- [tba-durability-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-durability-identity/README.md)
- [tba-durability-oauth-state](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-durability-oauth-state/README.md)
- [tba-durability-oidc-state](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-durability-oidc-state/README.md)
- [tba-durability-presentation](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-durability-presentation/README.md)
- [tba-durability-replay-protection](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-durability-replay-protection/README.md)

18 packages directly declare this dependency; the [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records the complete graph.

### Project Links

<!-- readme-standards:begin project-links -->
- [Documentation](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/005-bases/tba-bases-replay#readme)
- [Homepage](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/005-bases/tba-bases-replay#readme)
- [Issues](https://github.com/tigrbl/tigrbl_auth/issues)
- [PyPI](https://pypi.org/project/tba-bases-replay/)
- [Repository](https://github.com/tigrbl/tigrbl_auth)
- [Source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/005-bases/tba-bases-replay)
- [pypi: tba-bases-replay](https://pypi.org/project/tba-bases-replay/)
<!-- readme-standards:end project-links -->

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/005-bases/tba-bases-replay)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-replay/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-replay/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-replay/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-bases-replay/)

---

## Contributing

### How to Contribute

Follow the [contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md) and include a focused example or regression for changes to `tba-bases-replay`. Keep package behavior, its documented boundary, and its tests aligned.

### Development Setup

Work from the `pkgs/005-bases/tba-bases-replay` checkout. Synchronize its declared development environment with uv, then run the relevant package tests and `python -m pytest docs/readme/test_examples.py`. The repository’s dedicated README job installs `readme-standards==0.1.1` without resolving unrelated runtime packages.

### Notes for Maintainers

Edit authored prose directly in this `tba-bases-replay` README. Update source examples in `docs/readme/`, then run `readme-standards render --root . --write` from the package directory and review the diff. Required headings and generated blocks come from package-guide-v1.

---

## Governance

### Ownership and Decision Making

Changes to `tba-bases-replay` follow the maintainer review process of [tigrbl/tigrbl_auth](https://github.com/tigrbl/tigrbl_auth) and its contribution guide. Author attribution remains in the [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-replay/pyproject.toml); this README does not assign new publishing or administrative authority.

### Standards and Policies

`tba-bases-replay` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `005-bases` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

### Lifecycle and Migration

The `tba-bases-replay` source version is `0.4.0.dev3`. This change standardizes documentation and adds a development-only gate; it does not publish a new runtime version or declare a previously unpublished package released. Preserve explicit deprecation and replacement instructions where present.

---

## License and Attribution

### License

<!-- readme-standards:begin license -->
Licensed under `Apache-2.0`. See [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-replay/LICENSE).
<!-- readme-standards:end license -->

### Notices

<!-- readme-standards:begin notices -->
See [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-replay/NOTICE) for attribution.
<!-- readme-standards:end notices -->
