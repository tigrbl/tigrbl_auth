# tba-bases-security-trust-domain

<!-- readme-standards:begin branding -->
<p align="center"><a href="https://github.com/tigrbl/tigrbl_auth"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="300"></a></p>
<p align="center"><strong>tba-bases-security-trust-domain</strong></p>
<p align="center">Draft domain base classes composed from tigrbl security/trust contracts.</p>
<p align="center">
<a href="https://pypi.org/project/tba-bases-security-trust-domain/"><img alt="pypi: tba-bases-security-trust-domain" src="https://img.shields.io/pypi/v/tba-bases-security-trust-domain"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-security-trust-domain/pyproject.toml"><img alt="Source version: 0.1.1.dev1" src="https://img.shields.io/static/v1?label=Source%20version&amp;message=0.1.1.dev1&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-security-trust-domain/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/static/v1?label=Python&amp;message=%3E%3D3.10%2C%3C3.16&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-security-trust-domain/pyproject.toml"><img alt="Layer: 005-bases" src="https://img.shields.io/static/v1?label=Layer&amp;message=005-bases&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-security-trust-domain/README.md#lifecycle-and-migration"><img alt="Lifecycle: active" src="https://img.shields.io/static/v1?label=Lifecycle&amp;message=active&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-security-trust-domain/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/static/v1?label=License&amp;message=Apache-2.0&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-security-trust-domain/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/static/v1?label=Notice&amp;message=attribution&amp;color=525252"></a>
</p>
<p align="center">
<a href="https://pypi.org/project/tba-bases-security-trust-domain/"><img alt="Monthly PyPI downloads: tba-bases-security-trust-domain" src="https://img.shields.io/pypi/dm/tba-bases-security-trust-domain"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-security-trust-domain/README.md"><img alt="README hits: tba-bases-security-trust-domain" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/pkgs/005-bases/tba-bases-security-trust-domain/README.md.svg?label=README%20hits"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="README standards: CI gate" src="https://img.shields.io/static/v1?label=README%20standards&amp;message=CI%20gate&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-security-trust-domain/docs/readme/test_examples.py"><img alt="Tests: example source" src="https://img.shields.io/static/v1?label=Tests&amp;message=example%20source&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-security-trust-domain/README.md#certification-status"><img alt="Certification: not certified" src="https://img.shields.io/static/v1?label=Certification&amp;message=not%20certified&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/tools/readme/POLICY.md"><img alt="Governance: repository policy" src="https://img.shields.io/static/v1?label=Governance&amp;message=repository%20policy&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="Evidence: source and CI" src="https://img.shields.io/static/v1?label=Evidence&amp;message=source%20and%20CI&amp;color=525252"></a>
</p>
<p align="center"><a href="#overview">Overview</a> · <a href="#installation">Installation</a> · <a href="#quick-start">Quick Start</a> · <a href="#usage">Usage</a> · <a href="#public-api-and-import-surfaces">API</a> · <a href="#contributing">Contributing</a> · <a href="#governance">Governance</a> · <a href="#license">License</a></p>
<!-- readme-standards:end branding -->

---

## Overview

### Summary

Draft standalone package with abstract domain base classes composed from the horizontal security/trust contracts.

These bases are intentionally thin. They encode domain composition only; concrete providers still own runtime behavior.

- Package: `tba-bases-security-trust-domain`
- Layer: `005-bases`
- Responsibility: Draft domain base classes composed from tigrbl security/trust contracts.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-security-trust-domain/src/tba_bases_security_trust_domain/__init__.py).
- Distribution: Python package on PyPI.

### Why This Package

`tba-bases-security-trust-domain` isolates this responsibility: Draft domain base classes composed from tigrbl security/trust contracts. Its [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-security-trust-domain/src/tba_bases_security_trust_domain/__init__.py) exposes `AcrEvaluatorBase`, `AmrEvaluatorBase`, `ArtifactCodecBase`, `ArtifactIssuerBase`, `ArtifactOpenerBase`, `ArtifactVerifierBase`, `AttestationProviderBase`, `CapabilityProviderBase`, `CertificateDomainBase`, `CertificatePathValidatorBase`, `CertificateServiceDomainBase`, `CipherPolicyDomainBase`, `ClaimsProviderBase`, `ConfirmationBindingValidatorBase`, `CryptoDomainBase`, allowing consumers to select this package without treating adjacent packages as part of its public contract.

