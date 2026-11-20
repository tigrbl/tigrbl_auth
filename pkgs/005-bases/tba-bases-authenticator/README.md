# tba-bases-authenticator

<!-- readme-standards:begin branding -->
<p align="center"><a href="https://github.com/tigrbl/tigrbl_auth"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="300"></a></p>
<p align="center"><strong>tba-bases-authenticator</strong></p>
<p align="center">Authenticator base classes and mixins for the TBA package suite.</p>
<p align="center">
<a href="https://pypi.org/project/tba-bases-authenticator/"><img alt="pypi: tba-bases-authenticator" src="https://img.shields.io/pypi/v/tba-bases-authenticator"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-authenticator/pyproject.toml"><img alt="Source version: 0.1.1.dev1" src="https://img.shields.io/static/v1?label=Source%20version&amp;message=0.1.1.dev1&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-authenticator/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/static/v1?label=Python&amp;message=%3E%3D3.10%2C%3C3.16&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-authenticator/pyproject.toml"><img alt="Layer: 005-bases" src="https://img.shields.io/static/v1?label=Layer&amp;message=005-bases&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-authenticator/README.md#lifecycle-and-migration"><img alt="Lifecycle: active" src="https://img.shields.io/static/v1?label=Lifecycle&amp;message=active&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-authenticator/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/static/v1?label=License&amp;message=Apache-2.0&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-authenticator/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/static/v1?label=Notice&amp;message=attribution&amp;color=525252"></a>
</p>
<p align="center">
<a href="https://pypi.org/project/tba-bases-authenticator/"><img alt="Monthly PyPI downloads: tba-bases-authenticator" src="https://img.shields.io/pypi/dm/tba-bases-authenticator"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-authenticator/README.md"><img alt="README hits: tba-bases-authenticator" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/pkgs/005-bases/tba-bases-authenticator/README.md.svg?label=README%20hits"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="README standards: CI gate" src="https://img.shields.io/static/v1?label=README%20standards&amp;message=CI%20gate&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-authenticator/docs/readme/test_examples.py"><img alt="Tests: example source" src="https://img.shields.io/static/v1?label=Tests&amp;message=example%20source&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-authenticator/README.md#certification-status"><img alt="Certification: not certified" src="https://img.shields.io/static/v1?label=Certification&amp;message=not%20certified&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/tools/readme/POLICY.md"><img alt="Governance: repository policy" src="https://img.shields.io/static/v1?label=Governance&amp;message=repository%20policy&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="Evidence: source and CI" src="https://img.shields.io/static/v1?label=Evidence&amp;message=source%20and%20CI&amp;color=525252"></a>
</p>
<p align="center"><a href="#overview">Overview</a> · <a href="#installation">Installation</a> · <a href="#quick-start">Quick Start</a> · <a href="#usage">Usage</a> · <a href="#public-api-and-import-surfaces">API</a> · <a href="#contributing">Contributing</a> · <a href="#governance">Governance</a> · <a href="#license">License</a></p>
<!-- readme-standards:end branding -->

---

## Overview

### Summary

Build authenticator providers with shared metadata, evidence, and challenge interfaces.

- Package: `tba-bases-authenticator`
- Layer: `005-bases`
- Responsibility: Authenticator base classes and mixins for the TBA package suite.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-authenticator/src/tba_bases_authenticator/__init__.py).
- Distribution: Python package on PyPI.

### Why This Package

`tba-bases-authenticator` isolates this responsibility: Authenticator base classes and mixins for the TBA package suite. Its [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-authenticator/src/tba_bases_authenticator/__init__.py) exposes `AalEvidenceMixin`, `AmrEmitterMixin`, `AuthenticatorBase`, `AuthenticatorEvidenceEvaluatorBase`, `ChallengeAuthenticatorBase`, `ChallengeLifecycleMixin`, `CredentialKindMixin`, `CredentialLookupMixin`, `HardwareKeyProtectionEvaluatorBase`, `OtpVerifierMixin`, `PhishingResistanceEvaluatorBase`, `PhishingResistanceMixin`, `RecoveryCodeVerifierMixin`, `RemoteIntrospectionMixin`, `SecretVerifierMixin`, allowing consumers to select this package without treating adjacent packages as part of its public contract.

