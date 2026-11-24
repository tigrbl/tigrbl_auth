# tba-plugin-tigrbl

<!-- readme-standards:begin branding -->
<p align="center"><a href="https://github.com/tigrbl/tigrbl_auth"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="300"></a></p>
<p align="center"><strong>tba-plugin-tigrbl</strong></p>
<p align="center">Standalone TbaPlugin adoption adapter for installing TBA surfaces into an existing Tigrbl app.</p>
<p align="center">
<a href="https://pypi.org/project/tba-plugin-tigrbl/"><img alt="pypi: tba-plugin-tigrbl" src="https://img.shields.io/pypi/v/tba-plugin-tigrbl?labelColor=1E293B&amp;color=1D4ED8"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-plugin-tigrbl/pyproject.toml"><img alt="Source version: 0.4.0.dev3" src="https://img.shields.io/static/v1?label=Source%20version&amp;message=0.4.0.dev3&amp;labelColor=1E293B&amp;color=4338CA"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-plugin-tigrbl/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/static/v1?label=Python&amp;message=%3E%3D3.10%2C%3C3.16&amp;labelColor=1E293B&amp;color=0F766E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-plugin-tigrbl/pyproject.toml"><img alt="Layer: 060-runtime" src="https://img.shields.io/static/v1?label=Layer&amp;message=060-runtime&amp;labelColor=1E293B&amp;color=6D28D9"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-plugin-tigrbl/README.md#lifecycle-and-migration"><img alt="Lifecycle: active" src="https://img.shields.io/static/v1?label=Lifecycle&amp;message=active&amp;labelColor=1E293B&amp;color=166534"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-plugin-tigrbl/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/static/v1?label=License&amp;message=Apache-2.0&amp;labelColor=1E293B&amp;color=86198F"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-plugin-tigrbl/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/static/v1?label=Notice&amp;message=attribution&amp;labelColor=1E293B&amp;color=86198F"></a>
</p>
<p align="center">
<a href="https://pypi.org/project/tba-plugin-tigrbl/"><img alt="Monthly PyPI downloads: tba-plugin-tigrbl" src="https://img.shields.io/pypi/dm/tba-plugin-tigrbl?labelColor=1E293B&amp;color=0E7490"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-plugin-tigrbl/README.md"><img alt="README hits: tba-plugin-tigrbl" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/pkgs/060-runtime/tba-plugin-tigrbl/README.md.svg?label=README%20hits&amp;labelColor=1E293B&amp;color=0E7490"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="README standards: CI gate" src="https://img.shields.io/static/v1?label=README%20standards&amp;message=CI%20gate&amp;labelColor=1E293B&amp;color=1D4ED8"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-plugin-tigrbl/docs/readme/test_examples.py"><img alt="Tests: example source" src="https://img.shields.io/static/v1?label=Tests&amp;message=example%20source&amp;labelColor=1E293B&amp;color=0F766E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-plugin-tigrbl/README.md#certification-status"><img alt="Certification: not certified" src="https://img.shields.io/static/v1?label=Certification&amp;message=not%20certified&amp;labelColor=1E293B&amp;color=92400E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/tools/readme/POLICY.md"><img alt="Governance: repository policy" src="https://img.shields.io/static/v1?label=Governance&amp;message=repository%20policy&amp;labelColor=1E293B&amp;color=4338CA"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="Evidence: source and CI" src="https://img.shields.io/static/v1?label=Evidence&amp;message=source%20and%20CI&amp;labelColor=1E293B&amp;color=6D28D9"></a>
</p>
<p align="center"><a href="#overview">Overview</a> · <a href="#installation">Installation</a> · <a href="#quick-start">Quick Start</a> · <a href="#usage">Usage</a> · <a href="#public-api-and-import-surfaces">API</a> · <a href="#contributing">Contributing</a> · <a href="#governance">Governance</a> · <a href="#license">License</a></p>
<!-- readme-standards:end branding -->

---

## Overview

### Summary

Standalone `TbaPlugin` package for the TBA package suite.

- Package: `tba-plugin-tigrbl`
- Import root: `tba_plugin_tigrbl`
- Owns `TbaPlugin` and the `install()` convenience function.
- Installs TBA runtime surfaces into an existing `TigrblApp`.
- `tba_server_identity.plugin` and `tba_auth.plugin` are compatibility wrappers.

