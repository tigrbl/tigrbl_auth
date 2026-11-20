# tba-router-wit-issuance

<!-- readme-standards:begin branding -->
<p align="center"><a href="https://github.com/tigrbl/tigrbl_auth"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="300"></a></p>
<p align="center"><strong>tba-router-wit-issuance</strong></p>
<p align="center">Mountable native WIMSE WIT enrollment endpoint.</p>
<p align="center">
<a href="https://pypi.org/project/tba-router-wit-issuance/"><img alt="pypi: tba-router-wit-issuance" src="https://img.shields.io/pypi/v/tba-router-wit-issuance"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-wit-issuance/pyproject.toml"><img alt="Source version: 0.4.0.dev3" src="https://img.shields.io/static/v1?label=Source%20version&amp;message=0.4.0.dev3&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-wit-issuance/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/static/v1?label=Python&amp;message=%3E%3D3.10%2C%3C3.16&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-wit-issuance/pyproject.toml"><img alt="Layer: 080-routers" src="https://img.shields.io/static/v1?label=Layer&amp;message=080-routers&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-wit-issuance/README.md#lifecycle-and-migration"><img alt="Lifecycle: active" src="https://img.shields.io/static/v1?label=Lifecycle&amp;message=active&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-wit-issuance/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/static/v1?label=License&amp;message=Apache-2.0&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-wit-issuance/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/static/v1?label=Notice&amp;message=attribution&amp;color=525252"></a>
</p>
<p align="center">
<a href="https://pypi.org/project/tba-router-wit-issuance/"><img alt="Monthly PyPI downloads: tba-router-wit-issuance" src="https://img.shields.io/pypi/dm/tba-router-wit-issuance"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-wit-issuance/README.md"><img alt="README hits: tba-router-wit-issuance" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/pkgs/080-routers/tba-router-wit-issuance/README.md.svg?label=README%20hits"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="README standards: CI gate" src="https://img.shields.io/static/v1?label=README%20standards&amp;message=CI%20gate&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-wit-issuance/docs/readme/test_examples.py"><img alt="Tests: example source" src="https://img.shields.io/static/v1?label=Tests&amp;message=example%20source&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-wit-issuance/README.md#certification-status"><img alt="Certification: not certified" src="https://img.shields.io/static/v1?label=Certification&amp;message=not%20certified&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/tools/readme/POLICY.md"><img alt="Governance: repository policy" src="https://img.shields.io/static/v1?label=Governance&amp;message=repository%20policy&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="Evidence: source and CI" src="https://img.shields.io/static/v1?label=Evidence&amp;message=source%20and%20CI&amp;color=525252"></a>
</p>
<p align="center"><a href="#overview">Overview</a> · <a href="#installation">Installation</a> · <a href="#quick-start">Quick Start</a> · <a href="#usage">Usage</a> · <a href="#public-api-and-import-surfaces">API</a> · <a href="#contributing">Contributing</a> · <a href="#governance">Governance</a> · <a href="#license">License</a></p>
<!-- readme-standards:end branding -->

---

## Overview

### Summary

Mount `build_wit_issuance_router(service=..., authenticate=...)` on a Tigrbl app.
`POST /wit/issue` accepts JSON with `confirmation_jwk` and returns
`workload_identity_token`. The async authenticator supplies a trusted enrollment
principal. Construct `WitTokenService` with a configured signer, identity
resolver, and confirmation-key authorizer. The authorizer must bind the
presented public key to that principal, for example through a registered key
or an authenticated enrollment proof.

- Package: `tba-router-wit-issuance`
- Layer: `080-routers`
- Responsibility: Mountable native WIMSE WIT enrollment endpoint.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-wit-issuance/src/tba_router_wit_issuance/__init__.py).
- Distribution: Python package on PyPI.

### Why This Package

`tba-router-wit-issuance` isolates this responsibility: Mountable native WIMSE WIT enrollment endpoint. Its [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-wit-issuance/src/tba_router_wit_issuance/binding.py) exposes `build_wit_issuance_router`, allowing consumers to select this package without treating adjacent packages as part of its public contract.

### When to Use

Choose `tba-router-wit-issuance` for this responsibility: Mountable native WIMSE WIT enrollment endpoint. Its `080-routers` placement keeps transport-facing route composition separate from duplicating credential algorithms or storage ownership.

### Features

- `WitIssueRequest`: declared in src/tba_router_wit_issuance/schemas.py
- `WitIssueResponse`: declared in src/tba_router_wit_issuance/schemas.py

### Non-Goals

`tba-router-wit-issuance` does not take ownership of duplicating credential algorithms or storage ownership.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

---

## Getting Started

### Prerequisites

Python `>=3.10,<3.16` is required. The [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-wit-issuance/pyproject.toml) declares runtime dependencies including `tigrbl`, `pydantic`, `tba-runtime-identity`. Read the example’s inputs and service requirements before execution.

