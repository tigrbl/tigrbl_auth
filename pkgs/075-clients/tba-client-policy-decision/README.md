# tba-client-policy-decision

<!-- readme-standards:begin branding -->
<p align="center"><a href="https://github.com/tigrbl/tigrbl_auth"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="300"></a></p>
<p align="center"><strong>tba-client-policy-decision</strong></p>
<p align="center">Typed client for platform authorization decisions.</p>
<p align="center">
<a href="https://pypi.org/project/tba-client-policy-decision/"><img alt="pypi: tba-client-policy-decision" src="https://img.shields.io/pypi/v/tba-client-policy-decision?labelColor=1E293B&amp;color=1D4ED8"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/075-clients/tba-client-policy-decision/pyproject.toml"><img alt="Source version: 0.4.0.dev4" src="https://img.shields.io/static/v1?label=Source%20version&amp;message=0.4.0.dev4&amp;labelColor=1E293B&amp;color=4338CA"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/075-clients/tba-client-policy-decision/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/static/v1?label=Python&amp;message=%3E%3D3.10%2C%3C3.16&amp;labelColor=1E293B&amp;color=0F766E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/075-clients/tba-client-policy-decision/pyproject.toml"><img alt="Layer: 075-clients" src="https://img.shields.io/static/v1?label=Layer&amp;message=075-clients&amp;labelColor=1E293B&amp;color=6D28D9"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/075-clients/tba-client-policy-decision/README.md#lifecycle-and-migration"><img alt="Lifecycle: active" src="https://img.shields.io/static/v1?label=Lifecycle&amp;message=active&amp;labelColor=1E293B&amp;color=166534"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/075-clients/tba-client-policy-decision/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/static/v1?label=License&amp;message=Apache-2.0&amp;labelColor=1E293B&amp;color=86198F"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/075-clients/tba-client-policy-decision/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/static/v1?label=Notice&amp;message=attribution&amp;labelColor=1E293B&amp;color=86198F"></a>
</p>
<p align="center">
<a href="https://pypi.org/project/tba-client-policy-decision/"><img alt="Monthly PyPI downloads: tba-client-policy-decision" src="https://img.shields.io/pypi/dm/tba-client-policy-decision?labelColor=1E293B&amp;color=0E7490"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/075-clients/tba-client-policy-decision/README.md"><img alt="README hits: tba-client-policy-decision" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/pkgs/075-clients/tba-client-policy-decision/README.md.svg?label=README%20hits&amp;labelColor=1E293B&amp;color=0E7490"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="README standards: CI gate" src="https://img.shields.io/static/v1?label=README%20standards&amp;message=CI%20gate&amp;labelColor=1E293B&amp;color=1D4ED8"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/075-clients/tba-client-policy-decision/docs/readme/test_examples.py"><img alt="Tests: example source" src="https://img.shields.io/static/v1?label=Tests&amp;message=example%20source&amp;labelColor=1E293B&amp;color=0F766E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/075-clients/tba-client-policy-decision/README.md#certification-status"><img alt="Certification: not certified" src="https://img.shields.io/static/v1?label=Certification&amp;message=not%20certified&amp;labelColor=1E293B&amp;color=92400E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/tools/readme/POLICY.md"><img alt="Governance: repository policy" src="https://img.shields.io/static/v1?label=Governance&amp;message=repository%20policy&amp;labelColor=1E293B&amp;color=4338CA"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="Evidence: source and CI" src="https://img.shields.io/static/v1?label=Evidence&amp;message=source%20and%20CI&amp;labelColor=1E293B&amp;color=6D28D9"></a>
</p>
<p align="center"><a href="#overview">Overview</a> · <a href="#installation">Installation</a> · <a href="#quick-start">Quick Start</a> · <a href="#usage">Usage</a> · <a href="#public-api-and-import-surfaces">API</a> · <a href="#contributing">Contributing</a> · <a href="#governance">Governance</a> · <a href="#license">License</a></p>
<!-- readme-standards:end branding -->

---

## Overview

### Summary

