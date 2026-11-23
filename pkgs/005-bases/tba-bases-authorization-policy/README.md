# tba-bases-authorization-policy

<!-- readme-standards:begin branding -->
<p align="center"><a href="https://github.com/tigrbl/tigrbl_auth"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="300"></a></p>
<p align="center"><strong>tba-bases-authorization-policy</strong></p>
<p align="center">Base classes for concrete TBAorization policy implementations.</p>
<p align="center">
<a href="https://pypi.org/project/tba-bases-authorization-policy/"><img alt="pypi: tba-bases-authorization-policy" src="https://img.shields.io/pypi/v/tba-bases-authorization-policy?labelColor=1E293B&amp;color=1D4ED8"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-authorization-policy/pyproject.toml"><img alt="Source version: 0.4.0.dev3" src="https://img.shields.io/static/v1?label=Source%20version&amp;message=0.4.0.dev3&amp;labelColor=1E293B&amp;color=4338CA"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-authorization-policy/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/static/v1?label=Python&amp;message=%3E%3D3.10%2C%3C3.16&amp;labelColor=1E293B&amp;color=0F766E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-authorization-policy/pyproject.toml"><img alt="Layer: 005-bases" src="https://img.shields.io/static/v1?label=Layer&amp;message=005-bases&amp;labelColor=1E293B&amp;color=6D28D9"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-authorization-policy/README.md#lifecycle-and-migration"><img alt="Lifecycle: active" src="https://img.shields.io/static/v1?label=Lifecycle&amp;message=active&amp;labelColor=1E293B&amp;color=166534"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-authorization-policy/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/static/v1?label=License&amp;message=Apache-2.0&amp;labelColor=1E293B&amp;color=86198F"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-authorization-policy/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/static/v1?label=Notice&amp;message=attribution&amp;labelColor=1E293B&amp;color=86198F"></a>
</p>
<p align="center">
<a href="https://pypi.org/project/tba-bases-authorization-policy/"><img alt="Monthly PyPI downloads: tba-bases-authorization-policy" src="https://img.shields.io/pypi/dm/tba-bases-authorization-policy?labelColor=1E293B&amp;color=0E7490"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-authorization-policy/README.md"><img alt="README hits: tba-bases-authorization-policy" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/pkgs/005-bases/tba-bases-authorization-policy/README.md.svg?label=README%20hits&amp;labelColor=1E293B&amp;color=0E7490"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="README standards: CI gate" src="https://img.shields.io/static/v1?label=README%20standards&amp;message=CI%20gate&amp;labelColor=1E293B&amp;color=1D4ED8"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-authorization-policy/docs/readme/test_examples.py"><img alt="Tests: example source" src="https://img.shields.io/static/v1?label=Tests&amp;message=example%20source&amp;labelColor=1E293B&amp;color=0F766E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-authorization-policy/README.md#certification-status"><img alt="Certification: not certified" src="https://img.shields.io/static/v1?label=Certification&amp;message=not%20certified&amp;labelColor=1E293B&amp;color=92400E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/tools/readme/POLICY.md"><img alt="Governance: repository policy" src="https://img.shields.io/static/v1?label=Governance&amp;message=repository%20policy&amp;labelColor=1E293B&amp;color=4338CA"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="Evidence: source and CI" src="https://img.shields.io/static/v1?label=Evidence&amp;message=source%20and%20CI&amp;labelColor=1E293B&amp;color=6D28D9"></a>
</p>
<p align="center"><a href="#overview">Overview</a> · <a href="#installation">Installation</a> · <a href="#quick-start">Quick Start</a> · <a href="#usage">Usage</a> · <a href="#public-api-and-import-surfaces">API</a> · <a href="#contributing">Contributing</a> · <a href="#governance">Governance</a> · <a href="#license">License</a></p>
<!-- readme-standards:end branding -->

---

## Overview

### Summary

Base classes connecting policy implementations to authorization contracts.

