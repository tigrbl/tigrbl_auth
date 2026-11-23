# tba-primitives-identity

<!-- readme-standards:begin branding -->
<p align="center"><a href="https://github.com/tigrbl/tigrbl_auth"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="300"></a></p>
<p align="center"><strong>tba-primitives-identity</strong></p>
<p align="center">Dependency-light identity primitives, typed helpers, path safety, and RFC 8785 JSON canonicalization for TBA identity systems.</p>
<p align="center">
<a href="https://pypi.org/project/tba-primitives-identity/"><img alt="pypi: tba-primitives-identity" src="https://img.shields.io/pypi/v/tba-primitives-identity"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/000-primitives/tba-primitives-identity/pyproject.toml"><img alt="Source version: 0.4.0.dev3" src="https://img.shields.io/static/v1?label=Source%20version&amp;message=0.4.0.dev3&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/000-primitives/tba-primitives-identity/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/static/v1?label=Python&amp;message=%3E%3D3.10%2C%3C3.16&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/000-primitives/tba-primitives-identity/pyproject.toml"><img alt="Layer: 000-primitives" src="https://img.shields.io/static/v1?label=Layer&amp;message=000-primitives&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/000-primitives/tba-primitives-identity/README.md#lifecycle-and-migration"><img alt="Lifecycle: active" src="https://img.shields.io/static/v1?label=Lifecycle&amp;message=active&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/000-primitives/tba-primitives-identity/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/static/v1?label=License&amp;message=Apache-2.0&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/000-primitives/tba-primitives-identity/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/static/v1?label=Notice&amp;message=attribution&amp;color=525252"></a>
</p>
<p align="center">
<a href="https://pypi.org/project/tba-primitives-identity/"><img alt="Monthly PyPI downloads: tba-primitives-identity" src="https://img.shields.io/pypi/dm/tba-primitives-identity"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/000-primitives/tba-primitives-identity/README.md"><img alt="README hits: tba-primitives-identity" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/pkgs/000-primitives/tba-primitives-identity/README.md.svg?label=README%20hits"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="README standards: CI gate" src="https://img.shields.io/static/v1?label=README%20standards&amp;message=CI%20gate&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/000-primitives/tba-primitives-identity/docs/readme/test_examples.py"><img alt="Tests: example source" src="https://img.shields.io/static/v1?label=Tests&amp;message=example%20source&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/000-primitives/tba-primitives-identity/README.md#certification-status"><img alt="Certification: not certified" src="https://img.shields.io/static/v1?label=Certification&amp;message=not%20certified&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/tools/readme/POLICY.md"><img alt="Governance: repository policy" src="https://img.shields.io/static/v1?label=Governance&amp;message=repository%20policy&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="Evidence: source and CI" src="https://img.shields.io/static/v1?label=Evidence&amp;message=source%20and%20CI&amp;color=525252"></a>
</p>
<p align="center"><a href="#overview">Overview</a> · <a href="#installation">Installation</a> · <a href="#quick-start">Quick Start</a> · <a href="#usage">Usage</a> · <a href="#public-api-and-import-surfaces">API</a> · <a href="#contributing">Contributing</a> · <a href="#governance">Governance</a> · <a href="#license">License</a></p>
<!-- readme-standards:end branding -->

---

## Overview

### Summary

Encode and normalize shared identity values without pulling in a server stack.

- Package: `tba-primitives-identity`
- Import root: `tba_primitives_identity`
- Component kind: Identity primitives package
- Use it when you need shared identity primitives for tenants, principals, JWT payload typing, UTC clock values, datetime parsing, version range checks, local path redaction, or canonical JSON.
- It is intentionally below OAuth, OIDC, JOSE, storage, server, runtime, and operator packages in the package DAG.
- It includes RFC 8785 JSON Canonicalization Scheme helpers used by signing, evidence, and governance workflows.

### Why This Package

`tba-primitives-identity` isolates this responsibility: Dependency-light identity primitives, typed helpers, path safety, and RFC 8785 JSON canonicalization for TBA identity systems. Its [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/000-primitives/tba-primitives-identity/src/tba_primitives_identity/__init__.py) exposes `APPLICATION_AT_JWT`, `APPLICATION_COSE`, `APPLICATION_CWT`, `APPLICATION_DC_SD_JWT`, `APPLICATION_DID_JSON`, `APPLICATION_DID_LD_JSON`, `APPLICATION_EAT_CWT`, `APPLICATION_EAT_JWT`, `APPLICATION_JWT`, `APPLICATION_VC`, `APPLICATION_VC_COSE`, `APPLICATION_VC_JWT`, `APPLICATION_VP`, `APPLICATION_VP_COSE`, `APPLICATION_VP_JWT`, allowing consumers to select this package without treating adjacent packages as part of its public contract.

