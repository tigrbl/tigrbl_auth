# tba-provider-certificate-evidence

<!-- readme-standards:begin branding -->
<p align="center"><a href="https://github.com/tigrbl/tigrbl_auth"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="300"></a></p>
<p align="center"><strong>tba-provider-certificate-evidence</strong></p>
<p align="center">X.509 path, CRL, and RFC 6962 SCT verification.</p>
<p align="center">
<a href="https://pypi.org/project/tba-provider-certificate-evidence/"><img alt="pypi: tba-provider-certificate-evidence" src="https://img.shields.io/pypi/v/tba-provider-certificate-evidence"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-certificate-evidence/pyproject.toml"><img alt="Source version: 0.4.0.dev3" src="https://img.shields.io/static/v1?label=Source%20version&amp;message=0.4.0.dev3&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-certificate-evidence/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/static/v1?label=Python&amp;message=%3E%3D3.10%2C%3C3.16&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-certificate-evidence/pyproject.toml"><img alt="Layer: 020-providers" src="https://img.shields.io/static/v1?label=Layer&amp;message=020-providers&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-certificate-evidence/README.md#lifecycle-and-migration"><img alt="Lifecycle: active" src="https://img.shields.io/static/v1?label=Lifecycle&amp;message=active&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-certificate-evidence/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/static/v1?label=License&amp;message=Apache-2.0&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-certificate-evidence/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/static/v1?label=Notice&amp;message=attribution&amp;color=525252"></a>
</p>
<p align="center">
<a href="https://pypi.org/project/tba-provider-certificate-evidence/"><img alt="Monthly PyPI downloads: tba-provider-certificate-evidence" src="https://img.shields.io/pypi/dm/tba-provider-certificate-evidence"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-certificate-evidence/README.md"><img alt="README hits: tba-provider-certificate-evidence" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/pkgs/020-providers/tba-provider-certificate-evidence/README.md.svg?label=README%20hits"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="README standards: CI gate" src="https://img.shields.io/static/v1?label=README%20standards&amp;message=CI%20gate&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-certificate-evidence/docs/readme/test_examples.py"><img alt="Tests: example source" src="https://img.shields.io/static/v1?label=Tests&amp;message=example%20source&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-certificate-evidence/README.md#certification-status"><img alt="Certification: not certified" src="https://img.shields.io/static/v1?label=Certification&amp;message=not%20certified&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/tools/readme/POLICY.md"><img alt="Governance: repository policy" src="https://img.shields.io/static/v1?label=Governance&amp;message=repository%20policy&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="Evidence: source and CI" src="https://img.shields.io/static/v1?label=Evidence&amp;message=source%20and%20CI&amp;color=525252"></a>
</p>
<p align="center"><a href="#overview">Overview</a> · <a href="#installation">Installation</a> · <a href="#quick-start">Quick Start</a> · <a href="#usage">Usage</a> · <a href="#public-api-and-import-surfaces">API</a> · <a href="#contributing">Contributing</a> · <a href="#governance">Governance</a> · <a href="#license">License</a></p>
<!-- readme-standards:end branding -->

---

## Overview

### Summary

X.509 path, CRL, and RFC 6962 SCT verification.

Supply parsed certificates, explicit trust anchors, a timezone-aware
verification time, and evidence from your deployment. `verify_chain` returns
the selected chain in leaf-first order. Passing CRLs enables chain-wide
revocation checking. `load_crls` checks signed CRL freshness and
`verify_transparency` verifies embedded SCTs against configured log keys.

```python
from tba_provider_certificate_evidence import (
    load_crls,
    load_logs,
    verify_chain,
    verify_transparency,
)

chain = verify_chain(leaf, intermediates, roots, at)
crls = load_crls(chain, local_crls_by_url.get, at)
verify_chain(leaf, chain[1:-1], chain[-1:], at, crls)
verify_transparency(chain[0], chain[1], load_logs(ct_public_keys_pem), at)
```

The caller supplies the CRL source. The provider does not fetch distribution
point URLs or decide which anchors and logs are appropriate for a profile.

- Package: `tba-provider-certificate-evidence`
- Layer: `020-providers`
- Responsibility: X.509 path, CRL, and RFC 6962 SCT verification.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-certificate-evidence/src/tba_provider_certificate_evidence/__init__.py).
- Distribution: Python package on PyPI.

### Why This Package

