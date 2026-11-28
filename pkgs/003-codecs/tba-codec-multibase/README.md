# tba-codec-multibase

<!-- readme-standards:begin branding -->
<p align="center"><a href="https://github.com/tigrbl/tigrbl_auth"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="300"></a></p>
<p align="center"><strong>tba-codec-multibase</strong></p>
<p align="center">Multibase encoding and decoding for the base58btc alphabet.</p>
<p align="center">
<a href="https://pypi.org/project/tba-codec-multibase/"><img alt="pypi: tba-codec-multibase" src="https://img.shields.io/pypi/v/tba-codec-multibase?labelColor=1E293B&amp;color=1D4ED8"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-multibase/pyproject.toml"><img alt="Source version: 0.4.0.dev3" src="https://img.shields.io/static/v1?label=Source%20version&amp;message=0.4.0.dev3&amp;labelColor=1E293B&amp;color=4338CA"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-multibase/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/static/v1?label=Python&amp;message=%3E%3D3.10%2C%3C3.16&amp;labelColor=1E293B&amp;color=0F766E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-multibase/pyproject.toml"><img alt="Layer: 003-codecs" src="https://img.shields.io/static/v1?label=Layer&amp;message=003-codecs&amp;labelColor=1E293B&amp;color=6D28D9"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-multibase/README.md#lifecycle-and-migration"><img alt="Lifecycle: active" src="https://img.shields.io/static/v1?label=Lifecycle&amp;message=active&amp;labelColor=1E293B&amp;color=166534"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-multibase/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/static/v1?label=License&amp;message=Apache-2.0&amp;labelColor=1E293B&amp;color=86198F"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-multibase/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/static/v1?label=Notice&amp;message=attribution&amp;labelColor=1E293B&amp;color=86198F"></a>
</p>
<p align="center">
<a href="https://pypi.org/project/tba-codec-multibase/"><img alt="Monthly PyPI downloads: tba-codec-multibase" src="https://img.shields.io/pypi/dm/tba-codec-multibase?labelColor=1E293B&amp;color=0E7490"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-multibase/README.md"><img alt="README hits: tba-codec-multibase" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/pkgs/003-codecs/tba-codec-multibase/README.md.svg?label=README%20hits&amp;labelColor=1E293B&amp;color=0E7490"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="README standards: CI gate" src="https://img.shields.io/static/v1?label=README%20standards&amp;message=CI%20gate&amp;labelColor=1E293B&amp;color=1D4ED8"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-multibase/docs/readme/test_examples.py"><img alt="Tests: example source" src="https://img.shields.io/static/v1?label=Tests&amp;message=example%20source&amp;labelColor=1E293B&amp;color=0F766E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-multibase/README.md#certification-status"><img alt="Certification: not certified" src="https://img.shields.io/static/v1?label=Certification&amp;message=not%20certified&amp;labelColor=1E293B&amp;color=92400E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/tools/readme/POLICY.md"><img alt="Governance: repository policy" src="https://img.shields.io/static/v1?label=Governance&amp;message=repository%20policy&amp;labelColor=1E293B&amp;color=4338CA"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="Evidence: source and CI" src="https://img.shields.io/static/v1?label=Evidence&amp;message=source%20and%20CI&amp;labelColor=1E293B&amp;color=6D28D9"></a>
</p>
<p align="center"><a href="#overview">Overview</a> · <a href="#installation">Installation</a> · <a href="#quick-start">Quick Start</a> · <a href="#usage">Usage</a> · <a href="#public-api-and-import-surfaces">API</a> · <a href="#contributing">Contributing</a> · <a href="#governance">Governance</a> · <a href="#license">License</a></p>
<!-- readme-standards:end branding -->

---

## Overview

### Summary

Dependency-free Python codec for base58btc Multibase values. Use
`encode_base58btc(bytes)` and `decode_base58btc(str)`. Both functions handle
the lowercase `z` prefix and preserve leading zero bytes.

The codec converts bytes and text. Its callers set input size limits for
untrusted data and validate decoded values according to their protocols.

