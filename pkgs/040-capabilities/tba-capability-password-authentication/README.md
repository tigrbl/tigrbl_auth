# tba-capability-password-authentication

<!-- readme-standards:begin branding -->
<p align="center"><a href="https://github.com/tigrbl/tigrbl_auth"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="300"></a></p>
<p align="center"><strong>tba-capability-password-authentication</strong></p>
<p align="center">Password authentication capability.</p>
<p align="center">
<a href="https://pypi.org/project/tba-capability-password-authentication/"><img alt="pypi: tba-capability-password-authentication" src="https://img.shields.io/pypi/v/tba-capability-password-authentication?labelColor=1E293B&amp;color=1D4ED8"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-password-authentication/pyproject.toml"><img alt="Source version: 0.4.0.dev3" src="https://img.shields.io/static/v1?label=Source%20version&amp;message=0.4.0.dev3&amp;labelColor=1E293B&amp;color=4338CA"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-password-authentication/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/static/v1?label=Python&amp;message=%3E%3D3.10%2C%3C3.16&amp;labelColor=1E293B&amp;color=0F766E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-password-authentication/pyproject.toml"><img alt="Layer: 040-capabilities" src="https://img.shields.io/static/v1?label=Layer&amp;message=040-capabilities&amp;labelColor=1E293B&amp;color=6D28D9"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-password-authentication/README.md#lifecycle-and-migration"><img alt="Lifecycle: active" src="https://img.shields.io/static/v1?label=Lifecycle&amp;message=active&amp;labelColor=1E293B&amp;color=166534"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-password-authentication/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/static/v1?label=License&amp;message=Apache-2.0&amp;labelColor=1E293B&amp;color=86198F"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-password-authentication/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/static/v1?label=Notice&amp;message=attribution&amp;labelColor=1E293B&amp;color=86198F"></a>
</p>
<p align="center">
<a href="https://pypi.org/project/tba-capability-password-authentication/"><img alt="Monthly PyPI downloads: tba-capability-password-authentication" src="https://img.shields.io/pypi/dm/tba-capability-password-authentication?labelColor=1E293B&amp;color=0E7490"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-password-authentication/README.md"><img alt="README hits: tba-capability-password-authentication" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/pkgs/040-capabilities/tba-capability-password-authentication/README.md.svg?label=README%20hits&amp;labelColor=1E293B&amp;color=0E7490"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="README standards: CI gate" src="https://img.shields.io/static/v1?label=README%20standards&amp;message=CI%20gate&amp;labelColor=1E293B&amp;color=1D4ED8"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-password-authentication/docs/readme/test_examples.py"><img alt="Tests: example source" src="https://img.shields.io/static/v1?label=Tests&amp;message=example%20source&amp;labelColor=1E293B&amp;color=0F766E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-password-authentication/README.md#certification-status"><img alt="Certification: not certified" src="https://img.shields.io/static/v1?label=Certification&amp;message=not%20certified&amp;labelColor=1E293B&amp;color=92400E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/tools/readme/POLICY.md"><img alt="Governance: repository policy" src="https://img.shields.io/static/v1?label=Governance&amp;message=repository%20policy&amp;labelColor=1E293B&amp;color=4338CA"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="Evidence: source and CI" src="https://img.shields.io/static/v1?label=Evidence&amp;message=source%20and%20CI&amp;labelColor=1E293B&amp;color=6D28D9"></a>
</p>
<p align="center"><a href="#overview">Overview</a> · <a href="#installation">Installation</a> · <a href="#quick-start">Quick Start</a> · <a href="#usage">Usage</a> · <a href="#public-api-and-import-surfaces">API</a> · <a href="#contributing">Contributing</a> · <a href="#governance">Governance</a> · <a href="#license">License</a></p>
<!-- readme-standards:end branding -->

---

## Overview

### Summary

Mountable password authentication over injected identity lookup and a password authenticator provider.

- Package: `tba-capability-password-authentication`
- Layer: `040-capabilities`
- Responsibility: Password authentication capability.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-password-authentication/src/tba_capability_password_authentication/__init__.py).
- Distribution: Python package on PyPI.

### Why This Package

`tba-capability-password-authentication` isolates this responsibility: Password authentication capability. Its [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-password-authentication/src/tba_capability_password_authentication/capability.py) exposes `PasswordAuthenticationCapability`, allowing consumers to select this package without treating adjacent packages as part of its public contract.

### When to Use

Choose `tba-capability-password-authentication` for this responsibility: Password authentication capability. Its `040-capabilities` placement keeps use-case orchestration through explicit collaborators separate from HTTP wire schemas, direct table ownership, or hidden provider selection.

### Features

- `PasswordAuthenticationCapability`: declared in src/tba_capability_password_authentication/capability.py

### Non-Goals

- No HTTP or protocol wire schemas.
- No direct layer-01 table access.
- No hidden mutable persistence or provider selection.