- Package: `tba-plugin-tigrbl`
- Layer: `060-runtime`
- Responsibility: Standalone TbaPlugin adoption adapter for installing TBA surfaces into an existing Tigrbl app.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-plugin-tigrbl/src/tba_plugin_tigrbl/__init__.py).
- Distribution: Python package on PyPI.

### Why This Package

`tba-plugin-tigrbl` isolates this responsibility: Standalone TbaPlugin adoption adapter for installing TBA surfaces into an existing Tigrbl app. Its [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-plugin-tigrbl/src/tba_plugin_tigrbl/__init__.py) exposes `TbaPlugin`, `install`, allowing consumers to select this package without treating adjacent packages as part of its public contract.

### When to Use

Choose `tba-plugin-tigrbl` for this responsibility: Standalone TbaPlugin adoption adapter for installing TBA surfaces into an existing Tigrbl app. Its `060-runtime` placement keeps runtime composition and operator entry points separate from duplicating protocol grammars, table declarations, or provider implementations.

### Features

- `TbaPlugin`: Bind identity runtime lifecycle around an injected HTTP surface attacher.

### Non-Goals

`tba-plugin-tigrbl` does not take ownership of duplicating protocol grammars, table declarations, or provider implementations.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

---

## Getting Started

### Prerequisites

Python `>=3.10,<3.16` is required. The [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-plugin-tigrbl/pyproject.toml) declares runtime dependencies including `tba-runtime-identity`, `tba-server-identity`. Read the example’s inputs and service requirements before execution.

### Installation

Install the selected PyPI release of `tba-plugin-tigrbl`:

```bash
uv pip install tba-plugin-tigrbl
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/060-runtime/tba-plugin-tigrbl
```

#### uv

<!-- readme-standards:begin installation.uv -->
```bash
uv add tba-plugin-tigrbl
```
<!-- readme-standards:end installation.uv -->

#### pip

<!-- readme-standards:begin installation.pip -->
```bash
python -m pip install tba-plugin-tigrbl
```
<!-- readme-standards:end installation.pip -->

#### Poetry

<!-- readme-standards:begin installation.poetry -->
```bash
poetry add tba-plugin-tigrbl
```
<!-- readme-standards:end installation.poetry -->

### Quick Start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.


```bash
uv run --isolated --no-project --python 3.12 --with "tba-plugin-tigrbl==0.4.0.dev3" python quickstart.py
```

The import and assertion succeed when the TbaPlugin entry point is available.

#### Example

<!-- readme-standards:begin example.quick-start -->
Source: [docs/readme/quick_start.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-plugin-tigrbl/docs/readme/quick_start.py).

```python
from tba_plugin_tigrbl import TbaPlugin

assert callable(TbaPlugin)
```
<!-- readme-standards:end example.quick-start -->

#### Expected Result

The example demonstrates the documented `tba-plugin-tigrbl` source boundary or workflow. Complete its required configuration first. README CI checks the maintained source’s syntax and declarations; it does not claim that external services or the application workflow were exercised.

---

## Usage

### Common Workflows

<!-- readme-standards:begin example.usage -->
Source: [docs/readme/usage.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-plugin-tigrbl/docs/readme/usage.py).

```python
from tba_plugin_tigrbl import TbaPlugin

assert callable(TbaPlugin)
```
<!-- readme-standards:end example.usage -->

The following public-entry-point example belongs to `tba-plugin-tigrbl`. Standalone TbaPlugin adoption adapter for installing TBA surfaces into an existing Tigrbl app. Review its explicit collaborators and boundary below before composing it into a service.

### Configuration

For operation authorization, declare an `OperationSecurity` action and resource
type and install `OperationAuthorizationAdapter` on a Tigrbl app with the
`SECURITY` and `DEPENDENCIES` phases. The adapter registers its decision
dependency through `app.set_auth(operation_authorizer=...)`.

Supply credential verification, resource resolution and a policy loader. These
callbacks run before the operation transaction. For a write governed by mutable
resource state, enforce that condition in the write or within the transaction.
The adapter accepts only compatible policy catalogs and denies decisions with
outstanding obligations.

