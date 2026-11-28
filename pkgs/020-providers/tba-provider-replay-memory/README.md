# tba-provider-replay-memory

<!-- readme-standards:begin branding -->
<p align="center"><a href="https://github.com/tigrbl/tigrbl_auth"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="300"></a></p>
<p align="center"><strong>tba-provider-replay-memory</strong></p>
<p align="center">Non-durable single-process replay reservation provider.</p>
<p align="center">
<a href="https://pypi.org/project/tba-provider-replay-memory/"><img alt="pypi: tba-provider-replay-memory" src="https://img.shields.io/pypi/v/tba-provider-replay-memory?labelColor=1E293B&amp;color=1D4ED8"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-replay-memory/pyproject.toml"><img alt="Source version: 0.4.0.dev4" src="https://img.shields.io/static/v1?label=Source%20version&amp;message=0.4.0.dev4&amp;labelColor=1E293B&amp;color=4338CA"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-replay-memory/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/static/v1?label=Python&amp;message=%3E%3D3.10%2C%3C3.16&amp;labelColor=1E293B&amp;color=0F766E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-replay-memory/pyproject.toml"><img alt="Layer: 020-providers" src="https://img.shields.io/static/v1?label=Layer&amp;message=020-providers&amp;labelColor=1E293B&amp;color=6D28D9"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-replay-memory/README.md#lifecycle-and-migration"><img alt="Lifecycle: active" src="https://img.shields.io/static/v1?label=Lifecycle&amp;message=active&amp;labelColor=1E293B&amp;color=166534"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-replay-memory/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/static/v1?label=License&amp;message=Apache-2.0&amp;labelColor=1E293B&amp;color=86198F"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-replay-memory/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/static/v1?label=Notice&amp;message=attribution&amp;labelColor=1E293B&amp;color=86198F"></a>
</p>
<p align="center">
<a href="https://pypi.org/project/tba-provider-replay-memory/"><img alt="Monthly PyPI downloads: tba-provider-replay-memory" src="https://img.shields.io/pypi/dm/tba-provider-replay-memory?labelColor=1E293B&amp;color=0E7490"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-replay-memory/README.md"><img alt="README hits: tba-provider-replay-memory" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/pkgs/020-providers/tba-provider-replay-memory/README.md.svg?label=README%20hits&amp;labelColor=1E293B&amp;color=0E7490"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="README standards: CI gate" src="https://img.shields.io/static/v1?label=README%20standards&amp;message=CI%20gate&amp;labelColor=1E293B&amp;color=1D4ED8"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-replay-memory/docs/readme/test_examples.py"><img alt="Tests: example source" src="https://img.shields.io/static/v1?label=Tests&amp;message=example%20source&amp;labelColor=1E293B&amp;color=0F766E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-replay-memory/README.md#certification-status"><img alt="Certification: not certified" src="https://img.shields.io/static/v1?label=Certification&amp;message=not%20certified&amp;labelColor=1E293B&amp;color=92400E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/tools/readme/POLICY.md"><img alt="Governance: repository policy" src="https://img.shields.io/static/v1?label=Governance&amp;message=repository%20policy&amp;labelColor=1E293B&amp;color=4338CA"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="Evidence: source and CI" src="https://img.shields.io/static/v1?label=Evidence&amp;message=source%20and%20CI&amp;labelColor=1E293B&amp;color=6D28D9"></a>
</p>
<p align="center"><a href="#overview">Overview</a> · <a href="#installation">Installation</a> · <a href="#quick-start">Quick Start</a> · <a href="#usage">Usage</a> · <a href="#public-api-and-import-surfaces">API</a> · <a href="#contributing">Contributing</a> · <a href="#governance">Governance</a> · <a href="#license">License</a></p>
<!-- readme-standards:end branding -->

---

## Overview

### Summary

Atomic process-local replay reservations for tests, development, and explicit
single-process deployments. State is lost on restart and is not shared across
workers, so this provider is not suitable for horizontally scaled production.

- Package: `tba-provider-replay-memory`
- Layer: `020-providers`
- Responsibility: Non-durable single-process replay reservation provider.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-replay-memory/src/tba_provider_replay_memory/__init__.py).
- Distribution: Python package on PyPI.

### Why This Package

