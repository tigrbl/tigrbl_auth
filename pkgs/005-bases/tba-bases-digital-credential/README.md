# tba-bases-digital-credential

<!-- readme-standards:begin branding -->
<p align="center"><a href="https://github.com/tigrbl/tigrbl_auth"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="300"></a></p>
<p align="center"><strong>tba-bases-digital-credential</strong></p>
<p align="center">Protocol-neutral digital credential provider bases.</p>
<p align="center">
<a href="https://pypi.org/project/tba-bases-digital-credential/"><img alt="pypi: tba-bases-digital-credential" src="https://img.shields.io/pypi/v/tba-bases-digital-credential?labelColor=1E293B&amp;color=1D4ED8"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-digital-credential/pyproject.toml"><img alt="Source version: 0.4.0.dev3" src="https://img.shields.io/static/v1?label=Source%20version&amp;message=0.4.0.dev3&amp;labelColor=1E293B&amp;color=4338CA"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-digital-credential/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/static/v1?label=Python&amp;message=%3E%3D3.10%2C%3C3.16&amp;labelColor=1E293B&amp;color=0F766E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-digital-credential/pyproject.toml"><img alt="Layer: 005-bases" src="https://img.shields.io/static/v1?label=Layer&amp;message=005-bases&amp;labelColor=1E293B&amp;color=6D28D9"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-digital-credential/README.md#lifecycle-and-migration"><img alt="Lifecycle: active" src="https://img.shields.io/static/v1?label=Lifecycle&amp;message=active&amp;labelColor=1E293B&amp;color=166534"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-digital-credential/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/static/v1?label=License&amp;message=Apache-2.0&amp;labelColor=1E293B&amp;color=86198F"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-digital-credential/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/static/v1?label=Notice&amp;message=attribution&amp;labelColor=1E293B&amp;color=86198F"></a>
</p>
<p align="center">
<a href="https://pypi.org/project/tba-bases-digital-credential/"><img alt="Monthly PyPI downloads: tba-bases-digital-credential" src="https://img.shields.io/pypi/dm/tba-bases-digital-credential?labelColor=1E293B&amp;color=0E7490"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-digital-credential/README.md"><img alt="README hits: tba-bases-digital-credential" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/pkgs/005-bases/tba-bases-digital-credential/README.md.svg?label=README%20hits&amp;labelColor=1E293B&amp;color=0E7490"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="README standards: CI gate" src="https://img.shields.io/static/v1?label=README%20standards&amp;message=CI%20gate&amp;labelColor=1E293B&amp;color=1D4ED8"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-digital-credential/docs/readme/test_examples.py"><img alt="Tests: example source" src="https://img.shields.io/static/v1?label=Tests&amp;message=example%20source&amp;labelColor=1E293B&amp;color=0F766E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-digital-credential/README.md#certification-status"><img alt="Certification: not certified" src="https://img.shields.io/static/v1?label=Certification&amp;message=not%20certified&amp;labelColor=1E293B&amp;color=92400E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/tools/readme/POLICY.md"><img alt="Governance: repository policy" src="https://img.shields.io/static/v1?label=Governance&amp;message=repository%20policy&amp;labelColor=1E293B&amp;color=4338CA"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="Evidence: source and CI" src="https://img.shields.io/static/v1?label=Evidence&amp;message=source%20and%20CI&amp;labelColor=1E293B&amp;color=6D28D9"></a>
</p>
<p align="center"><a href="#overview">Overview</a> · <a href="#installation">Installation</a> · <a href="#quick-start">Quick Start</a> · <a href="#usage">Usage</a> · <a href="#public-api-and-import-surfaces">API</a> · <a href="#contributing">Contributing</a> · <a href="#governance">Governance</a> · <a href="#license">License</a></p>
<!-- readme-standards:end branding -->

---

## Overview

### Summary

Owns reusable implementation bases.

- Package: `tba-bases-digital-credential`
- Layer: `005-bases`
- Responsibility: Protocol-neutral digital credential provider bases.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-digital-credential/src/tba_bases_digital_credential/__init__.py).
- Distribution: Python package on PyPI.

### Why This Package

`tba-bases-digital-credential` isolates this responsibility: Protocol-neutral digital credential provider bases. Its [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-digital-credential/src/tba_bases_digital_credential/__init__.py) exposes `CredentialFormatBase`, `CredentialIssuerBase`, `CredentialStatusResolverBase`, `CredentialVerifierBase`, `PresentationFormatBase`, `PresentationVerifierBase`, `WalletAttestationVerifierBase`, allowing consumers to select this package without treating adjacent packages as part of its public contract.

### When to Use

