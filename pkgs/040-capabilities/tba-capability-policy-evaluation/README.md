# tba-capability-policy-evaluation

<!-- readme-standards:begin branding -->
<p align="center"><a href="https://github.com/tigrbl/tigrbl_auth"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="300"></a></p>
<p align="center"><strong>tba-capability-policy-evaluation</strong></p>
<p align="center">Composable protocol-neutral policy evaluation and entity-search capability.</p>
<p align="center">
<a href="https://pypi.org/project/tba-capability-policy-evaluation/"><img alt="pypi: tba-capability-policy-evaluation" src="https://img.shields.io/pypi/v/tba-capability-policy-evaluation?labelColor=1E293B&amp;color=1D4ED8"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-policy-evaluation/pyproject.toml"><img alt="Source version: 0.4.0.dev3" src="https://img.shields.io/static/v1?label=Source%20version&amp;message=0.4.0.dev3&amp;labelColor=1E293B&amp;color=4338CA"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-policy-evaluation/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/static/v1?label=Python&amp;message=%3E%3D3.10%2C%3C3.16&amp;labelColor=1E293B&amp;color=0F766E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-policy-evaluation/pyproject.toml"><img alt="Layer: 040-capabilities" src="https://img.shields.io/static/v1?label=Layer&amp;message=040-capabilities&amp;labelColor=1E293B&amp;color=6D28D9"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-policy-evaluation/README.md#lifecycle-and-migration"><img alt="Lifecycle: active" src="https://img.shields.io/static/v1?label=Lifecycle&amp;message=active&amp;labelColor=1E293B&amp;color=166534"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-policy-evaluation/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/static/v1?label=License&amp;message=Apache-2.0&amp;labelColor=1E293B&amp;color=86198F"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-policy-evaluation/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/static/v1?label=Notice&amp;message=attribution&amp;labelColor=1E293B&amp;color=86198F"></a>
</p>
<p align="center">
<a href="https://pypi.org/project/tba-capability-policy-evaluation/"><img alt="Monthly PyPI downloads: tba-capability-policy-evaluation" src="https://img.shields.io/pypi/dm/tba-capability-policy-evaluation?labelColor=1E293B&amp;color=0E7490"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-policy-evaluation/README.md"><img alt="README hits: tba-capability-policy-evaluation" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/pkgs/040-capabilities/tba-capability-policy-evaluation/README.md.svg?label=README%20hits&amp;labelColor=1E293B&amp;color=0E7490"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="README standards: CI gate" src="https://img.shields.io/static/v1?label=README%20standards&amp;message=CI%20gate&amp;labelColor=1E293B&amp;color=1D4ED8"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-policy-evaluation/docs/readme/test_examples.py"><img alt="Tests: example source" src="https://img.shields.io/static/v1?label=Tests&amp;message=example%20source&amp;labelColor=1E293B&amp;color=0F766E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-policy-evaluation/README.md#certification-status"><img alt="Certification: not certified" src="https://img.shields.io/static/v1?label=Certification&amp;message=not%20certified&amp;labelColor=1E293B&amp;color=92400E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/tools/readme/POLICY.md"><img alt="Governance: repository policy" src="https://img.shields.io/static/v1?label=Governance&amp;message=repository%20policy&amp;labelColor=1E293B&amp;color=4338CA"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="Evidence: source and CI" src="https://img.shields.io/static/v1?label=Evidence&amp;message=source%20and%20CI&amp;labelColor=1E293B&amp;color=6D28D9"></a>
</p>
<p align="center"><a href="#overview">Overview</a> · <a href="#installation">Installation</a> · <a href="#quick-start">Quick Start</a> · <a href="#usage">Usage</a> · <a href="#public-api-and-import-surfaces">API</a> · <a href="#contributing">Contributing</a> · <a href="#governance">Governance</a> · <a href="#license">License</a></p>
<!-- readme-standards:end branding -->

---

## Overview

### Summary

Layer-40 protocol-neutral composition for policy evaluation, batch evaluation,
entity search, and effective policy-service description.