`tba-provider-replay-memory` isolates this responsibility: Non-durable single-process replay reservation provider. Its [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-replay-memory/src/tba_provider_replay_memory/__init__.py) exposes `MemoryRPSessionProvider`, `MemoryRPStateProvider`, `MemoryReplayCheckProvider`, `MemoryReplayProvider`, `MemorySingleUseNonceProvider`, allowing consumers to select this package without treating adjacent packages as part of its public contract.

### When to Use

Choose `tba-provider-replay-memory` for this responsibility: Non-durable single-process replay reservation provider. Its `020-providers` placement keeps replaceable environment implementations separate from capability orchestration, storage table ownership, or HTTP routing.

### Features

- `MemoryReplayProvider`: declared in src/tba_provider_replay_memory/__init__.py
- `MemoryRPStateProvider`: Non-durable, process-local RP state provider for explicit injection.
- `MemoryRPSessionProvider`: Non-durable, process-local RP session provider for explicit injection.
- `MemoryReplayCheckProvider`: Atomically store new proofs and return whether they were accepted.
- `MemorySingleUseNonceProvider`: Synchronous non-durable single-use nonce provider.

### Non-Goals

`tba-provider-replay-memory` does not take ownership of capability orchestration, storage table ownership, or HTTP routing.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

---

## Getting Started

### Prerequisites

Python `>=3.10,<3.16` is required. The [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-replay-memory/pyproject.toml) declares runtime dependencies including `tba-contracts-identity`, `tba-bases-replay`, `tba-contracts-security-trust`, `tba-provider-security-proof-pkce`. Read the example’s inputs and service requirements before execution.

### Installation

Install the selected PyPI release of `tba-provider-replay-memory`:

```bash
uv pip install tba-provider-replay-memory
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/020-providers/tba-provider-replay-memory
```

#### uv

<!-- readme-standards:begin installation.uv -->
```bash
uv add tba-provider-replay-memory
```
<!-- readme-standards:end installation.uv -->

#### pip

<!-- readme-standards:begin installation.pip -->
```bash
python -m pip install tba-provider-replay-memory
```
<!-- readme-standards:end installation.pip -->

#### Poetry

<!-- readme-standards:begin installation.poetry -->
```bash
poetry add tba-provider-replay-memory
```
<!-- readme-standards:end installation.poetry -->

### Quick Start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.


```bash
uv run --isolated --no-project --python 3.12 --with "tba-provider-replay-memory==0.4.0.dev4" python quickstart.py
```

The import and assertion succeed when the MemoryReplayProvider entry point is available.

#### Example

<!-- readme-standards:begin example.quick-start -->
Source: [docs/readme/quick_start.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-replay-memory/docs/readme/quick_start.py).

```python
from tba_provider_replay_memory import MemoryReplayProvider

assert callable(MemoryReplayProvider)
```
<!-- readme-standards:end example.quick-start -->

#### Expected Result

The example demonstrates the documented `tba-provider-replay-memory` source boundary or workflow. Complete its required configuration first. README CI checks the maintained source’s syntax and declarations; it does not claim that external services or the application workflow were exercised.

---

## Usage

### Common Workflows

<!-- readme-standards:begin example.usage -->
Source: [docs/readme/usage.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-replay-memory/docs/readme/usage.py).

```python
from tba_provider_replay_memory import MemoryReplayProvider

assert callable(MemoryReplayProvider)
```
<!-- readme-standards:end example.usage -->

The following public-entry-point example belongs to `tba-provider-replay-memory`. Non-durable single-process replay reservation provider. Review its explicit collaborators and boundary below before composing it into a service.

### Configuration

Configure `tba-provider-replay-memory` through the APIs in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-replay-memory/src/tba_provider_replay_memory/__init__.py); its [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-replay-memory/pyproject.toml) describes installation requirements, not an implicit service configuration. No additional package-global configuration contract is inferred from dependencies.

### Error Handling

The inspected `tba-provider-replay-memory` source raises `ValueError`. Handle these at the calling boundary and consult the implementation for the triggering conditions.

### Best Practices

Use the explicit `tba-provider-replay-memory` imports documented below and keep collaborator configuration with the caller. Run the package’s relevant tests after changing `MemoryRPSessionProvider`, `MemoryRPStateProvider`, `MemoryReplayCheckProvider`, `MemoryReplayProvider`, `MemorySingleUseNonceProvider`; an import or successful installation alone does not establish its runtime guarantees.

---

## Package Boundary

### What It Owns