Choose `tba-bases-digital-credential` for this responsibility: Protocol-neutral digital credential provider bases. Its `005-bases` placement keeps reusable component bases separate from deployment composition or implicit provider selection.

### Features

- `CredentialFormatBase`: declared in src/tba_bases_digital_credential/__init__.py
- `PresentationFormatBase`: declared in src/tba_bases_digital_credential/__init__.py
- `CredentialIssuerBase`: declared in src/tba_bases_digital_credential/__init__.py
- `CredentialVerifierBase`: declared in src/tba_bases_digital_credential/__init__.py
- `PresentationVerifierBase`: declared in src/tba_bases_digital_credential/__init__.py
- `CredentialStatusResolverBase`: declared in src/tba_bases_digital_credential/__init__.py
- `WalletAttestationVerifierBase`: declared in src/tba_bases_digital_credential/__init__.py

### Non-Goals

Higher-layer orchestration, lower-layer persistence, and protocol behavior outside this package's declared layer are not owned here.

---

## Getting Started

### Prerequisites

Python `>=3.10,<3.16` is required. The [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-digital-credential/pyproject.toml) declares runtime dependencies including `tba-contracts-digital-credential`. Read the example’s inputs and service requirements before execution.

### Installation

Install the selected PyPI release of `tba-bases-digital-credential`:

```bash
uv pip install tba-bases-digital-credential
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/005-bases/tba-bases-digital-credential
```

#### uv

<!-- readme-standards:begin installation.uv -->
```bash
uv add tba-bases-digital-credential
```
<!-- readme-standards:end installation.uv -->

#### pip

<!-- readme-standards:begin installation.pip -->
```bash
python -m pip install tba-bases-digital-credential
```
<!-- readme-standards:end installation.pip -->

#### Poetry

<!-- readme-standards:begin installation.poetry -->
```bash
poetry add tba-bases-digital-credential
```
<!-- readme-standards:end installation.poetry -->

### Quick Start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.


```bash
uv run --isolated --no-project --python 3.12 --with "tba-bases-digital-credential==0.4.0.dev3" python quickstart.py
```

The import and assertion succeed when the CredentialFormatBase entry point is available.

#### Example

<!-- readme-standards:begin example.quick-start -->
Source: [docs/readme/quick_start.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-digital-credential/docs/readme/quick_start.py).

```python
from tba_bases_digital_credential import CredentialFormatBase

assert callable(CredentialFormatBase)
```
<!-- readme-standards:end example.quick-start -->

#### Expected Result

The example demonstrates the documented `tba-bases-digital-credential` source boundary or workflow. Complete its required configuration first. README CI checks the maintained source’s syntax and declarations; it does not claim that external services or the application workflow were exercised.

---

## Usage

### Common Workflows

<!-- readme-standards:begin example.usage -->
Source: [docs/readme/usage.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-digital-credential/docs/readme/usage.py).

```python
from tba_bases_digital_credential import CredentialFormatBase

assert callable(CredentialFormatBase)
```
<!-- readme-standards:end example.usage -->

The following public-entry-point example belongs to `tba-bases-digital-credential`. Protocol-neutral digital credential provider bases. Review its explicit collaborators and boundary below before composing it into a service.

### Configuration

Configure `tba-bases-digital-credential` through the APIs in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-digital-credential/src/tba_bases_digital_credential/__init__.py); its [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-digital-credential/pyproject.toml) describes installation requirements, not an implicit service configuration. No additional package-global configuration contract is inferred from dependencies.

### Error Handling

The inspected `tba-bases-digital-credential` source does not establish a package-wide exception hierarchy. Preserve errors from its declared dependencies and validate inputs using the specific public contract in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-digital-credential/src/tba_bases_digital_credential/__init__.py).

### Best Practices

Use the explicit `tba-bases-digital-credential` imports documented below and keep collaborator configuration with the caller. Run the package’s relevant tests after changing `CredentialFormatBase`, `CredentialIssuerBase`, `CredentialStatusResolverBase`, `CredentialVerifierBase`, `PresentationFormatBase`, `PresentationVerifierBase`, `WalletAttestationVerifierBase`; an import or successful installation alone does not establish its runtime guarantees.

---

## Package Boundary

### What It Owns

`tba-bases-digital-credential` belongs to `005-bases` and owns reusable component bases: Protocol-neutral digital credential provider bases.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-digital-credential/src/tba_bases_digital_credential/__init__.py). Public exports include `CredentialFormatBase`, `CredentialIssuerBase`, `CredentialStatusResolverBase`, `CredentialVerifierBase`, `PresentationVerifierBase`, `PresentationFormatBase`, `WalletAttestationVerifierBase`.