### When to Use

Extend `AuthenticatorBase` for a single ceremony or `ChallengeAuthenticatorBase` for start/finish flows. Supply the actual authentication behavior in your provider implementation. Use a layer 20 provider if you need a ready-made authenticator.

### Features

- `AuthenticatorBase`: Base for a single authenticator ceremony or proof verifier.
- `ChallengeAuthenticatorBase`: Base for authenticators that require a start/finish challenge ceremony.
- `AuthenticatorEvidenceEvaluatorBase`: declared in src/tba_bases_authenticator/evidence.py
- `PhishingResistanceEvaluatorBase`: declared in src/tba_bases_authenticator/evidence.py
- `HardwareKeyProtectionEvaluatorBase`: declared in src/tba_bases_authenticator/evidence.py
- `AmrEmitterMixin`: declared in src/tba_bases_authenticator/mixins.py
- `CredentialKindMixin`: declared in src/tba_bases_authenticator/mixins.py
- `CredentialLookupMixin`: declared in src/tba_bases_authenticator/mixins.py

### Non-Goals

`tba-bases-authenticator` does not take ownership of deployment composition or implicit provider selection.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

---

## Getting Started

### Prerequisites

Python `>=3.10,<3.16` is required. The [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-authenticator/pyproject.toml) declares runtime dependencies including `tba-contracts-identity`, `tba-contracts-security-trust`. Read the example’s inputs and service requirements before execution.

### Installation

Install the selected PyPI release of `tba-bases-authenticator`:

```bash
uv pip install tba-bases-authenticator
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/005-bases/tba-bases-authenticator
```

#### uv

<!-- readme-standards:begin installation.uv -->
```bash
uv add tba-bases-authenticator
```
<!-- readme-standards:end installation.uv -->

#### pip

<!-- readme-standards:begin installation.pip -->
```bash
python -m pip install tba-bases-authenticator
```
<!-- readme-standards:end installation.pip -->

#### Poetry

<!-- readme-standards:begin installation.poetry -->
```bash
poetry add tba-bases-authenticator
```
<!-- readme-standards:end installation.poetry -->

### Quick Start

Install the version used by this example.

```bash
python -m pip install "tba-bases-authenticator==0.1.1.dev1"
```

Save the following as `quickstart.py` and run `python quickstart.py`. The assertions should pass.

#### Example

<!-- readme-standards:begin example.quick-start -->
Source: [docs/readme/quick_start.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-authenticator/docs/readme/quick_start.py).

```python
from tba_bases_authenticator import AuthenticatorBase

base = AuthenticatorBase(kind="password_local", factor_class="knowledge", amr=("pwd",))
assert base.supported_amr() == ("pwd",)
assert base.metadata().challenge_based is False
```
<!-- readme-standards:end example.quick-start -->

#### Expected Result

The example demonstrates the documented `tba-bases-authenticator` source boundary or workflow. Complete its required configuration first. README CI checks the maintained source’s syntax and declarations; it does not claim that external services or the application workflow were exercised.

---

## Usage

### Common Workflows

<!-- readme-standards:begin example.usage -->
Source: [docs/readme/usage.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-authenticator/docs/readme/usage.py).

```python
from tba_bases_authenticator import AuthenticatorBase

base = AuthenticatorBase(kind="password_local", factor_class="knowledge", amr=("pwd",))
assert base.supported_amr() == ("pwd",)
assert base.metadata().challenge_based is False
```
<!-- readme-standards:end example.usage -->

The following public-entry-point example belongs to `tba-bases-authenticator`. Authenticator base classes and mixins for the TBA package suite. Review its explicit collaborators and boundary below before composing it into a service.

### Configuration

Configure `tba-bases-authenticator` through the APIs in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-authenticator/src/tba_bases_authenticator/__init__.py); its [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-authenticator/pyproject.toml) describes installation requirements, not an implicit service configuration. No additional package-global configuration contract is inferred from dependencies.

### Error Handling

The inspected `tba-bases-authenticator` source raises `ValueError`. Handle these at the calling boundary and consult the implementation for the triggering conditions.