See the [Multibase registry](https://github.com/multiformats/multibase)
and [Base58 test vectors](https://datatracker.ietf.org/doc/html/draft-msporny-base58-02#section-5).

- Package: `tba-codec-multibase`
- Layer: `003-codecs`
- Responsibility: Multibase encoding and decoding for the base58btc alphabet.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-multibase/src/tba_codec_multibase/__init__.py).
- Distribution: Python package on PyPI.

### Why This Package

`tba-codec-multibase` isolates this responsibility: Multibase encoding and decoding for the base58btc alphabet. Its [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-multibase/src/tba_codec_multibase/__init__.py) exposes `decode_base58btc`, `encode_base58btc`, allowing consumers to select this package without treating adjacent packages as part of its public contract.

### When to Use

Choose `tba-codec-multibase` for this responsibility: Multibase encoding and decoding for the base58btc alphabet. Its `003-codecs` placement keeps representation encoding and decoding separate from issuer trust policy, key lifecycle, or HTTP endpoints.

### Features

- Public source surface: `decode_base58btc`, `encode_base58btc`.
- Declared responsibility: Multibase encoding and decoding for the base58btc alphabet.
- Versioned package metadata and maintained checkout examples.

### Non-Goals

`tba-codec-multibase` does not take ownership of issuer trust policy, key lifecycle, or HTTP endpoints.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

---

## Getting Started

### Prerequisites

Python `>=3.10,<3.16` is required. The [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-multibase/pyproject.toml) declares no direct runtime dependencies. Read the example’s inputs and service requirements before execution.

### Installation

Install the selected PyPI release of `tba-codec-multibase`:

```bash
uv pip install tba-codec-multibase
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/003-codecs/tba-codec-multibase
```

#### uv

<!-- readme-standards:begin installation.uv -->
```bash
uv add tba-codec-multibase
```
<!-- readme-standards:end installation.uv -->

#### pip

<!-- readme-standards:begin installation.pip -->
```bash
python -m pip install tba-codec-multibase
```
<!-- readme-standards:end installation.pip -->

#### Poetry

<!-- readme-standards:begin installation.poetry -->
```bash
poetry add tba-codec-multibase
```
<!-- readme-standards:end installation.poetry -->

### Quick Start

Build the package from the repository root.

```bash
uv build --wheel pkgs/003-codecs/tba-codec-multibase
```

#### Example

<!-- readme-standards:begin example.quick-start -->
Source: [docs/readme/quick_start.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-multibase/docs/readme/quick_start.py).

```python
import tba_codec_multibase

print(tba_codec_multibase.__name__)
```
<!-- readme-standards:end example.quick-start -->

#### Expected Result

The example demonstrates the documented `tba-codec-multibase` source boundary or workflow. Complete its required configuration first. README CI checks the maintained source’s syntax and declarations; it does not claim that external services or the application workflow were exercised.

---

## Usage

### Common Workflows

<!-- readme-standards:begin example.usage -->
Source: [docs/readme/usage.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-multibase/docs/readme/usage.py).

```python
import tba_codec_multibase

print(tba_codec_multibase.__name__)
```
<!-- readme-standards:end example.usage -->

The following public-entry-point example belongs to `tba-codec-multibase`. Multibase encoding and decoding for the base58btc alphabet. Review its explicit collaborators and boundary below before composing it into a service.

### Configuration

Configure `tba-codec-multibase` through the APIs in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-multibase/src/tba_codec_multibase/__init__.py); its [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-multibase/pyproject.toml) describes installation requirements, not an implicit service configuration. No additional package-global configuration contract is inferred from dependencies.

### Error Handling

The inspected `tba-codec-multibase` source raises `ValueError`. Handle these at the calling boundary and consult the implementation for the triggering conditions.

### Best Practices

Use the explicit `tba-codec-multibase` imports documented below and keep collaborator configuration with the caller. Run the package’s relevant tests after changing `decode_base58btc`, `encode_base58btc`; an import or successful installation alone does not establish its runtime guarantees.

---

## Package Boundary

### What It Owns

`tba-codec-multibase` belongs to `003-codecs` and owns representation encoding and decoding: Multibase encoding and decoding for the base58btc alphabet.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-multibase/src/tba_codec_multibase/__init__.py). Public exports include `decode_base58btc`, `encode_base58btc`.

Keep issuer trust policy, key lifecycle, or HTTP endpoints in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

### Public API and Import Surfaces

Import namespace: `tba_codec_multibase`.

Source-declared exports or types: `decode_base58btc`, `encode_base58btc`.

Inspect [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-multibase/src/tba_codec_multibase/__init__.py) for exact signatures; this inventory does not designate every internal module as stable.

### Entry Points

<!-- readme-standards:begin entry-points -->
This package declares no command-line, GUI, or plugin entry points in its manifest.
<!-- readme-standards:end entry-points -->

### Injected Dependencies

The [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-multibase/src/tba_codec_multibase/__init__.py) for `tba-codec-multibase` does not declare an explicit service-constructor or keyword-only factory hook in the inspected source. Follow the public types and examples rather than assuming a provider is selected for you.

Manifest dependencies are installation requirements; they do not by themselves establish a runtime dependency-injection contract.

### Protocol Consumers

The following layer-50 manifests directly depend on `tba-codec-multibase`:

- [tba-protocol-ucan](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-ucan/README.md)
- [tba-protocol-zcap](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-zcap/README.md)

Other direct consumers include [tba-codec-cid](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-cid/README.md).

### Extensions

For `tba-codec-multibase`, use the source-declared public interfaces (`decode_base58btc`, `encode_base58btc`) when composing or extending behavior. Its entry-point section below is authoritative for registered plugins; no additional extension loader is inferred from the package name.

---

## Operations and Readiness

### Operational Requirements

`tba-codec-multibase` exposes representation encoding and decoding. Public operations found in its source:

- `encode_base58btc` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-multibase/src/tba_codec_multibase/__init__.py).
- `decode_base58btc` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-multibase/src/tba_codec_multibase/__init__.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

### Health and Observability

This README does not establish a standalone health endpoint for `tba-codec-multibase`. Observe the concrete caller’s results, exceptions, and existing test reports. An application that embeds this package must define its own health and telemetry contract.

### Security and Resource Limits

Apply the input, credential, and resource constraints implemented in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-multibase/src/tba_codec_multibase/__init__.py). The `tba-codec-multibase` README gate is a documentation check, not a security review or a substitute for the implementation’s limits and caller authorization.

### Compatibility

This source version of `tba-codec-multibase` declares Python `>=3.10,<3.16`. Consult its dependency constraints before upgrading. Source-version and registry-version badges have separate meanings; this migration makes no additional platform or interoperability certification claim.

---

## Verification

### Tests

Check that the build produces a wheel with the package version declared in `pyproject.toml`.

### Certification Status

No external certification is asserted for `tba-codec-multibase` by this documentation migration. README conformance, example syntax, runtime tests, and protocol or security certification are distinct evidence scopes.

### Evidence

The [README standards CI](https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml) records mechanical documentation results for its tested commit. The [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-multibase/src/tba_codec_multibase/__init__.py) and example sources support the package-boundary description; external runtime behavior requires its own test evidence.

---

## FAQ

### Why

**Why select this package?** `tba-codec-multibase` provides multibase encoding and decoding for the base58btc alphabet; use its own API boundary rather than assuming neighboring packages are bundled or configured automatically.

### How

**How do I start?** Install or synchronize the environment under Getting Started, follow the maintained example for `tba-codec-multibase`, and consult [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-multibase/src/tba_codec_multibase/__init__.py) for the exact types and signatures involved.

### When

**When should I validate an upgrade?** Recheck `tba-codec-multibase` whenever its source version, declared collaborators, configuration, or caller changes. Run relevant behavioral tests in addition to the README gate before promotion.

---

## Documentation and Related Packages

### More Documentation

The [repository contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md), [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-multibase/src/tba_codec_multibase/__init__.py), and [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-multibase/pyproject.toml) provide the supporting context for `tba-codec-multibase`. The [README policy](https://github.com/groupsum/readme-standards/blob/master/docs/outline.md) defines the common document structure.

### Related Packages

Direct downstream consumers:

- [tba-codec-cid](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-cid/README.md)
- [tba-protocol-ucan](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-ucan/README.md)
- [tba-protocol-zcap](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-zcap/README.md)

### Project Links

<!-- readme-standards:begin project-links -->
- [Documentation](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/003-codecs/tba-codec-multibase#readme)
- [Homepage](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/003-codecs/tba-codec-multibase#readme)
- [Issues](https://github.com/tigrbl/tigrbl_auth/issues)
- [PyPI](https://pypi.org/project/tba-codec-multibase/)
- [Repository](https://github.com/tigrbl/tigrbl_auth)
- [Source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/003-codecs/tba-codec-multibase)
- [pypi: tba-codec-multibase](https://pypi.org/project/tba-codec-multibase/)
<!-- readme-standards:end project-links -->

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/003-codecs/tba-codec-multibase)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-multibase/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-multibase/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-multibase/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-codec-multibase/)

---

## Contributing

### How to Contribute

Follow the [contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md) and include a focused example or regression for changes to `tba-codec-multibase`. Keep package behavior, its documented boundary, and its tests aligned.

### Development Setup

Work from the `pkgs/003-codecs/tba-codec-multibase` checkout. Synchronize its declared development environment with uv, then run the relevant package tests and `python -m pytest docs/readme/test_examples.py`. The repository’s dedicated README job installs `readme-standards==0.1.3` without resolving unrelated runtime packages.

### Notes for Maintainers

Edit authored prose directly in this `tba-codec-multibase` README. Update source examples in `docs/readme/`, then run `readme-standards render --root . --write` from the package directory and review the diff. Required headings and generated blocks come from package-guide-v1.

---

## Governance

### Ownership and Decision Making

Changes to `tba-codec-multibase` follow the maintainer review process of [tigrbl/tigrbl_auth](https://github.com/tigrbl/tigrbl_auth) and its contribution guide. Author attribution remains in the [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-multibase/pyproject.toml); this README does not assign new publishing or administrative authority.

### Standards and Policies

`tba-codec-multibase` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `003-codecs` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

### Lifecycle and Migration

The `tba-codec-multibase` source version is `0.4.0.dev3`. This change standardizes documentation and adds a development-only gate; it does not publish a new runtime version or declare a previously unpublished package released. Preserve explicit deprecation and replacement instructions where present.

---

## License and Attribution

### License

<!-- readme-standards:begin license -->
Licensed under `Apache-2.0`. See [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-multibase/LICENSE).
<!-- readme-standards:end license -->

### Notices

<!-- readme-standards:begin notices -->
See [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-multibase/NOTICE) for attribution.
<!-- readme-standards:end notices -->