Keep deployment composition or implicit provider selection in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

### Public API and Import Surfaces

Import namespace: `tba_bases_digital_credential`.

Source-declared exports or types: `CredentialFormatBase`, `CredentialIssuerBase`, `CredentialStatusResolverBase`, `CredentialVerifierBase`, `PresentationFormatBase`, `PresentationVerifierBase`, `WalletAttestationVerifierBase`.

Inspect [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-digital-credential/src/tba_bases_digital_credential/__init__.py) for exact signatures; this inventory does not designate every internal module as stable.

### Entry Points

<!-- readme-standards:begin entry-points -->
This package declares no command-line, GUI, or plugin entry points in its manifest.
<!-- readme-standards:end entry-points -->

### Injected Dependencies

The [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-digital-credential/src/tba_bases_digital_credential/__init__.py) for `tba-bases-digital-credential` does not declare an explicit service-constructor or keyword-only factory hook in the inspected source. Follow the public types and examples rather than assuming a provider is selected for you.

Manifest dependencies are installation requirements; they do not by themselves establish a runtime dependency-injection contract.

### Protocol Consumers

The following layer-50 manifests directly depend on `tba-bases-digital-credential`:

- [tba-protocol-credential-iso-mdoc](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-credential-iso-mdoc/README.md)

Other direct consumers include [tba-concrete-cwt-svid-extension-credential](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-cwt-svid-extension-credential/README.md), [tba-concrete-jwt-svid-credential](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-jwt-svid-credential/README.md), [tba-concrete-mdoc-credential](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-mdoc-credential/README.md), [tba-concrete-sd-jwt-vc-credential](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-sd-jwt-vc-credential/README.md), [tba-concrete-vc-cose-credential](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-vc-cose-credential/README.md), [tba-concrete-vc-jose-credential](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-vc-jose-credential/README.md), [tba-concrete-verifiable-credential](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-verifiable-credential/README.md), [tba-concrete-verifiable-presentation](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-verifiable-presentation/README.md).

### Extensions

For `tba-bases-digital-credential`, use the source-declared public interfaces (`CredentialFormatBase`, `CredentialIssuerBase`, `CredentialStatusResolverBase`, `CredentialVerifierBase`, `PresentationFormatBase`, `PresentationVerifierBase`, `WalletAttestationVerifierBase`) when composing or extending behavior. Its entry-point section below is authoritative for registered plugins; no additional extension loader is inferred from the package name.

---

## Operations and Readiness

### Operational Requirements

`tba-bases-digital-credential` exposes reusable component bases. Public operations found in its source:

- `CredentialIssuerBase.issue` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-digital-credential/src/tba_bases_digital_credential/__init__.py).
- `CredentialVerifierBase.verify` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-digital-credential/src/tba_bases_digital_credential/__init__.py).
- `PresentationVerifierBase.verify` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-digital-credential/src/tba_bases_digital_credential/__init__.py).
- `CredentialStatusResolverBase.resolve` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-digital-credential/src/tba_bases_digital_credential/__init__.py).
- `WalletAttestationVerifierBase.verify_wallet_attestation` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-digital-credential/src/tba_bases_digital_credential/__init__.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

### Health and Observability

This README does not establish a standalone health endpoint for `tba-bases-digital-credential`. Observe the concrete caller’s results, exceptions, and existing test reports. An application that embeds this package must define its own health and telemetry contract.

### Security and Resource Limits

Apply the input, credential, and resource constraints implemented in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-digital-credential/src/tba_bases_digital_credential/__init__.py). The `tba-bases-digital-credential` README gate is a documentation check, not a security review or a substitute for the implementation’s limits and caller authorization.

### Compatibility

This source version of `tba-bases-digital-credential` declares Python `>=3.10,<3.16`. Consult its dependency constraints before upgrading. Source-version and registry-version badges have separate meanings; this migration makes no additional platform or interoperability certification claim.

---

## Verification

### Tests

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-digital-credential/src/tba_bases_digital_credential/__init__.py).

### Certification Status

No external certification is asserted for `tba-bases-digital-credential` by this documentation migration. README conformance, example syntax, runtime tests, and protocol or security certification are distinct evidence scopes.

### Evidence

The [README standards CI](https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml) records mechanical documentation results for its tested commit. The [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-digital-credential/src/tba_bases_digital_credential/__init__.py) and example sources support the package-boundary description; external runtime behavior requires its own test evidence.

---

## FAQ

### Why

**Why select this package?** `tba-bases-digital-credential` provides protocol-neutral digital credential provider bases; use its own API boundary rather than assuming neighboring packages are bundled or configured automatically.

### How

