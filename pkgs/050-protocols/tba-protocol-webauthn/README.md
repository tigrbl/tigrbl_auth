# tba-protocol-webauthn

<!-- readme-standards:begin branding -->
<p align="center"><a href="https://github.com/tigrbl/tigrbl_auth"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="300"></a></p>
<p align="center"><strong>tba-protocol-webauthn</strong></p>
<p align="center">Versioned W3C Web Authentication relying-party protocol implementation.</p>
<p align="center">
<a href="https://pypi.org/project/tba-protocol-webauthn/"><img alt="pypi: tba-protocol-webauthn" src="https://img.shields.io/pypi/v/tba-protocol-webauthn"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-webauthn/pyproject.toml"><img alt="Source version: 0.4.0.dev3" src="https://img.shields.io/static/v1?label=Source%20version&amp;message=0.4.0.dev3&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-webauthn/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/static/v1?label=Python&amp;message=%3E%3D3.10%2C%3C3.16&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-webauthn/pyproject.toml"><img alt="Layer: 050-protocols" src="https://img.shields.io/static/v1?label=Layer&amp;message=050-protocols&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-webauthn/README.md#lifecycle-and-migration"><img alt="Lifecycle: active" src="https://img.shields.io/static/v1?label=Lifecycle&amp;message=active&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-webauthn/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/static/v1?label=License&amp;message=Apache-2.0&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-webauthn/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/static/v1?label=Notice&amp;message=attribution&amp;color=525252"></a>
</p>
<p align="center">
<a href="https://pypi.org/project/tba-protocol-webauthn/"><img alt="Monthly PyPI downloads: tba-protocol-webauthn" src="https://img.shields.io/pypi/dm/tba-protocol-webauthn"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-webauthn/README.md"><img alt="README hits: tba-protocol-webauthn" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/pkgs/050-protocols/tba-protocol-webauthn/README.md.svg?label=README%20hits"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="README standards: CI gate" src="https://img.shields.io/static/v1?label=README%20standards&amp;message=CI%20gate&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-webauthn/docs/readme/test_examples.py"><img alt="Tests: example source" src="https://img.shields.io/static/v1?label=Tests&amp;message=example%20source&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-webauthn/README.md#certification-status"><img alt="Certification: not certified" src="https://img.shields.io/static/v1?label=Certification&amp;message=not%20certified&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/tools/readme/POLICY.md"><img alt="Governance: repository policy" src="https://img.shields.io/static/v1?label=Governance&amp;message=repository%20policy&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="Evidence: source and CI" src="https://img.shields.io/static/v1?label=Evidence&amp;message=source%20and%20CI&amp;color=525252"></a>
</p>
<p align="center"><a href="#overview">Overview</a> · <a href="#installation">Installation</a> · <a href="#quick-start">Quick Start</a> · <a href="#usage">Usage</a> · <a href="#public-api-and-import-surfaces">API</a> · <a href="#contributing">Contributing</a> · <a href="#governance">Governance</a> · <a href="#license">License</a></p>
<!-- readme-standards:end branding -->

---

## Overview

### Summary

Versioned W3C WebAuthn relying-party schemas, codecs, registration verification, authentication verification, feature selection, and capability bindings.

This package does not implement CTAP transports or durable storage.

- Package: `tba-protocol-webauthn`
- Layer: `050-protocols`
- Responsibility: Versioned W3C Web Authentication relying-party protocol implementation.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-webauthn/src/tba_protocol_webauthn/__init__.py).
- Distribution: Python package on PyPI.

### Why This Package

`tba-protocol-webauthn` isolates this responsibility: Versioned W3C Web Authentication relying-party protocol implementation. Its [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-webauthn/src/tba_protocol_webauthn/__init__.py) exposes `AttestationObject`, `AttestationVerificationInput`, `AttestationVerifierRegistry`, `AttestedCredentialData`, `AuthenticationExpectation`, `AuthenticationVerificationError`, `AuthenticatorAssertionResponse`, `AuthenticatorAttestationResponse`, `AuthenticatorData`, `AuthenticatorDataError`, `AuthenticatorDataFlags`, `AuthenticatorSelectionCriteria`, `BASE_FEATURES`, `CAPABILITY_REQUIREMENTS`, `CLAIM_NAMES`, allowing consumers to select this package without treating adjacent packages as part of its public contract.

