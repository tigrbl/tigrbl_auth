# tba-profile-credential-vc-jose-cose

<!-- readme-standards:begin branding -->
<p align="center"><a href="https://github.com/tigrbl/tigrbl_auth"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="300"></a></p>
<p align="center"><strong>tba-profile-credential-vc-jose-cose</strong></p>
<p align="center">Versioned W3C VC-JOSE-COSE Recommendation ownership for secured Verifiable Credentials and Presentations.</p>
<p align="center">
<a href="https://pypi.org/project/tba-profile-credential-vc-jose-cose/"><img alt="pypi: tba-profile-credential-vc-jose-cose" src="https://img.shields.io/pypi/v/tba-profile-credential-vc-jose-cose"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-credential-vc-jose-cose/pyproject.toml"><img alt="Source version: 0.4.0.dev3" src="https://img.shields.io/static/v1?label=Source%20version&amp;message=0.4.0.dev3&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-credential-vc-jose-cose/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/static/v1?label=Python&amp;message=%3E%3D3.10%2C%3C3.16&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-credential-vc-jose-cose/pyproject.toml"><img alt="Layer: 055-profiles" src="https://img.shields.io/static/v1?label=Layer&amp;message=055-profiles&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-credential-vc-jose-cose/README.md#lifecycle-and-migration"><img alt="Lifecycle: active" src="https://img.shields.io/static/v1?label=Lifecycle&amp;message=active&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-credential-vc-jose-cose/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/static/v1?label=License&amp;message=Apache-2.0&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-credential-vc-jose-cose/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/static/v1?label=Notice&amp;message=attribution&amp;color=525252"></a>
</p>
<p align="center">
<a href="https://pypi.org/project/tba-profile-credential-vc-jose-cose/"><img alt="Monthly PyPI downloads: tba-profile-credential-vc-jose-cose" src="https://img.shields.io/pypi/dm/tba-profile-credential-vc-jose-cose"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-credential-vc-jose-cose/README.md"><img alt="README hits: tba-profile-credential-vc-jose-cose" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/pkgs/055-profiles/tba-profile-credential-vc-jose-cose/README.md.svg?label=README%20hits"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="README standards: CI gate" src="https://img.shields.io/static/v1?label=README%20standards&amp;message=CI%20gate&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-credential-vc-jose-cose/docs/readme/test_examples.py"><img alt="Tests: example source" src="https://img.shields.io/static/v1?label=Tests&amp;message=example%20source&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-credential-vc-jose-cose/README.md#certification-status"><img alt="Certification: not certified" src="https://img.shields.io/static/v1?label=Certification&amp;message=not%20certified&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/tools/readme/POLICY.md"><img alt="Governance: repository policy" src="https://img.shields.io/static/v1?label=Governance&amp;message=repository%20policy&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="Evidence: source and CI" src="https://img.shields.io/static/v1?label=Evidence&amp;message=source%20and%20CI&amp;color=525252"></a>
</p>
<p align="center"><a href="#overview">Overview</a> · <a href="#installation">Installation</a> · <a href="#quick-start">Quick Start</a> · <a href="#usage">Usage</a> · <a href="#public-api-and-import-surfaces">API</a> · <a href="#contributing">Contributing</a> · <a href="#governance">Governance</a> · <a href="#license">License</a></p>
<!-- readme-standards:end branding -->

---

## Overview

### Summary

Versioned W3C VC-JOSE-COSE Recommendation ownership for secured Verifiable Credentials and Presentations.

- Package: `tba-profile-credential-vc-jose-cose`
- Layer: `055-profiles`
- Responsibility: Versioned W3C VC-JOSE-COSE Recommendation ownership for secured Verifiable Credentials and Presentations.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-credential-vc-jose-cose/src/tba_profile_credential_vc_jose_cose/__init__.py).
- Distribution: Python package on PyPI.

### Why This Package

`tba-profile-credential-vc-jose-cose` isolates this responsibility: Versioned W3C VC-JOSE-COSE Recommendation ownership for secured Verifiable Credentials and Presentations. Its [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-credential-vc-jose-cose/src/tba_profile_credential_vc_jose_cose/bindings.py) exposes `CURRENT_VERSION`, `FORMATS`, `SecuredVcCredential`, `SecuredVcFormat`, `SecuredVcVerificationResult`, `VERSION_HISTORY`, `VcJoseCoseProtocol`, `VcJoseCoseVersion`, `select_format`, `validate_cose_vc`, `validate_jose_vc`, allowing consumers to select this package without treating adjacent packages as part of its public contract.

### When to Use

Choose `tba-profile-credential-vc-jose-cose` for this responsibility: Versioned W3C VC-JOSE-COSE Recommendation ownership for secured Verifiable Credentials and Presentations. Its `055-profiles` placement keeps focused protocol and credential profiles separate from a universal deployment or implicit trust-policy selection.

