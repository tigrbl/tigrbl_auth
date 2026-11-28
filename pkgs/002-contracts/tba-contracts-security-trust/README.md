# tba-contracts-security-trust

<!-- readme-standards:begin branding -->
<p align="center"><a href="https://github.com/tigrbl/tigrbl_auth"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="300"></a></p>
<p align="center"><strong>tba-contracts-security-trust</strong></p>
<p align="center">Draft horizontal contracts and DTOs for security, trust, key, crypto, and cipher-suite components.</p>
<p align="center">
<a href="https://pypi.org/project/tba-contracts-security-trust/"><img alt="pypi: tba-contracts-security-trust" src="https://img.shields.io/pypi/v/tba-contracts-security-trust?labelColor=1E293B&amp;color=1D4ED8"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-security-trust/pyproject.toml"><img alt="Source version: 0.1.1.dev1" src="https://img.shields.io/static/v1?label=Source%20version&amp;message=0.1.1.dev1&amp;labelColor=1E293B&amp;color=4338CA"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-security-trust/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/static/v1?label=Python&amp;message=%3E%3D3.10%2C%3C3.16&amp;labelColor=1E293B&amp;color=0F766E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-security-trust/pyproject.toml"><img alt="Layer: 002-contracts" src="https://img.shields.io/static/v1?label=Layer&amp;message=002-contracts&amp;labelColor=1E293B&amp;color=6D28D9"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-security-trust/README.md#lifecycle-and-migration"><img alt="Lifecycle: active" src="https://img.shields.io/static/v1?label=Lifecycle&amp;message=active&amp;labelColor=1E293B&amp;color=166534"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-security-trust/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/static/v1?label=License&amp;message=Apache-2.0&amp;labelColor=1E293B&amp;color=86198F"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-security-trust/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/static/v1?label=Notice&amp;message=attribution&amp;labelColor=1E293B&amp;color=86198F"></a>
</p>
<p align="center">
<a href="https://pypi.org/project/tba-contracts-security-trust/"><img alt="Monthly PyPI downloads: tba-contracts-security-trust" src="https://img.shields.io/pypi/dm/tba-contracts-security-trust?labelColor=1E293B&amp;color=0E7490"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-security-trust/README.md"><img alt="README hits: tba-contracts-security-trust" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/pkgs/002-contracts/tba-contracts-security-trust/README.md.svg?label=README%20hits&amp;labelColor=1E293B&amp;color=0E7490"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="README standards: CI gate" src="https://img.shields.io/static/v1?label=README%20standards&amp;message=CI%20gate&amp;labelColor=1E293B&amp;color=1D4ED8"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-security-trust/docs/readme/test_examples.py"><img alt="Tests: example source" src="https://img.shields.io/static/v1?label=Tests&amp;message=example%20source&amp;labelColor=1E293B&amp;color=0F766E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-security-trust/README.md#certification-status"><img alt="Certification: not certified" src="https://img.shields.io/static/v1?label=Certification&amp;message=not%20certified&amp;labelColor=1E293B&amp;color=92400E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/tools/readme/POLICY.md"><img alt="Governance: repository policy" src="https://img.shields.io/static/v1?label=Governance&amp;message=repository%20policy&amp;labelColor=1E293B&amp;color=4338CA"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="Evidence: source and CI" src="https://img.shields.io/static/v1?label=Evidence&amp;message=source%20and%20CI&amp;labelColor=1E293B&amp;color=6D28D9"></a>
</p>
<p align="center"><a href="#overview">Overview</a> · <a href="#installation">Installation</a> · <a href="#quick-start">Quick Start</a> · <a href="#usage">Usage</a> · <a href="#public-api-and-import-surfaces">API</a> · <a href="#contributing">Contributing</a> · <a href="#governance">Governance</a> · <a href="#license">License</a></p>
<!-- readme-standards:end branding -->

---

## Overview

### Summary

Draft standalone contract package for security/trust component analysis.

This package intentionally contains only small protocol contracts and dataclass DTOs. It does not implement signing, token issuance, certificate handling, cryptographic transforms, key storage, or cipher-suite policy.

- Package: `tba-contracts-security-trust`
- Layer: `002-contracts`
- Responsibility: Draft horizontal contracts and DTOs for security, trust, key, crypto, and cipher-suite components.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-security-trust/src/tba_contracts_security_trust/__init__.py).
- Distribution: Python package on PyPI.

### Why This Package