- Package: `tba-bases-authorization-policy`
- Layer: `005-bases`
- Responsibility: Base classes for concrete TBAorization policy implementations.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-authorization-policy/src/tba_bases_authorization_policy/__init__.py).
- Distribution: Python package on PyPI.

### Why This Package

`tba-bases-authorization-policy` isolates this responsibility: Base classes for concrete TBAorization policy implementations. Its [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-authorization-policy/src/tba_bases_authorization_policy/__init__.py) exposes `AdviceHandlerBase`, `AttributeResolverBase`, `AttributeSelectorBase`, `AuthzenEvaluationAdapterBase`, `AuthzenSearchAdapterBase`, `ConditionEvaluatorBase`, `ObligationHandlerBase`, `PolicyCombinerBase`, `PolicyRuleBase`, `RuleEvaluatorBase`, `ScopeMatcherBase`, `XacmlRequestMapperBase`, `XacmlResponseMapperBase`, allowing consumers to select this package without treating adjacent packages as part of its public contract.

### When to Use

Choose `tba-bases-authorization-policy` for this responsibility: Base classes for concrete TBAorization policy implementations. Its `005-bases` placement keeps reusable component bases separate from deployment composition or implicit provider selection.

### Features

- `ScopeMatcherBase`: declared in src/tba_bases_authorization_policy/__init__.py
- `PolicyRuleBase`: Base for concrete policy-rule dataclasses.
- `AttributeResolverBase`: declared in src/tba_bases_authorization_policy/__init__.py
- `AttributeSelectorBase`: declared in src/tba_bases_authorization_policy/__init__.py
- `PolicyCombinerBase`: declared in src/tba_bases_authorization_policy/__init__.py
- `ConditionEvaluatorBase`: declared in src/tba_bases_authorization_policy/__init__.py
- `RuleEvaluatorBase`: declared in src/tba_bases_authorization_policy/__init__.py
- `ObligationHandlerBase`: declared in src/tba_bases_authorization_policy/__init__.py

### Non-Goals

`tba-bases-authorization-policy` does not take ownership of deployment composition or implicit provider selection.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

---

## Getting Started

### Prerequisites

Python `>=3.10,<3.16` is required. The [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-authorization-policy/pyproject.toml) declares runtime dependencies including `tba-contracts-identity`. Read the example’s inputs and service requirements before execution.

### Installation

Install the selected PyPI release of `tba-bases-authorization-policy`:

```bash
uv pip install tba-bases-authorization-policy
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/005-bases/tba-bases-authorization-policy
```

#### uv

<!-- readme-standards:begin installation.uv -->
```bash
uv add tba-bases-authorization-policy
```
<!-- readme-standards:end installation.uv -->

#### pip

<!-- readme-standards:begin installation.pip -->
```bash
python -m pip install tba-bases-authorization-policy
```
<!-- readme-standards:end installation.pip -->

#### Poetry

<!-- readme-standards:begin installation.poetry -->
```bash
poetry add tba-bases-authorization-policy
```
<!-- readme-standards:end installation.poetry -->

### Quick Start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.


```bash
uv run --isolated --no-project --python 3.12 --with "tba-bases-authorization-policy==0.4.0.dev3" python quickstart.py
```

The import and assertion succeed when the ScopeMatcherBase entry point is available.

#### Example

<!-- readme-standards:begin example.quick-start -->
Source: [docs/readme/quick_start.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-authorization-policy/docs/readme/quick_start.py).

```python
from tba_bases_authorization_policy import ScopeMatcherBase

assert callable(ScopeMatcherBase)
```
<!-- readme-standards:end example.quick-start -->

#### Expected Result

The example demonstrates the documented `tba-bases-authorization-policy` source boundary or workflow. Complete its required configuration first. README CI checks the maintained source’s syntax and declarations; it does not claim that external services or the application workflow were exercised.

---

## Usage

### Common Workflows

<!-- readme-standards:begin example.usage -->
Source: [docs/readme/usage.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-authorization-policy/docs/readme/usage.py).

