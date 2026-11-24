# tba-protocol-ucan

<!-- readme-standards:begin branding -->
<p align="center"><a href="https://github.com/tigrbl/tigrbl_auth"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="300"></a></p>
<p align="center"><strong>tba-protocol-ucan</strong></p>
<p align="center">UCAN delegation and invocation verification for the TBA Ed25519 development profile.</p>
<p align="center">
<a href="https://pypi.org/project/tba-protocol-ucan/"><img alt="pypi: tba-protocol-ucan" src="https://img.shields.io/pypi/v/tba-protocol-ucan?labelColor=1E293B&amp;color=1D4ED8"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-ucan/pyproject.toml"><img alt="Source version: 0.4.0.dev3" src="https://img.shields.io/static/v1?label=Source%20version&amp;message=0.4.0.dev3&amp;labelColor=1E293B&amp;color=4338CA"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-ucan/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/static/v1?label=Python&amp;message=%3E%3D3.10%2C%3C3.16&amp;labelColor=1E293B&amp;color=0F766E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-ucan/pyproject.toml"><img alt="Layer: 050-protocols" src="https://img.shields.io/static/v1?label=Layer&amp;message=050-protocols&amp;labelColor=1E293B&amp;color=6D28D9"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-ucan/README.md#lifecycle-and-migration"><img alt="Lifecycle: active" src="https://img.shields.io/static/v1?label=Lifecycle&amp;message=active&amp;labelColor=1E293B&amp;color=166534"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-ucan/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/static/v1?label=License&amp;message=Apache-2.0&amp;labelColor=1E293B&amp;color=86198F"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-ucan/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/static/v1?label=Notice&amp;message=attribution&amp;labelColor=1E293B&amp;color=86198F"></a>
</p>
<p align="center">
<a href="https://pypi.org/project/tba-protocol-ucan/"><img alt="Monthly PyPI downloads: tba-protocol-ucan" src="https://img.shields.io/pypi/dm/tba-protocol-ucan?labelColor=1E293B&amp;color=0E7490"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-ucan/README.md"><img alt="README hits: tba-protocol-ucan" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/pkgs/050-protocols/tba-protocol-ucan/README.md.svg?label=README%20hits&amp;labelColor=1E293B&amp;color=0E7490"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="README standards: CI gate" src="https://img.shields.io/static/v1?label=README%20standards&amp;message=CI%20gate&amp;labelColor=1E293B&amp;color=1D4ED8"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-ucan/docs/readme/test_examples.py"><img alt="Tests: example source" src="https://img.shields.io/static/v1?label=Tests&amp;message=example%20source&amp;labelColor=1E293B&amp;color=0F766E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-ucan/README.md#certification-status"><img alt="Certification: not certified" src="https://img.shields.io/static/v1?label=Certification&amp;message=not%20certified&amp;labelColor=1E293B&amp;color=92400E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/tools/readme/POLICY.md"><img alt="Governance: repository policy" src="https://img.shields.io/static/v1?label=Governance&amp;message=repository%20policy&amp;labelColor=1E293B&amp;color=4338CA"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="Evidence: source and CI" src="https://img.shields.io/static/v1?label=Evidence&amp;message=source%20and%20CI&amp;labelColor=1E293B&amp;color=6D28D9"></a>
</p>
<p align="center"><a href="#overview">Overview</a> · <a href="#installation">Installation</a> · <a href="#quick-start">Quick Start</a> · <a href="#usage">Usage</a> · <a href="#public-api-and-import-surfaces">API</a> · <a href="#contributing">Contributing</a> · <a href="#governance">Governance</a> · <a href="#license">License</a></p>
<!-- readme-standards:end branding -->

---

## Overview

### Summary

UCAN delegation and invocation signing and verification for the TBA Ed25519
development profile. The wire tags are `ucan/dlg@1.0.0` and `ucan/inv@1.0.0`.