### When to Use

Choose `tba-protocol-webauthn` for this responsibility: Versioned W3C Web Authentication relying-party protocol implementation. Its `050-protocols` placement keeps protocol semantics and projections separate from deployment hosting or ownership of persistence implementations.

### Features

- `AttestationVerificationInput`: declared in src/tba_protocol_webauthn/attestation/registry.py
- `AttestationVerifierRegistry`: declared in src/tba_protocol_webauthn/attestation/registry.py
- `AuthenticationExpectation`: declared in src/tba_protocol_webauthn/ceremonies/authentication.py
- `RegistrationExpectation`: declared in src/tba_protocol_webauthn/ceremonies/registration.py
- `AttestationObject`: declared in src/tba_protocol_webauthn/codecs/attestation_object.py
- `AuthenticatorDataFlags`: declared in src/tba_protocol_webauthn/codecs/authenticator_data.py
- `AttestedCredentialData`: declared in src/tba_protocol_webauthn/codecs/authenticator_data.py
- `AuthenticatorData`: declared in src/tba_protocol_webauthn/codecs/authenticator_data.py

### Non-Goals

`tba-protocol-webauthn` does not take ownership of deployment hosting or ownership of persistence implementations.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

---

## Getting Started

### Prerequisites

Python `>=3.10,<3.16` is required. The [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-webauthn/pyproject.toml) declares runtime dependencies including `cbor2`, `tba-primitives-identity`, `tba-contracts-identity`, `tba-concrete-cose`, `tba-provider-cose-cryptography`, `tba-capability-public-key-registration`, `tba-capability-public-key-authentication`. Read the example’s inputs and service requirements before execution.

### Installation

Install the selected PyPI release of `tba-protocol-webauthn`:

```bash
uv pip install tba-protocol-webauthn
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/050-protocols/tba-protocol-webauthn
```

#### uv

<!-- readme-standards:begin installation.uv -->
```bash
uv add tba-protocol-webauthn
```
<!-- readme-standards:end installation.uv -->

#### pip

<!-- readme-standards:begin installation.pip -->
```bash
python -m pip install tba-protocol-webauthn
```
<!-- readme-standards:end installation.pip -->

#### Poetry

<!-- readme-standards:begin installation.poetry -->
```bash
poetry add tba-protocol-webauthn
```
<!-- readme-standards:end installation.poetry -->

### Quick Start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.


```bash
uv run --isolated --no-project --python 3.12 --with "tba-protocol-webauthn==0.4.0.dev3" python quickstart.py
```

The command prints the declared current revision.

#### Example

<!-- readme-standards:begin example.quick-start -->
Source: [docs/readme/quick_start.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-webauthn/docs/readme/quick_start.py).

```python
from tba_protocol_webauthn import CURRENT_VERSION

assert CURRENT_VERSION is not None
print(CURRENT_VERSION)
```
<!-- readme-standards:end example.quick-start -->

#### Expected Result

The example demonstrates the documented `tba-protocol-webauthn` source boundary or workflow. Complete its required configuration first. README CI checks the maintained source’s syntax and declarations; it does not claim that external services or the application workflow were exercised.

---

## Usage

### Common Workflows

<!-- readme-standards:begin example.usage -->
Source: [docs/readme/usage.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-webauthn/docs/readme/usage.py).

```python
from tba_protocol_webauthn import CURRENT_VERSION

assert CURRENT_VERSION is not None
print(CURRENT_VERSION)
```
<!-- readme-standards:end example.usage -->

The following public-entry-point example belongs to `tba-protocol-webauthn`. Versioned W3C Web Authentication relying-party protocol implementation. Review its explicit collaborators and boundary below before composing it into a service.

### Configuration

Configure `tba-protocol-webauthn` through the APIs in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-webauthn/src/tba_protocol_webauthn/__init__.py); its [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-webauthn/pyproject.toml) describes installation requirements, not an implicit service configuration. No additional package-global configuration contract is inferred from dependencies.