Configure `tba-plugin-tigrbl` through the APIs in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-plugin-tigrbl/src/tba_plugin_tigrbl/__init__.py); its [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-plugin-tigrbl/pyproject.toml) describes installation requirements, not an implicit service configuration. No additional package-global configuration contract is inferred from dependencies.

### Error Handling

The inspected `tba-plugin-tigrbl` source does not establish a package-wide exception hierarchy. Preserve errors from its declared dependencies and validate inputs using the specific public contract in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-plugin-tigrbl/src/tba_plugin_tigrbl/__init__.py).

### Best Practices

Use the explicit `tba-plugin-tigrbl` imports documented below and keep collaborator configuration with the caller. Run the package’s relevant tests after changing `TbaPlugin`, `install`; an import or successful installation alone does not establish its runtime guarantees.

---

## Package Boundary

### What It Owns

`tba-plugin-tigrbl` belongs to `060-runtime` and owns runtime composition and operator entry points: Standalone TbaPlugin adoption adapter for installing TBA surfaces into an existing Tigrbl app.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-plugin-tigrbl/src/tba_plugin_tigrbl/__init__.py). Public exports include `TbaPlugin`, `install`.

Keep duplicating protocol grammars, table declarations, or provider implementations in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

### Public API and Import Surfaces

Import namespace: `tba_plugin_tigrbl`.

Source-declared exports or types: `TbaPlugin`, `install`.

Inspect [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-plugin-tigrbl/src/tba_plugin_tigrbl/__init__.py) for exact signatures; this inventory does not designate every internal module as stable.

### Entry Points

<!-- readme-standards:begin entry-points -->
This package declares no command-line, GUI, or plugin entry points in its manifest.
<!-- readme-standards:end entry-points -->

### Injected Dependencies

Explicit construction inputs and collaborators for `tba-plugin-tigrbl`:

- `install` construction inputs: `surface_attacher`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-plugin-tigrbl/src/tba_plugin_tigrbl/plugin.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

### Protocol Consumers

Direct consumers in this checkout’s package manifests include `tba-auth`, `tba-app-backend-core`, `tba-workspace`. These edges describe declared dependencies, not protocol-conformance evidence.

### Extensions

For `tba-plugin-tigrbl`, use the source-declared public interfaces (`TbaPlugin`, `install`) when composing or extending behavior. Its entry-point section below is authoritative for registered plugins; no additional extension loader is inferred from the package name.

---

## Operations and Readiness

### Operational Requirements

`tba-plugin-tigrbl` exposes runtime composition and operator entry points. Public operations found in its source:

- `TbaPlugin.resolve_plugin_deployment` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-plugin-tigrbl/src/tba_plugin_tigrbl/plugin.py).
- `TbaPlugin.install` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-plugin-tigrbl/src/tba_plugin_tigrbl/plugin.py).
- `install` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-plugin-tigrbl/src/tba_plugin_tigrbl/plugin.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

### Health and Observability

This README does not establish a standalone health endpoint for `tba-plugin-tigrbl`. Observe the concrete caller’s results, exceptions, and existing test reports. An application that embeds this package must define its own health and telemetry contract.

### Security and Resource Limits

Apply the input, credential, and resource constraints implemented in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-plugin-tigrbl/src/tba_plugin_tigrbl/__init__.py). The `tba-plugin-tigrbl` README gate is a documentation check, not a security review or a substitute for the implementation’s limits and caller authorization.

### Compatibility

This source version of `tba-plugin-tigrbl` declares Python `>=3.10,<3.16`. Consult its dependency constraints before upgrading. Source-version and registry-version badges have separate meanings; this migration makes no additional platform or interoperability certification claim.

---

## Verification

### Tests

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-plugin-tigrbl/src/tba_plugin_tigrbl/__init__.py).

### Certification Status

No external certification is asserted for `tba-plugin-tigrbl` by this documentation migration. README conformance, example syntax, runtime tests, and protocol or security certification are distinct evidence scopes.

### Evidence

The [README standards CI](https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml) records mechanical documentation results for its tested commit. The [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-plugin-tigrbl/src/tba_plugin_tigrbl/__init__.py) and example sources support the package-boundary description; external runtime behavior requires its own test evidence.

---

## FAQ

### Why