### Best Practices

Use the explicit `tba-bases-authenticator` imports documented below and keep collaborator configuration with the caller. Run the package’s relevant tests after changing `AalEvidenceMixin`, `AmrEmitterMixin`, `AuthenticatorBase`, `AuthenticatorEvidenceEvaluatorBase`, `ChallengeAuthenticatorBase`, `ChallengeLifecycleMixin`, `CredentialKindMixin`, `CredentialLookupMixin`, `HardwareKeyProtectionEvaluatorBase`, `OtpVerifierMixin`, `PhishingResistanceEvaluatorBase`, `PhishingResistanceMixin`, `RecoveryCodeVerifierMixin`, `RemoteIntrospectionMixin`, `SecretVerifierMixin`; an import or successful installation alone does not establish its runtime guarantees.

---

## Package Boundary

### What It Owns

`tba-bases-authenticator` belongs to `005-bases` and owns reusable component bases: Authenticator base classes and mixins for the TBA package suite.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-authenticator/src/tba_bases_authenticator/__init__.py). Public exports include `AalEvidenceMixin`, `AmrEmitterMixin`, `AuthenticatorBase`, `AuthenticatorEvidenceEvaluatorBase`, `ChallengeAuthenticatorBase`, `ChallengeLifecycleMixin`, `CredentialKindMixin`, `CredentialLookupMixin`, `HardwareKeyProtectionEvaluatorBase`, `OtpVerifierMixin`, `PhishingResistanceMixin`, `PhishingResistanceEvaluatorBase`.

Keep deployment composition or implicit provider selection in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

### Public API and Import Surfaces

Import namespace: `tba_bases_authenticator`.

Source-declared exports or types: `AalEvidenceMixin`, `AmrEmitterMixin`, `AuthenticatorBase`, `AuthenticatorEvidenceEvaluatorBase`, `ChallengeAuthenticatorBase`, `ChallengeLifecycleMixin`, `CredentialKindMixin`, `CredentialLookupMixin`, `HardwareKeyProtectionEvaluatorBase`, `OtpVerifierMixin`, `PhishingResistanceEvaluatorBase`, `PhishingResistanceMixin`, `RecoveryCodeVerifierMixin`, `RemoteIntrospectionMixin`, `SecretVerifierMixin`.

Inspect [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-authenticator/src/tba_bases_authenticator/__init__.py) for exact signatures; this inventory does not designate every internal module as stable.

### Entry Points

<!-- readme-standards:begin entry-points -->
This package declares no command-line, GUI, or plugin entry points in its manifest.
<!-- readme-standards:end entry-points -->

### Injected Dependencies

Explicit construction inputs and collaborators for `tba-bases-authenticator`:

- `AuthenticatorBase` construction inputs: `kind`, `factor_class`, `credential_kind`, `amr`, `properties`, `challenge_based`, `description`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-authenticator/src/tba_bases_authenticator/bases.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

### Protocol Consumers

Direct consumers in this checkout’s package manifests include `tba-provider-authenticator-api-key-local`, `tba-provider-authenticator-client-secret-local`, `tba-provider-authenticator-dpop-proof`, `tba-provider-authenticator-federated-oidc`, `tba-provider-authenticator-mtls-client-cert`, `tba-provider-authenticator-otp-local`, `tba-provider-authenticator-password-local`, `tba-provider-authenticator-recovery-code-local`, `tba-provider-authenticator-remote-introspection`, `tba-provider-authenticator-service-key-local`, `tba-provider-authenticator-session-local`, `tba-provider-authenticator-totp-local`, `tba-workspace`. These edges describe declared dependencies, not protocol-conformance evidence.

### Extensions

For `tba-bases-authenticator`, use the source-declared public interfaces (`AalEvidenceMixin`, `AmrEmitterMixin`, `AuthenticatorBase`, `AuthenticatorEvidenceEvaluatorBase`, `ChallengeAuthenticatorBase`, `ChallengeLifecycleMixin`, `CredentialKindMixin`, `CredentialLookupMixin`, `HardwareKeyProtectionEvaluatorBase`, `OtpVerifierMixin`, `PhishingResistanceEvaluatorBase`, `PhishingResistanceMixin`, `RecoveryCodeVerifierMixin`, `RemoteIntrospectionMixin`, `SecretVerifierMixin`) when composing or extending behavior. Its entry-point section below is authoritative for registered plugins; no additional extension loader is inferred from the package name.