- [UCAN envelope](https://github.com/ucan-wg/spec/blob/8072f3f23f451eaa1271269fe763aebcf294f4db/README.md#envelope)
- [UCAN delegation](https://github.com/ucan-wg/delegation/blob/1cb32dbc9d4d15a23bf9844a02515d760b81e816/README.md)
- [UCAN invocation](https://github.com/ucan-wg/invocation/blob/0f4c11325af6aca298b565cc19e90009d10e0197/README.md)

This profile supports bare Ed25519 `did:key` identifiers, canonical DAG-CBOR
with integers in the interoperable 53-bit range, linear proof chains of up to
16 grants, finite expiries, and equality predicates on top-level arguments.
Invocations have a maximum remaining lifetime of five minutes. The profile
rejects unsupported algorithms, fields, and policy operators. It covers a
subset of the UCAN specifications.

- Package: `tba-protocol-ucan`
- Layer: `050-protocols`
- Responsibility: UCAN delegation and invocation verification for the TBA Ed25519 development profile.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-ucan/src/tba_protocol_ucan/__init__.py).
- Distribution: Python package on PyPI.

### Why This Package

`tba-protocol-ucan` isolates this responsibility: UCAN delegation and invocation verification for the TBA Ed25519 development profile. Its [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-ucan/src/tba_protocol_ucan/__init__.py) exposes `DELEGATION_TAG`, `INVOCATION_TAG`, `PROFILE`, `UcanDelegation`, `UcanEnvelopeCodec`, `UcanError`, `UcanInvocation`, `UcanVerifier`, `VerifiedUcanInvocation`, `content_id`, `did_key`, `sign_delegation`, `sign_invocation`, allowing consumers to select this package without treating adjacent packages as part of its public contract.

### When to Use

Choose `tba-protocol-ucan` for this responsibility: UCAN delegation and invocation verification for the TBA Ed25519 development profile. Its `050-protocols` placement keeps protocol semantics and projections separate from deployment hosting or ownership of persistence implementations.

### Features

- `UcanError`: Malformed or unauthorized UCAN within the supported profile.
- `UcanEnvelopeCodec`: Sign and verify the two supported UCAN v1 wire envelopes.
- `VerifiedUcanInvocation`: declared in src/tba_protocol_ucan/protocol.py
- `UcanVerifier`: Verify a closed delegation chain and reserve the invocation before execution.
- `UcanDelegation`: declared in src/tba_protocol_ucan/schemas.py
- `UcanInvocation`: declared in src/tba_protocol_ucan/schemas.py

### Non-Goals

`tba-protocol-ucan` does not take ownership of deployment hosting or ownership of persistence implementations.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

---

## Getting Started

### Prerequisites

Python `>=3.10,<3.16` is required. The [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-ucan/pyproject.toml) declares runtime dependencies including `cryptography`, `tba-codec-cid`, `tba-codec-dag-cbor`, `tba-codec-multibase`, `tba-contracts-replay`. Read the example’s inputs and service requirements before execution.

### Installation

Install the selected PyPI release of `tba-protocol-ucan`:

```bash
uv pip install tba-protocol-ucan
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/050-protocols/tba-protocol-ucan
```

#### uv

<!-- readme-standards:begin installation.uv -->
```bash
uv add tba-protocol-ucan
```
<!-- readme-standards:end installation.uv -->

#### pip

<!-- readme-standards:begin installation.pip -->
```bash
python -m pip install tba-protocol-ucan
```
<!-- readme-standards:end installation.pip -->

#### Poetry

<!-- readme-standards:begin installation.poetry -->
```bash
poetry add tba-protocol-ucan
```
<!-- readme-standards:end installation.poetry -->

### Quick Start

Build the package from the repository root.

```bash
uv build --wheel pkgs/050-protocols/tba-protocol-ucan
```

#### Example

<!-- readme-standards:begin example.quick-start -->
Source: [docs/readme/quick_start.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-ucan/docs/readme/quick_start.py).

```python
import tba_protocol_ucan

print(tba_protocol_ucan.__name__)
```
<!-- readme-standards:end example.quick-start -->

#### Expected Result

The example demonstrates the documented `tba-protocol-ucan` source boundary or workflow. Complete its required configuration first. README CI checks the maintained source’s syntax and declarations; it does not claim that external services or the application workflow were exercised.

---

## Usage

### Common Workflows

<!-- readme-standards:begin example.usage -->
Source: [docs/readme/usage.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-ucan/docs/readme/usage.py).

```python
import tba_protocol_ucan

print(tba_protocol_ucan.__name__)
```
<!-- readme-standards:end example.usage -->

The following public-entry-point example belongs to `tba-protocol-ucan`. UCAN delegation and invocation verification for the TBA Ed25519 development profile. Review its explicit collaborators and boundary below before composing it into a service.

### Configuration

Configure `tba-protocol-ucan` through the APIs in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-ucan/src/tba_protocol_ucan/__init__.py); its [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-ucan/pyproject.toml) describes installation requirements, not an implicit service configuration. No additional package-global configuration contract is inferred from dependencies.

### Error Handling

The inspected `tba-protocol-ucan` source raises `UcanError`. Handle these at the calling boundary and consult the implementation for the triggering conditions.

### Best Practices

Use the explicit `tba-protocol-ucan` imports documented below and keep collaborator configuration with the caller. Run the package’s relevant tests after changing `DELEGATION_TAG`, `INVOCATION_TAG`, `PROFILE`, `UcanDelegation`, `UcanEnvelopeCodec`, `UcanError`, `UcanInvocation`, `UcanVerifier`, `VerifiedUcanInvocation`, `content_id`, `did_key`, `sign_delegation`, `sign_invocation`; an import or successful installation alone does not establish its runtime guarantees.

---

## Package Boundary

### What It Owns

`tba-protocol-ucan` belongs to `050-protocols` and owns protocol semantics and projections: UCAN delegation and invocation verification for the TBA Ed25519 development profile.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-ucan/src/tba_protocol_ucan/__init__.py). Public exports include `DELEGATION_TAG`, `INVOCATION_TAG`, `PROFILE`, `UcanDelegation`, `UcanEnvelopeCodec`, `UcanError`, `UcanInvocation`, `UcanVerifier`, `VerifiedUcanInvocation`, `content_id`, `did_key`, `sign_delegation`.