### When to Use

Use these helpers for shared wire values such as base64url, digests, and nonces. The deterministic JSON helpers continue to produce the bytes used by existing policy hashes and key thumbprints.

For strict RFC 8785 canonicalization, use [tba-codec-jcs](../../003-codecs/tba-codec-jcs/README.md). The legacy `canonicalize` and `canonicalize_json` imports remain available and emit a `DeprecationWarning` when called. The legacy `tba_primitives_identity.rfc8785` module also warns when imported.

### Features

- `ArtifactKind`: declared in src/tba_primitives_identity/artifacts.py
- `CredentialFormat`: declared in src/tba_primitives_identity/artifacts.py
- `TokenKind`: declared in src/tba_primitives_identity/artifacts.py
- `PresentationKind`: declared in src/tba_primitives_identity/artifacts.py
- `IdentityDocumentKind`: declared in src/tba_primitives_identity/artifacts.py
- `ProtectedEnvelopeKind`: declared in src/tba_primitives_identity/artifacts.py
- `AttestationKind`: declared in src/tba_primitives_identity/artifacts.py
- `ManifestKind`: declared in src/tba_primitives_identity/artifacts.py

### Non-Goals

`tba-primitives-identity` does not take ownership of protocol flows, provider selection, or application hosting.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

---

## Getting Started

### Prerequisites

Python `>=3.10,<3.16` is required. The [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/000-primitives/tba-primitives-identity/pyproject.toml) declares no direct runtime dependencies. Read the example’s inputs and service requirements before execution.

### Installation

Install the selected PyPI release of `tba-primitives-identity`:

```bash
uv pip install tba-primitives-identity
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/000-primitives/tba-primitives-identity
```

#### uv

<!-- readme-standards:begin installation.uv -->
```bash
uv add tba-primitives-identity
```
<!-- readme-standards:end installation.uv -->

#### pip

<!-- readme-standards:begin installation.pip -->
```bash
python -m pip install tba-primitives-identity
```
<!-- readme-standards:end installation.pip -->

#### Poetry

<!-- readme-standards:begin installation.poetry -->
```bash
poetry add tba-primitives-identity
```
<!-- readme-standards:end installation.poetry -->

### Quick Start

Install the version used by this example.

```bash
python -m pip install "tba-primitives-identity==0.4.0.dev3"
```

Save the following as `quickstart.py` and run `python quickstart.py`. The assertions should pass.

#### Example

<!-- readme-standards:begin example.quick-start -->
Source: [docs/readme/quick_start.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/000-primitives/tba-primitives-identity/docs/readme/quick_start.py).

```python
from tba_primitives_identity import base64url_decode, base64url_encode

encoded = base64url_encode(b"tba")
assert encoded == "dGJh"
assert base64url_decode(encoded) == b"tba"
```
<!-- readme-standards:end example.quick-start -->

#### Expected Result

The example demonstrates the documented `tba-primitives-identity` source boundary or workflow. Complete its required configuration first. README CI checks the maintained source’s syntax and declarations; it does not claim that external services or the application workflow were exercised.

---

## Usage

### Common Workflows

<!-- readme-standards:begin example.usage -->
Source: [docs/readme/usage.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/000-primitives/tba-primitives-identity/docs/readme/usage.py).

```python
from tba_primitives_identity import base64url_decode, base64url_encode

encoded = base64url_encode(b"tba")
assert encoded == "dGJh"
assert base64url_decode(encoded) == b"tba"
```
<!-- readme-standards:end example.usage -->

The following public-entry-point example belongs to `tba-primitives-identity`. Dependency-light identity primitives, typed helpers, path safety, and RFC 8785 JSON canonicalization for TBA identity systems. Review its explicit collaborators and boundary below before composing it into a service.

### Configuration

Configure `tba-primitives-identity` through the APIs in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/000-primitives/tba-primitives-identity/src/tba_primitives_identity/__init__.py); its [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/000-primitives/tba-primitives-identity/pyproject.toml) describes installation requirements, not an implicit service configuration. No additional package-global configuration contract is inferred from dependencies.

