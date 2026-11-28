# tba-protocol-cwt

<!-- readme-standards:begin branding -->
<p align="center"><a href="https://github.com/tigrbl/tigrbl_auth"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="300"></a></p>
<p align="center"><strong>tba-protocol-cwt</strong></p>
<p align="center">Versioned RFC 8392 CWT claim-set composition.</p>
<p align="center">
<a href="https://pypi.org/project/tba-protocol-cwt/"><img alt="pypi: tba-protocol-cwt" src="https://img.shields.io/pypi/v/tba-protocol-cwt?labelColor=1E293B&amp;color=1D4ED8"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-cwt/pyproject.toml"><img alt="Source version: 0.4.0.dev4" src="https://img.shields.io/static/v1?label=Source%20version&amp;message=0.4.0.dev4&amp;labelColor=1E293B&amp;color=4338CA"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-cwt/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/static/v1?label=Python&amp;message=%3E%3D3.10%2C%3C3.16&amp;labelColor=1E293B&amp;color=0F766E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-cwt/pyproject.toml"><img alt="Layer: 050-protocols" src="https://img.shields.io/static/v1?label=Layer&amp;message=050-protocols&amp;labelColor=1E293B&amp;color=6D28D9"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-cwt/README.md#lifecycle-and-migration"><img alt="Lifecycle: active" src="https://img.shields.io/static/v1?label=Lifecycle&amp;message=active&amp;labelColor=1E293B&amp;color=166534"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-cwt/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/static/v1?label=License&amp;message=Apache-2.0&amp;labelColor=1E293B&amp;color=86198F"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-cwt/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/static/v1?label=Notice&amp;message=attribution&amp;labelColor=1E293B&amp;color=86198F"></a>
</p>
<p align="center">
<a href="https://pypi.org/project/tba-protocol-cwt/"><img alt="Monthly PyPI downloads: tba-protocol-cwt" src="https://img.shields.io/pypi/dm/tba-protocol-cwt?labelColor=1E293B&amp;color=0E7490"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-cwt/README.md"><img alt="README hits: tba-protocol-cwt" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/pkgs/050-protocols/tba-protocol-cwt/README.md.svg?label=README%20hits&amp;labelColor=1E293B&amp;color=0E7490"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="README standards: CI gate" src="https://img.shields.io/static/v1?label=README%20standards&amp;message=CI%20gate&amp;labelColor=1E293B&amp;color=1D4ED8"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-cwt/docs/readme/test_examples.py"><img alt="Tests: example source" src="https://img.shields.io/static/v1?label=Tests&amp;message=example%20source&amp;labelColor=1E293B&amp;color=0F766E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-cwt/README.md#certification-status"><img alt="Certification: not certified" src="https://img.shields.io/static/v1?label=Certification&amp;message=not%20certified&amp;labelColor=1E293B&amp;color=92400E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/tools/readme/POLICY.md"><img alt="Governance: repository policy" src="https://img.shields.io/static/v1?label=Governance&amp;message=repository%20policy&amp;labelColor=1E293B&amp;color=4338CA"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="Evidence: source and CI" src="https://img.shields.io/static/v1?label=Evidence&amp;message=source%20and%20CI&amp;labelColor=1E293B&amp;color=6D28D9"></a>
</p>
<p align="center"><a href="#overview">Overview</a> · <a href="#installation">Installation</a> · <a href="#quick-start">Quick Start</a> · <a href="#usage">Usage</a> · <a href="#public-api-and-import-surfaces">API</a> · <a href="#contributing">Contributing</a> · <a href="#governance">Governance</a> · <a href="#license">License</a></p>
<!-- readme-standards:end branding -->

---

## Overview

### Summary

Compose typed claims into a CBOR Web Token claims set using the RFC 8392 registry.

- Package: `tba-protocol-cwt`
- Layer: `050-protocols`
- Responsibility: Versioned RFC 8392 CWT claim-set composition.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-cwt/src/tba_protocol_cwt/__init__.py).
- Distribution: Python package on PyPI.

### Why This Package

