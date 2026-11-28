# tba-protocol-zcap

<!-- readme-standards:begin branding -->
<p align="center"><a href="https://github.com/tigrbl/tigrbl_auth"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="300"></a></p>
<p align="center"><strong>tba-protocol-zcap</strong></p>
<p align="center">ZCAP-LD delegation and HTTP invocation verification for the TBA Ed25519 development profile.</p>
<p align="center">
<a href="https://pypi.org/project/tba-protocol-zcap/"><img alt="pypi: tba-protocol-zcap" src="https://img.shields.io/pypi/v/tba-protocol-zcap?labelColor=1E293B&amp;color=1D4ED8"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-zcap/pyproject.toml"><img alt="Source version: 0.4.0.dev3" src="https://img.shields.io/static/v1?label=Source%20version&amp;message=0.4.0.dev3&amp;labelColor=1E293B&amp;color=4338CA"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-zcap/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/static/v1?label=Python&amp;message=%3E%3D3.10%2C%3C3.16&amp;labelColor=1E293B&amp;color=0F766E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-zcap/pyproject.toml"><img alt="Layer: 050-protocols" src="https://img.shields.io/static/v1?label=Layer&amp;message=050-protocols&amp;labelColor=1E293B&amp;color=6D28D9"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-zcap/README.md#lifecycle-and-migration"><img alt="Lifecycle: active" src="https://img.shields.io/static/v1?label=Lifecycle&amp;message=active&amp;labelColor=1E293B&amp;color=166534"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-zcap/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/static/v1?label=License&amp;message=Apache-2.0&amp;labelColor=1E293B&amp;color=86198F"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-zcap/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/static/v1?label=Notice&amp;message=attribution&amp;labelColor=1E293B&amp;color=86198F"></a>
</p>
<p align="center">
<a href="https://pypi.org/project/tba-protocol-zcap/"><img alt="Monthly PyPI downloads: tba-protocol-zcap" src="https://img.shields.io/pypi/dm/tba-protocol-zcap?labelColor=1E293B&amp;color=0E7490"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-zcap/README.md"><img alt="README hits: tba-protocol-zcap" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/pkgs/050-protocols/tba-protocol-zcap/README.md.svg?label=README%20hits&amp;labelColor=1E293B&amp;color=0E7490"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="README standards: CI gate" src="https://img.shields.io/static/v1?label=README%20standards&amp;message=CI%20gate&amp;labelColor=1E293B&amp;color=1D4ED8"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-zcap/docs/readme/test_examples.py"><img alt="Tests: example source" src="https://img.shields.io/static/v1?label=Tests&amp;message=example%20source&amp;labelColor=1E293B&amp;color=0F766E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-zcap/README.md#certification-status"><img alt="Certification: not certified" src="https://img.shields.io/static/v1?label=Certification&amp;message=not%20certified&amp;labelColor=1E293B&amp;color=92400E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/tools/readme/POLICY.md"><img alt="Governance: repository policy" src="https://img.shields.io/static/v1?label=Governance&amp;message=repository%20policy&amp;labelColor=1E293B&amp;color=4338CA"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="Evidence: source and CI" src="https://img.shields.io/static/v1?label=Evidence&amp;message=source%20and%20CI&amp;labelColor=1E293B&amp;color=6D28D9"></a>
</p>
<p align="center"><a href="#overview">Overview</a> · <a href="#installation">Installation</a> · <a href="#quick-start">Quick Start</a> · <a href="#usage">Usage</a> · <a href="#public-api-and-import-surfaces">API</a> · <a href="#contributing">Contributing</a> · <a href="#governance">Governance</a> · <a href="#license">License</a></p>
<!-- readme-standards:end branding -->

---

## Overview

### Summary

ZCAP-LD v0.4.0 delegation and HTTP invocation signing and verification for
the TBA Ed25519 development profile.