Call a policy decision point through a transport you supply.

- Package: `tba-client-policy-decision`
- Layer: `075-clients`
- Responsibility: Typed client for platform authorization decisions.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/075-clients/tba-client-policy-decision/src/tba_client_policy_decision/__init__.py).
- Distribution: Python package on PyPI.

### Why This Package

`tba-client-policy-decision` isolates this responsibility: Typed client for platform authorization decisions. Its [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/075-clients/tba-client-policy-decision/src/tba_client_policy_decision/__init__.py) exposes `PolicyDecisionClient`, allowing consumers to select this package without treating adjacent packages as part of its public contract.

### When to Use

Inject a callable that accepts a decision request mapping and returns a result mapping. The adapter owns network authentication, serialization, retries, and error handling. This example uses an in-process stub for one decision.

### Features

- `PolicyDecisionClient`: declared in src/tba_client_policy_decision/__init__.py

### Non-Goals

`tba-client-policy-decision` does not take ownership of authority-side policy decisions or server-owned persistence.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

---

## Getting Started

### Prerequisites

Python `>=3.10,<3.16` is required. The [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/075-clients/tba-client-policy-decision/pyproject.toml) declares runtime dependencies including `tba-contracts-authorization`. Read the example’s inputs and service requirements before execution.

### Installation

Install the selected PyPI release of `tba-client-policy-decision`:

```bash
uv pip install tba-client-policy-decision
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/075-clients/tba-client-policy-decision
```

#### uv

<!-- readme-standards:begin installation.uv -->
```bash
uv add tba-client-policy-decision
```
<!-- readme-standards:end installation.uv -->

#### pip

<!-- readme-standards:begin installation.pip -->
```bash
python -m pip install tba-client-policy-decision
```
<!-- readme-standards:end installation.pip -->

#### Poetry

<!-- readme-standards:begin installation.poetry -->
```bash
poetry add tba-client-policy-decision
```
<!-- readme-standards:end installation.poetry -->

### Quick Start

Install the version used by this example.

```bash
python -m pip install "tba-client-policy-decision==0.4.0.dev4"
```

Save the following as `quickstart.py` and run `python quickstart.py`. The assertions should pass.

#### Example

<!-- readme-standards:begin example.quick-start -->
Source: [docs/readme/quick_start.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/075-clients/tba-client-policy-decision/docs/readme/quick_start.py).

```python
from tba_client_policy_decision import PolicyDecisionClient

client = PolicyDecisionClient(
    request=lambda payload: {"allowed": payload["action"] == "read"}
)
assert client.decide({"action": "read"}) == {"allowed": True}
assert client.decide({"action": "write"}) == {"allowed": False}
```
<!-- readme-standards:end example.quick-start -->

#### Expected Result

The example demonstrates the documented `tba-client-policy-decision` source boundary or workflow. Complete its required configuration first. README CI checks the maintained source’s syntax and declarations; it does not claim that external services or the application workflow were exercised.

---

## Usage

### Common Workflows

<!-- readme-standards:begin example.usage -->
Source: [docs/readme/usage.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/075-clients/tba-client-policy-decision/docs/readme/usage.py).

```python
from tba_client_policy_decision import PolicyDecisionClient

client = PolicyDecisionClient(
    request=lambda payload: {"allowed": payload["action"] == "read"}
)
assert client.decide({"action": "read"}) == {"allowed": True}
assert client.decide({"action": "write"}) == {"allowed": False}
```
<!-- readme-standards:end example.usage -->

The following public-entry-point example belongs to `tba-client-policy-decision`. Typed client for platform authorization decisions. Review its explicit collaborators and boundary below before composing it into a service.

### Configuration

Configure `tba-client-policy-decision` through the APIs in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/075-clients/tba-client-policy-decision/src/tba_client_policy_decision/__init__.py); its [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/075-clients/tba-client-policy-decision/pyproject.toml) describes installation requirements, not an implicit service configuration. No additional package-global configuration contract is inferred from dependencies.

### Error Handling