### Installation

Install the selected PyPI release of `tba-router-wit-issuance`:

```bash
uv pip install tba-router-wit-issuance
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/080-routers/tba-router-wit-issuance
```

#### uv

<!-- readme-standards:begin installation.uv -->
```bash
uv add tba-router-wit-issuance
```
<!-- readme-standards:end installation.uv -->

#### pip

<!-- readme-standards:begin installation.pip -->
```bash
python -m pip install tba-router-wit-issuance
```
<!-- readme-standards:end installation.pip -->

#### Poetry

<!-- readme-standards:begin installation.poetry -->
```bash
poetry add tba-router-wit-issuance
```
<!-- readme-standards:end installation.poetry -->

### Quick Start

Build the package from the repository root:

```bash
uv build --wheel pkgs/080-routers/tba-router-wit-issuance
```

#### Example

<!-- readme-standards:begin example.quick-start -->
Source: [docs/readme/quick_start.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-wit-issuance/docs/readme/quick_start.py).

```python
import tba_router_wit_issuance

print(tba_router_wit_issuance.__name__)
```
<!-- readme-standards:end example.quick-start -->

#### Expected Result

The example demonstrates the documented `tba-router-wit-issuance` source boundary or workflow. Complete its required configuration first. README CI checks the maintained source’s syntax and declarations; it does not claim that external services or the application workflow were exercised.

---

## Usage

### Common Workflows

<!-- readme-standards:begin example.usage -->
Source: [docs/readme/usage.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-wit-issuance/docs/readme/usage.py).

```python
import tba_router_wit_issuance

print(tba_router_wit_issuance.__name__)
```
<!-- readme-standards:end example.usage -->

The following public-entry-point example belongs to `tba-router-wit-issuance`. Mountable native WIMSE WIT enrollment endpoint. Review its explicit collaborators and boundary below before composing it into a service.

### Configuration

Configure `tba-router-wit-issuance` through the APIs in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-wit-issuance/src/tba_router_wit_issuance/binding.py); its [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-wit-issuance/pyproject.toml) describes installation requirements, not an implicit service configuration. No additional package-global configuration contract is inferred from dependencies.

### Error Handling

The inspected `tba-router-wit-issuance` source raises `HTTPException`. Handle these at the calling boundary and consult the implementation for the triggering conditions.

### Best Practices

Use the explicit `tba-router-wit-issuance` imports documented below and keep collaborator configuration with the caller. Run the package’s relevant tests after changing `build_wit_issuance_router`; an import or successful installation alone does not establish its runtime guarantees.

---

## Package Boundary

### What It Owns

`tba-router-wit-issuance` belongs to `080-routers` and owns transport-facing route composition: Mountable native WIMSE WIT enrollment endpoint.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-wit-issuance/src/tba_router_wit_issuance/__init__.py). Public exports include `build_wit_issuance_router`.

Keep duplicating credential algorithms or storage ownership in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

### Public API and Import Surfaces

Import namespace: `tba_router_wit_issuance`.

Source-declared exports or types: `build_wit_issuance_router`.

Inspect [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-wit-issuance/src/tba_router_wit_issuance/binding.py) for exact signatures; this inventory does not designate every internal module as stable.

### Entry Points

<!-- readme-standards:begin entry-points -->
This package declares no command-line, GUI, or plugin entry points in its manifest.
<!-- readme-standards:end entry-points -->

### Injected Dependencies

Explicit construction inputs and collaborators for `tba-router-wit-issuance`:

- `build_wit_issuance_router` construction inputs: `service`, `authenticate`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-wit-issuance/src/tba_router_wit_issuance/binding.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

### Protocol Consumers

Direct consumers in this checkout’s package manifests include `tba-app-backend-wit-issuance`, `tba-workspace`. These edges describe declared dependencies, not protocol-conformance evidence.

### Extensions

For `tba-router-wit-issuance`, use the source-declared public interfaces (`build_wit_issuance_router`) when composing or extending behavior. Its entry-point section below is authoritative for registered plugins; no additional extension loader is inferred from the package name.

---

## Operations and Readiness

### Operational Requirements

`tba-router-wit-issuance` exposes transport-facing route composition. Public operations found in its source:

- `build_wit_issuance_router` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-wit-issuance/src/tba_router_wit_issuance/binding.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

### Health and Observability

This README does not establish a standalone health endpoint for `tba-router-wit-issuance`. Observe the concrete caller’s results, exceptions, and existing test reports. An application that embeds this package must define its own health and telemetry contract.

### Security and Resource Limits

Apply the input, credential, and resource constraints implemented in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-wit-issuance/src/tba_router_wit_issuance/binding.py). The `tba-router-wit-issuance` README gate is a documentation check, not a security review or a substitute for the implementation’s limits and caller authorization.