`tba-contracts-security-trust` isolates this responsibility: Draft horizontal contracts and DTOs for security, trust, key, crypto, and cipher-suite components. Its [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-security-trust/src/tba_contracts_security_trust/__init__.py) exposes `OpenRequest`, `OpenResult`, `ParseRequest`, `ParsedArtifact`, `CanonicalizeRequest`, `RewrapRequest`, `NormalizedDescriptor`, `ListKeysRequest`, allowing consumers to select this package without treating adjacent packages as part of its public contract.

### When to Use

Choose `tba-contracts-security-trust` for this responsibility: Draft horizontal contracts and DTOs for security, trust, key, crypto, and cipher-suite components. Its `002-contracts` placement keeps shared types and structural ports separate from environment-specific service implementations or HTTP routing.

### Features

- `OpenRequest`: Input to opening protected artifacts such as ciphertexts and envelopes.
- `OpenResult`: Output from opening protected artifacts.
- `ParseRequest`: Input to artifact parsing.
- `ParsedArtifact`: Structured parse result; trust depends on caller-selected verification.
- `CanonicalizeRequest`: Input to deterministic canonicalization before issuing or verifying.
- `RewrapRequest`: Input to recipient-set mutation for multi-recipient envelopes.
- `NormalizedDescriptor`: Provider-ready cipher-policy decision.
- `ListKeysRequest`: Input to generic key inventory discovery.

### Non-Goals

`tba-contracts-security-trust` does not take ownership of environment-specific service implementations or HTTP routing.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

---

## Getting Started

### Prerequisites

Python `>=3.10,<3.16` is required. The [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-security-trust/pyproject.toml) declares runtime dependencies including `tba-primitives-identity`. Read the example’s inputs and service requirements before execution.

### Installation

Install the selected PyPI release of `tba-contracts-security-trust`:

```bash
uv pip install tba-contracts-security-trust
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/002-contracts/tba-contracts-security-trust
```

#### uv

<!-- readme-standards:begin installation.uv -->
```bash
uv add tba-contracts-security-trust
```
<!-- readme-standards:end installation.uv -->

#### pip

<!-- readme-standards:begin installation.pip -->
```bash
python -m pip install tba-contracts-security-trust
```
<!-- readme-standards:end installation.pip -->

#### Poetry

<!-- readme-standards:begin installation.poetry -->
```bash
poetry add tba-contracts-security-trust
```
<!-- readme-standards:end installation.poetry -->

### Quick Start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.


```bash
uv run --isolated --no-project --python 3.12 --with "tba-contracts-security-trust==0.1.1.dev1" python quickstart.py
```

The import and assertion succeed when the AcrEvaluationRequest entry point is available.

#### Example

<!-- readme-standards:begin example.quick-start -->
Source: [docs/readme/quick_start.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-security-trust/docs/readme/quick_start.py).

```python
from tba_contracts_security_trust import AcrEvaluationRequest

assert callable(AcrEvaluationRequest)
```
<!-- readme-standards:end example.quick-start -->

#### Expected Result

The example demonstrates the documented `tba-contracts-security-trust` source boundary or workflow. Complete its required configuration first. README CI checks the maintained source’s syntax and declarations; it does not claim that external services or the application workflow were exercised.

---

## Usage

### Common Workflows

<!-- readme-standards:begin example.usage -->
Source: [docs/readme/usage.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-security-trust/docs/readme/usage.py).

```python
from tba_contracts_security_trust import AcrEvaluationRequest

assert callable(AcrEvaluationRequest)
```
<!-- readme-standards:end example.usage -->

The following public-entry-point example belongs to `tba-contracts-security-trust`. Draft horizontal contracts and DTOs for security, trust, key, crypto, and cipher-suite components. Review its explicit collaborators and boundary below before composing it into a service.

### Configuration

Configure `tba-contracts-security-trust` through the APIs in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-security-trust/src/tba_contracts_security_trust/__init__.py); its [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-security-trust/pyproject.toml) describes installation requirements, not an implicit service configuration. No additional package-global configuration contract is inferred from dependencies.

### Error Handling

The inspected `tba-contracts-security-trust` source raises `ValueError`. Handle these at the calling boundary and consult the implementation for the triggering conditions.

### Best Practices

Use the explicit `tba-contracts-security-trust` imports documented below and keep collaborator configuration with the caller. Run the package’s relevant tests after changing `OpenRequest`, `OpenResult`, `ParseRequest`, `ParsedArtifact`, `CanonicalizeRequest`, `RewrapRequest`, `NormalizedDescriptor`, `ListKeysRequest`; an import or successful installation alone does not establish its runtime guarantees.