The inspected `tba-client-policy-decision` source does not establish a package-wide exception hierarchy. Preserve errors from its declared dependencies and validate inputs using the specific public contract in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/075-clients/tba-client-policy-decision/src/tba_client_policy_decision/__init__.py).

### Best Practices

Use the explicit `tba-client-policy-decision` imports documented below and keep collaborator configuration with the caller. Run the package’s relevant tests after changing `PolicyDecisionClient`; an import or successful installation alone does not establish its runtime guarantees.

---

## Package Boundary

### What It Owns

`tba-client-policy-decision` belongs to `075-clients` and owns relying-party and client integration: Typed client for platform authorization decisions.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/075-clients/tba-client-policy-decision/src/tba_client_policy_decision/__init__.py). Public exports include `PolicyDecisionClient`.

Keep authority-side policy decisions or server-owned persistence in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

### Public API and Import Surfaces

Import namespace: `tba_client_policy_decision`.

Source-declared exports or types: `PolicyDecisionClient`.

Inspect [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/075-clients/tba-client-policy-decision/src/tba_client_policy_decision/__init__.py) for exact signatures; this inventory does not designate every internal module as stable.

### Entry Points

<!-- readme-standards:begin entry-points -->
This package declares no command-line, GUI, or plugin entry points in its manifest.
<!-- readme-standards:end entry-points -->

### Injected Dependencies

The [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/075-clients/tba-client-policy-decision/src/tba_client_policy_decision/__init__.py) for `tba-client-policy-decision` does not declare an explicit service-constructor or keyword-only factory hook in the inspected source. Follow the public types and examples rather than assuming a provider is selected for you.

Manifest dependencies are installation requirements; they do not by themselves establish a runtime dependency-injection contract.

### Protocol Consumers

Direct consumers in this checkout’s package manifests include `tba-middleware-policy-enforcement-asgi`, `tba-workspace`. These edges describe declared dependencies, not protocol-conformance evidence.

### Extensions

For `tba-client-policy-decision`, use the source-declared public interfaces (`PolicyDecisionClient`) when composing or extending behavior. Its entry-point section below is authoritative for registered plugins; no additional extension loader is inferred from the package name.

---

## Operations and Readiness

### Operational Requirements

`tba-client-policy-decision` exposes relying-party and client integration. Public operations found in its source:

- `PolicyDecisionClient.decide` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/075-clients/tba-client-policy-decision/src/tba_client_policy_decision/__init__.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

### Health and Observability

This README does not establish a standalone health endpoint for `tba-client-policy-decision`. Observe the concrete caller’s results, exceptions, and existing test reports. An application that embeds this package must define its own health and telemetry contract.

### Security and Resource Limits

Apply the input, credential, and resource constraints implemented in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/075-clients/tba-client-policy-decision/src/tba_client_policy_decision/__init__.py). The `tba-client-policy-decision` README gate is a documentation check, not a security review or a substitute for the implementation’s limits and caller authorization.

### Compatibility

This source version of `tba-client-policy-decision` declares Python `>=3.10,<3.16`. Consult its dependency constraints before upgrading. Source-version and registry-version badges have separate meanings; this migration makes no additional platform or interoperability certification claim.

---

## Verification

### Tests

Run the example above to check the public API against the installed package. Its assertions describe the expected behavior.