### Features

- `ProtocolProfileError`: The artifact or request does not satisfy the selected protocol profile.
- `SecuredVcFormat`: declared in src/tba_profile_credential_vc_jose_cose/formats.py
- `SecuredVcVerificationResult`: declared in src/tba_profile_credential_vc_jose_cose/protocol.py
- `VcJoseCoseProtocol`: declared in src/tba_profile_credential_vc_jose_cose/protocol.py
- `VcJoseCoseVersion`: declared in src/tba_profile_credential_vc_jose_cose/versions.py

### Non-Goals

`tba-profile-credential-vc-jose-cose` does not take ownership of a universal deployment or implicit trust-policy selection.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

---

## Getting Started

### Prerequisites

Python `>=3.10,<3.16` is required. The [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-credential-vc-jose-cose/pyproject.toml) declares runtime dependencies including `cbor2`, `tba-primitives-identity`, `tba-contracts-protected-envelope`, `tba-concrete-vc-jose-credential`, `tba-concrete-vc-cose-credential`, `tba-protocol-security-jws`, `tba-protocol-security-cose`. Read the example’s inputs and service requirements before execution.

### Installation

Install the selected PyPI release of `tba-profile-credential-vc-jose-cose`:

```bash
uv pip install tba-profile-credential-vc-jose-cose
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/055-profiles/tba-profile-credential-vc-jose-cose
```

#### uv

<!-- readme-standards:begin installation.uv -->
```bash
uv add tba-profile-credential-vc-jose-cose
```
<!-- readme-standards:end installation.uv -->

#### pip

<!-- readme-standards:begin installation.pip -->
```bash
python -m pip install tba-profile-credential-vc-jose-cose
```
<!-- readme-standards:end installation.pip -->

#### Poetry

<!-- readme-standards:begin installation.poetry -->
```bash
poetry add tba-profile-credential-vc-jose-cose
```
<!-- readme-standards:end installation.poetry -->

### Quick Start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.


```bash
uv run --isolated --no-project --python 3.12 --with "tba-profile-credential-vc-jose-cose==0.4.0.dev3" python quickstart.py
```

The command prints the declared current revision.

#### Example

<!-- readme-standards:begin example.quick-start -->
Source: [docs/readme/quick_start.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-credential-vc-jose-cose/docs/readme/quick_start.py).

```python
from tba_profile_credential_vc_jose_cose import CURRENT_VERSION

assert CURRENT_VERSION is not None
print(CURRENT_VERSION)
```
<!-- readme-standards:end example.quick-start -->

#### Expected Result

The example demonstrates the documented `tba-profile-credential-vc-jose-cose` source boundary or workflow. Complete its required configuration first. README CI checks the maintained source’s syntax and declarations; it does not claim that external services or the application workflow were exercised.

---

## Usage

### Common Workflows

<!-- readme-standards:begin example.usage -->
Source: [docs/readme/usage.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-credential-vc-jose-cose/docs/readme/usage.py).

```python
from tba_profile_credential_vc_jose_cose import CURRENT_VERSION

assert CURRENT_VERSION is not None
print(CURRENT_VERSION)
```
<!-- readme-standards:end example.usage -->

The following public-entry-point example belongs to `tba-profile-credential-vc-jose-cose`. Versioned W3C VC-JOSE-COSE Recommendation ownership for secured Verifiable Credentials and Presentations. Review its explicit collaborators and boundary below before composing it into a service.

### Configuration

Configure `tba-profile-credential-vc-jose-cose` through the APIs in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-credential-vc-jose-cose/src/tba_profile_credential_vc_jose_cose/bindings.py); its [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-credential-vc-jose-cose/pyproject.toml) describes installation requirements, not an implicit service configuration. No additional package-global configuration contract is inferred from dependencies.

### Error Handling

The inspected `tba-profile-credential-vc-jose-cose` source raises `RuntimeError`, `TypeError`, `ValueError`. Handle these at the calling boundary and consult the implementation for the triggering conditions.

### Best Practices

Use the explicit `tba-profile-credential-vc-jose-cose` imports documented below and keep collaborator configuration with the caller. Run the package’s relevant tests after changing `CURRENT_VERSION`, `FORMATS`, `SecuredVcCredential`, `SecuredVcFormat`, `SecuredVcVerificationResult`, `VERSION_HISTORY`, `VcJoseCoseProtocol`, `VcJoseCoseVersion`, `select_format`, `validate_cose_vc`, `validate_jose_vc`; an import or successful installation alone does not establish its runtime guarantees.

---

## Package Boundary

### What It Owns