**Why select this package?** `tba-plugin-tigrbl` provides standalone TbaPlugin adoption adapter for installing TBA surfaces into an existing Tigrbl app; use its own API boundary rather than assuming neighboring packages are bundled or configured automatically.

### How

**How do I start?** Install or synchronize the environment under Getting Started, follow the maintained example for `tba-plugin-tigrbl`, and consult [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-plugin-tigrbl/src/tba_plugin_tigrbl/__init__.py) for the exact types and signatures involved.

### When

**When should I validate an upgrade?** Recheck `tba-plugin-tigrbl` whenever its source version, declared collaborators, configuration, or caller changes. Run relevant behavioral tests in addition to the README gate before promotion.

---

## Documentation and Related Packages

### More Documentation

The [repository contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md), [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-plugin-tigrbl/src/tba_plugin_tigrbl/__init__.py), and [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-plugin-tigrbl/pyproject.toml) provide the supporting context for `tba-plugin-tigrbl`. The [README policy](https://github.com/groupsum/readme-standards/blob/master/docs/outline.md) defines the common document structure.

### Related Packages

Declared local runtime dependencies:

- [tba-runtime-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity/README.md)
- [tba-server-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-server-identity/README.md)

Direct downstream consumers:

- [tba-app-backend-core](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-core/README.md)
- [tba-auth](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-auth/README.md)

### Project Links

<!-- readme-standards:begin project-links -->
- [Documentation](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/060-runtime/tba-plugin-tigrbl#readme)
- [Homepage](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/060-runtime/tba-plugin-tigrbl#readme)
- [Issues](https://github.com/tigrbl/tigrbl_auth/issues)
- [PyPI](https://pypi.org/project/tba-plugin-tigrbl/)
- [Repository](https://github.com/tigrbl/tigrbl_auth)
- [SSOT](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [Source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/060-runtime/tba-plugin-tigrbl)
- [pypi: tba-plugin-tigrbl](https://pypi.org/project/tba-plugin-tigrbl/)
<!-- readme-standards:end project-links -->

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/060-runtime/tba-plugin-tigrbl)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-plugin-tigrbl/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-plugin-tigrbl/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-plugin-tigrbl/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-plugin-tigrbl/)

---

## Contributing

### How to Contribute

Follow the [contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md) and include a focused example or regression for changes to `tba-plugin-tigrbl`. Keep package behavior, its documented boundary, and its tests aligned.

### Development Setup

Work from the `pkgs/060-runtime/tba-plugin-tigrbl` checkout. Synchronize its declared development environment with uv, then run the relevant package tests and `python -m pytest docs/readme/test_examples.py`. The repository’s dedicated README job installs `readme-standards==0.1.3` without resolving unrelated runtime packages.

### Notes for Maintainers

**Adoption Option**

`TbaPlugin` is one adoption option for downstream applications that already own a `TigrblApp` and want to mount the identity provider surfaces into that app. Other adoption options remain valid: build a complete provider app through `tba-server-identity`, build a gateway through `tba-server-identity`, or run those app factories through `tba-runtime-identity`.

```python
from tba_plugin_tigrbl import TbaPlugin

plugin = TbaPlugin(settings=settings)
plugin.install(app)
```

---

## Governance

### Ownership and Decision Making

Changes to `tba-plugin-tigrbl` follow the maintainer review process of [tigrbl/tigrbl_auth](https://github.com/tigrbl/tigrbl_auth) and its contribution guide. Author attribution remains in the [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-plugin-tigrbl/pyproject.toml); this README does not assign new publishing or administrative authority.

### Standards and Policies

`tba-plugin-tigrbl` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `060-runtime` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

### Lifecycle and Migration

The `tba-plugin-tigrbl` source version is `0.4.0.dev3`. This change standardizes documentation and adds a development-only gate; it does not publish a new runtime version or declare a previously unpublished package released. Preserve explicit deprecation and replacement instructions where present.

---

## License and Attribution

### License

<!-- readme-standards:begin license -->
Licensed under `Apache-2.0`. See [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-plugin-tigrbl/LICENSE).
<!-- readme-standards:end license -->

### Notices

<!-- readme-standards:begin notices -->
See [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-plugin-tigrbl/NOTICE) for attribution.
<!-- readme-standards:end notices -->
