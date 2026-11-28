# tba-provider-bimi-mark-certificate

<!-- readme-standards:begin branding -->
<p align="center"><a href="https://github.com/tigrbl/tigrbl_auth"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="300"></a></p>
<p align="center"><strong>tba-provider-bimi-mark-certificate</strong></p>
<p align="center">BIMI Mark Certificate path and evidence verification.</p>
<p align="center">
<a href="https://pypi.org/project/tba-provider-bimi-mark-certificate/"><img alt="pypi: tba-provider-bimi-mark-certificate" src="https://img.shields.io/pypi/v/tba-provider-bimi-mark-certificate?labelColor=1E293B&amp;color=1D4ED8"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-bimi-mark-certificate/pyproject.toml"><img alt="Source version: 0.4.0.dev3" src="https://img.shields.io/static/v1?label=Source%20version&amp;message=0.4.0.dev3&amp;labelColor=1E293B&amp;color=4338CA"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-bimi-mark-certificate/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/static/v1?label=Python&amp;message=%3E%3D3.10%2C%3C3.16&amp;labelColor=1E293B&amp;color=0F766E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-bimi-mark-certificate/pyproject.toml"><img alt="Layer: 020-providers" src="https://img.shields.io/static/v1?label=Layer&amp;message=020-providers&amp;labelColor=1E293B&amp;color=6D28D9"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-bimi-mark-certificate/README.md#lifecycle-and-migration"><img alt="Lifecycle: active" src="https://img.shields.io/static/v1?label=Lifecycle&amp;message=active&amp;labelColor=1E293B&amp;color=166534"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-bimi-mark-certificate/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/static/v1?label=License&amp;message=Apache-2.0&amp;labelColor=1E293B&amp;color=86198F"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-bimi-mark-certificate/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/static/v1?label=Notice&amp;message=attribution&amp;labelColor=1E293B&amp;color=86198F"></a>
</p>
<p align="center">
<a href="https://pypi.org/project/tba-provider-bimi-mark-certificate/"><img alt="Monthly PyPI downloads: tba-provider-bimi-mark-certificate" src="https://img.shields.io/pypi/dm/tba-provider-bimi-mark-certificate?labelColor=1E293B&amp;color=0E7490"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-bimi-mark-certificate/README.md"><img alt="README hits: tba-provider-bimi-mark-certificate" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/pkgs/020-providers/tba-provider-bimi-mark-certificate/README.md.svg?label=README%20hits&amp;labelColor=1E293B&amp;color=0E7490"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="README standards: CI gate" src="https://img.shields.io/static/v1?label=README%20standards&amp;message=CI%20gate&amp;labelColor=1E293B&amp;color=1D4ED8"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-bimi-mark-certificate/docs/readme/test_examples.py"><img alt="Tests: example source" src="https://img.shields.io/static/v1?label=Tests&amp;message=example%20source&amp;labelColor=1E293B&amp;color=0F766E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-bimi-mark-certificate/README.md#certification-status"><img alt="Certification: not certified" src="https://img.shields.io/static/v1?label=Certification&amp;message=not%20certified&amp;labelColor=1E293B&amp;color=92400E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/tools/readme/POLICY.md"><img alt="Governance: repository policy" src="https://img.shields.io/static/v1?label=Governance&amp;message=repository%20policy&amp;labelColor=1E293B&amp;color=4338CA"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="Evidence: source and CI" src="https://img.shields.io/static/v1?label=Evidence&amp;message=source%20and%20CI&amp;labelColor=1E293B&amp;color=6D28D9"></a>
</p>
<p align="center"><a href="#overview">Overview</a> · <a href="#installation">Installation</a> · <a href="#quick-start">Quick Start</a> · <a href="#usage">Usage</a> · <a href="#public-api-and-import-surfaces">API</a> · <a href="#contributing">Contributing</a> · <a href="#governance">Governance</a> · <a href="#license">License</a></p>
<!-- readme-standards:end branding -->

---

## Overview

### Summary

BIMI Mark Certificate path and evidence verification.

`MarkCertificatePathBackend` accepts an explicit set of RFC 6962 CT log public
keys in PEM format and a callable that supplies CRL bytes by distribution-point
URL. It validates the X.509 path against BIMI-scoped anchors, verifies signed
CRL coverage for the leaf and intermediates, and verifies at least one
embedded SCT against the configured keys. Callers configure which roots and
logs they trust and how they obtain fresh CRLs.