- Package: `tba-capability-policy-evaluation`
- Layer: `040-capabilities`
- Responsibility: Composable protocol-neutral policy evaluation and entity-search capability.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-policy-evaluation/src/tba_capability_policy_evaluation/__init__.py).
- Distribution: Python package on PyPI.

### Why This Package

`tba-capability-policy-evaluation` isolates this responsibility: Composable protocol-neutral policy evaluation and entity-search capability. Its [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-policy-evaluation/src/tba_capability_policy_evaluation/__init__.py) exposes `DescriptionTarget`, `EntitySearchTarget`, `EvaluationTarget`, `PolicyEvaluationCapability`, allowing consumers to select this package without treating adjacent packages as part of its public contract.

### When to Use

Choose `tba-capability-policy-evaluation` for this responsibility: Composable protocol-neutral policy evaluation and entity-search capability. Its `040-capabilities` placement keeps use-case orchestration through explicit collaborators separate from HTTP wire schemas, direct table ownership, or hidden provider selection.

### Features

- `PolicyEvaluationCapability`: Expose one normalized policy decision point through reportable operations.

### Non-Goals

This package does not parse AuthZEN or XACML messages, choose HTTP paths,
authenticate callers, own policy state, open sessions, or implement a policy
decision algorithm.

---

## Getting Started

### Prerequisites

Python `>=3.10,<3.16` is required. The [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-policy-evaluation/pyproject.toml) declares runtime dependencies including `tba-concrete-capability`, `tba-contracts-identity`. Read the example’s inputs and service requirements before execution.

### Installation

Install the selected PyPI release of `tba-capability-policy-evaluation`:

```bash
uv pip install tba-capability-policy-evaluation
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/040-capabilities/tba-capability-policy-evaluation
```

#### uv

<!-- readme-standards:begin installation.uv -->
```bash
uv add tba-capability-policy-evaluation
```
<!-- readme-standards:end installation.uv -->

#### pip

<!-- readme-standards:begin installation.pip -->
```bash
python -m pip install tba-capability-policy-evaluation
```
<!-- readme-standards:end installation.pip -->

#### Poetry

<!-- readme-standards:begin installation.poetry -->
```bash
poetry add tba-capability-policy-evaluation
```
<!-- readme-standards:end installation.poetry -->

### Quick Start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.


```bash
uv run --isolated --no-project --python 3.12 --with "tba-capability-policy-evaluation==0.4.0.dev3" python quickstart.py
```

The import and assertion succeed when the PolicyEvaluationCapability entry point is available.

#### Example

<!-- readme-standards:begin example.quick-start -->
Source: [docs/readme/quick_start.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-policy-evaluation/docs/readme/quick_start.py).

```python
from tba_capability_policy_evaluation import PolicyEvaluationCapability

assert callable(PolicyEvaluationCapability)
```
<!-- readme-standards:end example.quick-start -->

#### Expected Result

The example demonstrates the documented `tba-capability-policy-evaluation` source boundary or workflow. Complete its required configuration first. README CI checks the maintained source’s syntax and declarations; it does not claim that external services or the application workflow were exercised.

---

## Usage

### Common Workflows

<!-- readme-standards:begin example.usage -->
Source: [docs/readme/usage.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-policy-evaluation/docs/readme/usage.py).

```python
from tba_capability_policy_evaluation import PolicyEvaluationCapability

assert callable(PolicyEvaluationCapability)
```
<!-- readme-standards:end example.usage -->

The following public-entry-point example belongs to `tba-capability-policy-evaluation`. Composable protocol-neutral policy evaluation and entity-search capability. Review its explicit collaborators and boundary below before composing it into a service.

### Configuration

Configure `tba-capability-policy-evaluation` through the APIs in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-policy-evaluation/src/tba_capability_policy_evaluation/__init__.py); its [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-policy-evaluation/pyproject.toml) describes installation requirements, not an implicit service configuration. No additional package-global configuration contract is inferred from dependencies.