### Error Handling

The inspected `tba-primitives-identity` source raises `JCSCanonicalizationError`, `TypeError`, `ValueError`. Handle these at the calling boundary and consult the implementation for the triggering conditions.

### Best Practices

Use the explicit `tba-primitives-identity` imports documented below and keep collaborator configuration with the caller. Run the package’s relevant tests after changing `APPLICATION_AT_JWT`, `APPLICATION_COSE`, `APPLICATION_CWT`, `APPLICATION_DC_SD_JWT`, `APPLICATION_DID_JSON`, `APPLICATION_DID_LD_JSON`, `APPLICATION_EAT_CWT`, `APPLICATION_EAT_JWT`, `APPLICATION_JWT`, `APPLICATION_VC`, `APPLICATION_VC_COSE`, `APPLICATION_VC_JWT`, `APPLICATION_VP`, `APPLICATION_VP_COSE`, `APPLICATION_VP_JWT`; an import or successful installation alone does not establish its runtime guarantees.

---

## Package Boundary

### What It Owns

- Identity errors and typed primitives
- UTC clock, datetime parsing, and version comparison helpers
- UUID and JWT payload typing helpers
- Path redaction for repo-safe evidence
- Deterministic JSON for existing policy hashes and key thumbprints.

For strict RFC 8785 canonicalization, use [tba-codec-jcs](../../003-codecs/tba-codec-jcs/README.md). The legacy `canonicalize` and `canonicalize_json` imports remain available and emit a `DeprecationWarning` when called. The legacy `tba_primitives_identity.rfc8785` module also warns when imported.

### Public API and Import Surfaces

Import namespace: `tba_primitives_identity`.

Source-declared exports or types: `APPLICATION_AT_JWT`, `APPLICATION_COSE`, `APPLICATION_CWT`, `APPLICATION_DC_SD_JWT`, `APPLICATION_DID_JSON`, `APPLICATION_DID_LD_JSON`, `APPLICATION_EAT_CWT`, `APPLICATION_EAT_JWT`, `APPLICATION_JWT`, `APPLICATION_VC`, `APPLICATION_VC_COSE`, `APPLICATION_VC_JWT`, `APPLICATION_VP`, `APPLICATION_VP_COSE`, `APPLICATION_VP_JWT`.

Inspect [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/000-primitives/tba-primitives-identity/src/tba_primitives_identity/__init__.py) for exact signatures; this inventory does not designate every internal module as stable.

### Entry Points

<!-- readme-standards:begin entry-points -->
This package declares no command-line, GUI, or plugin entry points in its manifest.
<!-- readme-standards:end entry-points -->

### Injected Dependencies

Explicit construction inputs and collaborators for `tba-primitives-identity`:

- `generate_nonce` construction inputs: `size`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/000-primitives/tba-primitives-identity/src/tba_primitives_identity/nonces.py).
- `validate_nonce` construction inputs: `min_length`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/000-primitives/tba-primitives-identity/src/tba_primitives_identity/nonces.py).
- `str_tuple` construction inputs: `sort`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/000-primitives/tba-primitives-identity/src/tba_primitives_identity/normalization.py).
- `safe_display_path` construction inputs: `external_label`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/000-primitives/tba-primitives-identity/src/tba_primitives_identity/path_safety.py).
- `require_absolute_uri` construction inputs: `https`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/000-primitives/tba-primitives-identity/src/tba_primitives_identity/uris.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

### Protocol Consumers

The following layer-50 manifests directly depend on `tba-primitives-identity`:

- [tba-protocol-credential-iso-mdoc](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-credential-iso-mdoc/README.md)
- [tba-protocol-credential-w3c-vcdm](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-credential-w3c-vcdm/README.md)
- [tba-protocol-cwt](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-cwt/README.md)
- [tba-protocol-oauth](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oauth/README.md)
- [tba-protocol-oidc](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oidc/README.md)
- [tba-protocol-security-cose](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-security-cose/README.md)
- [tba-protocol-security-jose](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-security-jose/README.md)
- [tba-protocol-security-jwe](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-security-jwe/README.md)
- [tba-protocol-security-jws](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-security-jws/README.md)
- [tba-protocol-webauthn](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-webauthn/README.md)