`tba-protocol-cwt` isolates this responsibility: Versioned RFC 8392 CWT claim-set composition. Its [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-cwt/src/tba_protocol_cwt/__init__.py) exposes `CAPABILITY_REQUIREMENTS`, `COMPATIBILITY_PATHS`, `CURRENT_VERSION`, `CWT_CARRIER`, `CWT_CLAIM_BY_LABEL`, `CWT_EXTENSION_CLAIMS`, `CWT_LABEL_BY_CLAIM`, `CWT_REGISTERED_CLAIMS`, `CwtCarrier`, `CwtClaimBinding`, `CwtCompatibility`, `CwtVersion`, `FEATURES_BY_VERSION`, `UnsupportedCwtMediaTypeError`, `VERSION_HISTORY`, allowing consumers to select this package without treating adjacent packages as part of its public contract.

### When to Use

This package maps registered claims to integer labels. Draft `actx` and `ath` remain text keys. `build_cwt_claims` accepts explicit `actx_field_labels` and represents `ath` as a SHA-256 digest. Use a COSE provider for signing and verification and a DPoP verifier for proof validation.

### Features

- `CwtClaimBinding`: declared in src/tba_protocol_cwt/claims.py
- `CwtCompatibility`: declared in src/tba_protocol_cwt/compatibility.py
- `CwtProtocolError`: Base error for an RFC 8392 mapping failure.
- `UnsupportedCwtMediaTypeError`: Raised when the selected carrier is not `application/cwt`.
- `CwtProfile`: declared in src/tba_protocol_cwt/profile.py
- `CwtProtocol`: declared in src/tba_protocol_cwt/protocol.py
- `CwtCarrier`: declared in src/tba_protocol_cwt/schemas.py
- `CwtVersion`: declared in src/tba_protocol_cwt/versions.py

### Non-Goals

`tba-protocol-cwt` does not take ownership of deployment hosting or ownership of persistence implementations.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

---

## Getting Started

### Prerequisites

Python `>=3.10,<3.16` is required. The [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-cwt/pyproject.toml) declares runtime dependencies including `tba-primitives-identity`, `tba-concrete-claim-authorization-context`, `tba-concrete-claim-access-token-digest`, `tba-concrete-cwt`, `tba-contracts-identity`, `tba-bases-claim`, `tba-concrete-claim-issuer`, `tba-concrete-claim-subject`, `tba-concrete-claim-audience`, `tba-concrete-claim-expiration`, `tba-concrete-claim-not-before`, `tba-concrete-claim-issued-at`. Read the example’s inputs and service requirements before execution.

### Installation

Install the selected PyPI release of `tba-protocol-cwt`:

```bash
uv pip install tba-protocol-cwt
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/050-protocols/tba-protocol-cwt
```

#### uv

<!-- readme-standards:begin installation.uv -->
```bash
uv add tba-protocol-cwt
```
<!-- readme-standards:end installation.uv -->

#### pip

<!-- readme-standards:begin installation.pip -->
```bash
python -m pip install tba-protocol-cwt
```
<!-- readme-standards:end installation.pip -->

#### Poetry

<!-- readme-standards:begin installation.poetry -->
```bash
poetry add tba-protocol-cwt
```
<!-- readme-standards:end installation.poetry -->

### Quick Start

Install the version used by this example.

```bash
python -m pip install "tba-protocol-cwt==0.4.0.dev4"
```

Save the following as `quickstart.py` and run `python quickstart.py`. The assertions should pass.


See the [protocol source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/050-protocols/tba-protocol-cwt/src/tba_protocol_cwt) for version history, carriers, and claim bindings.

#### Example

<!-- readme-standards:begin example.quick-start -->
Source: [docs/readme/quick_start.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-cwt/docs/readme/quick_start.py).

```python
from tba_concrete_claim_issuer import IssuerClaim
from tba_protocol_cwt import build_cwt_claims, cwt_label_for

issuer = IssuerClaim("https://issuer.example")
assert cwt_label_for(issuer) == 1
encoded = build_cwt_claims(issuer).encode()
assert encoded.startswith(b"\xa1\x01")
```
<!-- readme-standards:end example.quick-start -->

#### Expected Result

The example demonstrates the documented `tba-protocol-cwt` source boundary or workflow. Complete its required configuration first. README CI checks the maintained source’s syntax and declarations; it does not claim that external services or the application workflow were exercised.

