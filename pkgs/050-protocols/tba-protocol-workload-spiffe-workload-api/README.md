# tba-protocol-workload-spiffe-workload-api

<!-- readme-standards:begin branding -->
<p align="center"><a href="https://github.com/tigrbl/tigrbl_auth"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="300"></a></p>
<p align="center"><strong>tba-protocol-workload-spiffe-workload-api</strong></p>
<p align="center">SPIFFE Workload API service contract and carrier-neutral bindings.</p>
<p align="center">
<a href="https://pypi.org/project/tba-protocol-workload-spiffe-workload-api/"><img alt="pypi: tba-protocol-workload-spiffe-workload-api" src="https://img.shields.io/pypi/v/tba-protocol-workload-spiffe-workload-api?labelColor=1E293B&amp;color=1D4ED8"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-workload-spiffe-workload-api/pyproject.toml"><img alt="Source version: 0.4.0.dev3" src="https://img.shields.io/static/v1?label=Source%20version&amp;message=0.4.0.dev3&amp;labelColor=1E293B&amp;color=4338CA"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-workload-spiffe-workload-api/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/static/v1?label=Python&amp;message=%3E%3D3.10%2C%3C3.16&amp;labelColor=1E293B&amp;color=0F766E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-workload-spiffe-workload-api/pyproject.toml"><img alt="Layer: 050-protocols" src="https://img.shields.io/static/v1?label=Layer&amp;message=050-protocols&amp;labelColor=1E293B&amp;color=6D28D9"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-workload-spiffe-workload-api/README.md#lifecycle-and-migration"><img alt="Lifecycle: active" src="https://img.shields.io/static/v1?label=Lifecycle&amp;message=active&amp;labelColor=1E293B&amp;color=166534"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-workload-spiffe-workload-api/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/static/v1?label=License&amp;message=Apache-2.0&amp;labelColor=1E293B&amp;color=86198F"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-workload-spiffe-workload-api/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/static/v1?label=Notice&amp;message=attribution&amp;labelColor=1E293B&amp;color=86198F"></a>
</p>
<p align="center">
<a href="https://pypi.org/project/tba-protocol-workload-spiffe-workload-api/"><img alt="Monthly PyPI downloads: tba-protocol-workload-spiffe-workload-api" src="https://img.shields.io/pypi/dm/tba-protocol-workload-spiffe-workload-api?labelColor=1E293B&amp;color=0E7490"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-workload-spiffe-workload-api/README.md"><img alt="README hits: tba-protocol-workload-spiffe-workload-api" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/pkgs/050-protocols/tba-protocol-workload-spiffe-workload-api/README.md.svg?label=README%20hits&amp;labelColor=1E293B&amp;color=0E7490"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="README standards: CI gate" src="https://img.shields.io/static/v1?label=README%20standards&amp;message=CI%20gate&amp;labelColor=1E293B&amp;color=1D4ED8"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-workload-spiffe-workload-api/docs/readme/test_examples.py"><img alt="Tests: example source" src="https://img.shields.io/static/v1?label=Tests&amp;message=example%20source&amp;labelColor=1E293B&amp;color=0F766E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-workload-spiffe-workload-api/README.md#certification-status"><img alt="Certification: not certified" src="https://img.shields.io/static/v1?label=Certification&amp;message=not%20certified&amp;labelColor=1E293B&amp;color=92400E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/tools/readme/POLICY.md"><img alt="Governance: repository policy" src="https://img.shields.io/static/v1?label=Governance&amp;message=repository%20policy&amp;labelColor=1E293B&amp;color=4338CA"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="Evidence: source and CI" src="https://img.shields.io/static/v1?label=Evidence&amp;message=source%20and%20CI&amp;labelColor=1E293B&amp;color=6D28D9"></a>
</p>
<p align="center"><a href="#overview">Overview</a> · <a href="#installation">Installation</a> · <a href="#quick-start">Quick Start</a> · <a href="#usage">Usage</a> · <a href="#public-api-and-import-surfaces">API</a> · <a href="#contributing">Contributing</a> · <a href="#governance">Governance</a> · <a href="#license">License</a></p>
<!-- readme-standards:end branding -->

---

## Overview

### Summary

SPIFFE Workload API service contract and carrier-neutral bindings. This service is not extended with WIT or CWT RPCs.

- Package: `tba-protocol-workload-spiffe-workload-api`
- Layer: `050-protocols`
- Responsibility: SPIFFE Workload API service contract and carrier-neutral bindings.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-workload-spiffe-workload-api/src/tba_protocol_workload_spiffe_workload_api/__init__.py).
- Distribution: Python package on PyPI.

### Why This Package