The provider delegates PKIX, CRL, and SCT verification to
`tba-provider-certificate-evidence`. This package applies the Mark Certificate
algorithm and EKU rules and scopes the permitted trust anchors.

Supply a TBA `TrustAnchorProviderPort` to use the backend directly as a
`CertificatePathValidatorPort`. To use existing
`ProfiledCertificatePathValidator` dispatch, register the callable backend
under `CertificateProfile.BIMI_MARK`. The dispatcher's leaf status provider is
an additional check in that composition. The backend performs its own
request-local evidence verification in both cases.

The backend uses supplied CRLs and performs no HTTP requests. A missing fresh
CRL or an unconfigured CT log can yield an indeterminate decision. The provider
doesn't use the system Web PKI trust store for Mark Certificates.

- Package: `tba-provider-bimi-mark-certificate`
- Layer: `020-providers`
- Responsibility: BIMI Mark Certificate path and evidence verification.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-bimi-mark-certificate/src/tba_provider_bimi_mark_certificate/__init__.py).
- Distribution: Python package on PyPI.

### Why This Package

`tba-provider-bimi-mark-certificate` isolates this responsibility: BIMI Mark Certificate path and evidence verification. Its [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-bimi-mark-certificate/src/tba_provider_bimi_mark_certificate/revocation.py) exposes `CrlSource`, `MarkCertificatePathBackend`, allowing consumers to select this package without treating adjacent packages as part of its public contract.

### When to Use

Choose `tba-provider-bimi-mark-certificate` for this responsibility: BIMI Mark Certificate path and evidence verification. Its `020-providers` placement keeps replaceable environment implementations separate from capability orchestration, storage table ownership, or HTTP routing.

### Features

- `MarkCertificatePathBackend`: BIMI path backend with a request-local trust and evidence check.

### Non-Goals

`tba-provider-bimi-mark-certificate` does not take ownership of capability orchestration, storage table ownership, or HTTP routing.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

---

## Getting Started

### Prerequisites

Python `>=3.10,<3.16` is required. The [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-bimi-mark-certificate/pyproject.toml) declares runtime dependencies including `cryptography`, `tba-contracts-security-trust`, `tba-provider-certificate-evidence`. Read the example’s inputs and service requirements before execution.

### Installation

Install the selected PyPI release of `tba-provider-bimi-mark-certificate`:

```bash
uv pip install tba-provider-bimi-mark-certificate
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/020-providers/tba-provider-bimi-mark-certificate
```

#### uv

<!-- readme-standards:begin installation.uv -->
```bash
uv add tba-provider-bimi-mark-certificate
```
<!-- readme-standards:end installation.uv -->

#### pip

<!-- readme-standards:begin installation.pip -->
```bash
python -m pip install tba-provider-bimi-mark-certificate
```
<!-- readme-standards:end installation.pip -->

#### Poetry

<!-- readme-standards:begin installation.poetry -->
```bash
poetry add tba-provider-bimi-mark-certificate
```
<!-- readme-standards:end installation.poetry -->

### Quick Start

Build the package from the repository root.

```bash
uv build --wheel pkgs/020-providers/tba-provider-bimi-mark-certificate
```

#### Example

<!-- readme-standards:begin example.quick-start -->
Source: [docs/readme/quick_start.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-bimi-mark-certificate/docs/readme/quick_start.py).

```python
import tba_provider_bimi_mark_certificate

print(tba_provider_bimi_mark_certificate.__name__)
```
<!-- readme-standards:end example.quick-start -->

#### Expected Result

The example demonstrates the documented `tba-provider-bimi-mark-certificate` source boundary or workflow. Complete its required configuration first. README CI checks the maintained source’s syntax and declarations; it does not claim that external services or the application workflow were exercised.

---

## Usage

### Common Workflows

<!-- readme-standards:begin example.usage -->
Source: [docs/readme/usage.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-bimi-mark-certificate/docs/readme/usage.py).

```python
import tba_provider_bimi_mark_certificate

print(tba_provider_bimi_mark_certificate.__name__)
```
<!-- readme-standards:end example.usage -->

