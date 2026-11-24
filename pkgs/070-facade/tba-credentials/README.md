# tba-credentials

<!-- readme-standards:begin branding -->
<p align="center"><a href="https://github.com/tigrbl/tigrbl_auth"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="300"></a></p>
<p align="center"><strong>tba-credentials</strong></p>
<p align="center">Credential facade for authentication, digital, and workload credential domains in the TBA package suite.</p>
<p align="center">
<a href="https://pypi.org/project/tba-credentials/"><img alt="pypi: tba-credentials" src="https://img.shields.io/pypi/v/tba-credentials?labelColor=1E293B&amp;color=1D4ED8"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-credentials/pyproject.toml"><img alt="Source version: 0.4.0.dev3" src="https://img.shields.io/static/v1?label=Source%20version&amp;message=0.4.0.dev3&amp;labelColor=1E293B&amp;color=4338CA"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-credentials/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/static/v1?label=Python&amp;message=%3E%3D3.10%2C%3C3.16&amp;labelColor=1E293B&amp;color=0F766E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-credentials/pyproject.toml"><img alt="Layer: 070-facade" src="https://img.shields.io/static/v1?label=Layer&amp;message=070-facade&amp;labelColor=1E293B&amp;color=6D28D9"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-credentials/README.md#lifecycle-and-migration"><img alt="Lifecycle: active" src="https://img.shields.io/static/v1?label=Lifecycle&amp;message=active&amp;labelColor=1E293B&amp;color=166534"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-credentials/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/static/v1?label=License&amp;message=Apache-2.0&amp;labelColor=1E293B&amp;color=86198F"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-credentials/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/static/v1?label=Notice&amp;message=attribution&amp;labelColor=1E293B&amp;color=86198F"></a>
</p>
<p align="center">
<a href="https://pypi.org/project/tba-credentials/"><img alt="Monthly PyPI downloads: tba-credentials" src="https://img.shields.io/pypi/dm/tba-credentials?labelColor=1E293B&amp;color=0E7490"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-credentials/README.md"><img alt="README hits: tba-credentials" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/pkgs/070-facade/tba-credentials/README.md.svg?label=README%20hits&amp;labelColor=1E293B&amp;color=0E7490"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="README standards: CI gate" src="https://img.shields.io/static/v1?label=README%20standards&amp;message=CI%20gate&amp;labelColor=1E293B&amp;color=1D4ED8"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-credentials/docs/readme/test_examples.py"><img alt="Tests: example source" src="https://img.shields.io/static/v1?label=Tests&amp;message=example%20source&amp;labelColor=1E293B&amp;color=0F766E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-credentials/README.md#certification-status"><img alt="Certification: not certified" src="https://img.shields.io/static/v1?label=Certification&amp;message=not%20certified&amp;labelColor=1E293B&amp;color=92400E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/tools/readme/POLICY.md"><img alt="Governance: repository policy" src="https://img.shields.io/static/v1?label=Governance&amp;message=repository%20policy&amp;labelColor=1E293B&amp;color=4338CA"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="Evidence: source and CI" src="https://img.shields.io/static/v1?label=Evidence&amp;message=source%20and%20CI&amp;labelColor=1E293B&amp;color=6D28D9"></a>
</p>
<p align="center"><a href="#overview">Overview</a> · <a href="#installation">Installation</a> · <a href="#quick-start">Quick Start</a> · <a href="#usage">Usage</a> · <a href="#public-api-and-import-surfaces">API</a> · <a href="#contributing">Contributing</a> · <a href="#governance">Governance</a> · <a href="#license">License</a></p>
<!-- readme-standards:end branding -->

---

## Overview

### Summary

`tba-credentials` is the credential-focused facade for the TBA
package suite. It provides one stable entry point for authentication credential
lifecycle helpers plus representation-neutral digital and workload credential
contracts. Specialized packages remain the implementation owners.

- Package: `tba-credentials`
- Import root: `tba_credentials`
- Component kind: Layer-70 facade
- Use it as the curated entry point for authentication, digital, and workload credentials.
- Do not use it for authorization policy, permission decisions, or OAuth/OIDC wire semantics.
- `tigrbl-authn-credentials` and `tigrbl-identity-credentials` remain deprecated compatibility packages during the migration window.

### Why This Package

`tba-credentials` isolates this responsibility: Credential facade for authentication, digital, and workload credential domains in the TBA package suite. Its [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-credentials/src/tba_credentials/__init__.py) exposes `Credential`, `CredentialAuditAction`, `CredentialAuditEvent`, `CredentialError`, `CredentialKind`, `CredentialStateError`, `CredentialStatus`, `CredentialVerificationError`, `DpopKeyCredential`, `IssuedCredential`, `MtlsCertificateCredential`, `ProofBinding`, `consume_one_time_credential`, `create_api_key_credential`, `create_client_secret_credential`, allowing consumers to select this package without treating adjacent packages as part of its public contract.

