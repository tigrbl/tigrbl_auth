# tba-concrete-trust-federation-graph

<!-- readme-standards:begin branding -->
<p align="center"><a href="https://github.com/tigrbl/tigrbl_auth"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="300"></a></p>
<p align="center"><strong>tba-concrete-trust-federation-graph</strong></p>
<p align="center">Deterministic trust-federation graph and path algorithms.</p>
<p align="center">
<a href="https://pypi.org/project/tba-concrete-trust-federation-graph/"><img alt="pypi: tba-concrete-trust-federation-graph" src="https://img.shields.io/pypi/v/tba-concrete-trust-federation-graph?labelColor=1E293B&amp;color=1D4ED8"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-trust-federation-graph/pyproject.toml"><img alt="Source version: 0.4.0.dev3" src="https://img.shields.io/static/v1?label=Source%20version&amp;message=0.4.0.dev3&amp;labelColor=1E293B&amp;color=4338CA"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-trust-federation-graph/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/static/v1?label=Python&amp;message=%3E%3D3.10%2C%3C3.16&amp;labelColor=1E293B&amp;color=0F766E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-trust-federation-graph/pyproject.toml"><img alt="Layer: 010-concrete" src="https://img.shields.io/static/v1?label=Layer&amp;message=010-concrete&amp;labelColor=1E293B&amp;color=6D28D9"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-trust-federation-graph/README.md#lifecycle-and-migration"><img alt="Lifecycle: active" src="https://img.shields.io/static/v1?label=Lifecycle&amp;message=active&amp;labelColor=1E293B&amp;color=166534"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-trust-federation-graph/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/static/v1?label=License&amp;message=Apache-2.0&amp;labelColor=1E293B&amp;color=86198F"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-trust-federation-graph/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/static/v1?label=Notice&amp;message=attribution&amp;labelColor=1E293B&amp;color=86198F"></a>
</p>
<p align="center">
<a href="https://pypi.org/project/tba-concrete-trust-federation-graph/"><img alt="Monthly PyPI downloads: tba-concrete-trust-federation-graph" src="https://img.shields.io/pypi/dm/tba-concrete-trust-federation-graph?labelColor=1E293B&amp;color=0E7490"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-trust-federation-graph/README.md"><img alt="README hits: tba-concrete-trust-federation-graph" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/pkgs/010-concrete/tba-concrete-trust-federation-graph/README.md.svg?label=README%20hits&amp;labelColor=1E293B&amp;color=0E7490"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="README standards: CI gate" src="https://img.shields.io/static/v1?label=README%20standards&amp;message=CI%20gate&amp;labelColor=1E293B&amp;color=1D4ED8"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-trust-federation-graph/docs/readme/test_examples.py"><img alt="Tests: example source" src="https://img.shields.io/static/v1?label=Tests&amp;message=example%20source&amp;labelColor=1E293B&amp;color=0F766E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-trust-federation-graph/README.md#certification-status"><img alt="Certification: not certified" src="https://img.shields.io/static/v1?label=Certification&amp;message=not%20certified&amp;labelColor=1E293B&amp;color=92400E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/tools/readme/POLICY.md"><img alt="Governance: repository policy" src="https://img.shields.io/static/v1?label=Governance&amp;message=repository%20policy&amp;labelColor=1E293B&amp;color=4338CA"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="Evidence: source and CI" src="https://img.shields.io/static/v1?label=Evidence&amp;message=source%20and%20CI&amp;labelColor=1E293B&amp;color=6D28D9"></a>
</p>
<p align="center"><a href="#overview">Overview</a> · <a href="#installation">Installation</a> · <a href="#quick-start">Quick Start</a> · <a href="#usage">Usage</a> · <a href="#public-api-and-import-surfaces">API</a> · <a href="#contributing">Contributing</a> · <a href="#governance">Governance</a> · <a href="#license">License</a></p>
<!-- readme-standards:end branding -->

---

## Overview

### Summary

Deterministic, storage-neutral trust-domain graph traversal, path resolution,
revocation, and cross-cloud workload mapping.

This layer does not own database tables, sessions, providers, or protocols.

- Package: `tba-concrete-trust-federation-graph`
- Layer: `010-concrete`
- Responsibility: Deterministic trust-federation graph and path algorithms.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-trust-federation-graph/src/tba_concrete_trust_federation_graph/__init__.py).
- Distribution: Python package on PyPI.

### Why This Package