The following public-entry-point example belongs to `tba-provider-bimi-mark-certificate`. BIMI Mark Certificate path and evidence verification. Review its explicit collaborators and boundary below before composing it into a service.

### Configuration

Configure `tba-provider-bimi-mark-certificate` through the APIs in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-bimi-mark-certificate/src/tba_provider_bimi_mark_certificate/revocation.py); its [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-bimi-mark-certificate/pyproject.toml) describes installation requirements, not an implicit service configuration. No additional package-global configuration contract is inferred from dependencies.

### Error Handling

The inspected `tba-provider-bimi-mark-certificate` source raises `ValueError`. Handle these at the calling boundary and consult the implementation for the triggering conditions.

### Best Practices

Use the explicit `tba-provider-bimi-mark-certificate` imports documented below and keep collaborator configuration with the caller. Run the package’s relevant tests after changing `CrlSource`, `MarkCertificatePathBackend`; an import or successful installation alone does not establish its runtime guarantees.

---

## Package Boundary

### What It Owns

`tba-provider-bimi-mark-certificate` belongs to `020-providers` and owns replaceable environment implementations: BIMI Mark Certificate path and evidence verification.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-bimi-mark-certificate/src/tba_provider_bimi_mark_certificate/__init__.py). Public exports include `CrlSource`, `MarkCertificatePathBackend`.

Keep capability orchestration, storage table ownership, or HTTP routing in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

### Public API and Import Surfaces

Import namespace: `tba_provider_bimi_mark_certificate`.

Source-declared exports or types: `CrlSource`, `MarkCertificatePathBackend`.

Inspect [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-bimi-mark-certificate/src/tba_provider_bimi_mark_certificate/revocation.py) for exact signatures; this inventory does not designate every internal module as stable.

### Entry Points

<!-- readme-standards:begin entry-points -->
This package declares no command-line, GUI, or plugin entry points in its manifest.
<!-- readme-standards:end entry-points -->

### Injected Dependencies

Explicit construction inputs and collaborators for `tba-provider-bimi-mark-certificate`:

- `MarkCertificatePathBackend` construction inputs: `crl_source`, `ct_logs`, `anchors`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-bimi-mark-certificate/src/tba_provider_bimi_mark_certificate/path.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

### Protocol Consumers

No direct package-manifest dependency on `tba-provider-bimi-mark-certificate` was found in the audited three-repository inventory. External consumers may still use its documented imports or commands.

### Extensions

For `tba-provider-bimi-mark-certificate`, use the source-declared public interfaces (`CrlSource`, `MarkCertificatePathBackend`) when composing or extending behavior. Its entry-point section below is authoritative for registered plugins; no additional extension loader is inferred from the package name.

---

## Operations and Readiness

### Operational Requirements

`tba-provider-bimi-mark-certificate` exposes replaceable environment implementations. Public operations found in its source:

- `MarkCertificatePathBackend.validate` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-bimi-mark-certificate/src/tba_provider_bimi_mark_certificate/path.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

### Health and Observability

This README does not establish a standalone health endpoint for `tba-provider-bimi-mark-certificate`. Observe the concrete caller’s results, exceptions, and existing test reports. An application that embeds this package must define its own health and telemetry contract.

### Security and Resource Limits

Apply the input, credential, and resource constraints implemented in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-bimi-mark-certificate/src/tba_provider_bimi_mark_certificate/revocation.py). The `tba-provider-bimi-mark-certificate` README gate is a documentation check, not a security review or a substitute for the implementation’s limits and caller authorization.

### Compatibility

This source version of `tba-provider-bimi-mark-certificate` declares Python `>=3.10,<3.16`. Consult its dependency constraints before upgrading. Source-version and registry-version badges have separate meanings; this migration makes no additional platform or interoperability certification claim.

---

## Verification

### Tests

Check that the build produces a wheel with the package version declared in `pyproject.toml`.

### Certification Status

No external certification is asserted for `tba-provider-bimi-mark-certificate` by this documentation migration. README conformance, example syntax, runtime tests, and protocol or security certification are distinct evidence scopes.

### Evidence

The [README standards CI](https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml) records mechanical documentation results for its tested commit. The [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-bimi-mark-certificate/src/tba_provider_bimi_mark_certificate/revocation.py) and example sources support the package-boundary description; external runtime behavior requires its own test evidence.