### When to Use

Choose `tba-bases-security-trust-domain` for this responsibility: Draft domain base classes composed from tigrbl security/trust contracts. Its `005-bases` placement keeps reusable component bases separate from deployment composition or implicit provider selection.

### Features

- `SigningDomainBase`: Domain composition for detached or attached signing providers.
- `SigningProviderBase`: Base for provider-neutral signing and signature verification.
- `ProofOfPossessionDomainBase`: Domain composition for request-bound proof-of-possession providers.
- `PkceVerifierBase`: Base for PKCE challenge verification providers.
- `TokenServiceDomainBase`: Token service base with claim-aware convenience methods.
- `TokenDomainBase`: Backward-compatible alias for token service domain composition.
- `CertificateServiceDomainBase`: Certificate/CSR service base with X.509-aware convenience methods.
- `CertificateDomainBase`: Backward-compatible alias for certificate service domain composition.

### Non-Goals

`tba-bases-security-trust-domain` does not take ownership of deployment composition or implicit provider selection.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

---

## Getting Started

### Prerequisites

Python `>=3.10,<3.16` is required. The [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-security-trust-domain/pyproject.toml) declares runtime dependencies including `tba-bases-certificate`, `tba-bases-capability`, `tba-bases-did`, `tba-bases-encryption`, `tba-bases-claim`, `tba-contracts-identity`, `tba-bases-identity`, `tba-bases-authentication-context`, `tba-bases-protected-artifact`, `tba-contracts-security-trust`, `tba-bases-key`, `tba-bases-proof-of-possession`. Read the example’s inputs and service requirements before execution.

### Installation

Install the selected PyPI release of `tba-bases-security-trust-domain`:

```bash
uv pip install tba-bases-security-trust-domain
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/005-bases/tba-bases-security-trust-domain
```

#### uv

<!-- readme-standards:begin installation.uv -->
```bash
uv add tba-bases-security-trust-domain
```
<!-- readme-standards:end installation.uv -->

#### pip

<!-- readme-standards:begin installation.pip -->
```bash
python -m pip install tba-bases-security-trust-domain
```
<!-- readme-standards:end installation.pip -->

#### Poetry

<!-- readme-standards:begin installation.poetry -->
```bash
poetry add tba-bases-security-trust-domain
```
<!-- readme-standards:end installation.poetry -->

### Quick Start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.


```bash
uv run --isolated --no-project --python 3.12 --with "tba-bases-security-trust-domain==0.1.1.dev1" python quickstart.py
```

The import and assertion succeed when the ArtifactCodecBase entry point is available.

#### Example

<!-- readme-standards:begin example.quick-start -->
Source: [docs/readme/quick_start.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-security-trust-domain/docs/readme/quick_start.py).

```python
from tba_bases_security_trust_domain import ArtifactCodecBase

assert callable(ArtifactCodecBase)
```
<!-- readme-standards:end example.quick-start -->

#### Expected Result

The example demonstrates the documented `tba-bases-security-trust-domain` source boundary or workflow. Complete its required configuration first. README CI checks the maintained source’s syntax and declarations; it does not claim that external services or the application workflow were exercised.

---

## Usage

### Common Workflows

<!-- readme-standards:begin example.usage -->
Source: [docs/readme/usage.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-security-trust-domain/docs/readme/usage.py).

```python
from tba_bases_security_trust_domain import ArtifactCodecBase

assert callable(ArtifactCodecBase)
```
<!-- readme-standards:end example.usage -->

The following public-entry-point example belongs to `tba-bases-security-trust-domain`. Draft domain base classes composed from tigrbl security/trust contracts. Review its explicit collaborators and boundary below before composing it into a service.

### Configuration