Other direct consumers include [tba-app-backend-core](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-core/README.md), [tba-auth](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-auth/README.md), [tba-bases-identity-model](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-identity-model/README.md), [tba-capability-access-governance](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-access-governance/README.md), [tba-capability-policy-administration](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-policy-administration/README.md), [tba-capability-policy-assurance](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-policy-assurance/README.md), [tba-concrete-authorization-provenance](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-authorization-provenance/README.md), [tba-concrete-capability](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-capability/README.md).

### Extensions

For `tba-primitives-identity`, use the source-declared public interfaces (`APPLICATION_AT_JWT`, `APPLICATION_COSE`, `APPLICATION_CWT`, `APPLICATION_DC_SD_JWT`, `APPLICATION_DID_JSON`, `APPLICATION_DID_LD_JSON`, `APPLICATION_EAT_CWT`, `APPLICATION_EAT_JWT`, `APPLICATION_JWT`, `APPLICATION_VC`, `APPLICATION_VC_COSE`, `APPLICATION_VC_JWT`, `APPLICATION_VP`, `APPLICATION_VP_COSE`, `APPLICATION_VP_JWT`) when composing or extending behavior. Its entry-point section below is authoritative for registered plugins; no additional extension loader is inferred from the package name.

---

## Operations and Readiness

### Operational Requirements

`tba-primitives-identity` exposes shared identity primitives. Public operations found in its source:

- `base64url_encode` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/000-primitives/tba-primitives-identity/src/tba_primitives_identity/base64url.py).
- `base64url_decode` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/000-primitives/tba-primitives-identity/src/tba_primitives_identity/base64url.py).
- `Clock.now` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/000-primitives/tba-primitives-identity/src/tba_primitives_identity/clock.py).
- `SystemClock.now` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/000-primitives/tba-primitives-identity/src/tba_primitives_identity/clock.py).
- `FrozenClock.now` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/000-primitives/tba-primitives-identity/src/tba_primitives_identity/clock.py).
- `unix_seconds` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/000-primitives/tba-primitives-identity/src/tba_primitives_identity/clock.py).
- `utc_now` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/000-primitives/tba-primitives-identity/src/tba_primitives_identity/clock.py).
- `utc_now_iso` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/000-primitives/tba-primitives-identity/src/tba_primitives_identity/clock.py).
- `parse_time` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/000-primitives/tba-primitives-identity/src/tba_primitives_identity/clock.py).
- `bytes_equal` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/000-primitives/tba-primitives-identity/src/tba_primitives_identity/constant_time.py).
- `text_equal` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/000-primitives/tba-primitives-identity/src/tba_primitives_identity/constant_time.py).
- `digest_bytes` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/000-primitives/tba-primitives-identity/src/tba_primitives_identity/digests.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

### Health and Observability

This README does not establish a standalone health endpoint for `tba-primitives-identity`. Observe the concrete caller’s results, exceptions, and existing test reports. An application that embeds this package must define its own health and telemetry contract.

### Security and Resource Limits

Apply the input, credential, and resource constraints implemented in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/000-primitives/tba-primitives-identity/src/tba_primitives_identity/__init__.py). The `tba-primitives-identity` README gate is a documentation check, not a security review or a substitute for the implementation’s limits and caller authorization.

### Compatibility

This source version of `tba-primitives-identity` declares Python `>=3.10,<3.16`. Consult its dependency constraints before upgrading. Source-version and registry-version badges have separate meanings; this migration makes no additional platform or interoperability certification claim.

---

## Verification

### Tests

See the [related repository tests](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-architecture/tests/unit/test_identity_package_split_imports.py) for the implementation scope covered by this example.