Keep deployment hosting or ownership of persistence implementations in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

### Public API and Import Surfaces

Import namespace: `tba_protocol_ucan`.

Source-declared exports or types: `DELEGATION_TAG`, `INVOCATION_TAG`, `PROFILE`, `UcanDelegation`, `UcanEnvelopeCodec`, `UcanError`, `UcanInvocation`, `UcanVerifier`, `VerifiedUcanInvocation`, `content_id`, `did_key`, `sign_delegation`, `sign_invocation`.

Inspect [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-ucan/src/tba_protocol_ucan/__init__.py) for exact signatures; this inventory does not designate every internal module as stable.

### Entry Points

<!-- readme-standards:begin entry-points -->
This package declares no command-line, GUI, or plugin entry points in its manifest.
<!-- readme-standards:end entry-points -->

### Injected Dependencies

Explicit construction inputs and collaborators for `tba-protocol-ucan`:

- `UcanVerifier` construction inputs: `resolve_proof`, `is_revoked`, `replay`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-ucan/src/tba_protocol_ucan/protocol.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

### Protocol Consumers

Direct consumers in this checkout’s package manifests include `tba-workspace`. These edges describe declared dependencies, not protocol-conformance evidence.

### Extensions

For `tba-protocol-ucan`, use the source-declared public interfaces (`DELEGATION_TAG`, `INVOCATION_TAG`, `PROFILE`, `UcanDelegation`, `UcanEnvelopeCodec`, `UcanError`, `UcanInvocation`, `UcanVerifier`, `VerifiedUcanInvocation`, `content_id`, `did_key`, `sign_delegation`, `sign_invocation`) when composing or extending behavior. Its entry-point section below is authoritative for registered plugins; no additional extension loader is inferred from the package name.