Use `ZcapRoot` to configure a trusted local root and `sign_delegation`
to grant a controller restricted actions at a target. A signed delegation
embeds its immediate delegated parent and references older ancestors by ID.
Use `sign_http_invocation` to present a root by ID or a leaf delegation as
gzip-compressed, base64url-encoded JSON.

Configure `ZcapVerifier` with a trusted local root lookup, an Ed25519 key
lookup, a revocation check, and a TBA replay reservation provider. The key
lookup takes the controller, verification method ID, and required proof
purpose. Return a key only if the method is authorized for that controller
and purpose. The revocation check takes the root and delegated capability IDs.
Supply the operation's trusted root, method, target, and action to
`verify_invocation`, then dispatch using the verified request.

Delegation proofs use `eddsa-jcs-2022`. The verifier hashes the canonical
proof options and the canonical unsigned document separately, then checks
the Ed25519 signature over their concatenated hashes. The two fixed
JSON-LD contexts are checked locally. This suite uses JSON canonicalization
and needs no remote context fetching or RDF canonicalization.

The HTTP profile uses one RFC 9421 signature named `zcap`. It signs the
method, full target URI, Capability-Invocation field, SHA-256 Content-Digest,
and Content-Type when present. The application supplies the externally
effective URL and unmodified body. Preserve repeated headers so the verifier
can reject duplicates. Each signature includes a creation time, an expiry,
and a nonce. Use shared atomic replay storage for a multi-worker deployment.

The profile accepts one controller per capability, explicit action
restrictions on delegations, simple HTTPS paths without query strings, and
up to eight delegated capabilities. It uses this exact Capability-Invocation
field syntax for root and delegated invocations, respectively.

```text
zcap id="<root-id>",action="read"
zcap capability=<base64url-gzip-json>,action="read"
```

This is a bounded profile. It does not implement JSON invocation proofs,
arbitrary JSON-LD contexts or caveats, query attenuation, or a revocation
endpoint.