```python
from tba_bases_authorization_policy import ScopeMatcherBase

assert callable(ScopeMatcherBase)
```
<!-- readme-standards:end example.usage -->

The following public-entry-point example belongs to `tba-bases-authorization-policy`. Base classes for concrete TBAorization policy implementations. Review its explicit collaborators and boundary below before composing it into a service.

### Configuration

Configure `tba-bases-authorization-policy` through the APIs in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-authorization-policy/src/tba_bases_authorization_policy/__init__.py); its [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-authorization-policy/pyproject.toml) describes installation requirements, not an implicit service configuration. No additional package-global configuration contract is inferred from dependencies.

### Error Handling

The inspected `tba-bases-authorization-policy` source does not establish a package-wide exception hierarchy. Preserve errors from its declared dependencies and validate inputs using the specific public contract in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-authorization-policy/src/tba_bases_authorization_policy/__init__.py).

### Best Practices

Use the explicit `tba-bases-authorization-policy` imports documented below and keep collaborator configuration with the caller. Run the package’s relevant tests after changing `AdviceHandlerBase`, `AttributeResolverBase`, `AttributeSelectorBase`, `AuthzenEvaluationAdapterBase`, `AuthzenSearchAdapterBase`, `ConditionEvaluatorBase`, `ObligationHandlerBase`, `PolicyCombinerBase`, `PolicyRuleBase`, `RuleEvaluatorBase`, `ScopeMatcherBase`, `XacmlRequestMapperBase`, `XacmlResponseMapperBase`; an import or successful installation alone does not establish its runtime guarantees.

---

## Package Boundary

### What It Owns

`tba-bases-authorization-policy` belongs to `005-bases` and owns reusable component bases: Base classes for concrete TBAorization policy implementations.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-authorization-policy/src/tba_bases_authorization_policy/__init__.py). Public exports include `AdviceHandlerBase`, `AuthzenEvaluationAdapterBase`, `AuthzenSearchAdapterBase`, `AttributeResolverBase`, `AttributeSelectorBase`, `ConditionEvaluatorBase`, `ObligationHandlerBase`, `PolicyCombinerBase`, `PolicyRuleBase`, `RuleEvaluatorBase`, `ScopeMatcherBase`, `XacmlRequestMapperBase`.

Keep deployment composition or implicit provider selection in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

### Public API and Import Surfaces

Import namespace: `tba_bases_authorization_policy`.

Source-declared exports or types: `AdviceHandlerBase`, `AttributeResolverBase`, `AttributeSelectorBase`, `AuthzenEvaluationAdapterBase`, `AuthzenSearchAdapterBase`, `ConditionEvaluatorBase`, `ObligationHandlerBase`, `PolicyCombinerBase`, `PolicyRuleBase`, `RuleEvaluatorBase`, `ScopeMatcherBase`, `XacmlRequestMapperBase`, `XacmlResponseMapperBase`.

Inspect [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-authorization-policy/src/tba_bases_authorization_policy/__init__.py) for exact signatures; this inventory does not designate every internal module as stable.

### Entry Points

<!-- readme-standards:begin entry-points -->
This package declares no command-line, GUI, or plugin entry points in its manifest.
<!-- readme-standards:end entry-points -->

### Injected Dependencies

The [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-authorization-policy/src/tba_bases_authorization_policy/__init__.py) for `tba-bases-authorization-policy` does not declare an explicit service-constructor or keyword-only factory hook in the inspected source. Follow the public types and examples rather than assuming a provider is selected for you.

Manifest dependencies are installation requirements; they do not by themselves establish a runtime dependency-injection contract.

### Protocol Consumers

Direct consumers in this checkout’s package manifests include `tba-concrete-authorization-policy-attributes-mapping`, `tba-concrete-authorization-policy-combiner-default`, `tba-concrete-authorization-policy-evaluators-default`, `tba-concrete-authorization-policy-obligations`, `tba-concrete-authorization-policy-rules`, `tba-concrete-authorization-scope-set-matcher`, `tba-workspace`. These edges describe declared dependencies, not protocol-conformance evidence.