`tba-protocol-workload-spiffe-workload-api` isolates this responsibility: SPIFFE Workload API service contract and carrier-neutral bindings. Its [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-workload-spiffe-workload-api/src/tba_protocol_workload_spiffe_workload_api/bindings.py) exposes `CURRENT_VERSION`, `FORBIDDEN_EXTENSION_RPCS`, `RPC_DEFINITIONS`, `RPC_NAMES`, `RpcDefinition`, `VERSION_HISTORY`, `WorkloadApiService`, `WorkloadApiVersion`, `validate_endpoint`, `validate_full_snapshot`, allowing consumers to select this package without treating adjacent packages as part of its public contract.

### When to Use

Choose `tba-protocol-workload-spiffe-workload-api` for this responsibility: SPIFFE Workload API service contract and carrier-neutral bindings. Its `050-protocols` placement keeps protocol semantics and projections separate from deployment hosting or ownership of persistence implementations.

### Features

- `ProtocolProfileError`: The artifact or request does not satisfy the selected protocol profile.
- `RpcDefinition`: declared in src/tba_protocol_workload_spiffe_workload_api/rpcs.py
- `WorkloadApiService`: declared in src/tba_protocol_workload_spiffe_workload_api/service.py
- `WorkloadApiVersion`: declared in src/tba_protocol_workload_spiffe_workload_api/versions.py

### Non-Goals

`tba-protocol-workload-spiffe-workload-api` does not take ownership of deployment hosting or ownership of persistence implementations.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

---

## Getting Started

### Prerequisites

Python `>=3.10,<3.16` is required. The [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-workload-spiffe-workload-api/pyproject.toml) declares no direct runtime dependencies. Read the example’s inputs and service requirements before execution.

### Installation

Install the selected PyPI release of `tba-protocol-workload-spiffe-workload-api`:

```bash
uv pip install tba-protocol-workload-spiffe-workload-api
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/050-protocols/tba-protocol-workload-spiffe-workload-api
```

#### uv

<!-- readme-standards:begin installation.uv -->
```bash
uv add tba-protocol-workload-spiffe-workload-api
```
<!-- readme-standards:end installation.uv -->

#### pip

<!-- readme-standards:begin installation.pip -->
```bash
python -m pip install tba-protocol-workload-spiffe-workload-api
```
<!-- readme-standards:end installation.pip -->

#### Poetry

<!-- readme-standards:begin installation.poetry -->
```bash
poetry add tba-protocol-workload-spiffe-workload-api
```
<!-- readme-standards:end installation.poetry -->

### Quick Start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.


```bash
uv run --isolated --no-project --python 3.12 --with "tba-protocol-workload-spiffe-workload-api==0.4.0.dev3" python quickstart.py
```

The command prints the declared current revision.

#### Example

<!-- readme-standards:begin example.quick-start -->
Source: [docs/readme/quick_start.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-workload-spiffe-workload-api/docs/readme/quick_start.py).

```python
from tba_protocol_workload_spiffe_workload_api import CURRENT_VERSION

assert CURRENT_VERSION is not None
print(CURRENT_VERSION)
```
<!-- readme-standards:end example.quick-start -->

#### Expected Result

The example demonstrates the documented `tba-protocol-workload-spiffe-workload-api` source boundary or workflow. Complete its required configuration first. README CI checks the maintained source’s syntax and declarations; it does not claim that external services or the application workflow were exercised.

---

## Usage

### Common Workflows

<!-- readme-standards:begin example.usage -->
Source: [docs/readme/usage.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-workload-spiffe-workload-api/docs/readme/usage.py).

```python
from tba_protocol_workload_spiffe_workload_api import CURRENT_VERSION

assert CURRENT_VERSION is not None
print(CURRENT_VERSION)
```
<!-- readme-standards:end example.usage -->

The following public-entry-point example belongs to `tba-protocol-workload-spiffe-workload-api`. SPIFFE Workload API service contract and carrier-neutral bindings. Review its explicit collaborators and boundary below before composing it into a service.

### Configuration

Configure `tba-protocol-workload-spiffe-workload-api` through the APIs in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-workload-spiffe-workload-api/src/tba_protocol_workload_spiffe_workload_api/bindings.py); its [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-workload-spiffe-workload-api/pyproject.toml) describes installation requirements, not an implicit service configuration. No additional package-global configuration contract is inferred from dependencies.

### Error Handling

The inspected `tba-protocol-workload-spiffe-workload-api` source raises `ValueError`. Handle these at the calling boundary and consult the implementation for the triggering conditions.

### Best Practices