- [ZCAP-LD v0.4.0](https://w3c-ccg.github.io/zcap-spec/v0.4.0/)
- [W3C EdDSA Data Integrity suites](https://www.w3.org/TR/vc-di-eddsa/#eddsa-jcs-2022)
- [RFC 9421 HTTP Message Signatures](https://www.rfc-editor.org/rfc/rfc9421.html)
- [RFC 9530 Digest Fields](https://www.rfc-editor.org/rfc/rfc9530.html)

- Package: `tba-protocol-zcap`
- Layer: `050-protocols`
- Responsibility: ZCAP-LD delegation and HTTP invocation verification for the TBA Ed25519 development profile.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-zcap/src/tba_protocol_zcap/__init__.py).
- Distribution: Python package on PyPI.

### Why This Package

`tba-protocol-zcap` isolates this responsibility: ZCAP-LD delegation and HTTP invocation verification for the TBA Ed25519 development profile. Its [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-zcap/src/tba_protocol_zcap/__init__.py) exposes `CRYPTOSUITE`, `PROFILE`, `SPEC_VERSION`, `VerifiedZcapInvocation`, `ZcapDelegation`, `ZcapError`, `ZcapHttpInvocation`, `ZcapRoot`, `ZcapVerifier`, `sign_delegation`, `sign_http_invocation`, allowing consumers to select this package without treating adjacent packages as part of its public contract.

### When to Use

Choose `tba-protocol-zcap` for this responsibility: ZCAP-LD delegation and HTTP invocation verification for the TBA Ed25519 development profile. Its `050-protocols` placement keeps protocol semantics and projections separate from deployment hosting or ownership of persistence implementations.

### Features

- `InvocationSignature`: declared in src/tba_protocol_zcap/http.py
- `VerifiedZcapInvocation`: declared in src/tba_protocol_zcap/protocol.py
- `ZcapVerifier`: Use local trust, purpose-aware key resolution, and atomic replay storage.
- `ZcapError`: Malformed or unauthorized ZCAP-LD input.
- `ZcapRoot`: declared in src/tba_protocol_zcap/schemas.py
- `ZcapDelegation`: declared in src/tba_protocol_zcap/schemas.py
- `ZcapHttpInvocation`: declared in src/tba_protocol_zcap/schemas.py

### Non-Goals

`tba-protocol-zcap` does not take ownership of deployment hosting or ownership of persistence implementations.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

---

## Getting Started

### Prerequisites

Python `>=3.10,<3.16` is required. The [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-zcap/pyproject.toml) declares runtime dependencies including `cryptography`, `tba-codec-jcs`, `tba-codec-multibase`, `tba-contracts-replay`. Read the example’s inputs and service requirements before execution.

### Installation

Install the selected PyPI release of `tba-protocol-zcap`:

```bash
uv pip install tba-protocol-zcap
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/050-protocols/tba-protocol-zcap
```

#### uv

<!-- readme-standards:begin installation.uv -->
```bash
uv add tba-protocol-zcap
```
<!-- readme-standards:end installation.uv -->

#### pip

<!-- readme-standards:begin installation.pip -->
```bash
python -m pip install tba-protocol-zcap
```
<!-- readme-standards:end installation.pip -->

#### Poetry

<!-- readme-standards:begin installation.poetry -->
```bash
poetry add tba-protocol-zcap
```
<!-- readme-standards:end installation.poetry -->

### Quick Start

Build the package from the repository root.

```bash
uv build --wheel pkgs/050-protocols/tba-protocol-zcap
```

#### Example

<!-- readme-standards:begin example.quick-start -->
Source: [docs/readme/quick_start.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-zcap/docs/readme/quick_start.py).

```python
import tba_protocol_zcap

print(tba_protocol_zcap.__name__)
```
<!-- readme-standards:end example.quick-start -->

#### Expected Result

The example demonstrates the documented `tba-protocol-zcap` source boundary or workflow. Complete its required configuration first. README CI checks the maintained source’s syntax and declarations; it does not claim that external services or the application workflow were exercised.

---

## Usage

### Common Workflows

<!-- readme-standards:begin example.usage -->
Source: [docs/readme/usage.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-zcap/docs/readme/usage.py).

```python
import tba_protocol_zcap

print(tba_protocol_zcap.__name__)
```
<!-- readme-standards:end example.usage -->

The following public-entry-point example belongs to `tba-protocol-zcap`. ZCAP-LD delegation and HTTP invocation verification for the TBA Ed25519 development profile. Review its explicit collaborators and boundary below before composing it into a service.

### Configuration

Configure `tba-protocol-zcap` through the APIs in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-zcap/src/tba_protocol_zcap/__init__.py); its [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-zcap/pyproject.toml) describes installation requirements, not an implicit service configuration. No additional package-global configuration contract is inferred from dependencies.

### Error Handling

The inspected `tba-protocol-zcap` source raises `ZcapError`. Handle these at the calling boundary and consult the implementation for the triggering conditions.

### Best Practices

Use the explicit `tba-protocol-zcap` imports documented below and keep collaborator configuration with the caller. Run the package’s relevant tests after changing `CRYPTOSUITE`, `PROFILE`, `SPEC_VERSION`, `VerifiedZcapInvocation`, `ZcapDelegation`, `ZcapError`, `ZcapHttpInvocation`, `ZcapRoot`, `ZcapVerifier`, `sign_delegation`, `sign_http_invocation`; an import or successful installation alone does not establish its runtime guarantees.

---

## Package Boundary

### What It Owns

`tba-protocol-zcap` belongs to `050-protocols` and owns protocol semantics and projections: ZCAP-LD delegation and HTTP invocation verification for the TBA Ed25519 development profile.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-zcap/src/tba_protocol_zcap/__init__.py). Public exports include `CRYPTOSUITE`, `PROFILE`, `SPEC_VERSION`, `VerifiedZcapInvocation`, `ZcapDelegation`, `ZcapError`, `ZcapHttpInvocation`, `ZcapRoot`, `ZcapVerifier`, `sign_delegation`, `sign_http_invocation`.

Keep deployment hosting or ownership of persistence implementations in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

### Public API and Import Surfaces

Import namespace: `tba_protocol_zcap`.

Source-declared exports or types: `CRYPTOSUITE`, `PROFILE`, `SPEC_VERSION`, `VerifiedZcapInvocation`, `ZcapDelegation`, `ZcapError`, `ZcapHttpInvocation`, `ZcapRoot`, `ZcapVerifier`, `sign_delegation`, `sign_http_invocation`.

Inspect [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-zcap/src/tba_protocol_zcap/__init__.py) for exact signatures; this inventory does not designate every internal module as stable.

### Entry Points

<!-- readme-standards:begin entry-points -->
This package declares no command-line, GUI, or plugin entry points in its manifest.
<!-- readme-standards:end entry-points -->

### Injected Dependencies

Explicit construction inputs and collaborators for `tba-protocol-zcap`:

- `sign_http_invocation` construction inputs: `method`, `target`, `action`, `key_id`, `key`, `created`, `expires`, `nonce`, `body`, `content_type`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-zcap/src/tba_protocol_zcap/http.py).
- `sign_delegation` construction inputs: `verification_method`, `key`, `created`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-zcap/src/tba_protocol_zcap/proofs.py).
- `ZcapVerifier` construction inputs: `resolve_root`, `resolve_key`, `is_revoked`, `replay`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-zcap/src/tba_protocol_zcap/protocol.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

