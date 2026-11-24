# tba-codec-dag-cbor

<!-- readme-standards:begin branding -->
<p align="center"><a href="https://github.com/tigrbl/tigrbl_auth"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="300"></a></p>
<p align="center"><strong>tba-codec-dag-cbor</strong></p>
<p align="center">Strict canonical DAG-CBOR with IPLD CID links.</p>
<p align="center">
<a href="https://pypi.org/project/tba-codec-dag-cbor/"><img alt="pypi: tba-codec-dag-cbor" src="https://img.shields.io/pypi/v/tba-codec-dag-cbor?labelColor=1E293B&amp;color=1D4ED8"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-dag-cbor/pyproject.toml"><img alt="Source version: 0.4.0.dev3" src="https://img.shields.io/static/v1?label=Source%20version&amp;message=0.4.0.dev3&amp;labelColor=1E293B&amp;color=4338CA"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-dag-cbor/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/static/v1?label=Python&amp;message=%3E%3D3.10%2C%3C3.16&amp;labelColor=1E293B&amp;color=0F766E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-dag-cbor/pyproject.toml"><img alt="Layer: 003-codecs" src="https://img.shields.io/static/v1?label=Layer&amp;message=003-codecs&amp;labelColor=1E293B&amp;color=6D28D9"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-dag-cbor/README.md#lifecycle-and-migration"><img alt="Lifecycle: active" src="https://img.shields.io/static/v1?label=Lifecycle&amp;message=active&amp;labelColor=1E293B&amp;color=166534"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-dag-cbor/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/static/v1?label=License&amp;message=Apache-2.0&amp;labelColor=1E293B&amp;color=86198F"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-dag-cbor/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/static/v1?label=Notice&amp;message=attribution&amp;labelColor=1E293B&amp;color=86198F"></a>
</p>
<p align="center">
<a href="https://pypi.org/project/tba-codec-dag-cbor/"><img alt="Monthly PyPI downloads: tba-codec-dag-cbor" src="https://img.shields.io/pypi/dm/tba-codec-dag-cbor?labelColor=1E293B&amp;color=0E7490"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-dag-cbor/README.md"><img alt="README hits: tba-codec-dag-cbor" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/pkgs/003-codecs/tba-codec-dag-cbor/README.md.svg?label=README%20hits&amp;labelColor=1E293B&amp;color=0E7490"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="README standards: CI gate" src="https://img.shields.io/static/v1?label=README%20standards&amp;message=CI%20gate&amp;labelColor=1E293B&amp;color=1D4ED8"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-dag-cbor/docs/readme/test_examples.py"><img alt="Tests: example source" src="https://img.shields.io/static/v1?label=Tests&amp;message=example%20source&amp;labelColor=1E293B&amp;color=0F766E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-dag-cbor/README.md#certification-status"><img alt="Certification: not certified" src="https://img.shields.io/static/v1?label=Certification&amp;message=not%20certified&amp;labelColor=1E293B&amp;color=92400E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/tools/readme/POLICY.md"><img alt="Governance: repository policy" src="https://img.shields.io/static/v1?label=Governance&amp;message=repository%20policy&amp;labelColor=1E293B&amp;color=4338CA"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="Evidence: source and CI" src="https://img.shields.io/static/v1?label=Evidence&amp;message=source%20and%20CI&amp;labelColor=1E293B&amp;color=6D28D9"></a>
</p>
<p align="center"><a href="#overview">Overview</a> · <a href="#installation">Installation</a> · <a href="#quick-start">Quick Start</a> · <a href="#usage">Usage</a> · <a href="#public-api-and-import-surfaces">API</a> · <a href="#contributing">Contributing</a> · <a href="#governance">Governance</a> · <a href="#license">License</a></p>
<!-- readme-standards:end branding -->

---

## Overview

### Summary

Use `encode` and `decode` for canonical DAG-CBOR. CID links use tag 42 and the binary identity prefix. Decoding rejects duplicate keys, trailing data and noncanonical encodings. Callers set message size limits and protocol constraints.