---

## Usage

### Common Workflows

<!-- readme-standards:begin example.usage -->
Source: [docs/readme/usage.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-cwt/docs/readme/usage.py).

```python
from tba_concrete_claim_issuer import IssuerClaim
from tba_protocol_cwt import build_cwt_claims, cwt_label_for

issuer = IssuerClaim("https://issuer.example")
assert cwt_label_for(issuer) == 1
encoded = build_cwt_claims(issuer).encode()
assert encoded.startswith(b"\xa1\x01")
```
<!-- readme-standards:end example.usage -->

The following public-entry-point example belongs to `tba-protocol-cwt`. Versioned RFC 8392 CWT claim-set composition. Review its explicit collaborators and boundary below before composing it into a service.

### Configuration

Configure `tba-protocol-cwt` through the APIs in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-cwt/src/tba_protocol_cwt/__init__.py); its [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-cwt/pyproject.toml) describes installation requirements, not an implicit service configuration. No additional package-global configuration contract is inferred from dependencies.

### Error Handling

The inspected `tba-protocol-cwt` source raises `UnsupportedCwtMediaTypeError`, `ValueError`. Handle these at the calling boundary and consult the implementation for the triggering conditions.

### Best Practices

Use the explicit `tba-protocol-cwt` imports documented below and keep collaborator configuration with the caller. Run the package’s relevant tests after changing `CAPABILITY_REQUIREMENTS`, `COMPATIBILITY_PATHS`, `CURRENT_VERSION`, `CWT_CARRIER`, `CWT_CLAIM_BY_LABEL`, `CWT_EXTENSION_CLAIMS`, `CWT_LABEL_BY_CLAIM`, `CWT_REGISTERED_CLAIMS`, `CwtCarrier`, `CwtClaimBinding`, `CwtCompatibility`, `CwtVersion`, `FEATURES_BY_VERSION`, `UnsupportedCwtMediaTypeError`, `VERSION_HISTORY`; an import or successful installation alone does not establish its runtime guarantees.

---

## Package Boundary

### What It Owns

`tba-protocol-cwt` belongs to `050-protocols` and owns protocol semantics and projections: Versioned RFC 8392 CWT claim-set composition.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-cwt/src/tba_protocol_cwt/__init__.py). Public exports include `CAPABILITY_REQUIREMENTS`, `COMPATIBILITY_PATHS`, `CURRENT_VERSION`, `CWT_CARRIER`, `CWT_REGISTERED_CLAIMS`, `CWT_CLAIM_BY_LABEL`, `CWT_EXTENSION_CLAIMS`, `build_cwt_claims`, `CWT_LABEL_BY_CLAIM`, `CwtClaimBinding`, `FEATURES_BY_VERSION`, `VERSION_HISTORY`.

Keep deployment hosting or ownership of persistence implementations in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

### Public API and Import Surfaces

Import namespace: `tba_protocol_cwt`.

Source-declared exports or types: `CAPABILITY_REQUIREMENTS`, `COMPATIBILITY_PATHS`, `CURRENT_VERSION`, `CWT_CARRIER`, `CWT_CLAIM_BY_LABEL`, `CWT_EXTENSION_CLAIMS`, `CWT_LABEL_BY_CLAIM`, `CWT_REGISTERED_CLAIMS`, `CwtCarrier`, `CwtClaimBinding`, `CwtCompatibility`, `CwtVersion`, `FEATURES_BY_VERSION`, `UnsupportedCwtMediaTypeError`, `VERSION_HISTORY`.

Inspect [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-cwt/src/tba_protocol_cwt/__init__.py) for exact signatures; this inventory does not designate every internal module as stable.

### Entry Points

<!-- readme-standards:begin entry-points -->
This package declares no command-line, GUI, or plugin entry points in its manifest.
<!-- readme-standards:end entry-points -->

### Injected Dependencies

Explicit construction inputs and collaborators for `tba-protocol-cwt`:

- `compose_cwt_claim_set` construction inputs: `version`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-cwt/src/tba_protocol_cwt/claims.py).
- `build_cwt_claims` construction inputs: `actx_field_labels`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-cwt/src/tba_protocol_cwt/claims.py).
- `migrate_claims` construction inputs: `source`, `target`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-cwt/src/tba_protocol_cwt/migrations.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