### Compatibility

This source version of `tba-router-wit-issuance` declares Python `>=3.10,<3.16`. Consult its dependency constraints before upgrading. Source-version and registry-version badges have separate meanings; this migration makes no additional platform or interoperability certification claim.

---

## Verification

### Tests

Exercise native WIC issuance and WIT/WPT runtime composition from the repository root:

```bash
uv run --extra test pytest pkgs/120-tests/tba-tests-workload-composition/tests/test_native_wimse_services.py
```

### Certification Status

No external certification is asserted for `tba-router-wit-issuance` by this documentation migration. README conformance, example syntax, runtime tests, and protocol or security certification are distinct evidence scopes.

### Evidence

The [README standards CI](https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml) records mechanical documentation results for its tested commit. The [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-wit-issuance/src/tba_router_wit_issuance/binding.py) and example sources support the package-boundary description; external runtime behavior requires its own test evidence.

---

## FAQ

### Why

**Why select this package?** `tba-router-wit-issuance` provides mountable native WIMSE WIT enrollment endpoint; use its own API boundary rather than assuming neighboring packages are bundled or configured automatically.

### How

**How do I start?** Install or synchronize the environment under Getting Started, follow the maintained example for `tba-router-wit-issuance`, and consult [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-wit-issuance/src/tba_router_wit_issuance/binding.py) for the exact types and signatures involved.

### When

**When should I validate an upgrade?** Recheck `tba-router-wit-issuance` whenever its source version, declared collaborators, configuration, or caller changes. Run relevant behavioral tests in addition to the README gate before promotion.

---

## Documentation and Related Packages

### More Documentation

The [repository contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md), [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-wit-issuance/src/tba_router_wit_issuance/binding.py), and [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-wit-issuance/pyproject.toml) provide the supporting context for `tba-router-wit-issuance`. The [README policy](https://github.com/groupsum/readme-standards/blob/master/docs/outline.md) defines the common document structure.

### Related Packages

Declared local runtime dependencies:

- [tba-runtime-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity/README.md)

Direct downstream consumers:

- [tba-app-backend-wit-issuance](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-wit-issuance/README.md)

### Project Links

<!-- readme-standards:begin project-links -->
- [Documentation](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/080-routers/tba-router-wit-issuance#readme)
- [Homepage](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/080-routers/tba-router-wit-issuance#readme)
- [Issues](https://github.com/tigrbl/tigrbl_auth/issues)
- [PyPI](https://pypi.org/project/tba-router-wit-issuance/)
- [Repository](https://github.com/tigrbl/tigrbl_auth)
- [Source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/080-routers/tba-router-wit-issuance)
- [pypi: tba-router-wit-issuance](https://pypi.org/project/tba-router-wit-issuance/)
<!-- readme-standards:end project-links -->

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/080-routers/tba-router-wit-issuance)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-wit-issuance/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-wit-issuance/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-wit-issuance/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-router-wit-issuance/)

---

## Contributing

### How to Contribute

Follow the [contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md) and include a focused example or regression for changes to `tba-router-wit-issuance`. Keep package behavior, its documented boundary, and its tests aligned.

### Development Setup

Work from the `pkgs/080-routers/tba-router-wit-issuance` checkout. Synchronize its declared development environment with uv, then run the relevant package tests and `python -m pytest docs/readme/test_examples.py`. The repository’s dedicated README job installs `readme-standards==0.1.1` without resolving unrelated runtime packages.

### Notes for Maintainers

Edit authored prose directly in this `tba-router-wit-issuance` README. Update source examples in `docs/readme/`, then run `readme-standards render --root . --write` from the package directory and review the diff. Required headings and generated blocks come from package-guide-v1.

---

## Governance

### Ownership and Decision Making

Changes to `tba-router-wit-issuance` follow the maintainer review process of [tigrbl/tigrbl_auth](https://github.com/tigrbl/tigrbl_auth) and its contribution guide. Author attribution remains in the [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-wit-issuance/pyproject.toml); this README does not assign new publishing or administrative authority.

### Standards and Policies

`tba-router-wit-issuance` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `080-routers` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

### Lifecycle and Migration

The `tba-router-wit-issuance` source version is `0.4.0.dev3`. This change standardizes documentation and adds a development-only gate; it does not publish a new runtime version or declare a previously unpublished package released. Preserve explicit deprecation and replacement instructions where present.

---

## License and Attribution

### License

<!-- readme-standards:begin license -->
Licensed under `Apache-2.0`. See [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-wit-issuance/LICENSE).
<!-- readme-standards:end license -->

### Notices

<!-- readme-standards:begin notices -->
See [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-wit-issuance/NOTICE) for attribution.
<!-- readme-standards:end notices -->