`tba-concrete-trust-federation-graph` isolates this responsibility: Deterministic trust-federation graph and path algorithms. Its [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-trust-federation-graph/src/tba_concrete_trust_federation_graph/__init__.py) exposes `TrustFederationGraph`, `graph_edge_to_trust_edge`, `graph_node_to_trust_domain`, `trust_domain_to_graph_node_payload`, `trust_edge_to_graph_edge_payload`, allowing consumers to select this package without treating adjacent packages as part of its public contract.

### When to Use

Choose `tba-concrete-trust-federation-graph` for this responsibility: Deterministic trust-federation graph and path algorithms. Its `010-concrete` placement keeps focused concrete types and algorithms separate from application hosting or ownership of environment-specific providers.

### Features

- `WorkloadIdentityLike`: declared in src/tba_concrete_trust_federation_graph/__init__.py
- `TrustFederationGraph`: declared in src/tba_concrete_trust_federation_graph/__init__.py

### Non-Goals

`tba-concrete-trust-federation-graph` does not take ownership of application hosting or ownership of environment-specific providers.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

---

## Getting Started

### Prerequisites

Python `>=3.10,<3.16` is required. The [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-trust-federation-graph/pyproject.toml) declares runtime dependencies including `tba-contracts-identity`. Read the example’s inputs and service requirements before execution.

### Installation

Install the selected PyPI release of `tba-concrete-trust-federation-graph`:

```bash
uv pip install tba-concrete-trust-federation-graph
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/010-concrete/tba-concrete-trust-federation-graph
```

#### uv

<!-- readme-standards:begin installation.uv -->
```bash
uv add tba-concrete-trust-federation-graph
```
<!-- readme-standards:end installation.uv -->

#### pip

<!-- readme-standards:begin installation.pip -->
```bash
python -m pip install tba-concrete-trust-federation-graph
```
<!-- readme-standards:end installation.pip -->

#### Poetry

<!-- readme-standards:begin installation.poetry -->
```bash
poetry add tba-concrete-trust-federation-graph
```
<!-- readme-standards:end installation.poetry -->

### Quick Start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.


```bash
uv run --isolated --no-project --python 3.12 --with "tba-concrete-trust-federation-graph==0.4.0.dev3" python quickstart.py
```

The import and assertion succeed when the WorkloadIdentityLike entry point is available.

#### Example

<!-- readme-standards:begin example.quick-start -->
Source: [docs/readme/quick_start.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-trust-federation-graph/docs/readme/quick_start.py).

```python
from tba_concrete_trust_federation_graph import WorkloadIdentityLike

assert callable(WorkloadIdentityLike)
```
<!-- readme-standards:end example.quick-start -->

#### Expected Result

The example demonstrates the documented `tba-concrete-trust-federation-graph` source boundary or workflow. Complete its required configuration first. README CI checks the maintained source’s syntax and declarations; it does not claim that external services or the application workflow were exercised.

---

## Usage

### Common Workflows

<!-- readme-standards:begin example.usage -->
Source: [docs/readme/usage.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-trust-federation-graph/docs/readme/usage.py).

```python
from tba_concrete_trust_federation_graph import WorkloadIdentityLike

assert callable(WorkloadIdentityLike)
```
<!-- readme-standards:end example.usage -->

The following public-entry-point example belongs to `tba-concrete-trust-federation-graph`. Deterministic trust-federation graph and path algorithms. Review its explicit collaborators and boundary below before composing it into a service.

### Configuration

Configure `tba-concrete-trust-federation-graph` through the APIs in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-trust-federation-graph/src/tba_concrete_trust_federation_graph/__init__.py); its [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-trust-federation-graph/pyproject.toml) describes installation requirements, not an implicit service configuration. No additional package-global configuration contract is inferred from dependencies.

### Error Handling

The inspected `tba-concrete-trust-federation-graph` source raises `KeyError`, `PermissionError`. Handle these at the calling boundary and consult the implementation for the triggering conditions.

### Best Practices

Use the explicit `tba-concrete-trust-federation-graph` imports documented below and keep collaborator configuration with the caller. Run the package’s relevant tests after changing `TrustFederationGraph`, `graph_edge_to_trust_edge`, `graph_node_to_trust_domain`, `trust_domain_to_graph_node_payload`, `trust_edge_to_graph_edge_payload`; an import or successful installation alone does not establish its runtime guarantees.

---

## Package Boundary

### What It Owns

`tba-concrete-trust-federation-graph` belongs to `010-concrete` and owns focused concrete types and algorithms: Deterministic trust-federation graph and path algorithms.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-trust-federation-graph/src/tba_concrete_trust_federation_graph/__init__.py). Public exports include `TrustFederationGraph`, `graph_edge_to_trust_edge`, `graph_node_to_trust_domain`, `trust_domain_to_graph_node_payload`, `trust_edge_to_graph_edge_payload`.