---

## Getting Started

### Prerequisites

Python `>=3.10,<3.16` is required. The [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-password-authentication/pyproject.toml) declares runtime dependencies including `tba-concrete-capability`, `tba-contracts-identity`, `tba-provider-authenticator-password-local`. Read the example’s inputs and service requirements before execution.

### Installation

Install the selected PyPI release of `tba-capability-password-authentication`:

```bash
uv pip install tba-capability-password-authentication
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/040-capabilities/tba-capability-password-authentication
```

#### uv

<!-- readme-standards:begin installation.uv -->
```bash
uv add tba-capability-password-authentication
```
<!-- readme-standards:end installation.uv -->

#### pip

<!-- readme-standards:begin installation.pip -->
```bash
python -m pip install tba-capability-password-authentication
```
<!-- readme-standards:end installation.pip -->

#### Poetry

<!-- readme-standards:begin installation.poetry -->
```bash
poetry add tba-capability-password-authentication
```
<!-- readme-standards:end installation.poetry -->

### Quick Start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.


```bash
uv run --isolated --no-project --python 3.12 --with "tba-capability-password-authentication==0.4.0.dev3" python quickstart.py
```

The import and assertion succeed when the PasswordAuthenticationCapability entry point is available.

#### Example

<!-- readme-standards:begin example.quick-start -->
Source: [docs/readme/quick_start.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-password-authentication/docs/readme/quick_start.py).

```python
from tba_capability_password_authentication import PasswordAuthenticationCapability

assert callable(PasswordAuthenticationCapability)
```
<!-- readme-standards:end example.quick-start -->

#### Expected Result

The example demonstrates the documented `tba-capability-password-authentication` source boundary or workflow. Complete its required configuration first. README CI checks the maintained source’s syntax and declarations; it does not claim that external services or the application workflow were exercised.

---

## Usage

### Common Workflows

<!-- readme-standards:begin example.usage -->
Source: [docs/readme/usage.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-password-authentication/docs/readme/usage.py).

```python
from tba_capability_password_authentication import PasswordAuthenticationCapability

assert callable(PasswordAuthenticationCapability)
```
<!-- readme-standards:end example.usage -->

The following public-entry-point example belongs to `tba-capability-password-authentication`. Password authentication capability. Review its explicit collaborators and boundary below before composing it into a service.

### Configuration

Configure `tba-capability-password-authentication` through the APIs in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-password-authentication/src/tba_capability_password_authentication/capability.py); its [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-password-authentication/pyproject.toml) describes installation requirements, not an implicit service configuration. No additional package-global configuration contract is inferred from dependencies.

### Error Handling

The inspected `tba-capability-password-authentication` source does not establish a package-wide exception hierarchy. Preserve errors from its declared dependencies and validate inputs using the specific public contract in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-password-authentication/src/tba_capability_password_authentication/capability.py).

### Best Practices

Use the explicit `tba-capability-password-authentication` imports documented below and keep collaborator configuration with the caller. Run the package’s relevant tests after changing `PasswordAuthenticationCapability`; an import or successful installation alone does not establish its runtime guarantees.

---

## Package Boundary

### What It Owns

`tba-capability-password-authentication` belongs to `040-capabilities` and owns use-case orchestration through explicit collaborators: Password authentication capability.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-password-authentication/src/tba_capability_password_authentication/__init__.py).

Keep HTTP wire schemas, direct table ownership, or hidden provider selection in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

### Public API and Import Surfaces

Import namespace: `tba_capability_password_authentication`.

Source-declared exports or types: `PasswordAuthenticationCapability`.

Inspect [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-password-authentication/src/tba_capability_password_authentication/capability.py) for exact signatures; this inventory does not designate every internal module as stable.

### Entry Points

<!-- readme-standards:begin entry-points -->
This package declares no command-line, GUI, or plugin entry points in its manifest.
<!-- readme-standards:end entry-points -->

### Injected Dependencies

- `tba-provider-authenticator-password-local`

### Protocol Consumers

- Protocol-neutral; layer-50 packages may bind these operations.

### Extensions

For `tba-capability-password-authentication`, use the source-declared public interfaces (`PasswordAuthenticationCapability`) when composing or extending behavior. Its entry-point section below is authoritative for registered plugins; no additional extension loader is inferred from the package name.

---

## Operations and Readiness

### Operational Requirements

- `authenticate_password`

For `tba-capability-password-authentication`, these operation names identify the callable surface, not a readiness guarantee. Validate its explicit collaborators and behavioral checks in Verification before deployment.

### Health and Observability

This README does not establish a standalone health endpoint for `tba-capability-password-authentication`. Observe the concrete caller’s results, exceptions, and existing test reports. An application that embeds this package must define its own health and telemetry contract.

### Security and Resource Limits