Configure `tba-bases-security-trust-domain` through the APIs in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-security-trust-domain/src/tba_bases_security_trust_domain/__init__.py); its [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-security-trust-domain/pyproject.toml) describes installation requirements, not an implicit service configuration. No additional package-global configuration contract is inferred from dependencies.

### Error Handling

The inspected `tba-bases-security-trust-domain` source does not establish a package-wide exception hierarchy. Preserve errors from its declared dependencies and validate inputs using the specific public contract in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-security-trust-domain/src/tba_bases_security_trust_domain/__init__.py).

### Best Practices

Use the explicit `tba-bases-security-trust-domain` imports documented below and keep collaborator configuration with the caller. Run the package’s relevant tests after changing `AcrEvaluatorBase`, `AmrEvaluatorBase`, `ArtifactCodecBase`, `ArtifactIssuerBase`, `ArtifactOpenerBase`, `ArtifactVerifierBase`, `AttestationProviderBase`, `CapabilityProviderBase`, `CertificateDomainBase`, `CertificatePathValidatorBase`, `CertificateServiceDomainBase`, `CipherPolicyDomainBase`, `ClaimsProviderBase`, `ConfirmationBindingValidatorBase`, `CryptoDomainBase`; an import or successful installation alone does not establish its runtime guarantees.

---

## Package Boundary

### What It Owns

`tba-bases-security-trust-domain` belongs to `005-bases` and owns reusable component bases: Draft domain base classes composed from tigrbl security/trust contracts.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-security-trust-domain/src/tba_bases_security_trust_domain/__init__.py). Public exports include `ArtifactCodecBase`, `ArtifactIssuerBase`, `ArtifactOpenerBase`, `ArtifactVerifierBase`, `AcrEvaluatorBase`, `AmrEvaluatorBase`, `AttestationProviderBase`, `CapabilityProviderBase`, `CertificateDomainBase`, `CertificatePathValidatorBase`, `CertificateServiceDomainBase`, `CipherPolicyDomainBase`.

Keep deployment composition or implicit provider selection in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

### Public API and Import Surfaces

Import namespace: `tba_bases_security_trust_domain`.

Source-declared exports or types: `AcrEvaluatorBase`, `AmrEvaluatorBase`, `ArtifactCodecBase`, `ArtifactIssuerBase`, `ArtifactOpenerBase`, `ArtifactVerifierBase`, `AttestationProviderBase`, `CapabilityProviderBase`, `CertificateDomainBase`, `CertificatePathValidatorBase`, `CertificateServiceDomainBase`, `CipherPolicyDomainBase`, `ClaimsProviderBase`, `ConfirmationBindingValidatorBase`, `CryptoDomainBase`.

Inspect [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-security-trust-domain/src/tba_bases_security_trust_domain/__init__.py) for exact signatures; this inventory does not designate every internal module as stable.

### Entry Points

<!-- readme-standards:begin entry-points -->
This package declares no command-line, GUI, or plugin entry points in its manifest.
<!-- readme-standards:end entry-points -->

### Injected Dependencies

The [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-security-trust-domain/src/tba_bases_security_trust_domain/__init__.py) for `tba-bases-security-trust-domain` does not declare an explicit service-constructor or keyword-only factory hook in the inspected source. Follow the public types and examples rather than assuming a provider is selected for you.

Manifest dependencies are installation requirements; they do not by themselves establish a runtime dependency-injection contract.

### Protocol Consumers

Direct consumers in this checkout’s package manifests include `tba-provider-security-oidc-federation`, `tba-provider-security-webfinger`, `tba-workspace`. These edges describe declared dependencies, not protocol-conformance evidence.

### Extensions

For `tba-bases-security-trust-domain`, use the source-declared public interfaces (`AcrEvaluatorBase`, `AmrEvaluatorBase`, `ArtifactCodecBase`, `ArtifactIssuerBase`, `ArtifactOpenerBase`, `ArtifactVerifierBase`, `AttestationProviderBase`, `CapabilityProviderBase`, `CertificateDomainBase`, `CertificatePathValidatorBase`, `CertificateServiceDomainBase`, `CipherPolicyDomainBase`, `ClaimsProviderBase`, `ConfirmationBindingValidatorBase`, `CryptoDomainBase`) when composing or extending behavior. Its entry-point section below is authoritative for registered plugins; no additional extension loader is inferred from the package name.