`tba-provider-replay-memory` belongs to `020-providers` and owns replaceable environment implementations: Non-durable single-process replay reservation provider.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-replay-memory/src/tba_provider_replay_memory/__init__.py). Public exports include `MemoryReplayCheckProvider`, `MemoryReplayProvider`, `MemoryRPSessionProvider`, `MemoryRPStateProvider`, `MemorySingleUseNonceProvider`.

Keep capability orchestration, storage table ownership, or HTTP routing in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

### Public API and Import Surfaces

Import namespace: `tba_provider_replay_memory`.

Source-declared exports or types: `MemoryRPSessionProvider`, `MemoryRPStateProvider`, `MemoryReplayCheckProvider`, `MemoryReplayProvider`, `MemorySingleUseNonceProvider`.

Inspect [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-replay-memory/src/tba_provider_replay_memory/__init__.py) for exact signatures; this inventory does not designate every internal module as stable.

### Entry Points

<!-- readme-standards:begin entry-points -->
This package declares no command-line, GUI, or plugin entry points in its manifest.
<!-- readme-standards:end entry-points -->

### Injected Dependencies

The [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-replay-memory/src/tba_provider_replay_memory/__init__.py) for `tba-provider-replay-memory` does not declare an explicit service-constructor or keyword-only factory hook in the inspected source. Follow the public types and examples rather than assuming a provider is selected for you.

Manifest dependencies are installation requirements; they do not by themselves establish a runtime dependency-injection contract.

### Protocol Consumers

Direct consumers in this checkout’s package manifests include `tba-server-identity`, `tba-workspace`. These edges describe declared dependencies, not protocol-conformance evidence.

### Extensions

For `tba-provider-replay-memory`, use the source-declared public interfaces (`MemoryRPSessionProvider`, `MemoryRPStateProvider`, `MemoryReplayCheckProvider`, `MemoryReplayProvider`, `MemorySingleUseNonceProvider`) when composing or extending behavior. Its entry-point section below is authoritative for registered plugins; no additional extension loader is inferred from the package name.

---

## Operations and Readiness

### Operational Requirements

`tba-provider-replay-memory` exposes replaceable environment implementations. Public operations found in its source:

- `MemoryReplayProvider.check_and_reserve` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-replay-memory/src/tba_provider_replay_memory/__init__.py).
- `MemoryReplayProvider.contains_digest` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-replay-memory/src/tba_provider_replay_memory/__init__.py).
- `MemoryRPStateProvider.create` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-replay-memory/src/tba_provider_replay_memory/__init__.py).
- `MemoryRPStateProvider.consume` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-replay-memory/src/tba_provider_replay_memory/__init__.py).
- `MemoryRPSessionProvider.save` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-replay-memory/src/tba_provider_replay_memory/__init__.py).
- `MemoryRPSessionProvider.get` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-replay-memory/src/tba_provider_replay_memory/__init__.py).
- `MemoryReplayCheckProvider.check_and_store` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-replay-memory/src/tba_provider_replay_memory/__init__.py).
- `MemoryReplayCheckProvider.snapshot` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-replay-memory/src/tba_provider_replay_memory/__init__.py).
- `MemoryReplayCheckProvider.clear` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-replay-memory/src/tba_provider_replay_memory/__init__.py).
- `MemorySingleUseNonceProvider.issue` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-replay-memory/src/tba_provider_replay_memory/__init__.py).
- `MemorySingleUseNonceProvider.register` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-replay-memory/src/tba_provider_replay_memory/__init__.py).
- `MemorySingleUseNonceProvider.consume` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-replay-memory/src/tba_provider_replay_memory/__init__.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

### Health and Observability

This README does not establish a standalone health endpoint for `tba-provider-replay-memory`. Observe the concrete caller’s results, exceptions, and existing test reports. An application that embeds this package must define its own health and telemetry contract.

### Security and Resource Limits

Apply the input, credential, and resource constraints implemented in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-replay-memory/src/tba_provider_replay_memory/__init__.py). The `tba-provider-replay-memory` README gate is a documentation check, not a security review or a substitute for the implementation’s limits and caller authorization.

### Compatibility

This source version of `tba-provider-replay-memory` declares Python `>=3.10,<3.16`. Consult its dependency constraints before upgrading. Source-version and registry-version badges have separate meanings; this migration makes no additional platform or interoperability certification claim.

---

## Verification

### Tests

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-replay-memory/src/tba_provider_replay_memory/__init__.py).