---

## Operations and Readiness

### Operational Requirements

`tba-protocol-ucan` exposes protocol semantics and projections. Public operations found in its source:

- `did_key` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-ucan/src/tba_protocol_ucan/codec.py).
- `content_id` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-ucan/src/tba_protocol_ucan/codec.py).
- `UcanEnvelopeCodec.sign` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-ucan/src/tba_protocol_ucan/codec.py).
- `UcanEnvelopeCodec.verify` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-ucan/src/tba_protocol_ucan/codec.py).
- `sign_delegation` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-ucan/src/tba_protocol_ucan/protocol.py).
- `sign_invocation` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-ucan/src/tba_protocol_ucan/protocol.py).
- `UcanVerifier.verify_invocation` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-ucan/src/tba_protocol_ucan/protocol.py).
- `UcanDelegation.from_payload` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-ucan/src/tba_protocol_ucan/schemas.py).
- `UcanDelegation.to_payload` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-ucan/src/tba_protocol_ucan/schemas.py).
- `UcanInvocation.executor` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-ucan/src/tba_protocol_ucan/schemas.py).
- `UcanInvocation.from_payload` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-ucan/src/tba_protocol_ucan/schemas.py).
- `UcanInvocation.to_payload` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-ucan/src/tba_protocol_ucan/schemas.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

### Health and Observability

This README does not establish a standalone health endpoint for `tba-protocol-ucan`. Observe the concrete caller’s results, exceptions, and existing test reports. An application that embeds this package must define its own health and telemetry contract.

### Security and Resource Limits

Apply the input, credential, and resource constraints implemented in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-ucan/src/tba_protocol_ucan/__init__.py). The `tba-protocol-ucan` README gate is a documentation check, not a security review or a substitute for the implementation’s limits and caller authorization.

### Compatibility

This source version of `tba-protocol-ucan` declares Python `>=3.10,<3.16`. Consult its dependency constraints before upgrading. Source-version and registry-version badges have separate meanings; this migration makes no additional platform or interoperability certification claim.

---

## Verification

### Tests

Check that the build produces a wheel with the package version declared in `pyproject.toml`.

### Certification Status

No external certification is asserted for `tba-protocol-ucan` by this documentation migration. README conformance, example syntax, runtime tests, and protocol or security certification are distinct evidence scopes.

### Evidence

The [README standards CI](https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml) records mechanical documentation results for its tested commit. The [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-ucan/src/tba_protocol_ucan/__init__.py) and example sources support the package-boundary description; external runtime behavior requires its own test evidence.

---

## FAQ

### Why

**Why select this package?** `tba-protocol-ucan` provides uCAN delegation and invocation verification for the TBA Ed25519 development profile; use its own API boundary rather than assuming neighboring packages are bundled or configured automatically.

### How

**How do I start?** Install or synchronize the environment under Getting Started, follow the maintained example for `tba-protocol-ucan`, and consult [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-ucan/src/tba_protocol_ucan/__init__.py) for the exact types and signatures involved.

### When

**When should I validate an upgrade?** Recheck `tba-protocol-ucan` whenever its source version, declared collaborators, configuration, or caller changes. Run relevant behavioral tests in addition to the README gate before promotion.

---

## Documentation and Related Packages

### More Documentation