---

## Operations and Readiness

### Operational Requirements

`tba-bases-security-trust-domain` exposes reusable component bases. Public operations found in its source:

- `SigningProviderBase.sign` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-security-trust-domain/src/tba_bases_security_trust_domain/bases.py).
- `SigningProviderBase.verify_signature` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-security-trust-domain/src/tba_bases_security_trust_domain/bases.py).
- `PkceVerifierBase.verify_challenge` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-security-trust-domain/src/tba_bases_security_trust_domain/bases.py).
- `TokenServiceDomainBase.issue_token` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-security-trust-domain/src/tba_bases_security_trust_domain/bases.py).
- `TokenServiceDomainBase.verify_token` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-security-trust-domain/src/tba_bases_security_trust_domain/bases.py).
- `TokenServiceDomainBase.export_verification_keys` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-security-trust-domain/src/tba_bases_security_trust_domain/bases.py).
- `CertificateServiceDomainBase.create_csr` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-security-trust-domain/src/tba_bases_security_trust_domain/bases.py).
- `CertificateServiceDomainBase.issue_certificate` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-security-trust-domain/src/tba_bases_security_trust_domain/bases.py).
- `CertificateServiceDomainBase.verify_certificate` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-security-trust-domain/src/tba_bases_security_trust_domain/bases.py).
- `CertificateServiceDomainBase.parse_certificate` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-security-trust-domain/src/tba_bases_security_trust_domain/bases.py).
- `KeyProviderDomainBase.resolve_key` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-security-trust-domain/src/tba_bases_security_trust_domain/bases.py).
- `KeyProviderDomainBase.create_key` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-security-trust-domain/src/tba_bases_security_trust_domain/bases.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

### Health and Observability

This README does not establish a standalone health endpoint for `tba-bases-security-trust-domain`. Observe the concrete caller’s results, exceptions, and existing test reports. An application that embeds this package must define its own health and telemetry contract.

### Security and Resource Limits

Apply the input, credential, and resource constraints implemented in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-security-trust-domain/src/tba_bases_security_trust_domain/__init__.py). The `tba-bases-security-trust-domain` README gate is a documentation check, not a security review or a substitute for the implementation’s limits and caller authorization.

### Compatibility

This source version of `tba-bases-security-trust-domain` declares Python `>=3.10,<3.16`. Consult its dependency constraints before upgrading. Source-version and registry-version badges have separate meanings; this migration makes no additional platform or interoperability certification claim.

---

## Verification

### Tests

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-security-trust-domain/src/tba_bases_security_trust_domain/__init__.py).

### Certification Status

No external certification is asserted for `tba-bases-security-trust-domain` by this documentation migration. README conformance, example syntax, runtime tests, and protocol or security certification are distinct evidence scopes.

### Evidence

The [README standards CI](https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml) records mechanical documentation results for its tested commit. The [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-security-trust-domain/src/tba_bases_security_trust_domain/__init__.py) and example sources support the package-boundary description; external runtime behavior requires its own test evidence.

---

## FAQ

### Why

**Why select this package?** `tba-bases-security-trust-domain` provides draft domain base classes composed from tigrbl security/trust contracts; use its own API boundary rather than assuming neighboring packages are bundled or configured automatically.

### How

**How do I start?** Install or synchronize the environment under Getting Started, follow the maintained example for `tba-bases-security-trust-domain`, and consult [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-security-trust-domain/src/tba_bases_security_trust_domain/__init__.py) for the exact types and signatures involved.

### When

**When should I validate an upgrade?** Recheck `tba-bases-security-trust-domain` whenever its source version, declared collaborators, configuration, or caller changes. Run relevant behavioral tests in addition to the README gate before promotion.

---

## Documentation and Related Packages

### More Documentation