Apply the input, credential, and resource constraints implemented in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-password-authentication/src/tba_capability_password_authentication/capability.py). The `tba-capability-password-authentication` README gate is a documentation check, not a security review or a substitute for the implementation’s limits and caller authorization.

### Compatibility

This source version of `tba-capability-password-authentication` declares Python `>=3.10,<3.16`. Consult its dependency constraints before upgrading. Source-version and registry-version badges have separate meanings; this migration makes no additional platform or interoperability certification claim.

---

## Verification

### Tests

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-password-authentication/src/tba_capability_password_authentication/__init__.py).

### Certification Status

No external certification is asserted for `tba-capability-password-authentication` by this documentation migration. README conformance, example syntax, runtime tests, and protocol or security certification are distinct evidence scopes.

### Evidence

The [README standards CI](https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml) records mechanical documentation results for its tested commit. The [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-password-authentication/src/tba_capability_password_authentication/capability.py) and example sources support the package-boundary description; external runtime behavior requires its own test evidence.

---

## FAQ

### Why

**Why select this package?** `tba-capability-password-authentication` provides password authentication capability; use its own API boundary rather than assuming neighboring packages are bundled or configured automatically.

### How

**How do I start?** Install or synchronize the environment under Getting Started, follow the maintained example for `tba-capability-password-authentication`, and consult [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-password-authentication/src/tba_capability_password_authentication/capability.py) for the exact types and signatures involved.

### When

**When should I validate an upgrade?** Recheck `tba-capability-password-authentication` whenever its source version, declared collaborators, configuration, or caller changes. Run relevant behavioral tests in addition to the README gate before promotion.

---

## Documentation and Related Packages

### More Documentation

The [repository contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md), [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-password-authentication/src/tba_capability_password_authentication/capability.py), and [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-password-authentication/pyproject.toml) provide the supporting context for `tba-capability-password-authentication`. The [README policy](https://github.com/groupsum/readme-standards/blob/master/docs/outline.md) defines the common document structure.

### Related Packages

Declared local runtime dependencies:

- [tba-concrete-capability](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-capability/README.md)
- [tba-contracts-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-identity/README.md)
- [tba-provider-authenticator-password-local](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-authenticator-password-local/README.md)

Direct downstream consumers:

- [tba-server-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-server-identity/README.md)

### Project Links

<!-- readme-standards:begin project-links -->
- [Documentation](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/040-capabilities/tba-capability-password-authentication#readme)
- [Homepage](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/040-capabilities/tba-capability-password-authentication#readme)
- [Issues](https://github.com/tigrbl/tigrbl_auth/issues)
- [PyPI](https://pypi.org/project/tba-capability-password-authentication/)
- [Repository](https://github.com/tigrbl/tigrbl_auth)
- [Source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/040-capabilities/tba-capability-password-authentication)
- [pypi: tba-capability-password-authentication](https://pypi.org/project/tba-capability-password-authentication/)
<!-- readme-standards:end project-links -->

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/040-capabilities/tba-capability-password-authentication)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-password-authentication/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-password-authentication/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-password-authentication/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-capability-password-authentication/)

---

## Contributing

### How to Contribute

Follow the [contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md) and include a focused example or regression for changes to `tba-capability-password-authentication`. Keep package behavior, its documented boundary, and its tests aligned.

### Development Setup

Work from the `pkgs/040-capabilities/tba-capability-password-authentication` checkout. Synchronize its declared development environment with uv, then run the relevant package tests and `python -m pytest docs/readme/test_examples.py`. The repository’s dedicated README job installs `readme-standards==0.1.3` without resolving unrelated runtime packages.

### Notes for Maintainers

Edit authored prose directly in this `tba-capability-password-authentication` README. Update source examples in `docs/readme/`, then run `readme-standards render --root . --write` from the package directory and review the diff. Required headings and generated blocks come from package-guide-v1.

---

## Governance

### Ownership and Decision Making

Changes to `tba-capability-password-authentication` follow the maintainer review process of [tigrbl/tigrbl_auth](https://github.com/tigrbl/tigrbl_auth) and its contribution guide. Author attribution remains in the [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-password-authentication/pyproject.toml); this README does not assign new publishing or administrative authority.

### Standards and Policies

`tba-capability-password-authentication` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `040-capabilities` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

### Lifecycle and Migration

The `tba-capability-password-authentication` source version is `0.4.0.dev3`. This change standardizes documentation and adds a development-only gate; it does not publish a new runtime version or declare a previously unpublished package released. Preserve explicit deprecation and replacement instructions where present.

---

## License and Attribution

### License

<!-- readme-standards:begin license -->
Licensed under `Apache-2.0`. See [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-password-authentication/LICENSE).
<!-- readme-standards:end license -->

### Notices

<!-- readme-standards:begin notices -->
See [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-password-authentication/NOTICE) for attribution.
<!-- readme-standards:end notices -->