### Extensions

For `tba-bases-authorization-policy`, use the source-declared public interfaces (`AdviceHandlerBase`, `AttributeResolverBase`, `AttributeSelectorBase`, `AuthzenEvaluationAdapterBase`, `AuthzenSearchAdapterBase`, `ConditionEvaluatorBase`, `ObligationHandlerBase`, `PolicyCombinerBase`, `PolicyRuleBase`, `RuleEvaluatorBase`, `ScopeMatcherBase`, `XacmlRequestMapperBase`, `XacmlResponseMapperBase`) when composing or extending behavior. Its entry-point section below is authoritative for registered plugins; no additional extension loader is inferred from the package name.

---

## Operations and Readiness

### Operational Requirements

`tba-bases-authorization-policy` exposes reusable component bases. Public operations found in its source:

- `ScopeMatcherBase.match` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-authorization-policy/src/tba_bases_authorization_policy/__init__.py).
- `AttributeResolverBase.resolve` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-authorization-policy/src/tba_bases_authorization_policy/__init__.py).
- `AttributeSelectorBase.select` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-authorization-policy/src/tba_bases_authorization_policy/__init__.py).
- `PolicyCombinerBase.combine` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-authorization-policy/src/tba_bases_authorization_policy/__init__.py).
- `ConditionEvaluatorBase.evaluate_condition` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-authorization-policy/src/tba_bases_authorization_policy/__init__.py).
- `RuleEvaluatorBase.evaluate_rule` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-authorization-policy/src/tba_bases_authorization_policy/__init__.py).
- `ObligationHandlerBase.handle_obligation` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-authorization-policy/src/tba_bases_authorization_policy/__init__.py).
- `AdviceHandlerBase.handle_advice` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-authorization-policy/src/tba_bases_authorization_policy/__init__.py).
- `AuthzenEvaluationAdapterBase.evaluate` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-authorization-policy/src/tba_bases_authorization_policy/interop.py).
- `AuthzenSearchAdapterBase.search` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-authorization-policy/src/tba_bases_authorization_policy/interop.py).
- `XacmlRequestMapperBase.map_request` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-authorization-policy/src/tba_bases_authorization_policy/interop.py).
- `XacmlResponseMapperBase.map_response` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-authorization-policy/src/tba_bases_authorization_policy/interop.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

### Health and Observability

This README does not establish a standalone health endpoint for `tba-bases-authorization-policy`. Observe the concrete caller’s results, exceptions, and existing test reports. An application that embeds this package must define its own health and telemetry contract.

### Security and Resource Limits

Apply the input, credential, and resource constraints implemented in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-authorization-policy/src/tba_bases_authorization_policy/__init__.py). The `tba-bases-authorization-policy` README gate is a documentation check, not a security review or a substitute for the implementation’s limits and caller authorization.

### Compatibility

This source version of `tba-bases-authorization-policy` declares Python `>=3.10,<3.16`. Consult its dependency constraints before upgrading. Source-version and registry-version badges have separate meanings; this migration makes no additional platform or interoperability certification claim.

---

## Verification

### Tests

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-authorization-policy/src/tba_bases_authorization_policy/__init__.py).

### Certification Status

No external certification is asserted for `tba-bases-authorization-policy` by this documentation migration. README conformance, example syntax, runtime tests, and protocol or security certification are distinct evidence scopes.

### Evidence

The [README standards CI](https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml) records mechanical documentation results for its tested commit. The [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-authorization-policy/src/tba_bases_authorization_policy/__init__.py) and example sources support the package-boundary description; external runtime behavior requires its own test evidence.

---

## FAQ

### Why

**Why select this package?** `tba-bases-authorization-policy` provides base classes for concrete TBAorization policy implementations; use its own API boundary rather than assuming neighboring packages are bundled or configured automatically.

### How

**How do I start?** Install or synchronize the environment under Getting Started, follow the maintained example for `tba-bases-authorization-policy`, and consult [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-authorization-policy/src/tba_bases_authorization_policy/__init__.py) for the exact types and signatures involved.