`tba-provider-certificate-evidence` isolates this responsibility: X.509 path, CRL, and RFC 6962 SCT verification. Its [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-certificate-evidence/src/tba_provider_certificate_evidence/__init__.py) exposes `CrlSource`, `CtEvidenceUnavailable`, `PathValidationError`, `load_crls`, `load_logs`, `verify_chain`, `verify_transparency`, allowing consumers to select this package without treating adjacent packages as part of its public contract.

### When to Use

Choose `tba-provider-certificate-evidence` for this responsibility: X.509 path, CRL, and RFC 6962 SCT verification. Its `020-providers` placement keeps replaceable environment implementations separate from capability orchestration, storage table ownership, or HTTP routing.

### Features

- `CtEvidenceUnavailable`: declared in src/tba_provider_certificate_evidence/ct.py
- `PathValidationError`: declared in src/tba_provider_certificate_evidence/pkix.py

### Non-Goals

`tba-provider-certificate-evidence` does not take ownership of capability orchestration, storage table ownership, or HTTP routing.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

---

## Getting Started

### Prerequisites

Python `>=3.10,<3.16` is required. The [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-certificate-evidence/pyproject.toml) declares runtime dependencies including `asn1crypto`, `cryptography`, `pyopenssl`. Read the example’s inputs and service requirements before execution.

### Installation

Install the selected PyPI release of `tba-provider-certificate-evidence`:

```bash
uv pip install tba-provider-certificate-evidence
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/020-providers/tba-provider-certificate-evidence
```

#### uv

<!-- readme-standards:begin installation.uv -->
```bash
uv add tba-provider-certificate-evidence
```
<!-- readme-standards:end installation.uv -->

#### pip

<!-- readme-standards:begin installation.pip -->
```bash
python -m pip install tba-provider-certificate-evidence
```
<!-- readme-standards:end installation.pip -->

#### Poetry

<!-- readme-standards:begin installation.poetry -->
```bash
poetry add tba-provider-certificate-evidence
```
<!-- readme-standards:end installation.poetry -->

### Quick Start

Build the package from the repository root.

```bash
uv build --wheel pkgs/020-providers/tba-provider-certificate-evidence
```

#### Example

The maintained integration example defines `verify_certificate_evidence` with explicit caller-owned inputs: `at, ct_public_keys_pem, intermediates, leaf, local_crls_by_url, roots`. Invoke it with those inputs; loading the example file alone does not execute the integration.

<!-- readme-standards:begin example.quick-start -->
Source: [docs/readme/quick_start.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-certificate-evidence/docs/readme/quick_start.py).

```python
from tba_provider_certificate_evidence import (
    load_crls,
    load_logs,
    verify_chain,
    verify_transparency,
)


def verify_certificate_evidence(
    *, at, ct_public_keys_pem, intermediates, leaf, local_crls_by_url, roots
):
    """Supply caller-owned integration inputs; this definition does not execute a deployment."""
    chain = verify_chain(leaf, intermediates, roots, at)
    crls = load_crls(chain, local_crls_by_url.get, at)
    verify_chain(leaf, chain[1:-1], chain[-1:], at, crls)
    verify_transparency(chain[0], chain[1], load_logs(ct_public_keys_pem), at)
```
<!-- readme-standards:end example.quick-start -->

#### Expected Result

The example demonstrates the documented `tba-provider-certificate-evidence` source boundary or workflow. Complete its required configuration first. README CI checks the maintained source’s syntax and declarations; it does not claim that external services or the application workflow were exercised.

---

## Usage

### Common Workflows

The maintained integration example defines `verify_certificate_evidence` with explicit caller-owned inputs: `at, ct_public_keys_pem, intermediates, leaf, local_crls_by_url, roots`. Invoke it with those inputs; loading the example file alone does not execute the integration.

<!-- readme-standards:begin example.usage -->
Source: [docs/readme/usage.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-certificate-evidence/docs/readme/usage.py).

```python
from tba_provider_certificate_evidence import (
    load_crls,
    load_logs,
    verify_chain,
    verify_transparency,
)


def verify_certificate_evidence(
    *, at, ct_public_keys_pem, intermediates, leaf, local_crls_by_url, roots
):
    """Supply caller-owned integration inputs; this definition does not execute a deployment."""
    chain = verify_chain(leaf, intermediates, roots, at)
    crls = load_crls(chain, local_crls_by_url.get, at)
    verify_chain(leaf, chain[1:-1], chain[-1:], at, crls)
    verify_transparency(chain[0], chain[1], load_logs(ct_public_keys_pem), at)
```
<!-- readme-standards:end example.usage -->