---

## FAQ

### Why

**Why select this package?** `tba-provider-bimi-mark-certificate` provides bIMI Mark Certificate path and evidence verification; use its own API boundary rather than assuming neighboring packages are bundled or configured automatically.

### How

**How do I start?** Install or synchronize the environment under Getting Started, follow the maintained example for `tba-provider-bimi-mark-certificate`, and consult [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-bimi-mark-certificate/src/tba_provider_bimi_mark_certificate/revocation.py) for the exact types and signatures involved.

### When

**When should I validate an upgrade?** Recheck `tba-provider-bimi-mark-certificate` whenever its source version, declared collaborators, configuration, or caller changes. Run relevant behavioral tests in addition to the README gate before promotion.

---

## Documentation and Related Packages

### More Documentation

The [repository contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md), [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-bimi-mark-certificate/src/tba_provider_bimi_mark_certificate/revocation.py), and [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-bimi-mark-certificate/pyproject.toml) provide the supporting context for `tba-provider-bimi-mark-certificate`. The [README policy](https://github.com/groupsum/readme-standards/blob/master/docs/outline.md) defines the common document structure.

### Related Packages

Declared local runtime dependencies:

- [tba-contracts-security-trust](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-security-trust/README.md)
- [tba-provider-certificate-evidence](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-certificate-evidence/README.md)

### Project Links

<!-- readme-standards:begin project-links -->
- [Documentation](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/020-providers/tba-provider-bimi-mark-certificate#readme)
- [Homepage](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/020-providers/tba-provider-bimi-mark-certificate#readme)
- [Issues](https://github.com/tigrbl/tigrbl_auth/issues)
- [PyPI](https://pypi.org/project/tba-provider-bimi-mark-certificate/)
- [Repository](https://github.com/tigrbl/tigrbl_auth)
- [Source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/020-providers/tba-provider-bimi-mark-certificate)
- [pypi: tba-provider-bimi-mark-certificate](https://pypi.org/project/tba-provider-bimi-mark-certificate/)
<!-- readme-standards:end project-links -->

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/020-providers/tba-provider-bimi-mark-certificate)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-bimi-mark-certificate/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-bimi-mark-certificate/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-bimi-mark-certificate/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-provider-bimi-mark-certificate/)

---

## Contributing

### How to Contribute

Follow the [contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md) and include a focused example or regression for changes to `tba-provider-bimi-mark-certificate`. Keep package behavior, its documented boundary, and its tests aligned.

### Development Setup

Work from the `pkgs/020-providers/tba-provider-bimi-mark-certificate` checkout. Synchronize its declared development environment with uv, then run the relevant package tests and `python -m pytest docs/readme/test_examples.py`. The repository’s dedicated README job installs `readme-standards==0.1.3` without resolving unrelated runtime packages.

### Notes for Maintainers

Edit authored prose directly in this `tba-provider-bimi-mark-certificate` README. Update source examples in `docs/readme/`, then run `readme-standards render --root . --write` from the package directory and review the diff. Required headings and generated blocks come from package-guide-v1.

---

## Governance

### Ownership and Decision Making

Changes to `tba-provider-bimi-mark-certificate` follow the maintainer review process of [tigrbl/tigrbl_auth](https://github.com/tigrbl/tigrbl_auth) and its contribution guide. Author attribution remains in the [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-bimi-mark-certificate/pyproject.toml); this README does not assign new publishing or administrative authority.

### Standards and Policies

`tba-provider-bimi-mark-certificate` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `020-providers` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

### Lifecycle and Migration

The `tba-provider-bimi-mark-certificate` source version is `0.4.0.dev3`. This change standardizes documentation and adds a development-only gate; it does not publish a new runtime version or declare a previously unpublished package released. Preserve explicit deprecation and replacement instructions where present.

---

## License and Attribution

### License

<!-- readme-standards:begin license -->
Licensed under `Apache-2.0`. See [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-bimi-mark-certificate/LICENSE).
<!-- readme-standards:end license -->

### Notices

<!-- readme-standards:begin notices -->
See [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-bimi-mark-certificate/NOTICE) for attribution.
<!-- readme-standards:end notices -->