### Error Handling

The inspected `tba-protocol-webauthn` source raises `AuthenticationVerificationError`, `RegistrationVerificationError`, `TypeError`, `ValueError`, `WebAuthnVerificationError`. Handle these at the calling boundary and consult the implementation for the triggering conditions.

### Best Practices

Use the explicit `tba-protocol-webauthn` imports documented below and keep collaborator configuration with the caller. Run the package’s relevant tests after changing `AttestationObject`, `AttestationVerificationInput`, `AttestationVerifierRegistry`, `AttestedCredentialData`, `AuthenticationExpectation`, `AuthenticationVerificationError`, `AuthenticatorAssertionResponse`, `AuthenticatorAttestationResponse`, `AuthenticatorData`, `AuthenticatorDataError`, `AuthenticatorDataFlags`, `AuthenticatorSelectionCriteria`, `BASE_FEATURES`, `CAPABILITY_REQUIREMENTS`, `CLAIM_NAMES`; an import or successful installation alone does not establish its runtime guarantees.

---

## Package Boundary

### What It Owns

`tba-protocol-webauthn` belongs to `050-protocols` and owns protocol semantics and projections: Versioned W3C Web Authentication relying-party protocol implementation.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-webauthn/src/tba_protocol_webauthn/__init__.py). Public exports include `AttestationObject`, `AttestationVerificationInput`, `AttestationVerifierRegistry`, `AttestedCredentialData`, `AuthenticationExpectation`, `AuthenticationVerificationError`, `AuthenticatorAssertionResponse`, `AuthenticatorAttestationResponse`, `AuthenticatorData`, `AuthenticatorDataError`, `AuthenticatorDataFlags`, `AuthenticatorSelectionCriteria`.

Keep deployment hosting or ownership of persistence implementations in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

### Public API and Import Surfaces

Import namespace: `tba_protocol_webauthn`.

Source-declared exports or types: `AttestationObject`, `AttestationVerificationInput`, `AttestationVerifierRegistry`, `AttestedCredentialData`, `AuthenticationExpectation`, `AuthenticationVerificationError`, `AuthenticatorAssertionResponse`, `AuthenticatorAttestationResponse`, `AuthenticatorData`, `AuthenticatorDataError`, `AuthenticatorDataFlags`, `AuthenticatorSelectionCriteria`, `BASE_FEATURES`, `CAPABILITY_REQUIREMENTS`, `CLAIM_NAMES`.

Inspect [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-webauthn/src/tba_protocol_webauthn/__init__.py) for exact signatures; this inventory does not designate every internal module as stable.

### Entry Points

<!-- readme-standards:begin entry-points -->
This package declares no command-line, GUI, or plugin entry points in its manifest.
<!-- readme-standards:end entry-points -->

### Injected Dependencies

Explicit construction inputs and collaborators for `tba-protocol-webauthn`:

- `build_attestation_registry` construction inputs: `packed`, `u2f`, `tpm`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-webauthn/src/tba_protocol_webauthn/attestation/adapters.py).
- `AttestationVerifierRegistry` construction inputs: `verifiers`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-webauthn/src/tba_protocol_webauthn/attestation/registry.py).
- `build_request_options` construction inputs: `rp_id`, `allowed_credentials`, `user_verification`, `timeout_ms`, `challenge`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-webauthn/src/tba_protocol_webauthn/ceremonies/authentication.py).
- `verify_authentication_response` construction inputs: `expected`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-webauthn/src/tba_protocol_webauthn/ceremonies/authentication.py).
- `build_creation_options` construction inputs: `rp_id`, `rp_name`, `user_handle`, `user_name`, `user_display_name`, `algorithms`, `excluded_credential_ids`, `user_verification`, `resident_key`, `attestation`, `timeout_ms`, `challenge`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-webauthn/src/tba_protocol_webauthn/ceremonies/registration.py).
- `verify_registration_response` construction inputs: `expected`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-webauthn/src/tba_protocol_webauthn/ceremonies/registration.py).
- `parse_client_data` construction inputs: `expected_type`, `expected_challenge`, `expected_origin`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-webauthn/src/tba_protocol_webauthn/codecs/client_data.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