`tba-profile-credential-vc-jose-cose` belongs to `055-profiles` and owns focused protocol and credential profiles: Versioned W3C VC-JOSE-COSE Recommendation ownership for secured Verifiable Credentials and Presentations.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-credential-vc-jose-cose/src/tba_profile_credential_vc_jose_cose/__init__.py). Public exports include `SecuredVcCredential`, `SecuredVcVerificationResult`, `VcJoseCoseProtocol`, `CURRENT_VERSION`, `FORMATS`, `VERSION_HISTORY`, `SecuredVcFormat`, `VcJoseCoseVersion`, `select_format`, `validate_cose_vc`, `validate_jose_vc`.

Keep a universal deployment or implicit trust-policy selection in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

### Public API and Import Surfaces

Import namespace: `tba_profile_credential_vc_jose_cose`.

Source-declared exports or types: `CURRENT_VERSION`, `FORMATS`, `SecuredVcCredential`, `SecuredVcFormat`, `SecuredVcVerificationResult`, `VERSION_HISTORY`, `VcJoseCoseProtocol`, `VcJoseCoseVersion`, `select_format`, `validate_cose_vc`, `validate_jose_vc`.

Inspect [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-credential-vc-jose-cose/src/tba_profile_credential_vc_jose_cose/bindings.py) for exact signatures; this inventory does not designate every internal module as stable.

### Entry Points

<!-- readme-standards:begin entry-points -->
This package declares no command-line, GUI, or plugin entry points in its manifest.
<!-- readme-standards:end entry-points -->

### Injected Dependencies

Explicit construction inputs and collaborators for `tba-profile-credential-vc-jose-cose`:

- `VcJoseCoseProtocol` construction inputs: `jws_protocol`, `cose_protocol`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-credential-vc-jose-cose/src/tba_profile_credential_vc_jose_cose/protocol.py).
- `validate_jose_vc` construction inputs: `media_type`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-credential-vc-jose-cose/src/tba_profile_credential_vc_jose_cose/validation.py).
- `validate_cose_vc` construction inputs: `media_type`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-credential-vc-jose-cose/src/tba_profile_credential_vc_jose_cose/validation.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

### Protocol Consumers

Direct consumers in this checkout’s package manifests include `tba-runtime-identity`, `tba-workspace`. These edges describe declared dependencies, not protocol-conformance evidence.

### Extensions

For `tba-profile-credential-vc-jose-cose`, use the source-declared public interfaces (`CURRENT_VERSION`, `FORMATS`, `SecuredVcCredential`, `SecuredVcFormat`, `SecuredVcVerificationResult`, `VERSION_HISTORY`, `VcJoseCoseProtocol`, `VcJoseCoseVersion`, `select_format`, `validate_cose_vc`, `validate_jose_vc`) when composing or extending behavior. Its entry-point section below is authoritative for registered plugins; no additional extension loader is inferred from the package name.

---

## Operations and Readiness

### Operational Requirements

`tba-profile-credential-vc-jose-cose` exposes focused protocol and credential profiles. Public operations found in its source:

- `select_format` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-credential-vc-jose-cose/src/tba_profile_credential_vc_jose_cose/formats.py).
- `VcJoseCoseProtocol.issue` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-credential-vc-jose-cose/src/tba_profile_credential_vc_jose_cose/protocol.py).
- `VcJoseCoseProtocol.verify` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-credential-vc-jose-cose/src/tba_profile_credential_vc_jose_cose/protocol.py).
- `validate_jose_vc` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-credential-vc-jose-cose/src/tba_profile_credential_vc_jose_cose/validation.py).
- `validate_cose_vc` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-credential-vc-jose-cose/src/tba_profile_credential_vc_jose_cose/validation.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

### Health and Observability

This README does not establish a standalone health endpoint for `tba-profile-credential-vc-jose-cose`. Observe the concrete caller’s results, exceptions, and existing test reports. An application that embeds this package must define its own health and telemetry contract.

### Security and Resource Limits

Apply the input, credential, and resource constraints implemented in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-credential-vc-jose-cose/src/tba_profile_credential_vc_jose_cose/bindings.py). The `tba-profile-credential-vc-jose-cose` README gate is a documentation check, not a security review or a substitute for the implementation’s limits and caller authorization.

### Compatibility

This source version of `tba-profile-credential-vc-jose-cose` declares Python `>=3.10,<3.16`. Consult its dependency constraints before upgrading. Source-version and registry-version badges have separate meanings; this migration makes no additional platform or interoperability certification claim.

---

## Verification

### Tests

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-credential-vc-jose-cose/src/tba_profile_credential_vc_jose_cose/__init__.py).

### Certification Status

No external certification is asserted for `tba-profile-credential-vc-jose-cose` by this documentation migration. README conformance, example syntax, runtime tests, and protocol or security certification are distinct evidence scopes.

### Evidence

The [README standards CI](https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml) records mechanical documentation results for its tested commit. The [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-credential-vc-jose-cose/src/tba_profile_credential_vc_jose_cose/bindings.py) and example sources support the package-boundary description; external runtime behavior requires its own test evidence.