Use the explicit `tba-protocol-workload-spiffe-workload-api` imports documented below and keep collaborator configuration with the caller. Run the package’s relevant tests after changing `CURRENT_VERSION`, `FORBIDDEN_EXTENSION_RPCS`, `RPC_DEFINITIONS`, `RPC_NAMES`, `RpcDefinition`, `VERSION_HISTORY`, `WorkloadApiService`, `WorkloadApiVersion`, `validate_endpoint`, `validate_full_snapshot`; an import or successful installation alone does not establish its runtime guarantees.

---

## Package Boundary

### What It Owns

`tba-protocol-workload-spiffe-workload-api` belongs to `050-protocols` and owns protocol semantics and projections: SPIFFE Workload API service contract and carrier-neutral bindings.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-workload-spiffe-workload-api/src/tba_protocol_workload_spiffe_workload_api/__init__.py). Public exports include `CURRENT_VERSION`, `FORBIDDEN_EXTENSION_RPCS`, `RPC_DEFINITIONS`, `RPC_NAMES`, `VERSION_HISTORY`, `RpcDefinition`, `WorkloadApiService`, `WorkloadApiVersion`, `validate_endpoint`, `validate_full_snapshot`.

Keep deployment hosting or ownership of persistence implementations in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

### Public API and Import Surfaces

Import namespace: `tba_protocol_workload_spiffe_workload_api`.

Source-declared exports or types: `CURRENT_VERSION`, `FORBIDDEN_EXTENSION_RPCS`, `RPC_DEFINITIONS`, `RPC_NAMES`, `RpcDefinition`, `VERSION_HISTORY`, `WorkloadApiService`, `WorkloadApiVersion`, `validate_endpoint`, `validate_full_snapshot`.

Inspect [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-workload-spiffe-workload-api/src/tba_protocol_workload_spiffe_workload_api/bindings.py) for exact signatures; this inventory does not designate every internal module as stable.

### Entry Points

<!-- readme-standards:begin entry-points -->
This package declares no command-line, GUI, or plugin entry points in its manifest.
<!-- readme-standards:end entry-points -->

### Injected Dependencies

Explicit construction inputs and collaborators for `tba-protocol-workload-spiffe-workload-api`:

- `WorkloadApiService` construction inputs: `handlers`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-workload-spiffe-workload-api/src/tba_protocol_workload_spiffe_workload_api/service.py).
- `validate_full_snapshot` construction inputs: `declared_full_snapshot`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-workload-spiffe-workload-api/src/tba_protocol_workload_spiffe_workload_api/streams.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

### Protocol Consumers

Direct consumers in this checkout’s package manifests include `tba-workspace`. These edges describe declared dependencies, not protocol-conformance evidence.

### Extensions

For `tba-protocol-workload-spiffe-workload-api`, use the source-declared public interfaces (`CURRENT_VERSION`, `FORBIDDEN_EXTENSION_RPCS`, `RPC_DEFINITIONS`, `RPC_NAMES`, `RpcDefinition`, `VERSION_HISTORY`, `WorkloadApiService`, `WorkloadApiVersion`, `validate_endpoint`, `validate_full_snapshot`) when composing or extending behavior. Its entry-point section below is authoritative for registered plugins; no additional extension loader is inferred from the package name.

---

## Operations and Readiness

### Operational Requirements

`tba-protocol-workload-spiffe-workload-api` exposes protocol semantics and projections. Public operations found in its source:

- `validate_endpoint` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-workload-spiffe-workload-api/src/tba_protocol_workload_spiffe_workload_api/endpoint.py).
- `WorkloadApiService.dispatch` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-workload-spiffe-workload-api/src/tba_protocol_workload_spiffe_workload_api/service.py).
- `validate_full_snapshot` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-workload-spiffe-workload-api/src/tba_protocol_workload_spiffe_workload_api/streams.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

### Health and Observability

This README does not establish a standalone health endpoint for `tba-protocol-workload-spiffe-workload-api`. Observe the concrete caller’s results, exceptions, and existing test reports. An application that embeds this package must define its own health and telemetry contract.

### Security and Resource Limits

Apply the input, credential, and resource constraints implemented in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-workload-spiffe-workload-api/src/tba_protocol_workload_spiffe_workload_api/bindings.py). The `tba-protocol-workload-spiffe-workload-api` README gate is a documentation check, not a security review or a substitute for the implementation’s limits and caller authorization.

### Compatibility

This source version of `tba-protocol-workload-spiffe-workload-api` declares Python `>=3.10,<3.16`. Consult its dependency constraints before upgrading. Source-version and registry-version badges have separate meanings; this migration makes no additional platform or interoperability certification claim.

---

## Verification

### Tests

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-workload-spiffe-workload-api/src/tba_protocol_workload_spiffe_workload_api/__init__.py).

### Certification Status

No external certification is asserted for `tba-protocol-workload-spiffe-workload-api` by this documentation migration. README conformance, example syntax, runtime tests, and protocol or security certification are distinct evidence scopes.