The [repository contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md), [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-security-trust-domain/src/tba_bases_security_trust_domain/__init__.py), and [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-security-trust-domain/pyproject.toml) provide the supporting context for `tba-bases-security-trust-domain`. The [README policy](https://github.com/groupsum/readme-standards/blob/master/docs/outline.md) defines the common document structure.

### Related Packages

Declared local runtime dependencies:

- [tba-bases-authentication-context](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-authentication-context/README.md)
- [tba-bases-capability](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-capability/README.md)
- [tba-bases-certificate](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-certificate/README.md)
- [tba-bases-claim](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-claim/README.md)
- [tba-bases-did](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-did/README.md)
- [tba-bases-encryption](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-encryption/README.md)
- [tba-bases-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-identity/README.md)
- [tba-bases-key](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-key/README.md)
- [tba-bases-proof-of-possession](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-proof-of-possession/README.md)
- [tba-bases-protected-artifact](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-protected-artifact/README.md)
- [tba-bases-signing](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-signing/README.md)
- [tba-bases-token-introspection](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-token-introspection/README.md)
- [tba-bases-trust](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-trust/README.md)
- [tba-bases-workload-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-workload-identity/README.md)
- [tba-contracts-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-identity/README.md)
- [tba-contracts-security-trust](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-security-trust/README.md)

Direct downstream consumers:

- [tba-provider-security-oidc-federation](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-security-oidc-federation/README.md)
- [tba-provider-security-webfinger](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-security-webfinger/README.md)

### Project Links

<!-- readme-standards:begin project-links -->
- [Documentation](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/005-bases/tba-bases-security-trust-domain#readme)
- [Homepage](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/005-bases/tba-bases-security-trust-domain#readme)
- [Issues](https://github.com/tigrbl/tigrbl_auth/issues)
- [PyPI](https://pypi.org/project/tba-bases-security-trust-domain/)
- [Repository](https://github.com/tigrbl/tigrbl_auth)
- [Source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/005-bases/tba-bases-security-trust-domain)
- [pypi: tba-bases-security-trust-domain](https://pypi.org/project/tba-bases-security-trust-domain/)
<!-- readme-standards:end project-links -->

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/005-bases/tba-bases-security-trust-domain)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-security-trust-domain/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-security-trust-domain/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-security-trust-domain/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-bases-security-trust-domain/)

---

## Contributing

### How to Contribute

Follow the [contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md) and include a focused example or regression for changes to `tba-bases-security-trust-domain`. Keep package behavior, its documented boundary, and its tests aligned.

### Development Setup

Work from the `pkgs/005-bases/tba-bases-security-trust-domain` checkout. Synchronize its declared development environment with uv, then run the relevant package tests and `python -m pytest docs/readme/test_examples.py`. The repository’s dedicated README job installs `readme-standards==0.1.1` without resolving unrelated runtime packages.

### Notes for Maintainers

Edit authored prose directly in this `tba-bases-security-trust-domain` README. Update source examples in `docs/readme/`, then run `readme-standards render --root . --write` from the package directory and review the diff. Required headings and generated blocks come from package-guide-v1.

---

## Governance

### Ownership and Decision Making

Changes to `tba-bases-security-trust-domain` follow the maintainer review process of [tigrbl/tigrbl_auth](https://github.com/tigrbl/tigrbl_auth) and its contribution guide. Author attribution remains in the [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-security-trust-domain/pyproject.toml); this README does not assign new publishing or administrative authority.

### Standards and Policies

`tba-bases-security-trust-domain` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `005-bases` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

### Lifecycle and Migration

The `tba-bases-security-trust-domain` source version is `0.1.1.dev1`. This change standardizes documentation and adds a development-only gate; it does not publish a new runtime version or declare a previously unpublished package released. Preserve explicit deprecation and replacement instructions where present.

---

## License and Attribution

### License

<!-- readme-standards:begin license -->
Licensed under `Apache-2.0`. See [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-security-trust-domain/LICENSE).
<!-- readme-standards:end license -->

### Notices

<!-- readme-standards:begin notices -->
See [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-security-trust-domain/NOTICE) for attribution.
<!-- readme-standards:end notices -->