[Workspace and package catalog](https://github.com/tigrbl/tigrbl_auth#package-catalog) · [tba-contracts-identity-document](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/002-contracts/tba-contracts-identity-document#readme) · [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues) · [Repository license](https://github.com/tigrbl/tigrbl_auth/blob/master/LICENSE)

### Certification Status

No external certification is asserted for `tba-primitives-identity` by this documentation migration. README conformance, example syntax, runtime tests, and protocol or security certification are distinct evidence scopes.

### Evidence

The [README standards CI](https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml) records mechanical documentation results for its tested commit. The [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/000-primitives/tba-primitives-identity/src/tba_primitives_identity/__init__.py) and example sources support the package-boundary description; external runtime behavior requires its own test evidence.

---

## FAQ

### Why

**Why select this package?** `tba-primitives-identity` provides dependency-light identity primitives, typed helpers, path safety, and RFC 8785 JSON canonicalization for TBA identity systems; use its own API boundary rather than assuming neighboring packages are bundled or configured automatically.

### How

**How do I start?** Install or synchronize the environment under Getting Started, follow the maintained example for `tba-primitives-identity`, and consult [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/000-primitives/tba-primitives-identity/src/tba_primitives_identity/__init__.py) for the exact types and signatures involved.

### When

**When should I validate an upgrade?** Recheck `tba-primitives-identity` whenever its source version, declared collaborators, configuration, or caller changes. Run relevant behavioral tests in addition to the README gate before promotion.

---

## Documentation and Related Packages

### More Documentation

The [repository contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md), [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/000-primitives/tba-primitives-identity/src/tba_primitives_identity/__init__.py), and [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/000-primitives/tba-primitives-identity/pyproject.toml) provide the supporting context for `tba-primitives-identity`. The [README policy](https://github.com/groupsum/readme-standards/blob/master/docs/outline.md) defines the common document structure.

### Related Packages

- [tba-primitives-identity](https://pypi.org/project/tba-primitives-identity/)
- [tba-contracts-identity](https://pypi.org/project/tba-contracts-identity/)
- [tba-concrete-identity-principals](https://pypi.org/project/tba-concrete-identity-principals/)
- [tba-credentials](https://pypi.org/project/tba-credentials/)
- [tba-provider-identity-jose](https://pypi.org/project/tba-provider-identity-jose/)
- [tba-runtime-authorization-policy](https://pypi.org/project/tba-runtime-authorization-policy/)

### Project Links

<!-- readme-standards:begin project-links -->
- [Documentation](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/000-primitives/tba-primitives-identity#readme)
- [Homepage](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/000-primitives/tba-primitives-identity#readme)
- [Issues](https://github.com/tigrbl/tigrbl_auth/issues)
- [PyPI](https://pypi.org/project/tba-primitives-identity/)
- [Repository](https://github.com/tigrbl/tigrbl_auth)
- [SSOT](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [Source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/000-primitives/tba-primitives-identity)
- [pypi: tba-primitives-identity](https://pypi.org/project/tba-primitives-identity/)
<!-- readme-standards:end project-links -->

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/000-primitives/tba-primitives-identity)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/000-primitives/tba-primitives-identity/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/000-primitives/tba-primitives-identity/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/000-primitives/tba-primitives-identity/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-primitives-identity/)

---

## Contributing

### How to Contribute

Follow the [contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md) and include a focused example or regression for changes to `tba-primitives-identity`. Keep package behavior, its documented boundary, and its tests aligned.

### Development Setup

Work from the `pkgs/000-primitives/tba-primitives-identity` checkout. Synchronize its declared development environment with uv, then run the relevant package tests and `python -m pytest docs/readme/test_examples.py`. The repository’s dedicated README job installs `readme-standards==0.1.1` without resolving unrelated runtime packages.

### Notes for Maintainers

Edit authored prose directly in this `tba-primitives-identity` README. Update source examples in `docs/readme/`, then run `readme-standards render --root . --write` from the package directory and review the diff. Required headings and generated blocks come from package-guide-v1.

---

## Governance

### Ownership and Decision Making

Changes to `tba-primitives-identity` follow the maintainer review process of [tigrbl/tigrbl_auth](https://github.com/tigrbl/tigrbl_auth) and its contribution guide. Author attribution remains in the [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/000-primitives/tba-primitives-identity/pyproject.toml); this README does not assign new publishing or administrative authority.

### Standards and Policies

This package is part of the SSOT-governed TBA identity package suite. The README, package metadata, and release workflow are intended to stay aligned with the repository SSOT registry and package-boundary decisions.

`tba-primitives-identity` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `000-primitives` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

### Lifecycle and Migration

The `tba-primitives-identity` source version is `0.4.0.dev3`. This change standardizes documentation and adds a development-only gate; it does not publish a new runtime version or declare a previously unpublished package released. Preserve explicit deprecation and replacement instructions where present.

---

## License and Attribution

### License

<!-- readme-standards:begin license -->
Licensed under `Apache-2.0`. See [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/000-primitives/tba-primitives-identity/LICENSE).
<!-- readme-standards:end license -->

### Notices

<!-- readme-standards:begin notices -->
See [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/000-primitives/tba-primitives-identity/NOTICE) for attribution.
<!-- readme-standards:end notices -->