The following public-entry-point example belongs to `tba-provider-certificate-evidence`. X.509 path, CRL, and RFC 6962 SCT verification. Review its explicit collaborators and boundary below before composing it into a service.

### Configuration

Configure `tba-provider-certificate-evidence` through the APIs in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-certificate-evidence/src/tba_provider_certificate_evidence/__init__.py); its [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-certificate-evidence/pyproject.toml) describes installation requirements, not an implicit service configuration. No additional package-global configuration contract is inferred from dependencies.

### Error Handling

The inspected `tba-provider-certificate-evidence` source raises `CtEvidenceUnavailable`, `PathValidationError`, `ValueError`. Handle these at the calling boundary and consult the implementation for the triggering conditions.

### Best Practices

Use the explicit `tba-provider-certificate-evidence` imports documented below and keep collaborator configuration with the caller. Run the package’s relevant tests after changing `CrlSource`, `CtEvidenceUnavailable`, `PathValidationError`, `load_crls`, `load_logs`, `verify_chain`, `verify_transparency`; an import or successful installation alone does not establish its runtime guarantees.

---

## Package Boundary

### What It Owns

`tba-provider-certificate-evidence` belongs to `020-providers` and owns replaceable environment implementations: X.509 path, CRL, and RFC 6962 SCT verification.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-certificate-evidence/src/tba_provider_certificate_evidence/__init__.py). Public exports include `CrlSource`, `CtEvidenceUnavailable`, `PathValidationError`, `load_crls`, `load_logs`, `verify_chain`, `verify_transparency`.

Keep capability orchestration, storage table ownership, or HTTP routing in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

### Public API and Import Surfaces

Import namespace: `tba_provider_certificate_evidence`.

Source-declared exports or types: `CrlSource`, `CtEvidenceUnavailable`, `PathValidationError`, `load_crls`, `load_logs`, `verify_chain`, `verify_transparency`.

Inspect [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-certificate-evidence/src/tba_provider_certificate_evidence/__init__.py) for exact signatures; this inventory does not designate every internal module as stable.

### Entry Points

<!-- readme-standards:begin entry-points -->
This package declares no command-line, GUI, or plugin entry points in its manifest.
<!-- readme-standards:end entry-points -->

### Injected Dependencies

Explicit construction inputs and collaborators for `tba-provider-certificate-evidence`:

- `PathValidationError` construction inputs: `message`, `revoked`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-certificate-evidence/src/tba_provider_certificate_evidence/pkix.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

### Protocol Consumers

Direct consumers in this checkout’s package manifests include `tba-provider-bimi-mark-certificate`. These edges describe declared dependencies, not protocol-conformance evidence.

### Extensions

For `tba-provider-certificate-evidence`, use the source-declared public interfaces (`CrlSource`, `CtEvidenceUnavailable`, `PathValidationError`, `load_crls`, `load_logs`, `verify_chain`, `verify_transparency`) when composing or extending behavior. Its entry-point section below is authoritative for registered plugins; no additional extension loader is inferred from the package name.

---

## Operations and Readiness

### Operational Requirements

`tba-provider-certificate-evidence` exposes replaceable environment implementations. Public operations found in its source:

- `load_crls` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-certificate-evidence/src/tba_provider_certificate_evidence/crl.py).
- `load_logs` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-certificate-evidence/src/tba_provider_certificate_evidence/ct.py).
- `verify_transparency` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-certificate-evidence/src/tba_provider_certificate_evidence/ct.py).
- `verify_chain` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-certificate-evidence/src/tba_provider_certificate_evidence/pkix.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

### Health and Observability

This README does not establish a standalone health endpoint for `tba-provider-certificate-evidence`. Observe the concrete caller’s results, exceptions, and existing test reports. An application that embeds this package must define its own health and telemetry contract.

### Security and Resource Limits

Apply the input, credential, and resource constraints implemented in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-certificate-evidence/src/tba_provider_certificate_evidence/__init__.py). The `tba-provider-certificate-evidence` README gate is a documentation check, not a security review or a substitute for the implementation’s limits and caller authorization.

### Compatibility

This source version of `tba-provider-certificate-evidence` declares Python `>=3.10,<3.16`. Consult its dependency constraints before upgrading. Source-version and registry-version badges have separate meanings; this migration makes no additional platform or interoperability certification claim.