---

## Package Boundary

### What It Owns

`tba-contracts-security-trust` belongs to `002-contracts` and owns shared types and structural ports: Draft horizontal contracts and DTOs for security, trust, key, crypto, and cipher-suite components.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-security-trust/src/tba_contracts_security_trust/__init__.py).

Keep environment-specific service implementations or HTTP routing in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

### Public API and Import Surfaces

Import namespace: `tba_contracts_security_trust`.

Source-declared exports or types: `OpenRequest`, `OpenResult`, `ParseRequest`, `ParsedArtifact`, `CanonicalizeRequest`, `RewrapRequest`, `NormalizedDescriptor`, `ListKeysRequest`.

Inspect [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-security-trust/src/tba_contracts_security_trust/__init__.py) for exact signatures; this inventory does not designate every internal module as stable.

### Entry Points

<!-- readme-standards:begin entry-points -->
This package declares no command-line, GUI, or plugin entry points in its manifest.
<!-- readme-standards:end entry-points -->

### Injected Dependencies

The [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-security-trust/src/tba_contracts_security_trust/__init__.py) for `tba-contracts-security-trust` does not declare an explicit service-constructor or keyword-only factory hook in the inspected source. Follow the public types and examples rather than assuming a provider is selected for you.

Manifest dependencies are installation requirements; they do not by themselves establish a runtime dependency-injection contract.

### Protocol Consumers

The following layer-50 manifests directly depend on `tba-contracts-security-trust`:

- [tba-protocol-oauth](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oauth/README.md)
- [tba-protocol-oauth-protected-resource](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oauth-protected-resource/README.md)
- [tba-protocol-workload-spiffe-svid](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-workload-spiffe-svid/README.md)

Other direct consumers include [tba-bases-authentication-context](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-authentication-context/README.md), [tba-bases-authenticator](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-authenticator/README.md), [tba-bases-capability](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-capability/README.md), [tba-bases-certificate](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-certificate/README.md), [tba-bases-encryption](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-encryption/README.md), [tba-bases-key](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-key/README.md), [tba-bases-proof-of-possession](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-proof-of-possession/README.md), [tba-bases-protected-artifact](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-protected-artifact/README.md).

### Extensions

For `tba-contracts-security-trust`, use the source-declared public interfaces (`OpenRequest`, `OpenResult`, `ParseRequest`, `ParsedArtifact`, `CanonicalizeRequest`, `RewrapRequest`, `NormalizedDescriptor`, `ListKeysRequest`) when composing or extending behavior. Its entry-point section below is authoritative for registered plugins; no additional extension loader is inferred from the package name.

---

## Operations and Readiness

### Operational Requirements

`tba-contracts-security-trust` exposes shared types and structural ports. Inspect the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-security-trust/src/tba_contracts_security_trust/__init__.py) for the exported types and composition surface.

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

### Health and Observability

This README does not establish a standalone health endpoint for `tba-contracts-security-trust`. Observe the concrete caller’s results, exceptions, and existing test reports. An application that embeds this package must define its own health and telemetry contract.

### Security and Resource Limits

Apply the input, credential, and resource constraints implemented in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-security-trust/src/tba_contracts_security_trust/__init__.py). The `tba-contracts-security-trust` README gate is a documentation check, not a security review or a substitute for the implementation’s limits and caller authorization.

### Compatibility

This source version of `tba-contracts-security-trust` declares Python `>=3.10,<3.16`. Consult its dependency constraints before upgrading. Source-version and registry-version badges have separate meanings; this migration makes no additional platform or interoperability certification claim.

---

## Verification

### Tests

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-security-trust/src/tba_contracts_security_trust/__init__.py).

### Certification Status

No external certification is asserted for `tba-contracts-security-trust` by this documentation migration. README conformance, example syntax, runtime tests, and protocol or security certification are distinct evidence scopes.

### Evidence

The [README standards CI](https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml) records mechanical documentation results for its tested commit. The [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-security-trust/src/tba_contracts_security_trust/__init__.py) and example sources support the package-boundary description; external runtime behavior requires its own test evidence.

---

## FAQ

### Why

**Why select this package?** `tba-contracts-security-trust` provides draft horizontal contracts and DTOs for security, trust, key, crypto, and cipher-suite components; use its own API boundary rather than assuming neighboring packages are bundled or configured automatically.