[Specification](https://ipld.io/specs/codecs/dag-cbor/spec/)

- Package: `tba-codec-dag-cbor`
- Layer: `003-codecs`
- Responsibility: Strict canonical DAG-CBOR with IPLD CID links.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-dag-cbor/src/tba_codec_dag_cbor/__init__.py).
- Distribution: Python package on PyPI.

### Why This Package

`tba-codec-dag-cbor` isolates this responsibility: Strict canonical DAG-CBOR with IPLD CID links. Its [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-dag-cbor/src/tba_codec_dag_cbor/__init__.py) exposes `CBORTag`, `cid_link`, `decode`, `encode`, `link_cid`, allowing consumers to select this package without treating adjacent packages as part of its public contract.

### When to Use

Choose `tba-codec-dag-cbor` for this responsibility: Strict canonical DAG-CBOR with IPLD CID links. Its `003-codecs` placement keeps representation encoding and decoding separate from issuer trust policy, key lifecycle, or HTTP endpoints.

### Features

- Public source surface: `CBORTag`, `cid_link`, `decode`, `encode`, `link_cid`.
- Declared responsibility: Strict canonical DAG-CBOR with IPLD CID links.
- Versioned package metadata and maintained checkout examples.

### Non-Goals

`tba-codec-dag-cbor` does not take ownership of issuer trust policy, key lifecycle, or HTTP endpoints.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

---

## Getting Started

### Prerequisites

Python `>=3.10,<3.16` is required. The [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-dag-cbor/pyproject.toml) declares runtime dependencies including `cbor2`, `tba-codec-cid`. Read the example’s inputs and service requirements before execution.

### Installation

Install the selected PyPI release of `tba-codec-dag-cbor`:

```bash
uv pip install tba-codec-dag-cbor
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/003-codecs/tba-codec-dag-cbor
```

#### uv

<!-- readme-standards:begin installation.uv -->
```bash
uv add tba-codec-dag-cbor
```
<!-- readme-standards:end installation.uv -->

#### pip

<!-- readme-standards:begin installation.pip -->
```bash
python -m pip install tba-codec-dag-cbor
```
<!-- readme-standards:end installation.pip -->

#### Poetry

<!-- readme-standards:begin installation.poetry -->
```bash
poetry add tba-codec-dag-cbor
```
<!-- readme-standards:end installation.poetry -->

### Quick Start

Build the package from the repository root.

```bash
uv build --wheel pkgs/003-codecs/tba-codec-dag-cbor
```

#### Example

<!-- readme-standards:begin example.quick-start -->
Source: [docs/readme/quick_start.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-dag-cbor/docs/readme/quick_start.py).

```python
import tba_codec_dag_cbor

print(tba_codec_dag_cbor.__name__)
```
<!-- readme-standards:end example.quick-start -->

#### Expected Result

The example demonstrates the documented `tba-codec-dag-cbor` source boundary or workflow. Complete its required configuration first. README CI checks the maintained source’s syntax and declarations; it does not claim that external services or the application workflow were exercised.

---

## Usage

### Common Workflows

<!-- readme-standards:begin example.usage -->
Source: [docs/readme/usage.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-dag-cbor/docs/readme/usage.py).

```python
import tba_codec_dag_cbor

print(tba_codec_dag_cbor.__name__)
```
<!-- readme-standards:end example.usage -->

The following public-entry-point example belongs to `tba-codec-dag-cbor`. Strict canonical DAG-CBOR with IPLD CID links. Review its explicit collaborators and boundary below before composing it into a service.

### Configuration

Configure `tba-codec-dag-cbor` through the APIs in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-dag-cbor/src/tba_codec_dag_cbor/__init__.py); its [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-dag-cbor/pyproject.toml) describes installation requirements, not an implicit service configuration. No additional package-global configuration contract is inferred from dependencies.

### Error Handling