### When

**When should I validate an upgrade?** Recheck `tba-bases-authorization-policy` whenever its source version, declared collaborators, configuration, or caller changes. Run relevant behavioral tests in addition to the README gate before promotion.

---

## Documentation and Related Packages

### More Documentation

The [repository contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md), [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-authorization-policy/src/tba_bases_authorization_policy/__init__.py), and [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-authorization-policy/pyproject.toml) provide the supporting context for `tba-bases-authorization-policy`. The [README policy](https://github.com/groupsum/readme-standards/blob/master/docs/outline.md) defines the common document structure.

### Related Packages

Declared local runtime dependencies:

- [tba-contracts-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-identity/README.md)

Direct downstream consumers:

- [tba-concrete-authorization-policy-attributes-mapping](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-authorization-policy-attributes-mapping/README.md)
- [tba-concrete-authorization-policy-combiner-default](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-authorization-policy-combiner-default/README.md)
- [tba-concrete-authorization-policy-evaluators-default](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-authorization-policy-evaluators-default/README.md)
- [tba-concrete-authorization-policy-obligations](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-authorization-policy-obligations/README.md)
- [tba-concrete-authorization-policy-rules](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-authorization-policy-rules/README.md)
- [tba-concrete-authorization-scope-set-matcher](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-authorization-scope-set-matcher/README.md)

### Project Links

<!-- readme-standards:begin project-links -->
- [Documentation](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/005-bases/tba-bases-authorization-policy#readme)
- [Homepage](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/005-bases/tba-bases-authorization-policy#readme)
- [Issues](https://github.com/tigrbl/tigrbl_auth/issues)
- [PyPI](https://pypi.org/project/tba-bases-authorization-policy/)
- [Repository](https://github.com/tigrbl/tigrbl_auth)
- [Source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/005-bases/tba-bases-authorization-policy)
- [pypi: tba-bases-authorization-policy](https://pypi.org/project/tba-bases-authorization-policy/)
<!-- readme-standards:end project-links -->

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/005-bases/tba-bases-authorization-policy)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-authorization-policy/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-authorization-policy/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-authorization-policy/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-bases-authorization-policy/)

---

## Contributing

### How to Contribute

Follow the [contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md) and include a focused example or regression for changes to `tba-bases-authorization-policy`. Keep package behavior, its documented boundary, and its tests aligned.

### Development Setup

Work from the `pkgs/005-bases/tba-bases-authorization-policy` checkout. Synchronize its declared development environment with uv, then run the relevant package tests and `python -m pytest docs/readme/test_examples.py`. The repository’s dedicated README job installs `readme-standards==0.1.3` without resolving unrelated runtime packages.

### Notes for Maintainers

Edit authored prose directly in this `tba-bases-authorization-policy` README. Update source examples in `docs/readme/`, then run `readme-standards render --root . --write` from the package directory and review the diff. Required headings and generated blocks come from package-guide-v1.

---

## Governance

### Ownership and Decision Making

Changes to `tba-bases-authorization-policy` follow the maintainer review process of [tigrbl/tigrbl_auth](https://github.com/tigrbl/tigrbl_auth) and its contribution guide. Author attribution remains in the [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-authorization-policy/pyproject.toml); this README does not assign new publishing or administrative authority.

### Standards and Policies

`tba-bases-authorization-policy` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `005-bases` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

### Lifecycle and Migration

The `tba-bases-authorization-policy` source version is `0.4.0.dev3`. This change standardizes documentation and adds a development-only gate; it does not publish a new runtime version or declare a previously unpublished package released. Preserve explicit deprecation and replacement instructions where present.

---

## License and Attribution

### License

<!-- readme-standards:begin license -->
Licensed under `Apache-2.0`. See [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-authorization-policy/LICENSE).
<!-- readme-standards:end license -->

### Notices

<!-- readme-standards:begin notices -->
See [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-authorization-policy/NOTICE) for attribution.
<!-- readme-standards:end notices -->