### Protocol Consumers

Direct consumers in this checkout’s package manifests include `tba-profile-workload-credential-cwt-svid-extension`, `tba-runtime-identity`, `tba-workspace`. These edges describe declared dependencies, not protocol-conformance evidence.

### Extensions

For `tba-protocol-cwt`, use the source-declared public interfaces (`CAPABILITY_REQUIREMENTS`, `COMPATIBILITY_PATHS`, `CURRENT_VERSION`, `CWT_CARRIER`, `CWT_CLAIM_BY_LABEL`, `CWT_EXTENSION_CLAIMS`, `CWT_LABEL_BY_CLAIM`, `CWT_REGISTERED_CLAIMS`, `CwtCarrier`, `CwtClaimBinding`, `CwtCompatibility`, `CwtVersion`, `FEATURES_BY_VERSION`, `UnsupportedCwtMediaTypeError`, `VERSION_HISTORY`) when composing or extending behavior. Its entry-point section below is authoritative for registered plugins; no additional extension loader is inferred from the package name.

---

## Operations and Readiness

### Operational Requirements

`tba-protocol-cwt` exposes protocol semantics and projections. Public operations found in its source:

- `capability_report` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-cwt/src/tba_protocol_cwt/__init__.py).
- `CwtClaimBinding.semantic_name` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-cwt/src/tba_protocol_cwt/claims.py).
- `compose_cwt_claim_set` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-cwt/src/tba_protocol_cwt/claims.py).
- `cwt_label_for` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-cwt/src/tba_protocol_cwt/claims.py).
- `build_cwt_claims` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-cwt/src/tba_protocol_cwt/claims.py).
- `compatibility` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-cwt/src/tba_protocol_cwt/compatibility.py).
- `supports` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-cwt/src/tba_protocol_cwt/features.py).
- `migrate_claims` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-cwt/src/tba_protocol_cwt/migrations.py).
- `select_carrier` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-cwt/src/tba_protocol_cwt/schemas.py).
- `select_version` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-cwt/src/tba_protocol_cwt/versions.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

### Health and Observability

This README does not establish a standalone health endpoint for `tba-protocol-cwt`. Observe the concrete caller’s results, exceptions, and existing test reports. An application that embeds this package must define its own health and telemetry contract.

### Security and Resource Limits

Apply the input, credential, and resource constraints implemented in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-cwt/src/tba_protocol_cwt/__init__.py). The `tba-protocol-cwt` README gate is a documentation check, not a security review or a substitute for the implementation’s limits and caller authorization.

### Compatibility

This source version of `tba-protocol-cwt` declares Python `>=3.10,<3.16`. Consult its dependency constraints before upgrading. Source-version and registry-version badges have separate meanings; this migration makes no additional platform or interoperability certification claim.

---

## Verification

### Tests

See the [related repository tests](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-jose/tests/unit/test_cwt_standalone_claim_packages.py) for the implementation scope covered by this example.