### Certification Status

No external certification is asserted for `tba-provider-replay-memory` by this documentation migration. README conformance, example syntax, runtime tests, and protocol or security certification are distinct evidence scopes.

### Evidence

The [README standards CI](https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml) records mechanical documentation results for its tested commit. The [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-replay-memory/src/tba_provider_replay_memory/__init__.py) and example sources support the package-boundary description; external runtime behavior requires its own test evidence.

---

## FAQ

### Why

**Why select this package?** `tba-provider-replay-memory` provides non-durable single-process replay reservation provider; use its own API boundary rather than assuming neighboring packages are bundled or configured automatically.

### How

**How do I start?** Install or synchronize the environment under Getting Started, follow the maintained example for `tba-provider-replay-memory`, and consult [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-replay-memory/src/tba_provider_replay_memory/__init__.py) for the exact types and signatures involved.

### When

**When should I validate an upgrade?** Recheck `tba-provider-replay-memory` whenever its source version, declared collaborators, configuration, or caller changes. Run relevant behavioral tests in addition to the README gate before promotion.

---

## Documentation and Related Packages

### More Documentation

The [repository contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md), [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-replay-memory/src/tba_provider_replay_memory/__init__.py), and [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-replay-memory/pyproject.toml) provide the supporting context for `tba-provider-replay-memory`. The [README policy](https://github.com/groupsum/readme-standards/blob/master/docs/outline.md) defines the common document structure.

### Related Packages

Declared local runtime dependencies:

- [tba-bases-replay](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-replay/README.md)
- [tba-contracts-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-identity/README.md)
- [tba-contracts-security-trust](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-security-trust/README.md)
- [tba-provider-security-proof-pkce](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-security-proof-pkce/README.md)

Direct downstream consumers:

- [tba-server-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-server-identity/README.md)

### Project Links

<!-- readme-standards:begin project-links -->
- [Documentation](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/020-providers/tba-provider-replay-memory#readme)
- [Homepage](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/020-providers/tba-provider-replay-memory#readme)
- [Issues](https://github.com/tigrbl/tigrbl_auth/issues)
- [PyPI](https://pypi.org/project/tba-provider-replay-memory/)
- [Repository](https://github.com/tigrbl/tigrbl_auth)
- [Source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/020-providers/tba-provider-replay-memory)
- [pypi: tba-provider-replay-memory](https://pypi.org/project/tba-provider-replay-memory/)
<!-- readme-standards:end project-links -->

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/020-providers/tba-provider-replay-memory)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-replay-memory/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-replay-memory/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-replay-memory/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-provider-replay-memory/)

---

## Contributing

### How to Contribute

Follow the [contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md) and include a focused example or regression for changes to `tba-provider-replay-memory`. Keep package behavior, its documented boundary, and its tests aligned.

### Development Setup

Work from the `pkgs/020-providers/tba-provider-replay-memory` checkout. Synchronize its declared development environment with uv, then run the relevant package tests and `python -m pytest docs/readme/test_examples.py`. The repository’s dedicated README job installs `readme-standards==0.1.3` without resolving unrelated runtime packages.

### Notes for Maintainers

Edit authored prose directly in this `tba-provider-replay-memory` README. Update source examples in `docs/readme/`, then run `readme-standards render --root . --write` from the package directory and review the diff. Required headings and generated blocks come from package-guide-v1.

---

## Governance

### Ownership and Decision Making

Changes to `tba-provider-replay-memory` follow the maintainer review process of [tigrbl/tigrbl_auth](https://github.com/tigrbl/tigrbl_auth) and its contribution guide. Author attribution remains in the [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-replay-memory/pyproject.toml); this README does not assign new publishing or administrative authority.

### Standards and Policies

`tba-provider-replay-memory` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `020-providers` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

### Lifecycle and Migration

The `tba-provider-replay-memory` source version is `0.4.0.dev4`. This change standardizes documentation and adds a development-only gate; it does not publish a new runtime version or declare a previously unpublished package released. Preserve explicit deprecation and replacement instructions where present.

---

## License and Attribution

### License

<!-- readme-standards:begin license -->
Licensed under `Apache-2.0`. See [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-replay-memory/LICENSE).
<!-- readme-standards:end license -->

### Notices

<!-- readme-standards:begin notices -->
See [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-replay-memory/NOTICE) for attribution.
<!-- readme-standards:end notices -->