### Protocol Consumers

Direct consumers in this checkout’s package manifests include `tba-profile-fido2-server`, `tba-runtime-identity`, `tba-auth`, `tba-router-webauthn`, `tba-workspace`. These edges describe declared dependencies, not protocol-conformance evidence.

### Extensions

For `tba-protocol-webauthn`, use the source-declared public interfaces (`AttestationObject`, `AttestationVerificationInput`, `AttestationVerifierRegistry`, `AttestedCredentialData`, `AuthenticationExpectation`, `AuthenticationVerificationError`, `AuthenticatorAssertionResponse`, `AuthenticatorAttestationResponse`, `AuthenticatorData`, `AuthenticatorDataError`, `AuthenticatorDataFlags`, `AuthenticatorSelectionCriteria`, `BASE_FEATURES`, `CAPABILITY_REQUIREMENTS`, `CLAIM_NAMES`) when composing or extending behavior. Its entry-point section below is authoritative for registered plugins; no additional extension loader is inferred from the package name.

---

## Operations and Readiness

### Operational Requirements

`tba-protocol-webauthn` exposes protocol semantics and projections. Public operations found in its source:

- `build_attestation_registry` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-webauthn/src/tba_protocol_webauthn/attestation/adapters.py).
- `AttestationVerifierRegistry.register` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-webauthn/src/tba_protocol_webauthn/attestation/registry.py).
- `AttestationVerifierRegistry.verify` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-webauthn/src/tba_protocol_webauthn/attestation/registry.py).
- `AttestationVerifierRegistry.supported_formats` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-webauthn/src/tba_protocol_webauthn/attestation/registry.py).
- `build_request_options` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-webauthn/src/tba_protocol_webauthn/ceremonies/authentication.py).
- `verify_authentication_response` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-webauthn/src/tba_protocol_webauthn/ceremonies/authentication.py).
- `build_creation_options` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-webauthn/src/tba_protocol_webauthn/ceremonies/registration.py).
- `verify_registration_response` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-webauthn/src/tba_protocol_webauthn/ceremonies/registration.py).
- `decode_attestation_object` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-webauthn/src/tba_protocol_webauthn/codecs/attestation_object.py).
- `AuthenticatorData.user_present` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-webauthn/src/tba_protocol_webauthn/codecs/authenticator_data.py).
- `AuthenticatorData.user_verified` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-webauthn/src/tba_protocol_webauthn/codecs/authenticator_data.py).
- `AuthenticatorData.matches_rp_id_hash` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-webauthn/src/tba_protocol_webauthn/codecs/authenticator_data.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

### Health and Observability

This README does not establish a standalone health endpoint for `tba-protocol-webauthn`. Observe the concrete caller’s results, exceptions, and existing test reports. An application that embeds this package must define its own health and telemetry contract.

### Security and Resource Limits

Apply the input, credential, and resource constraints implemented in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-webauthn/src/tba_protocol_webauthn/__init__.py). The `tba-protocol-webauthn` README gate is a documentation check, not a security review or a substitute for the implementation’s limits and caller authorization.

### Compatibility

This source version of `tba-protocol-webauthn` declares Python `>=3.10,<3.16`. Consult its dependency constraints before upgrading. Source-version and registry-version badges have separate meanings; this migration makes no additional platform or interoperability certification claim.

---

## Verification

### Tests

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-webauthn/src/tba_protocol_webauthn/__init__.py).

### Certification Status

No external certification is asserted for `tba-protocol-webauthn` by this documentation migration. README conformance, example syntax, runtime tests, and protocol or security certification are distinct evidence scopes.

### Evidence

The [README standards CI](https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml) records mechanical documentation results for its tested commit. The [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-webauthn/src/tba_protocol_webauthn/__init__.py) and example sources support the package-boundary description; external runtime behavior requires its own test evidence.

---

## FAQ

### Why

**Why select this package?** `tba-protocol-webauthn` provides versioned W3C Web Authentication relying-party protocol implementation; use its own API boundary rather than assuming neighboring packages are bundled or configured automatically.