The inspected `tba-codec-dag-cbor` source raises `ValueError`. Handle these at the calling boundary and consult the implementation for the triggering conditions.

### Best Practices

Use the explicit `tba-codec-dag-cbor` imports documented below and keep collaborator configuration with the caller. Run the package’s relevant tests after changing `CBORTag`, `cid_link`, `decode`, `encode`, `link_cid`; an import or successful installation alone does not establish its runtime guarantees.

---

## Package Boundary

### What It Owns

`tba-codec-dag-cbor` belongs to `003-codecs` and owns representation encoding and decoding: Strict canonical DAG-CBOR with IPLD CID links.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-dag-cbor/src/tba_codec_dag_cbor/__init__.py). Public exports include `CBORTag`, `cid_link`, `decode`, `encode`, `link_cid`.

Keep issuer trust policy, key lifecycle, or HTTP endpoints in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

### Public API and Import Surfaces

Import namespace: `tba_codec_dag_cbor`.

Source-declared exports or types: `CBORTag`, `cid_link`, `decode`, `encode`, `link_cid`.

Inspect [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-dag-cbor/src/tba_codec_dag_cbor/__init__.py) for exact signatures; this inventory does not designate every internal module as stable.

### Entry Points

<!-- readme-standards:begin entry-points -->
This package declares no command-line, GUI, or plugin entry points in its manifest.
<!-- readme-standards:end entry-points -->

### Injected Dependencies

Explicit construction inputs and collaborators for `tba-codec-dag-cbor`:

- `encode` construction inputs: `max_depth`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-dag-cbor/src/tba_codec_dag_cbor/__init__.py).
- `decode` construction inputs: `max_depth`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-dag-cbor/src/tba_codec_dag_cbor/__init__.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

### Protocol Consumers

The following layer-50 manifests directly depend on `tba-codec-dag-cbor`:

- [tba-protocol-ucan](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-ucan/README.md)

### Extensions

For `tba-codec-dag-cbor`, use the source-declared public interfaces (`CBORTag`, `cid_link`, `decode`, `encode`, `link_cid`) when composing or extending behavior. Its entry-point section below is authoritative for registered plugins; no additional extension loader is inferred from the package name.

---

## Operations and Readiness

### Operational Requirements

`tba-codec-dag-cbor` exposes representation encoding and decoding. Public operations found in its source:

- `cid_link` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-dag-cbor/src/tba_codec_dag_cbor/__init__.py).
- `link_cid` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-dag-cbor/src/tba_codec_dag_cbor/__init__.py).
- `encode` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-dag-cbor/src/tba_codec_dag_cbor/__init__.py).
- `decode` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-dag-cbor/src/tba_codec_dag_cbor/__init__.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

### Health and Observability

This README does not establish a standalone health endpoint for `tba-codec-dag-cbor`. Observe the concrete caller’s results, exceptions, and existing test reports. An application that embeds this package must define its own health and telemetry contract.

### Security and Resource Limits

Apply the input, credential, and resource constraints implemented in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-dag-cbor/src/tba_codec_dag_cbor/__init__.py). The `tba-codec-dag-cbor` README gate is a documentation check, not a security review or a substitute for the implementation’s limits and caller authorization.

### Compatibility

This source version of `tba-codec-dag-cbor` declares Python `>=3.10,<3.16`. Consult its dependency constraints before upgrading. Source-version and registry-version badges have separate meanings; this migration makes no additional platform or interoperability certification claim.

---

## Verification

### Tests

Check that the build produces a wheel with the package version declared in `pyproject.toml`.

### Certification Status

No external certification is asserted for `tba-codec-dag-cbor` by this documentation migration. README conformance, example syntax, runtime tests, and protocol or security certification are distinct evidence scopes.

### Evidence

The [README standards CI](https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml) records mechanical documentation results for its tested commit. The [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-dag-cbor/src/tba_codec_dag_cbor/__init__.py) and example sources support the package-boundary description; external runtime behavior requires its own test evidence.