### Protocol Consumers

Direct consumers in this checkout’s package manifests include `tba-workspace`. These edges describe declared dependencies, not protocol-conformance evidence.

### Extensions

For `tba-protocol-zcap`, use the source-declared public interfaces (`CRYPTOSUITE`, `PROFILE`, `SPEC_VERSION`, `VerifiedZcapInvocation`, `ZcapDelegation`, `ZcapError`, `ZcapHttpInvocation`, `ZcapRoot`, `ZcapVerifier`, `sign_delegation`, `sign_http_invocation`) when composing or extending behavior. Its entry-point section below is authoritative for registered plugins; no additional extension loader is inferred from the package name.

---

## Operations and Readiness

### Operational Requirements

`tba-protocol-zcap` exposes protocol semantics and projections. Public operations found in its source:

- `sign_http_invocation` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-zcap/src/tba_protocol_zcap/http.py).
- `sign_delegation` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-zcap/src/tba_protocol_zcap/proofs.py).
- `ZcapVerifier.verify_invocation` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-zcap/src/tba_protocol_zcap/protocol.py).
- `ZcapRoot.id` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-zcap/src/tba_protocol_zcap/schemas.py).
- `ZcapRoot.to_document` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-zcap/src/tba_protocol_zcap/schemas.py).
- `ZcapDelegation.to_document` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-zcap/src/tba_protocol_zcap/schemas.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

### Health and Observability

This README does not establish a standalone health endpoint for `tba-protocol-zcap`. Observe the concrete caller’s results, exceptions, and existing test reports. An application that embeds this package must define its own health and telemetry contract.

### Security and Resource Limits

Apply the input, credential, and resource constraints implemented in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-zcap/src/tba_protocol_zcap/__init__.py). The `tba-protocol-zcap` README gate is a documentation check, not a security review or a substitute for the implementation’s limits and caller authorization.

### Compatibility

This source version of `tba-protocol-zcap` declares Python `>=3.10,<3.16`. Consult its dependency constraints before upgrading. Source-version and registry-version badges have separate meanings; this migration makes no additional platform or interoperability certification claim.

---

## Verification

### Tests

Check that the build produces a wheel with the package version declared in `pyproject.toml`.

### Certification Status

No external certification is asserted for `tba-protocol-zcap` by this documentation migration. README conformance, example syntax, runtime tests, and protocol or security certification are distinct evidence scopes.

### Evidence