### How

**How do I start?** Install or synchronize the environment under Getting Started, follow the maintained example for `tba-protocol-webauthn`, and consult [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-webauthn/src/tba_protocol_webauthn/__init__.py) for the exact types and signatures involved.

### When

**When should I validate an upgrade?** Recheck `tba-protocol-webauthn` whenever its source version, declared collaborators, configuration, or caller changes. Run relevant behavioral tests in addition to the README gate before promotion.

---

## Documentation and Related Packages

### More Documentation

The [repository contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md), [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-webauthn/src/tba_protocol_webauthn/__init__.py), and [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-webauthn/pyproject.toml) provide the supporting context for `tba-protocol-webauthn`. The [README policy](https://github.com/groupsum/readme-standards/blob/master/docs/outline.md) defines the common document structure.

### Related Packages

Declared local runtime dependencies:

- [tba-capability-public-key-authentication](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-public-key-authentication/README.md)
- [tba-capability-public-key-registration](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-public-key-registration/README.md)
- [tba-concrete-cose](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-cose/README.md)
- [tba-contracts-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-identity/README.md)
- [tba-primitives-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/000-primitives/tba-primitives-identity/README.md)
- [tba-provider-cose-cryptography](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-cose-cryptography/README.md)

Direct downstream consumers:

- [tba-auth](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-auth/README.md)
- [tba-profile-fido2-server](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-fido2-server/README.md)
- [tba-router-webauthn](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-webauthn/README.md)
- [tba-runtime-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity/README.md)

### Project Links

<!-- readme-standards:begin project-links -->
- [Documentation](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/050-protocols/tba-protocol-webauthn#readme)
- [Homepage](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/050-protocols/tba-protocol-webauthn#readme)
- [Issues](https://github.com/tigrbl/tigrbl_auth/issues)
- [PyPI](https://pypi.org/project/tba-protocol-webauthn/)
- [Repository](https://github.com/tigrbl/tigrbl_auth)
- [Source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/050-protocols/tba-protocol-webauthn)
- [pypi: tba-protocol-webauthn](https://pypi.org/project/tba-protocol-webauthn/)
<!-- readme-standards:end project-links -->

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/050-protocols/tba-protocol-webauthn)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-webauthn/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-webauthn/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-webauthn/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-protocol-webauthn/)

---

## Contributing

### How to Contribute

Follow the [contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md) and include a focused example or regression for changes to `tba-protocol-webauthn`. Keep package behavior, its documented boundary, and its tests aligned.

### Development Setup

Work from the `pkgs/050-protocols/tba-protocol-webauthn` checkout. Synchronize its declared development environment with uv, then run the relevant package tests and `python -m pytest docs/readme/test_examples.py`. The repository’s dedicated README job installs `readme-standards==0.1.1` without resolving unrelated runtime packages.

### Notes for Maintainers

Edit authored prose directly in this `tba-protocol-webauthn` README. Update source examples in `docs/readme/`, then run `readme-standards render --root . --write` from the package directory and review the diff. Required headings and generated blocks come from package-guide-v1.

---

## Governance

### Ownership and Decision Making

Changes to `tba-protocol-webauthn` follow the maintainer review process of [tigrbl/tigrbl_auth](https://github.com/tigrbl/tigrbl_auth) and its contribution guide. Author attribution remains in the [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-webauthn/pyproject.toml); this README does not assign new publishing or administrative authority.

### Standards and Policies

`tba-protocol-webauthn` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `050-protocols` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

### Lifecycle and Migration

The `tba-protocol-webauthn` source version is `0.4.0.dev3`. This change standardizes documentation and adds a development-only gate; it does not publish a new runtime version or declare a previously unpublished package released. Preserve explicit deprecation and replacement instructions where present.

---

## License and Attribution

### License

<!-- readme-standards:begin license -->
Licensed under `Apache-2.0`. See [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-webauthn/LICENSE).
<!-- readme-standards:end license -->

### Notices

<!-- readme-standards:begin notices -->
See [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-webauthn/NOTICE) for attribution.
<!-- readme-standards:end notices -->