The [repository contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md), [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-ucan/src/tba_protocol_ucan/__init__.py), and [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-ucan/pyproject.toml) provide the supporting context for `tba-protocol-ucan`. The [README policy](https://github.com/groupsum/readme-standards/blob/master/docs/outline.md) defines the common document structure.

### Related Packages

Declared local runtime dependencies:

- [tba-codec-cid](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-cid/README.md)
- [tba-codec-dag-cbor](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-dag-cbor/README.md)
- [tba-codec-multibase](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-multibase/README.md)
- [tba-contracts-replay](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-replay/README.md)

### Project Links

<!-- readme-standards:begin project-links -->
- [Documentation](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/050-protocols/tba-protocol-ucan#readme)
- [Homepage](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/050-protocols/tba-protocol-ucan#readme)
- [Issues](https://github.com/tigrbl/tigrbl_auth/issues)
- [PyPI](https://pypi.org/project/tba-protocol-ucan/)
- [Repository](https://github.com/tigrbl/tigrbl_auth)
- [Source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/050-protocols/tba-protocol-ucan)
- [pypi: tba-protocol-ucan](https://pypi.org/project/tba-protocol-ucan/)
<!-- readme-standards:end project-links -->

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/050-protocols/tba-protocol-ucan)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-ucan/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-ucan/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-ucan/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-protocol-ucan/)

---

## Contributing

### How to Contribute

Follow the [contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md) and include a focused example or regression for changes to `tba-protocol-ucan`. Keep package behavior, its documented boundary, and its tests aligned.

### Development Setup

Work from the `pkgs/050-protocols/tba-protocol-ucan` checkout. Synchronize its declared development environment with uv, then run the relevant package tests and `python -m pytest docs/readme/test_examples.py`. The repository’s dedicated README job installs `readme-standards==0.1.3` without resolving unrelated runtime packages.

### Notes for Maintainers

**Verifying a call**

Use `sign_delegation` and `sign_invocation` with the issuer's Ed25519 private
key. Index signed delegations with `content_id` and list their CIDs in
`UcanInvocation.prf` from root to leaf. Configure `UcanVerifier` with a
proof lookup, a revocation check, and a TBA replay reservation provider.
Call `verify_invocation` with the trusted subject, the local executor, and the
expected command. Dispatch the command with the arguments in the returned
invocation. The verifier checks every delegation's policy against those
arguments and atomically reserves the invocation CID before returning.

The caller supplies the mapping from trusted subjects and commands to local
resources. A deployment with multiple workers needs a shared replay store
with atomic reservations. Revocation storage is supplied by the caller.

**Wire codec**

**DAG-CBOR** produces deterministic binary bytes for the signed map. The
verifier rejects duplicate keys, noncanonical encodings, and values outside
the profile. **Varsig** is the header inside that map identifying Ed25519 and
DAG-CBOR. The signature covers both the header and the versioned payload.

A **CID** identifies the complete signed envelope. Its binary representation
contains CIDv1, the DAG-CBOR codec code, the SHA-256 multihash code and length,
and the digest. The text form uses base58btc. In the invocation proof list,
each CID is a DAG-CBOR tag 42 link with a leading zero byte followed by the
binary CID. The verifier recomputes the CID of every resolved proof before
accepting it.

See [DAG-CBOR](https://ipld.io/specs/codecs/dag-cbor/spec/) and
[Varsig](https://github.com/ChainAgnostic/varsig).

---

## Governance

### Ownership and Decision Making

Changes to `tba-protocol-ucan` follow the maintainer review process of [tigrbl/tigrbl_auth](https://github.com/tigrbl/tigrbl_auth) and its contribution guide. Author attribution remains in the [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-ucan/pyproject.toml); this README does not assign new publishing or administrative authority.

### Standards and Policies

`tba-protocol-ucan` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `050-protocols` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

### Lifecycle and Migration

The `tba-protocol-ucan` source version is `0.4.0.dev3`. This change standardizes documentation and adds a development-only gate; it does not publish a new runtime version or declare a previously unpublished package released. Preserve explicit deprecation and replacement instructions where present.

---

## License and Attribution

### License

<!-- readme-standards:begin license -->
Licensed under `Apache-2.0`. See [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-ucan/LICENSE).
<!-- readme-standards:end license -->

### Notices

<!-- readme-standards:begin notices -->
See [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-ucan/NOTICE) for attribution.
<!-- readme-standards:end notices -->