---

## Verification

### Tests

Check that the build produces a wheel with the package version declared in `pyproject.toml`.

### Certification Status

No external certification is asserted for `tba-provider-certificate-evidence` by this documentation migration. README conformance, example syntax, runtime tests, and protocol or security certification are distinct evidence scopes.

### Evidence

The [README standards CI](https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml) records mechanical documentation results for its tested commit. The [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-certificate-evidence/src/tba_provider_certificate_evidence/__init__.py) and example sources support the package-boundary description; external runtime behavior requires its own test evidence.

---

## FAQ

### Why

**Why select this package?** `tba-provider-certificate-evidence` provides x.509 path, CRL, and RFC 6962 SCT verification; use its own API boundary rather than assuming neighboring packages are bundled or configured automatically.

### How

**How do I start?** Install or synchronize the environment under Getting Started, follow the maintained example for `tba-provider-certificate-evidence`, and consult [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-certificate-evidence/src/tba_provider_certificate_evidence/__init__.py) for the exact types and signatures involved.

### When

**When should I validate an upgrade?** Recheck `tba-provider-certificate-evidence` whenever its source version, declared collaborators, configuration, or caller changes. Run relevant behavioral tests in addition to the README gate before promotion.

---

## Documentation and Related Packages

### More Documentation

The [repository contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md), [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-certificate-evidence/src/tba_provider_certificate_evidence/__init__.py), and [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-certificate-evidence/pyproject.toml) provide the supporting context for `tba-provider-certificate-evidence`. The [README policy](https://github.com/groupsum/readme-standards/blob/master/docs/outline.md) defines the common document structure.

### Related Packages

Direct downstream consumers:

- [tba-provider-bimi-mark-certificate](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-bimi-mark-certificate/README.md)

### Project Links

<!-- readme-standards:begin project-links -->
- [Documentation](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/020-providers/tba-provider-certificate-evidence#readme)
- [Homepage](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/020-providers/tba-provider-certificate-evidence#readme)
- [Issues](https://github.com/tigrbl/tigrbl_auth/issues)
- [PyPI](https://pypi.org/project/tba-provider-certificate-evidence/)
- [Repository](https://github.com/tigrbl/tigrbl_auth)
- [Source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/020-providers/tba-provider-certificate-evidence)
- [pypi: tba-provider-certificate-evidence](https://pypi.org/project/tba-provider-certificate-evidence/)
<!-- readme-standards:end project-links -->

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/020-providers/tba-provider-certificate-evidence)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-certificate-evidence/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-certificate-evidence/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-certificate-evidence/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-provider-certificate-evidence/)

---

## Contributing

### How to Contribute

Follow the [contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md) and include a focused example or regression for changes to `tba-provider-certificate-evidence`. Keep package behavior, its documented boundary, and its tests aligned.

### Development Setup

Work from the `pkgs/020-providers/tba-provider-certificate-evidence` checkout. Synchronize its declared development environment with uv, then run the relevant package tests and `python -m pytest docs/readme/test_examples.py`. The repository’s dedicated README job installs `readme-standards==0.1.1` without resolving unrelated runtime packages.

### Notes for Maintainers

Edit authored prose directly in this `tba-provider-certificate-evidence` README. Update source examples in `docs/readme/`, then run `readme-standards render --root . --write` from the package directory and review the diff. Required headings and generated blocks come from package-guide-v1.

---

## Governance

### Ownership and Decision Making

Changes to `tba-provider-certificate-evidence` follow the maintainer review process of [tigrbl/tigrbl_auth](https://github.com/tigrbl/tigrbl_auth) and its contribution guide. Author attribution remains in the [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-certificate-evidence/pyproject.toml); this README does not assign new publishing or administrative authority.

### Standards and Policies

`tba-provider-certificate-evidence` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `020-providers` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

### Lifecycle and Migration

The `tba-provider-certificate-evidence` source version is `0.4.0.dev3`. This change standardizes documentation and adds a development-only gate; it does not publish a new runtime version or declare a previously unpublished package released. Preserve explicit deprecation and replacement instructions where present.

---

## License and Attribution

### License

<!-- readme-standards:begin license -->
Licensed under `Apache-2.0`. See [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-certificate-evidence/LICENSE).
<!-- readme-standards:end license -->

### Notices

<!-- readme-standards:begin notices -->
See [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-certificate-evidence/NOTICE) for attribution.
<!-- readme-standards:end notices -->