Keep application hosting or ownership of environment-specific providers in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

### Public API and Import Surfaces

Import namespace: `tba_concrete_trust_federation_graph`.

Source-declared exports or types: `TrustFederationGraph`, `graph_edge_to_trust_edge`, `graph_node_to_trust_domain`, `trust_domain_to_graph_node_payload`, `trust_edge_to_graph_edge_payload`.

Inspect [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-trust-federation-graph/src/tba_concrete_trust_federation_graph/__init__.py) for exact signatures; this inventory does not designate every internal module as stable.

### Entry Points

<!-- readme-standards:begin entry-points -->
This package declares no command-line, GUI, or plugin entry points in its manifest.
<!-- readme-standards:end entry-points -->

### Injected Dependencies

Explicit construction inputs and collaborators for `tba-concrete-trust-federation-graph`:

- `trust_domain_to_graph_node_payload` construction inputs: `graph_id`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-trust-federation-graph/src/tba_concrete_trust_federation_graph/__init__.py).
- `trust_edge_to_graph_edge_payload` construction inputs: `graph_id`, `src_id`, `dst_id`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-trust-federation-graph/src/tba_concrete_trust_federation_graph/__init__.py).
- `graph_edge_to_trust_edge` construction inputs: `source_domain`, `target_domain`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-trust-federation-graph/src/tba_concrete_trust_federation_graph/__init__.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

### Protocol Consumers

Direct consumers in this checkout’s package manifests include `tba-durability-identity-administration-trust-federation-graph`, `tba-runtime-identity-administration`, `tba-workspace`. These edges describe declared dependencies, not protocol-conformance evidence.

### Extensions

For `tba-concrete-trust-federation-graph`, use the source-declared public interfaces (`TrustFederationGraph`, `graph_edge_to_trust_edge`, `graph_node_to_trust_domain`, `trust_domain_to_graph_node_payload`, `trust_edge_to_graph_edge_payload`) when composing or extending behavior. Its entry-point section below is authoritative for registered plugins; no additional extension loader is inferred from the package name.

---

## Operations and Readiness

### Operational Requirements

`tba-concrete-trust-federation-graph` exposes focused concrete types and algorithms. Public operations found in its source:

- `TrustFederationGraph.domains` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-trust-federation-graph/src/tba_concrete_trust_federation_graph/__init__.py).
- `TrustFederationGraph.edges` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-trust-federation-graph/src/tba_concrete_trust_federation_graph/__init__.py).
- `TrustFederationGraph.add_domain` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-trust-federation-graph/src/tba_concrete_trust_federation_graph/__init__.py).
- `TrustFederationGraph.add_edge` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-trust-federation-graph/src/tba_concrete_trust_federation_graph/__init__.py).
- `TrustFederationGraph.revoke_edge` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-trust-federation-graph/src/tba_concrete_trust_federation_graph/__init__.py).
- `TrustFederationGraph.resolve_path` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-trust-federation-graph/src/tba_concrete_trust_federation_graph/__init__.py).
- `TrustFederationGraph.map_cross_cloud_workload` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-trust-federation-graph/src/tba_concrete_trust_federation_graph/__init__.py).
- `trust_domain_to_graph_node_payload` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-trust-federation-graph/src/tba_concrete_trust_federation_graph/__init__.py).
- `trust_edge_to_graph_edge_payload` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-trust-federation-graph/src/tba_concrete_trust_federation_graph/__init__.py).
- `graph_node_to_trust_domain` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-trust-federation-graph/src/tba_concrete_trust_federation_graph/__init__.py).
- `graph_edge_to_trust_edge` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-trust-federation-graph/src/tba_concrete_trust_federation_graph/__init__.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

### Health and Observability

This README does not establish a standalone health endpoint for `tba-concrete-trust-federation-graph`. Observe the concrete caller’s results, exceptions, and existing test reports. An application that embeds this package must define its own health and telemetry contract.

### Security and Resource Limits

Apply the input, credential, and resource constraints implemented in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-trust-federation-graph/src/tba_concrete_trust_federation_graph/__init__.py). The `tba-concrete-trust-federation-graph` README gate is a documentation check, not a security review or a substitute for the implementation’s limits and caller authorization.

### Compatibility

This source version of `tba-concrete-trust-federation-graph` declares Python `>=3.10,<3.16`. Consult its dependency constraints before upgrading. Source-version and registry-version badges have separate meanings; this migration makes no additional platform or interoperability certification claim.

---

## Verification

### Tests

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-trust-federation-graph/src/tba_concrete_trust_federation_graph/__init__.py).

### Certification Status