---

## Operations and Readiness

### Operational Requirements

`tba-bases-authenticator` exposes reusable component bases. Public operations found in its source:

- `AuthenticatorBase.metadata` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-authenticator/src/tba_bases_authenticator/bases.py).
- `AuthenticatorBase.supported_amr` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-authenticator/src/tba_bases_authenticator/bases.py).
- `AuthenticatorBase.authenticate` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-authenticator/src/tba_bases_authenticator/bases.py).
- `ChallengeAuthenticatorBase.start_challenge` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-authenticator/src/tba_bases_authenticator/bases.py).
- `ChallengeAuthenticatorBase.finish_challenge` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-authenticator/src/tba_bases_authenticator/bases.py).
- `AuthenticatorEvidenceEvaluatorBase.evaluate_evidence` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-authenticator/src/tba_bases_authenticator/evidence.py).
- `PhishingResistanceEvaluatorBase.is_phishing_resistant` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-authenticator/src/tba_bases_authenticator/evidence.py).
- `HardwareKeyProtectionEvaluatorBase.is_hardware_protected` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-authenticator/src/tba_bases_authenticator/evidence.py).
- `AmrEmitterMixin.normalize_amr` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-authenticator/src/tba_bases_authenticator/mixins.py).
- `AmrEmitterMixin.evidence` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-authenticator/src/tba_bases_authenticator/mixins.py).
- `CredentialKindMixin.expects_credential_kind` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-authenticator/src/tba_bases_authenticator/mixins.py).
- `CredentialLookupMixin.lookup_credential` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-authenticator/src/tba_bases_authenticator/mixins.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

### Health and Observability

This README does not establish a standalone health endpoint for `tba-bases-authenticator`. Observe the concrete caller’s results, exceptions, and existing test reports. An application that embeds this package must define its own health and telemetry contract.

### Security and Resource Limits

Apply the input, credential, and resource constraints implemented in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-authenticator/src/tba_bases_authenticator/__init__.py). The `tba-bases-authenticator` README gate is a documentation check, not a security review or a substitute for the implementation’s limits and caller authorization.

### Compatibility

This source version of `tba-bases-authenticator` declares Python `>=3.10,<3.16`. Consult its dependency constraints before upgrading. Source-version and registry-version badges have separate meanings; this migration makes no additional platform or interoperability certification claim.

---

## Verification

### Tests

See the [related repository tests](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-authentication/tests/unit/test_authenticator_contracts_and_providers.py) for the implementation scope covered by this example.