### How

**How do I start?** Install or synchronize the environment under Getting Started, follow the maintained example for `tba-contracts-security-trust`, and consult [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-security-trust/src/tba_contracts_security_trust/__init__.py) for the exact types and signatures involved.

### When

**When should I validate an upgrade?** Recheck `tba-contracts-security-trust` whenever its source version, declared collaborators, configuration, or caller changes. Run relevant behavioral tests in addition to the README gate before promotion.

---

## Documentation and Related Packages

### More Documentation

The [repository contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md), [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-security-trust/src/tba_contracts_security_trust/__init__.py), and [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-security-trust/pyproject.toml) provide the supporting context for `tba-contracts-security-trust`. The [README policy](https://github.com/groupsum/readme-standards/blob/master/docs/outline.md) defines the common document structure.

### Related Packages

Declared local runtime dependencies:

- [tba-primitives-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/000-primitives/tba-primitives-identity/README.md)

Direct downstream consumers:

- [tba-bases-authentication-context](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-authentication-context/README.md)
- [tba-bases-authenticator](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-authenticator/README.md)
- [tba-bases-capability](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-capability/README.md)
- [tba-bases-certificate](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-certificate/README.md)
- [tba-bases-encryption](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-encryption/README.md)
- [tba-bases-key](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-key/README.md)
- [tba-bases-proof-of-possession](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-proof-of-possession/README.md)
- [tba-bases-protected-artifact](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-protected-artifact/README.md)
- [tba-bases-security-provenance](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-security-provenance/README.md)
- [tba-bases-security-trust-domain](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-security-trust-domain/README.md)
- [tba-bases-signing](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-signing/README.md)
- [tba-bases-token-introspection](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-token-introspection/README.md)

62 packages directly declare this dependency; the [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records the complete graph.

### Project Links

<!-- readme-standards:begin project-links -->
- [Documentation](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/002-contracts/tba-contracts-security-trust#readme)
- [Homepage](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/002-contracts/tba-contracts-security-trust#readme)
- [Issues](https://github.com/tigrbl/tigrbl_auth/issues)
- [PyPI](https://pypi.org/project/tba-contracts-security-trust/)
- [Repository](https://github.com/tigrbl/tigrbl_auth)
- [Source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/002-contracts/tba-contracts-security-trust)
- [pypi: tba-contracts-security-trust](https://pypi.org/project/tba-contracts-security-trust/)
<!-- readme-standards:end project-links -->

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/002-contracts/tba-contracts-security-trust)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-security-trust/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-security-trust/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-security-trust/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-contracts-security-trust/)

---

## Contributing

### How to Contribute

Follow the [contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md) and include a focused example or regression for changes to `tba-contracts-security-trust`. Keep package behavior, its documented boundary, and its tests aligned.

### Development Setup

Work from the `pkgs/002-contracts/tba-contracts-security-trust` checkout. Synchronize its declared development environment with uv, then run the relevant package tests and `python -m pytest docs/readme/test_examples.py`. The repository’s dedicated README job installs `readme-standards==0.1.3` without resolving unrelated runtime packages.

### Notes for Maintainers

Edit authored prose directly in this `tba-contracts-security-trust` README. Update source examples in `docs/readme/`, then run `readme-standards render --root . --write` from the package directory and review the diff. Required headings and generated blocks come from package-guide-v1.

---

## Governance

### Ownership and Decision Making

Changes to `tba-contracts-security-trust` follow the maintainer review process of [tigrbl/tigrbl_auth](https://github.com/tigrbl/tigrbl_auth) and its contribution guide. Author attribution remains in the [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-security-trust/pyproject.toml); this README does not assign new publishing or administrative authority.

### Standards and Policies

`tba-contracts-security-trust` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `002-contracts` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

### Lifecycle and Migration

The `tba-contracts-security-trust` source version is `0.1.1.dev1`. This change standardizes documentation and adds a development-only gate; it does not publish a new runtime version or declare a previously unpublished package released. Preserve explicit deprecation and replacement instructions where present.

---

## License and Attribution

### License

<!-- readme-standards:begin license -->
Licensed under `Apache-2.0`. See [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-security-trust/LICENSE).
<!-- readme-standards:end license -->

### Notices

<!-- readme-standards:begin notices -->
See [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-security-trust/NOTICE) for attribution.
<!-- readme-standards:end notices -->