### Error Handling

The inspected `tba-capability-policy-evaluation` source raises `NotImplementedError`, `TypeError`. Handle these at the calling boundary and consult the implementation for the triggering conditions.

### Best Practices

Use the explicit `tba-capability-policy-evaluation` imports documented below and keep collaborator configuration with the caller. Run the package’s relevant tests after changing `DescriptionTarget`, `EntitySearchTarget`, `EvaluationTarget`, `PolicyEvaluationCapability`; an import or successful installation alone does not establish its runtime guarantees.

---

## Package Boundary

### What It Owns

`tba-capability-policy-evaluation` belongs to `040-capabilities` and owns use-case orchestration through explicit collaborators: Composable protocol-neutral policy evaluation and entity-search capability.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-policy-evaluation/src/tba_capability_policy_evaluation/__init__.py). Public exports include `DescriptionTarget`, `EntitySearchTarget`, `EvaluationTarget`, `PolicyEvaluationCapability`.

Keep HTTP wire schemas, direct table ownership, or hidden provider selection in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

### Public API and Import Surfaces

Import namespace: `tba_capability_policy_evaluation`.

Source-declared exports or types: `DescriptionTarget`, `EntitySearchTarget`, `EvaluationTarget`, `PolicyEvaluationCapability`.

Inspect [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-policy-evaluation/src/tba_capability_policy_evaluation/__init__.py) for exact signatures; this inventory does not designate every internal module as stable.

### Entry Points

<!-- readme-standards:begin entry-points -->
This package declares no command-line, GUI, or plugin entry points in its manifest.
<!-- readme-standards:end entry-points -->

### Injected Dependencies

A policy evaluation callable is required. Entity search and service-description
callables are optional. The targets are supplied by layer-10/20 implementations
or layer-60 composition; this package does not construct an evaluator.

### Protocol Consumers

The layer-50 AuthZEN package maps Authorization API 1.0 evaluation, batch,
search, and PDP-metadata requirements to these operations. XACML adapters may
consume the same normalized capability through their own versioned mappings.

### Extensions

For `tba-capability-policy-evaluation`, use the source-declared public interfaces (`DescriptionTarget`, `EntitySearchTarget`, `EvaluationTarget`, `PolicyEvaluationCapability`) when composing or extending behavior. Its entry-point section below is authoritative for registered plugins; no additional extension loader is inferred from the package name.

---

## Operations and Readiness

### Operational Requirements

`evaluate` is required. `evaluate_many` is available as an order-preserving
composition of `evaluate`. `search_entities` and `describe` are optional and
are reported unavailable when their targets are not bound. Readiness follows
the required evaluation target.

### Health and Observability

This README does not establish a standalone health endpoint for `tba-capability-policy-evaluation`. Observe the concrete caller’s results, exceptions, and existing test reports. An application that embeds this package must define its own health and telemetry contract.

### Security and Resource Limits

Apply the input, credential, and resource constraints implemented in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-policy-evaluation/src/tba_capability_policy_evaluation/__init__.py). The `tba-capability-policy-evaluation` README gate is a documentation check, not a security review or a substitute for the implementation’s limits and caller authorization.

### Compatibility

This source version of `tba-capability-policy-evaluation` declares Python `>=3.10,<3.16`. Consult its dependency constraints before upgrading. Source-version and registry-version badges have separate meanings; this migration makes no additional platform or interoperability certification claim.

---

## Verification

### Tests

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-policy-evaluation/src/tba_capability_policy_evaluation/__init__.py).

### Certification Status

No external certification is asserted for `tba-capability-policy-evaluation` by this documentation migration. README conformance, example syntax, runtime tests, and protocol or security certification are distinct evidence scopes.

### Evidence

The [README standards CI](https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml) records mechanical documentation results for its tested commit. The [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-policy-evaluation/src/tba_capability_policy_evaluation/__init__.py) and example sources support the package-boundary description; external runtime behavior requires its own test evidence.

---

## FAQ

### Why