---

## FAQ

### Why

**Why select this package?** `tba-codec-dag-cbor` provides strict canonical DAG-CBOR with IPLD CID links; use its own API boundary rather than assuming neighboring packages are bundled or configured automatically.

### How

**How do I start?** Install or synchronize the environment under Getting Started, follow the maintained example for `tba-codec-dag-cbor`, and consult [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-dag-cbor/src/tba_codec_dag_cbor/__init__.py) for the exact types and signatures involved.

### When

**When should I validate an upgrade?** Recheck `tba-codec-dag-cbor` whenever its source version, declared collaborators, configuration, or caller changes. Run relevant behavioral tests in addition to the README gate before promotion.

---

## Documentation and Related Packages

### More Documentation

The [repository contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md), [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-dag-cbor/src/tba_codec_dag_cbor/__init__.py), and [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-dag-cbor/pyproject.toml) provide the supporting context for `tba-codec-dag-cbor`. The [README policy](https://github.com/groupsum/readme-standards/blob/master/docs/outline.md) defines the common document structure.

### Related Packages

Declared local runtime dependencies:

- [tba-codec-cid](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-cid/README.md)

Direct downstream consumers:

- [tba-protocol-ucan](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-ucan/README.md)

### Project Links

<!-- readme-standards:begin project-links -->
- [Documentation](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/003-codecs/tba-codec-dag-cbor#readme)
- [Homepage](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/003-codecs/tba-codec-dag-cbor#readme)
- [Issues](https://github.com/tigrbl/tigrbl_auth/issues)
- [PyPI](https://pypi.org/project/tba-codec-dag-cbor/)
- [Repository](https://github.com/tigrbl/tigrbl_auth)
- [Source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/003-codecs/tba-codec-dag-cbor)
- [pypi: tba-codec-dag-cbor](https://pypi.org/project/tba-codec-dag-cbor/)
<!-- readme-standards:end project-links -->

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/003-codecs/tba-codec-dag-cbor)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-dag-cbor/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-dag-cbor/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-dag-cbor/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-codec-dag-cbor/)

---

## Contributing

### How to Contribute

Follow the [contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md) and include a focused example or regression for changes to `tba-codec-dag-cbor`. Keep package behavior, its documented boundary, and its tests aligned.

### Development Setup

Work from the `pkgs/003-codecs/tba-codec-dag-cbor` checkout. Synchronize its declared development environment with uv, then run the relevant package tests and `python -m pytest docs/readme/test_examples.py`. The repository’s dedicated README job installs `readme-standards==0.1.3` without resolving unrelated runtime packages.

### Notes for Maintainers

Edit authored prose directly in this `tba-codec-dag-cbor` README. Update source examples in `docs/readme/`, then run `readme-standards render --root . --write` from the package directory and review the diff. Required headings and generated blocks come from package-guide-v1.

---

## Governance

### Ownership and Decision Making

Changes to `tba-codec-dag-cbor` follow the maintainer review process of [tigrbl/tigrbl_auth](https://github.com/tigrbl/tigrbl_auth) and its contribution guide. Author attribution remains in the [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-dag-cbor/pyproject.toml); this README does not assign new publishing or administrative authority.

### Standards and Policies

`tba-codec-dag-cbor` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `003-codecs` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

### Lifecycle and Migration

The `tba-codec-dag-cbor` source version is `0.4.0.dev3`. This change standardizes documentation and adds a development-only gate; it does not publish a new runtime version or declare a previously unpublished package released. Preserve explicit deprecation and replacement instructions where present.

---

## License and Attribution

### License

<!-- readme-standards:begin license -->
Licensed under `Apache-2.0`. See [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-dag-cbor/LICENSE).
<!-- readme-standards:end license -->

### Notices

<!-- readme-standards:begin notices -->
See [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-dag-cbor/NOTICE) for attribution.
<!-- readme-standards:end notices -->