### When to Use

Choose `tba-credentials` for this responsibility: Credential facade for authentication, digital, and workload credential domains in the TBA package suite. Its `070-facade` placement keeps curated public entry points separate from moving implementation ownership out of focused packages.

### Features

- `AuthError`: declared in src/tba_credentials/backends.py
- `PasswordBackend`: declared in src/tba_credentials/backends.py
- `ApiKeyBackend`: declared in src/tba_credentials/backends.py

### Non-Goals

`tba-credentials` does not take ownership of moving implementation ownership out of focused packages.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

---

## Getting Started

### Prerequisites

Python `>=3.10,<3.16` is required. The [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-credentials/pyproject.toml) declares runtime dependencies including `tba-provider-secret-hashing-bcrypt`, `tba-concrete-credential-api-key`, `tba-concrete-credential-client-secret`, `tba-concrete-credential-dpop-key`, `tba-concrete-credential-mfa`, `tba-concrete-credential-mtls-certificate`, `tba-concrete-credential-passkey`, `tba-concrete-credential-password`, `tba-concrete-credential-password-reset`, `tba-concrete-credential-service-key`, `tba-provider-identity-jose`, `tba-contracts-identity`. Read the example’s inputs and service requirements before execution.

### Installation

```bash
pip install tba-credentials
# or
uv add tba-credentials
```

Install the current `tba-credentials` source checkout when working ahead of a PyPI release:

```bash
uv pip install ./pkgs/070-facade/tba-credentials
```

#### uv

<!-- readme-standards:begin installation.uv -->
```bash
uv add tba-credentials
```
<!-- readme-standards:end installation.uv -->

#### pip

<!-- readme-standards:begin installation.pip -->
```bash
python -m pip install tba-credentials
```
<!-- readme-standards:end installation.pip -->

#### Poetry

<!-- readme-standards:begin installation.poetry -->
```bash
poetry add tba-credentials
```
<!-- readme-standards:end installation.poetry -->

### Quick Start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.


```bash
uv run --isolated --no-project --python 3.12 --with "tba-credentials==0.4.0.dev3" python quickstart.py
```

The import and assertion succeed when the Credential entry point is available.

#### Example

<!-- readme-standards:begin example.quick-start -->
Source: [docs/readme/quick_start.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-credentials/docs/readme/quick_start.py).

```python
from tba_credentials import Credential

assert callable(Credential)
```
<!-- readme-standards:end example.quick-start -->

#### Expected Result

The example demonstrates the documented `tba-credentials` source boundary or workflow. Complete its required configuration first. README CI checks the maintained source’s syntax and declarations; it does not claim that external services or the application workflow were exercised.

---

## Usage

### Common Workflows

<!-- readme-standards:begin example.usage -->
Source: [docs/readme/usage.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-credentials/docs/readme/usage.py).

```python
from tba_credentials import (
    CredentialKind,
    create_password_credential,
    verify_credential,
)
from tba_credentials import digital, workload

credential = create_password_credential("subject:alice", "correct horse battery staple")
assert credential.kind is CredentialKind.PASSWORD
assert verify_credential(credential, "correct horse battery staple")
```
<!-- readme-standards:end example.usage -->

### Configuration

Configure `tba-credentials` through the APIs in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-credentials/src/tba_credentials/__init__.py); its [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-credentials/pyproject.toml) describes installation requirements, not an implicit service configuration. No additional package-global configuration contract is inferred from dependencies.

### Error Handling

The inspected `tba-credentials` source raises `AuthError`, `CredentialStateError`, `CredentialVerificationError`, `ValueError`. Handle these at the calling boundary and consult the implementation for the triggering conditions.

### Best Practices

Use the explicit `tba-credentials` imports documented below and keep collaborator configuration with the caller. Run the package’s relevant tests after changing `Credential`, `CredentialAuditAction`, `CredentialAuditEvent`, `CredentialError`, `CredentialKind`, `CredentialStateError`, `CredentialStatus`, `CredentialVerificationError`, `DpopKeyCredential`, `IssuedCredential`, `MtlsCertificateCredential`, `ProofBinding`, `consume_one_time_credential`, `create_api_key_credential`, `create_client_secret_credential`; an import or successful installation alone does not establish its runtime guarantees.

---

## Package Boundary

### What It Owns