**Why select this package?** `tba-capability-policy-evaluation` provides composable protocol-neutral policy evaluation and entity-search capability; use its own API boundary rather than assuming neighboring packages are bundled or configured automatically.

### How

**How do I start?** Install or synchronize the environment under Getting Started, follow the maintained example for `tba-capability-policy-evaluation`, and consult [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-policy-evaluation/src/tba_capability_policy_evaluation/__init__.py) for the exact types and signatures involved.

### When

**When should I validate an upgrade?** Recheck `tba-capability-policy-evaluation` whenever its source version, declared collaborators, configuration, or caller changes. Run relevant behavioral tests in addition to the README gate before promotion.

---

## Documentation and Related Packages

### More Documentation

The [repository contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md), [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-policy-evaluation/src/tba_capability_policy_evaluation/__init__.py), and [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-policy-evaluation/pyproject.toml) provide the supporting context for `tba-capability-policy-evaluation`. The [README policy](https://github.com/groupsum/readme-standards/blob/master/docs/outline.md) defines the common document structure.

### Related Packages

Declared local runtime dependencies:

- [tba-concrete-capability](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-capability/README.md)
- [tba-contracts-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-identity/README.md)

Direct downstream consumers:

- [tba-protocol-authzen](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-authzen/README.md)

### Project Links

<!-- readme-standards:begin project-links -->
- [Documentation](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/040-capabilities/tba-capability-policy-evaluation#readme)
- [Homepage](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/040-capabilities/tba-capability-policy-evaluation#readme)
- [Issues](https://github.com/tigrbl/tigrbl_auth/issues)
- [PyPI](https://pypi.org/project/tba-capability-policy-evaluation/)
- [Repository](https://github.com/tigrbl/tigrbl_auth)
- [Source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/040-capabilities/tba-capability-policy-evaluation)
- [pypi: tba-capability-policy-evaluation](https://pypi.org/project/tba-capability-policy-evaluation/)
<!-- readme-standards:end project-links -->

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/040-capabilities/tba-capability-policy-evaluation)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-policy-evaluation/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-policy-evaluation/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-policy-evaluation/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-capability-policy-evaluation/)

---

## Contributing

### How to Contribute

Follow the [contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md) and include a focused example or regression for changes to `tba-capability-policy-evaluation`. Keep package behavior, its documented boundary, and its tests aligned.

### Development Setup

Work from the `pkgs/040-capabilities/tba-capability-policy-evaluation` checkout. Synchronize its declared development environment with uv, then run the relevant package tests and `python -m pytest docs/readme/test_examples.py`. The repository’s dedicated README job installs `readme-standards==0.1.3` without resolving unrelated runtime packages.

### Notes for Maintainers

Edit authored prose directly in this `tba-capability-policy-evaluation` README. Update source examples in `docs/readme/`, then run `readme-standards render --root . --write` from the package directory and review the diff. Required headings and generated blocks come from package-guide-v1.

---

## Governance

### Ownership and Decision Making

Changes to `tba-capability-policy-evaluation` follow the maintainer review process of [tigrbl/tigrbl_auth](https://github.com/tigrbl/tigrbl_auth) and its contribution guide. Author attribution remains in the [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-policy-evaluation/pyproject.toml); this README does not assign new publishing or administrative authority.

### Standards and Policies

`tba-capability-policy-evaluation` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `040-capabilities` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

### Lifecycle and Migration

The `tba-capability-policy-evaluation` source version is `0.4.0.dev3`. This change standardizes documentation and adds a development-only gate; it does not publish a new runtime version or declare a previously unpublished package released. Preserve explicit deprecation and replacement instructions where present.

---

## License and Attribution

### License

<!-- readme-standards:begin license -->
Licensed under `Apache-2.0`. See [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-policy-evaluation/LICENSE).
<!-- readme-standards:end license -->

### Notices

<!-- readme-standards:begin notices -->
See [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-policy-evaluation/NOTICE) for attribution.
<!-- readme-standards:end notices -->