[Workspace and package catalog](https://github.com/tigrbl/tigrbl_auth#package-catalog) · [tba-provider-authenticator-password-local](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/020-providers/tba-provider-authenticator-password-local#readme) · [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues) · [Repository license](https://github.com/tigrbl/tigrbl_auth/blob/master/LICENSE)

### Certification Status

No external certification is asserted for `tba-bases-authenticator` by this documentation migration. README conformance, example syntax, runtime tests, and protocol or security certification are distinct evidence scopes.

### Evidence

The [README standards CI](https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml) records mechanical documentation results for its tested commit. The [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-authenticator/src/tba_bases_authenticator/__init__.py) and example sources support the package-boundary description; external runtime behavior requires its own test evidence.

---

## FAQ

### Why

**Why select this package?** `tba-bases-authenticator` provides authenticator base classes and mixins for the TBA package suite; use its own API boundary rather than assuming neighboring packages are bundled or configured automatically.

### How

**How do I start?** Install or synchronize the environment under Getting Started, follow the maintained example for `tba-bases-authenticator`, and consult [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-authenticator/src/tba_bases_authenticator/__init__.py) for the exact types and signatures involved.

### When

**When should I validate an upgrade?** Recheck `tba-bases-authenticator` whenever its source version, declared collaborators, configuration, or caller changes. Run relevant behavioral tests in addition to the README gate before promotion.

---

## Documentation and Related Packages

### More Documentation

The [repository contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md), [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-authenticator/src/tba_bases_authenticator/__init__.py), and [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-authenticator/pyproject.toml) provide the supporting context for `tba-bases-authenticator`. The [README policy](https://github.com/groupsum/readme-standards/blob/master/docs/outline.md) defines the common document structure.

### Related Packages

Declared local runtime dependencies:

- [tba-contracts-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-identity/README.md)
- [tba-contracts-security-trust](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-security-trust/README.md)

Direct downstream consumers:

- [tba-provider-authenticator-api-key-local](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-authenticator-api-key-local/README.md)
- [tba-provider-authenticator-client-secret-local](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-authenticator-client-secret-local/README.md)
- [tba-provider-authenticator-dpop-proof](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-authenticator-dpop-proof/README.md)
- [tba-provider-authenticator-federated-oidc](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-authenticator-federated-oidc/README.md)
- [tba-provider-authenticator-mtls-client-cert](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-authenticator-mtls-client-cert/README.md)
- [tba-provider-authenticator-otp-local](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-authenticator-otp-local/README.md)
- [tba-provider-authenticator-password-local](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-authenticator-password-local/README.md)
- [tba-provider-authenticator-recovery-code-local](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-authenticator-recovery-code-local/README.md)
- [tba-provider-authenticator-remote-introspection](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-authenticator-remote-introspection/README.md)
- [tba-provider-authenticator-service-key-local](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-authenticator-service-key-local/README.md)
- [tba-provider-authenticator-session-local](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-authenticator-session-local/README.md)
- [tba-provider-authenticator-totp-local](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-authenticator-totp-local/README.md)

### Project Links

<!-- readme-standards:begin project-links -->
- [Documentation](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/005-bases/tba-bases-authenticator#readme)
- [Homepage](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/005-bases/tba-bases-authenticator#readme)
- [Issues](https://github.com/tigrbl/tigrbl_auth/issues)
- [PyPI](https://pypi.org/project/tba-bases-authenticator/)
- [Repository](https://github.com/tigrbl/tigrbl_auth)
- [Source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/005-bases/tba-bases-authenticator)
- [pypi: tba-bases-authenticator](https://pypi.org/project/tba-bases-authenticator/)
<!-- readme-standards:end project-links -->

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/005-bases/tba-bases-authenticator)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-authenticator/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-authenticator/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-authenticator/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-bases-authenticator/)

---

## Contributing

### How to Contribute

Follow the [contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md) and include a focused example or regression for changes to `tba-bases-authenticator`. Keep package behavior, its documented boundary, and its tests aligned.

### Development Setup

Work from the `pkgs/005-bases/tba-bases-authenticator` checkout. Synchronize its declared development environment with uv, then run the relevant package tests and `python -m pytest docs/readme/test_examples.py`. The repository’s dedicated README job installs `readme-standards==0.1.1` without resolving unrelated runtime packages.

### Notes for Maintainers

Edit authored prose directly in this `tba-bases-authenticator` README. Update source examples in `docs/readme/`, then run `readme-standards render --root . --write` from the package directory and review the diff. Required headings and generated blocks come from package-guide-v1.

---

## Governance

### Ownership and Decision Making

Changes to `tba-bases-authenticator` follow the maintainer review process of [tigrbl/tigrbl_auth](https://github.com/tigrbl/tigrbl_auth) and its contribution guide. Author attribution remains in the [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-authenticator/pyproject.toml); this README does not assign new publishing or administrative authority.

### Standards and Policies

`tba-bases-authenticator` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `005-bases` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

### Lifecycle and Migration

The `tba-bases-authenticator` source version is `0.1.1.dev1`. This change standardizes documentation and adds a development-only gate; it does not publish a new runtime version or declare a previously unpublished package released. Preserve explicit deprecation and replacement instructions where present.

---

## License and Attribution

### License

<!-- readme-standards:begin license -->
Licensed under `Apache-2.0`. See [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-authenticator/LICENSE).
<!-- readme-standards:end license -->

### Notices

<!-- readme-standards:begin notices -->
See [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-authenticator/NOTICE) for attribution.
<!-- readme-standards:end notices -->