No external certification is asserted for `tba-concrete-trust-federation-graph` by this documentation migration. README conformance, example syntax, runtime tests, and protocol or security certification are distinct evidence scopes.

### Evidence

The [README standards CI](https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml) records mechanical documentation results for its tested commit. The [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-trust-federation-graph/src/tba_concrete_trust_federation_graph/__init__.py) and example sources support the package-boundary description; external runtime behavior requires its own test evidence.

---

## FAQ

### Why

**Why select this package?** `tba-concrete-trust-federation-graph` provides deterministic trust-federation graph and path algorithms; use its own API boundary rather than assuming neighboring packages are bundled or configured automatically.

### How

**How do I start?** Install or synchronize the environment under Getting Started, follow the maintained example for `tba-concrete-trust-federation-graph`, and consult [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-trust-federation-graph/src/tba_concrete_trust_federation_graph/__init__.py) for the exact types and signatures involved.

### When

**When should I validate an upgrade?** Recheck `tba-concrete-trust-federation-graph` whenever its source version, declared collaborators, configuration, or caller changes. Run relevant behavioral tests in addition to the README gate before promotion.

---

## Documentation and Related Packages

### More Documentation

The [repository contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md), [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-trust-federation-graph/src/tba_concrete_trust_federation_graph/__init__.py), and [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-trust-federation-graph/pyproject.toml) provide the supporting context for `tba-concrete-trust-federation-graph`. The [README policy](https://github.com/groupsum/readme-standards/blob/master/docs/outline.md) defines the common document structure.

### Related Packages

Declared local runtime dependencies:

- [tba-contracts-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-identity/README.md)

Direct downstream consumers:

- [tba-durability-identity-administration-trust-federation-graph](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-durability-identity-administration-trust-federation-graph/README.md)
- [tba-runtime-identity-administration](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity-administration/README.md)

### Project Links

<!-- readme-standards:begin project-links -->
- [Documentation](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/010-concrete/tba-concrete-trust-federation-graph#readme)
- [Homepage](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/010-concrete/tba-concrete-trust-federation-graph#readme)
- [Issues](https://github.com/tigrbl/tigrbl_auth/issues)
- [PyPI](https://pypi.org/project/tba-concrete-trust-federation-graph/)
- [Repository](https://github.com/tigrbl/tigrbl_auth)
- [Source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/010-concrete/tba-concrete-trust-federation-graph)
- [pypi: tba-concrete-trust-federation-graph](https://pypi.org/project/tba-concrete-trust-federation-graph/)
<!-- readme-standards:end project-links -->

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/010-concrete/tba-concrete-trust-federation-graph)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-trust-federation-graph/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-trust-federation-graph/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-trust-federation-graph/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-concrete-trust-federation-graph/)

---

## Contributing

### How to Contribute

Follow the [contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md) and include a focused example or regression for changes to `tba-concrete-trust-federation-graph`. Keep package behavior, its documented boundary, and its tests aligned.

### Development Setup

Work from the `pkgs/010-concrete/tba-concrete-trust-federation-graph` checkout. Synchronize its declared development environment with uv, then run the relevant package tests and `python -m pytest docs/readme/test_examples.py`. The repository’s dedicated README job installs `readme-standards==0.1.3` without resolving unrelated runtime packages.

### Notes for Maintainers

Edit authored prose directly in this `tba-concrete-trust-federation-graph` README. Update source examples in `docs/readme/`, then run `readme-standards render --root . --write` from the package directory and review the diff. Required headings and generated blocks come from package-guide-v1.

---

## Governance

### Ownership and Decision Making

Changes to `tba-concrete-trust-federation-graph` follow the maintainer review process of [tigrbl/tigrbl_auth](https://github.com/tigrbl/tigrbl_auth) and its contribution guide. Author attribution remains in the [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-trust-federation-graph/pyproject.toml); this README does not assign new publishing or administrative authority.

### Standards and Policies

`tba-concrete-trust-federation-graph` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `010-concrete` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

### Lifecycle and Migration

The `tba-concrete-trust-federation-graph` source version is `0.4.0.dev3`. This change standardizes documentation and adds a development-only gate; it does not publish a new runtime version or declare a previously unpublished package released. Preserve explicit deprecation and replacement instructions where present.

---

## License and Attribution

### License

<!-- readme-standards:begin license -->
Licensed under `Apache-2.0`. See [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-trust-federation-graph/LICENSE).
<!-- readme-standards:end license -->

### Notices

<!-- readme-standards:begin notices -->
See [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-trust-federation-graph/NOTICE) for attribution.
<!-- readme-standards:end notices -->