### Evidence

The [README standards CI](https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml) records mechanical documentation results for its tested commit. The [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-workload-spiffe-workload-api/src/tba_protocol_workload_spiffe_workload_api/bindings.py) and example sources support the package-boundary description; external runtime behavior requires its own test evidence.

---

## FAQ

### Why

**Why select this package?** `tba-protocol-workload-spiffe-workload-api` provides sPIFFE Workload API service contract and carrier-neutral bindings; use its own API boundary rather than assuming neighboring packages are bundled or configured automatically.

### How

**How do I start?** Install or synchronize the environment under Getting Started, follow the maintained example for `tba-protocol-workload-spiffe-workload-api`, and consult [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-workload-spiffe-workload-api/src/tba_protocol_workload_spiffe_workload_api/bindings.py) for the exact types and signatures involved.

### When

**When should I validate an upgrade?** Recheck `tba-protocol-workload-spiffe-workload-api` whenever its source version, declared collaborators, configuration, or caller changes. Run relevant behavioral tests in addition to the README gate before promotion.

---

## Documentation and Related Packages

### More Documentation

The [repository contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md), [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-workload-spiffe-workload-api/src/tba_protocol_workload_spiffe_workload_api/bindings.py), and [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-workload-spiffe-workload-api/pyproject.toml) provide the supporting context for `tba-protocol-workload-spiffe-workload-api`. The [README policy](https://github.com/groupsum/readme-standards/blob/master/docs/outline.md) defines the common document structure.

### Related Packages

`tba-protocol-workload-spiffe-workload-api` declares no local runtime dependency and has no direct consumer in the active manifest graph. Browse the [050-protocols layer](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/050-protocols) for adjacent package responsibilities; adjacency does not imply a dependency.

### Project Links

<!-- readme-standards:begin project-links -->
- [Documentation](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/050-protocols/tba-protocol-workload-spiffe-workload-api#readme)
- [Homepage](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/050-protocols/tba-protocol-workload-spiffe-workload-api#readme)
- [Issues](https://github.com/tigrbl/tigrbl_auth/issues)
- [PyPI](https://pypi.org/project/tba-protocol-workload-spiffe-workload-api/)
- [Repository](https://github.com/tigrbl/tigrbl_auth)
- [Source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/050-protocols/tba-protocol-workload-spiffe-workload-api)
- [pypi: tba-protocol-workload-spiffe-workload-api](https://pypi.org/project/tba-protocol-workload-spiffe-workload-api/)
<!-- readme-standards:end project-links -->

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/050-protocols/tba-protocol-workload-spiffe-workload-api)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-workload-spiffe-workload-api/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-workload-spiffe-workload-api/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-workload-spiffe-workload-api/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-protocol-workload-spiffe-workload-api/)

---

## Contributing

### How to Contribute

Follow the [contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md) and include a focused example or regression for changes to `tba-protocol-workload-spiffe-workload-api`. Keep package behavior, its documented boundary, and its tests aligned.

### Development Setup

Work from the `pkgs/050-protocols/tba-protocol-workload-spiffe-workload-api` checkout. Synchronize its declared development environment with uv, then run the relevant package tests and `python -m pytest docs/readme/test_examples.py`. The repository’s dedicated README job installs `readme-standards==0.1.3` without resolving unrelated runtime packages.

### Notes for Maintainers

Edit authored prose directly in this `tba-protocol-workload-spiffe-workload-api` README. Update source examples in `docs/readme/`, then run `readme-standards render --root . --write` from the package directory and review the diff. Required headings and generated blocks come from package-guide-v1.

---

## Governance

### Ownership and Decision Making

Changes to `tba-protocol-workload-spiffe-workload-api` follow the maintainer review process of [tigrbl/tigrbl_auth](https://github.com/tigrbl/tigrbl_auth) and its contribution guide. Author attribution remains in the [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-workload-spiffe-workload-api/pyproject.toml); this README does not assign new publishing or administrative authority.

### Standards and Policies

`tba-protocol-workload-spiffe-workload-api` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `050-protocols` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

### Lifecycle and Migration

The `tba-protocol-workload-spiffe-workload-api` source version is `0.4.0.dev3`. This change standardizes documentation and adds a development-only gate; it does not publish a new runtime version or declare a previously unpublished package released. Preserve explicit deprecation and replacement instructions where present.

---

## License and Attribution

### License

<!-- readme-standards:begin license -->
Licensed under `Apache-2.0`. See [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-workload-spiffe-workload-api/LICENSE).
<!-- readme-standards:end license -->

### Notices

<!-- readme-standards:begin notices -->
See [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-workload-spiffe-workload-api/NOTICE) for attribution.
<!-- readme-standards:end notices -->