- Authentication credential construction, verification, rotation, and revocation helpers
- Representation-neutral digital credential contracts under `tba_credentials.digital`
- Protocol-neutral workload credential contracts under `tba_credentials.workload`
- Curated imports only; concrete, provider, capability, storage, and protocol packages retain ownership

This facade does not define a secret-hash encoding or provide durable credential
storage. Shared-secret hashing is delegated to the bcrypt provider; durable
credential and audit state belongs to layers 01 and 30.

### Public API and Import Surfaces

Import namespace: `tba_credentials`.

Source-declared exports or types: `Credential`, `CredentialAuditAction`, `CredentialAuditEvent`, `CredentialError`, `CredentialKind`, `CredentialStateError`, `CredentialStatus`, `CredentialVerificationError`, `DpopKeyCredential`, `IssuedCredential`, `MtlsCertificateCredential`, `ProofBinding`, `consume_one_time_credential`, `create_api_key_credential`, `create_client_secret_credential`.

Inspect [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-credentials/src/tba_credentials/__init__.py) for exact signatures; this inventory does not designate every internal module as stable.

### Entry Points

<!-- readme-standards:begin entry-points -->
This package declares no command-line, GUI, or plugin entry points in its manifest.
<!-- readme-standards:end entry-points -->

### Injected Dependencies

Explicit construction inputs and collaborators for `tba-credentials`:

- `issue_shared_secret` construction inputs: `secret`, `public_id`, `ttl`, `metadata`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-credentials/src/tba_credentials/lifecycle.py).
- `create_password_reset_credential` construction inputs: `ttl`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-credentials/src/tba_credentials/lifecycle.py).
- `create_api_key_credential` construction inputs: `public_id`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-credentials/src/tba_credentials/lifecycle.py).
- `create_service_key_credential` construction inputs: `public_id`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-credentials/src/tba_credentials/lifecycle.py).
- `create_client_secret_credential` construction inputs: `public_id`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-credentials/src/tba_credentials/lifecycle.py).
- `create_mfa_factor_credential` construction inputs: `factor_type`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-credentials/src/tba_credentials/lifecycle.py).
- `create_passkey_credential` construction inputs: `credential_id`, `public_key`, `sign_count`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-credentials/src/tba_credentials/lifecycle.py).
- `verify_credential` construction inputs: `now`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-credentials/src/tba_credentials/lifecycle.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

### Protocol Consumers

Direct consumers in this checkout’s package manifests include `tba-auth`, `tba-workspace`. These edges describe declared dependencies, not protocol-conformance evidence.

### Extensions

For `tba-credentials`, use the source-declared public interfaces (`Credential`, `CredentialAuditAction`, `CredentialAuditEvent`, `CredentialError`, `CredentialKind`, `CredentialStateError`, `CredentialStatus`, `CredentialVerificationError`, `DpopKeyCredential`, `IssuedCredential`, `MtlsCertificateCredential`, `ProofBinding`, `consume_one_time_credential`, `create_api_key_credential`, `create_client_secret_credential`) when composing or extending behavior. Its entry-point section below is authoritative for registered plugins; no additional extension loader is inferred from the package name.

---

## Operations and Readiness

### Operational Requirements

`tba-credentials` exposes curated public entry points. Public operations found in its source:

- `new_credential_id` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-credentials/src/tba_credentials/lifecycle.py).
- `utc_now` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-credentials/src/tba_credentials/lifecycle.py).
- `hash_secret` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-credentials/src/tba_credentials/lifecycle.py).
- `verify_secret` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-credentials/src/tba_credentials/lifecycle.py).
- `issue_shared_secret` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-credentials/src/tba_credentials/lifecycle.py).
- `create_password_credential` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-credentials/src/tba_credentials/lifecycle.py).
- `create_password_reset_credential` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-credentials/src/tba_credentials/lifecycle.py).
- `create_api_key_credential` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-credentials/src/tba_credentials/lifecycle.py).
- `create_service_key_credential` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-credentials/src/tba_credentials/lifecycle.py).
- `create_client_secret_credential` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-credentials/src/tba_credentials/lifecycle.py).
- `create_mfa_factor_credential` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-credentials/src/tba_credentials/lifecycle.py).
- `create_passkey_credential` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-credentials/src/tba_credentials/lifecycle.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

### Health and Observability

This README does not establish a standalone health endpoint for `tba-credentials`. Observe the concrete caller’s results, exceptions, and existing test reports. An application that embeds this package must define its own health and telemetry contract.

### Security and Resource Limits

Apply the input, credential, and resource constraints implemented in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-credentials/src/tba_credentials/__init__.py). The `tba-credentials` README gate is a documentation check, not a security review or a substitute for the implementation’s limits and caller authorization.

### Compatibility