[Workspace and package catalog](https://github.com/tigrbl/tigrbl_auth#package-catalog) · [tba-middleware-policy-enforcement-asgi](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/085-middleware/tba-middleware-policy-enforcement-asgi#readme) · [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues) · [Repository license](https://github.com/tigrbl/tigrbl_auth/blob/master/LICENSE)

### Certification Status

No external certification is asserted for `tba-client-policy-decision` by this documentation migration. README conformance, example syntax, runtime tests, and protocol or security certification are distinct evidence scopes.

### Evidence

The [README standards CI](https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml) records mechanical documentation results for its tested commit. The [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/075-clients/tba-client-policy-decision/src/tba_client_policy_decision/__init__.py) and example sources support the package-boundary description; external runtime behavior requires its own test evidence.

---

## FAQ

### Why

**Why select this package?** `tba-client-policy-decision` provides typed client for platform authorization decisions; use its own API boundary rather than assuming neighboring packages are bundled or configured automatically.

### How

**How do I start?** Install or synchronize the environment under Getting Started, follow the maintained example for `tba-client-policy-decision`, and consult [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/075-clients/tba-client-policy-decision/src/tba_client_policy_decision/__init__.py) for the exact types and signatures involved.

### When

**When should I validate an upgrade?** Recheck `tba-client-policy-decision` whenever its source version, declared collaborators, configuration, or caller changes. Run relevant behavioral tests in addition to the README gate before promotion.

---

## Documentation and Related Packages

### More Documentation

The [repository contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md), [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/075-clients/tba-client-policy-decision/src/tba_client_policy_decision/__init__.py), and [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/075-clients/tba-client-policy-decision/pyproject.toml) provide the supporting context for `tba-client-policy-decision`. The [README policy](https://github.com/groupsum/readme-standards/blob/master/docs/outline.md) defines the common document structure.

### Related Packages

Declared local runtime dependencies:

- [tba-contracts-authorization](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-authorization/README.md)

Direct downstream consumers:

- [tba-middleware-policy-enforcement-asgi](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/085-middleware/tba-middleware-policy-enforcement-asgi/README.md)

### Project Links

<!-- readme-standards:begin project-links -->
- [Documentation](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/075-clients/tba-client-policy-decision#readme)
- [Homepage](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/075-clients/tba-client-policy-decision#readme)
- [Issues](https://github.com/tigrbl/tigrbl_auth/issues)
- [PyPI](https://pypi.org/project/tba-client-policy-decision/)
- [Repository](https://github.com/tigrbl/tigrbl_auth)
- [Source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/075-clients/tba-client-policy-decision)
- [pypi: tba-client-policy-decision](https://pypi.org/project/tba-client-policy-decision/)
<!-- readme-standards:end project-links -->

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/075-clients/tba-client-policy-decision)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/075-clients/tba-client-policy-decision/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/075-clients/tba-client-policy-decision/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/075-clients/tba-client-policy-decision/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-client-policy-decision/)

---

## Contributing

### How to Contribute

Follow the [contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md) and include a focused example or regression for changes to `tba-client-policy-decision`. Keep package behavior, its documented boundary, and its tests aligned.

### Development Setup

Work from the `pkgs/075-clients/tba-client-policy-decision` checkout. Synchronize its declared development environment with uv, then run the relevant package tests and `python -m pytest docs/readme/test_examples.py`. The repository’s dedicated README job installs `readme-standards==0.1.3` without resolving unrelated runtime packages.

### Notes for Maintainers

Edit authored prose directly in this `tba-client-policy-decision` README. Update source examples in `docs/readme/`, then run `readme-standards render --root . --write` from the package directory and review the diff. Required headings and generated blocks come from package-guide-v1.

---

## Governance

### Ownership and Decision Making

Changes to `tba-client-policy-decision` follow the maintainer review process of [tigrbl/tigrbl_auth](https://github.com/tigrbl/tigrbl_auth) and its contribution guide. Author attribution remains in the [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/075-clients/tba-client-policy-decision/pyproject.toml); this README does not assign new publishing or administrative authority.

### Standards and Policies

`tba-client-policy-decision` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `075-clients` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

### Lifecycle and Migration

The `tba-client-policy-decision` source version is `0.4.0.dev4`. This change standardizes documentation and adds a development-only gate; it does not publish a new runtime version or declare a previously unpublished package released. Preserve explicit deprecation and replacement instructions where present.

---

## License and Attribution

### License

<!-- readme-standards:begin license -->
Licensed under `Apache-2.0`. See [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/075-clients/tba-client-policy-decision/LICENSE).
<!-- readme-standards:end license -->

### Notices

<!-- readme-standards:begin notices -->
See [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/075-clients/tba-client-policy-decision/NOTICE) for attribution.
<!-- readme-standards:end notices -->