**How do I start?** Install or synchronize the environment under Getting Started, follow the maintained example for `tba-bases-digital-credential`, and consult [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-digital-credential/src/tba_bases_digital_credential/__init__.py) for the exact types and signatures involved.

### When

**When should I validate an upgrade?** Recheck `tba-bases-digital-credential` whenever its source version, declared collaborators, configuration, or caller changes. Run relevant behavioral tests in addition to the README gate before promotion.

---

## Documentation and Related Packages

### More Documentation

The [repository contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md), [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-digital-credential/src/tba_bases_digital_credential/__init__.py), and [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-digital-credential/pyproject.toml) provide the supporting context for `tba-bases-digital-credential`. The [README policy](https://github.com/groupsum/readme-standards/blob/master/docs/outline.md) defines the common document structure.

### Related Packages

Declared local runtime dependencies:

- [tba-contracts-digital-credential](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-digital-credential/README.md)

Direct downstream consumers:

- [tba-concrete-cwt-svid-extension-credential](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-cwt-svid-extension-credential/README.md)
- [tba-concrete-jwt-svid-credential](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-jwt-svid-credential/README.md)
- [tba-concrete-mdoc-credential](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-mdoc-credential/README.md)
- [tba-concrete-sd-jwt-vc-credential](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-sd-jwt-vc-credential/README.md)
- [tba-concrete-vc-cose-credential](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-vc-cose-credential/README.md)
- [tba-concrete-vc-jose-credential](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-vc-jose-credential/README.md)
- [tba-concrete-verifiable-credential](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-verifiable-credential/README.md)
- [tba-concrete-verifiable-presentation](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-verifiable-presentation/README.md)
- [tba-concrete-wit-svid-credential](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-wit-svid-credential/README.md)
- [tba-concrete-x509-svid-credential](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-x509-svid-credential/README.md)
- [tba-protocol-credential-iso-mdoc](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-credential-iso-mdoc/README.md)
- [tba-provider-digital-credential-status](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-digital-credential-status/README.md)

15 packages directly declare this dependency; the [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records the complete graph.

### Project Links

<!-- readme-standards:begin project-links -->
- [Documentation](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/005-bases/tba-bases-digital-credential#readme)
- [Homepage](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/005-bases/tba-bases-digital-credential#readme)
- [Issues](https://github.com/tigrbl/tigrbl_auth/issues)
- [PyPI](https://pypi.org/project/tba-bases-digital-credential/)
- [Repository](https://github.com/tigrbl/tigrbl_auth)
- [Source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/005-bases/tba-bases-digital-credential)
- [pypi: tba-bases-digital-credential](https://pypi.org/project/tba-bases-digital-credential/)
<!-- readme-standards:end project-links -->

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/005-bases/tba-bases-digital-credential)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-digital-credential/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-digital-credential/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-digital-credential/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-bases-digital-credential/)

---

## Contributing

### How to Contribute

Follow the [contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md) and include a focused example or regression for changes to `tba-bases-digital-credential`. Keep package behavior, its documented boundary, and its tests aligned.

### Development Setup

Work from the `pkgs/005-bases/tba-bases-digital-credential` checkout. Synchronize its declared development environment with uv, then run the relevant package tests and `python -m pytest docs/readme/test_examples.py`. The repository’s dedicated README job installs `readme-standards==0.1.3` without resolving unrelated runtime packages.

### Notes for Maintainers

Edit authored prose directly in this `tba-bases-digital-credential` README. Update source examples in `docs/readme/`, then run `readme-standards render --root . --write` from the package directory and review the diff. Required headings and generated blocks come from package-guide-v1.

---

## Governance

### Ownership and Decision Making

Changes to `tba-bases-digital-credential` follow the maintainer review process of [tigrbl/tigrbl_auth](https://github.com/tigrbl/tigrbl_auth) and its contribution guide. Author attribution remains in the [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-digital-credential/pyproject.toml); this README does not assign new publishing or administrative authority.

### Standards and Policies

`tba-bases-digital-credential` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `005-bases` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

### Lifecycle and Migration

The `tba-bases-digital-credential` source version is `0.4.0.dev3`. This change standardizes documentation and adds a development-only gate; it does not publish a new runtime version or declare a previously unpublished package released. Preserve explicit deprecation and replacement instructions where present.

---

## License and Attribution

### License

<!-- readme-standards:begin license -->
Licensed under `Apache-2.0`. See [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-digital-credential/LICENSE).
<!-- readme-standards:end license -->

### Notices

<!-- readme-standards:begin notices -->
See [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-digital-credential/NOTICE) for attribution.
<!-- readme-standards:end notices -->