This source version of `tba-credentials` declares Python `>=3.10,<3.16`. Consult its dependency constraints before upgrading. Source-version and registry-version badges have separate meanings; this migration makes no additional platform or interoperability certification claim.

---

## Verification

### Tests

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-credentials/src/tba_credentials/__init__.py).

### Certification Status

No external certification is asserted for `tba-credentials` by this documentation migration. README conformance, example syntax, runtime tests, and protocol or security certification are distinct evidence scopes.

### Evidence

The [README standards CI](https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml) records mechanical documentation results for its tested commit. The [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-credentials/src/tba_credentials/__init__.py) and example sources support the package-boundary description; external runtime behavior requires its own test evidence.

---

## FAQ

### Why

**Why select this package?** `tba-credentials` provides credential facade for authentication, digital, and workload credential domains in the TBA package suite; use its own API boundary rather than assuming neighboring packages are bundled or configured automatically.

### How

**How do I start?** Install or synchronize the environment under Getting Started, follow the maintained example for `tba-credentials`, and consult [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-credentials/src/tba_credentials/__init__.py) for the exact types and signatures involved.

### When

**When should I validate an upgrade?** Recheck `tba-credentials` whenever its source version, declared collaborators, configuration, or caller changes. Run relevant behavioral tests in addition to the README gate before promotion.

---

## Documentation and Related Packages

### More Documentation

The [repository contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md), [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-credentials/src/tba_credentials/__init__.py), and [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-credentials/pyproject.toml) provide the supporting context for `tba-credentials`. The [README policy](https://github.com/groupsum/readme-standards/blob/master/docs/outline.md) defines the common document structure.

### Related Packages

- [tigrbl-authn-credentials](https://pypi.org/project/tigrbl-authn-credentials/) remains a deprecated compatibility package.
- [tigrbl-identity-credentials](https://pypi.org/project/tigrbl-identity-credentials/) remains a deprecated compatibility package.
- [tba-protocol-oauth](https://pypi.org/project/tba-protocol-oauth/) owns OAuth wire behavior.
- [tba-runtime-authorization-policy](https://pypi.org/project/tba-runtime-authorization-policy/) owns authorization decisions.

### Project Links

<!-- readme-standards:begin project-links -->
- [Documentation](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/070-facade/tba-credentials#readme)
- [Homepage](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/070-facade/tba-credentials#readme)
- [Issues](https://github.com/tigrbl/tigrbl_auth/issues)
- [PyPI](https://pypi.org/project/tba-credentials/)
- [Repository](https://github.com/tigrbl/tigrbl_auth)
- [SSOT](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [Source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/070-facade/tba-credentials)
- [pypi: tba-credentials](https://pypi.org/project/tba-credentials/)
<!-- readme-standards:end project-links -->

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/070-facade/tba-credentials)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-credentials/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-credentials/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-credentials/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-credentials/)

---

## Contributing

### How to Contribute

Follow the [contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md) and include a focused example or regression for changes to `tba-credentials`. Keep package behavior, its documented boundary, and its tests aligned.

### Development Setup

Work from the `pkgs/070-facade/tba-credentials` checkout. Synchronize its declared development environment with uv, then run the relevant package tests and `python -m pytest docs/readme/test_examples.py`. The repository’s dedicated README job installs `readme-standards==0.1.3` without resolving unrelated runtime packages.

### Notes for Maintainers

Edit authored prose directly in this `tba-credentials` README. Update source examples in `docs/readme/`, then run `readme-standards render --root . --write` from the package directory and review the diff. Required headings and generated blocks come from package-guide-v1.

---

## Governance

### Ownership and Decision Making

Changes to `tba-credentials` follow the maintainer review process of [tigrbl/tigrbl_auth](https://github.com/tigrbl/tigrbl_auth) and its contribution guide. Author attribution remains in the [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-credentials/pyproject.toml); this README does not assign new publishing or administrative authority.

### Standards and Policies

This package is part of the SSOT-governed TBA package suite. New facade-level credential imports should prefer `tba_credentials`; implementation work should continue in the specialized owner package.

`tba-credentials` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `070-facade` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

### Lifecycle and Migration

The `tba-credentials` source version is `0.4.0.dev3`. This change standardizes documentation and adds a development-only gate; it does not publish a new runtime version or declare a previously unpublished package released. Preserve explicit deprecation and replacement instructions where present.

---

## License and Attribution

### License

<!-- readme-standards:begin license -->
Licensed under `Apache-2.0`. See [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-credentials/LICENSE).
<!-- readme-standards:end license -->

### Notices

<!-- readme-standards:begin notices -->
See [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-credentials/NOTICE) for attribution.
<!-- readme-standards:end notices -->