[Workspace and package catalog](https://github.com/tigrbl/tigrbl_auth#package-catalog) · [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues) · [Repository license](https://github.com/tigrbl/tigrbl_auth/blob/master/LICENSE)

### Certification Status

No external certification is asserted for `tba-protocol-cwt` by this documentation migration. README conformance, example syntax, runtime tests, and protocol or security certification are distinct evidence scopes.

### Evidence

The [README standards CI](https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml) records mechanical documentation results for its tested commit. The [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-cwt/src/tba_protocol_cwt/__init__.py) and example sources support the package-boundary description; external runtime behavior requires its own test evidence.

---

## FAQ

### Why

**Why select this package?** `tba-protocol-cwt` provides versioned RFC 8392 CWT claim-set composition; use its own API boundary rather than assuming neighboring packages are bundled or configured automatically.

### How

**How do I start?** Install or synchronize the environment under Getting Started, follow the maintained example for `tba-protocol-cwt`, and consult [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-cwt/src/tba_protocol_cwt/__init__.py) for the exact types and signatures involved.

### When

**When should I validate an upgrade?** Recheck `tba-protocol-cwt` whenever its source version, declared collaborators, configuration, or caller changes. Run relevant behavioral tests in addition to the README gate before promotion.

---

## Documentation and Related Packages

### More Documentation

The [repository contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md), [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-cwt/src/tba_protocol_cwt/__init__.py), and [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-cwt/pyproject.toml) provide the supporting context for `tba-protocol-cwt`. The [README policy](https://github.com/groupsum/readme-standards/blob/master/docs/outline.md) defines the common document structure.

### Related Packages

Declared local runtime dependencies:

- [tba-bases-claim](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-claim/README.md)
- [tba-concrete-claim-access-token-digest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-claim-access-token-digest/README.md)
- [tba-concrete-claim-audience](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-claim-audience/README.md)
- [tba-concrete-claim-authorization-context](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-claim-authorization-context/README.md)
- [tba-concrete-claim-expiration](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-claim-expiration/README.md)
- [tba-concrete-claim-issued-at](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-claim-issued-at/README.md)
- [tba-concrete-claim-issuer](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-claim-issuer/README.md)
- [tba-concrete-claim-jwt-id](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-claim-jwt-id/README.md)
- [tba-concrete-claim-not-before](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-claim-not-before/README.md)
- [tba-concrete-claim-subject](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-claim-subject/README.md)
- [tba-concrete-cwt](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-cwt/README.md)
- [tba-contracts-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-identity/README.md)
- [tba-primitives-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/000-primitives/tba-primitives-identity/README.md)

Direct downstream consumers:

- [tba-profile-workload-credential-cwt-svid-extension](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-credential-cwt-svid-extension/README.md)
- [tba-runtime-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity/README.md)

### Project Links

<!-- readme-standards:begin project-links -->
- [Documentation](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/050-protocols/tba-protocol-cwt#readme)
- [Homepage](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/050-protocols/tba-protocol-cwt#readme)
- [Issues](https://github.com/tigrbl/tigrbl_auth/issues)
- [PyPI](https://pypi.org/project/tba-protocol-cwt/)
- [Repository](https://github.com/tigrbl/tigrbl_auth)
- [Source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/050-protocols/tba-protocol-cwt)
- [pypi: tba-protocol-cwt](https://pypi.org/project/tba-protocol-cwt/)
<!-- readme-standards:end project-links -->

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/050-protocols/tba-protocol-cwt)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-cwt/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-cwt/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-cwt/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-protocol-cwt/)

---

## Contributing

### How to Contribute

Follow the [contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md) and include a focused example or regression for changes to `tba-protocol-cwt`. Keep package behavior, its documented boundary, and its tests aligned.

### Development Setup

Work from the `pkgs/050-protocols/tba-protocol-cwt` checkout. Synchronize its declared development environment with uv, then run the relevant package tests and `python -m pytest docs/readme/test_examples.py`. The repository’s dedicated README job installs `readme-standards==0.1.3` without resolving unrelated runtime packages.

### Notes for Maintainers

Edit authored prose directly in this `tba-protocol-cwt` README. Update source examples in `docs/readme/`, then run `readme-standards render --root . --write` from the package directory and review the diff. Required headings and generated blocks come from package-guide-v1.

---

## Governance

### Ownership and Decision Making

Changes to `tba-protocol-cwt` follow the maintainer review process of [tigrbl/tigrbl_auth](https://github.com/tigrbl/tigrbl_auth) and its contribution guide. Author attribution remains in the [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-cwt/pyproject.toml); this README does not assign new publishing or administrative authority.

### Standards and Policies

`tba-protocol-cwt` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `050-protocols` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

### Lifecycle and Migration

The `tba-protocol-cwt` source version is `0.4.0.dev4`. This change standardizes documentation and adds a development-only gate; it does not publish a new runtime version or declare a previously unpublished package released. Preserve explicit deprecation and replacement instructions where present.

---

## License and Attribution

### License

<!-- readme-standards:begin license -->
Licensed under `Apache-2.0`. See [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-cwt/LICENSE).
<!-- readme-standards:end license -->

### Notices

<!-- readme-standards:begin notices -->
See [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-cwt/NOTICE) for attribution.
<!-- readme-standards:end notices -->