---

## FAQ

### Why

**Why select this package?** `tba-profile-credential-vc-jose-cose` provides versioned W3C VC-JOSE-COSE Recommendation ownership for secured Verifiable Credentials and Presentations; use its own API boundary rather than assuming neighboring packages are bundled or configured automatically.

### How

**How do I start?** Install or synchronize the environment under Getting Started, follow the maintained example for `tba-profile-credential-vc-jose-cose`, and consult [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-credential-vc-jose-cose/src/tba_profile_credential_vc_jose_cose/bindings.py) for the exact types and signatures involved.

### When

**When should I validate an upgrade?** Recheck `tba-profile-credential-vc-jose-cose` whenever its source version, declared collaborators, configuration, or caller changes. Run relevant behavioral tests in addition to the README gate before promotion.

---

## Documentation and Related Packages

### More Documentation

The [repository contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md), [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-credential-vc-jose-cose/src/tba_profile_credential_vc_jose_cose/bindings.py), and [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-credential-vc-jose-cose/pyproject.toml) provide the supporting context for `tba-profile-credential-vc-jose-cose`. The [README policy](https://github.com/groupsum/readme-standards/blob/master/docs/outline.md) defines the common document structure.

### Related Packages

Declared local runtime dependencies:

- [tba-concrete-vc-cose-credential](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-vc-cose-credential/README.md)
- [tba-concrete-vc-jose-credential](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-vc-jose-credential/README.md)
- [tba-contracts-protected-envelope](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-protected-envelope/README.md)
- [tba-primitives-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/000-primitives/tba-primitives-identity/README.md)
- [tba-protocol-security-cose](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-security-cose/README.md)
- [tba-protocol-security-jws](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-security-jws/README.md)

Direct downstream consumers:

- [tba-runtime-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity/README.md)

### Project Links

<!-- readme-standards:begin project-links -->
- [Documentation](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/055-profiles/tba-profile-credential-vc-jose-cose#readme)
- [Homepage](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/055-profiles/tba-profile-credential-vc-jose-cose#readme)
- [Issues](https://github.com/tigrbl/tigrbl_auth/issues)
- [PyPI](https://pypi.org/project/tba-profile-credential-vc-jose-cose/)
- [Repository](https://github.com/tigrbl/tigrbl_auth)
- [Source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/055-profiles/tba-profile-credential-vc-jose-cose)
- [pypi: tba-profile-credential-vc-jose-cose](https://pypi.org/project/tba-profile-credential-vc-jose-cose/)
<!-- readme-standards:end project-links -->

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/055-profiles/tba-profile-credential-vc-jose-cose)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-credential-vc-jose-cose/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-credential-vc-jose-cose/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-credential-vc-jose-cose/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-profile-credential-vc-jose-cose/)

---

## Contributing

### How to Contribute

Follow the [contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md) and include a focused example or regression for changes to `tba-profile-credential-vc-jose-cose`. Keep package behavior, its documented boundary, and its tests aligned.

### Development Setup

Work from the `pkgs/055-profiles/tba-profile-credential-vc-jose-cose` checkout. Synchronize its declared development environment with uv, then run the relevant package tests and `python -m pytest docs/readme/test_examples.py`. The repository’s dedicated README job installs `readme-standards==0.1.1` without resolving unrelated runtime packages.

### Notes for Maintainers

Edit authored prose directly in this `tba-profile-credential-vc-jose-cose` README. Update source examples in `docs/readme/`, then run `readme-standards render --root . --write` from the package directory and review the diff. Required headings and generated blocks come from package-guide-v1.

---

## Governance

### Ownership and Decision Making

Changes to `tba-profile-credential-vc-jose-cose` follow the maintainer review process of [tigrbl/tigrbl_auth](https://github.com/tigrbl/tigrbl_auth) and its contribution guide. Author attribution remains in the [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-credential-vc-jose-cose/pyproject.toml); this README does not assign new publishing or administrative authority.

### Standards and Policies

`tba-profile-credential-vc-jose-cose` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `055-profiles` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

### Lifecycle and Migration

The `tba-profile-credential-vc-jose-cose` source version is `0.4.0.dev3`. This change standardizes documentation and adds a development-only gate; it does not publish a new runtime version or declare a previously unpublished package released. Preserve explicit deprecation and replacement instructions where present.

---

## License and Attribution

### License

<!-- readme-standards:begin license -->
Licensed under `Apache-2.0`. See [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-credential-vc-jose-cose/LICENSE).
<!-- readme-standards:end license -->

### Notices

<!-- readme-standards:begin notices -->
See [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-credential-vc-jose-cose/NOTICE) for attribution.
<!-- readme-standards:end notices -->