The [README standards CI](https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml) records mechanical documentation results for its tested commit. The [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-zcap/src/tba_protocol_zcap/__init__.py) and example sources support the package-boundary description; external runtime behavior requires its own test evidence.

---

## FAQ

### Why

**Why select this package?** `tba-protocol-zcap` provides zCAP-LD delegation and HTTP invocation verification for the TBA Ed25519 development profile; use its own API boundary rather than assuming neighboring packages are bundled or configured automatically.

### How

**How do I start?** Install or synchronize the environment under Getting Started, follow the maintained example for `tba-protocol-zcap`, and consult [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-zcap/src/tba_protocol_zcap/__init__.py) for the exact types and signatures involved.

### When

**When should I validate an upgrade?** Recheck `tba-protocol-zcap` whenever its source version, declared collaborators, configuration, or caller changes. Run relevant behavioral tests in addition to the README gate before promotion.

---

## Documentation and Related Packages

### More Documentation

The [repository contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md), [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-zcap/src/tba_protocol_zcap/__init__.py), and [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-zcap/pyproject.toml) provide the supporting context for `tba-protocol-zcap`. The [README policy](https://github.com/groupsum/readme-standards/blob/master/docs/outline.md) defines the common document structure.

### Related Packages

Declared local runtime dependencies:

- [tba-codec-jcs](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-jcs/README.md)
- [tba-codec-multibase](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-multibase/README.md)
- [tba-contracts-replay](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-replay/README.md)

### Project Links

<!-- readme-standards:begin project-links -->
- [Documentation](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/050-protocols/tba-protocol-zcap#readme)
- [Homepage](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/050-protocols/tba-protocol-zcap#readme)
- [Issues](https://github.com/tigrbl/tigrbl_auth/issues)
- [PyPI](https://pypi.org/project/tba-protocol-zcap/)
- [Repository](https://github.com/tigrbl/tigrbl_auth)
- [Source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/050-protocols/tba-protocol-zcap)
- [pypi: tba-protocol-zcap](https://pypi.org/project/tba-protocol-zcap/)
<!-- readme-standards:end project-links -->

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/050-protocols/tba-protocol-zcap)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-zcap/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-zcap/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-zcap/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-protocol-zcap/)

---

## Contributing

### How to Contribute

Follow the [contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md) and include a focused example or regression for changes to `tba-protocol-zcap`. Keep package behavior, its documented boundary, and its tests aligned.

### Development Setup

Work from the `pkgs/050-protocols/tba-protocol-zcap` checkout. Synchronize its declared development environment with uv, then run the relevant package tests and `python -m pytest docs/readme/test_examples.py`. The repository’s dedicated README job installs `readme-standards==0.1.3` without resolving unrelated runtime packages.

### Notes for Maintainers

Edit authored prose directly in this `tba-protocol-zcap` README. Update source examples in `docs/readme/`, then run `readme-standards render --root . --write` from the package directory and review the diff. Required headings and generated blocks come from package-guide-v1.

---

## Governance

### Ownership and Decision Making

Changes to `tba-protocol-zcap` follow the maintainer review process of [tigrbl/tigrbl_auth](https://github.com/tigrbl/tigrbl_auth) and its contribution guide. Author attribution remains in the [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-zcap/pyproject.toml); this README does not assign new publishing or administrative authority.

### Standards and Policies

`tba-protocol-zcap` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `050-protocols` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

### Lifecycle and Migration

The `tba-protocol-zcap` source version is `0.4.0.dev3`. This change standardizes documentation and adds a development-only gate; it does not publish a new runtime version or declare a previously unpublished package released. Preserve explicit deprecation and replacement instructions where present.

---

## License and Attribution

### License

<!-- readme-standards:begin license -->
Licensed under `Apache-2.0`. See [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-zcap/LICENSE).
<!-- readme-standards:end license -->

### Notices

<!-- readme-standards:begin notices -->
See [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-zcap/NOTICE) for attribution.
<!-- readme-standards:end notices -->
