# tba-contracts-identity

<!-- readme-standards:begin branding -->
<p align="center"><a href="https://github.com/tigrbl/tigrbl_auth"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="300"></a></p>
<p align="center"><strong>tba-contracts-identity</strong></p>
<p align="center">Dependency-light identity contract dataclasses, enums, protocols, and plane access metadata.</p>
<p align="center">
<a href="https://pypi.org/project/tba-contracts-identity/"><img alt="pypi: tba-contracts-identity" src="https://img.shields.io/pypi/v/tba-contracts-identity"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-identity/pyproject.toml"><img alt="Source version: 0.4.0.dev3" src="https://img.shields.io/static/v1?label=Source%20version&amp;message=0.4.0.dev3&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-identity/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/static/v1?label=Python&amp;message=%3E%3D3.10%2C%3C3.16&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-identity/pyproject.toml"><img alt="Layer: 002-contracts" src="https://img.shields.io/static/v1?label=Layer&amp;message=002-contracts&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-identity/README.md#lifecycle-and-migration"><img alt="Lifecycle: active" src="https://img.shields.io/static/v1?label=Lifecycle&amp;message=active&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-identity/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/static/v1?label=License&amp;message=Apache-2.0&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-identity/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/static/v1?label=Notice&amp;message=attribution&amp;color=525252"></a>
</p>
<p align="center">
<a href="https://pypi.org/project/tba-contracts-identity/"><img alt="Monthly PyPI downloads: tba-contracts-identity" src="https://img.shields.io/pypi/dm/tba-contracts-identity"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-identity/README.md"><img alt="README hits: tba-contracts-identity" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/pkgs/002-contracts/tba-contracts-identity/README.md.svg?label=README%20hits"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="README standards: CI gate" src="https://img.shields.io/static/v1?label=README%20standards&amp;message=CI%20gate&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-identity/docs/readme/test_examples.py"><img alt="Tests: example source" src="https://img.shields.io/static/v1?label=Tests&amp;message=example%20source&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-identity/README.md#certification-status"><img alt="Certification: not certified" src="https://img.shields.io/static/v1?label=Certification&amp;message=not%20certified&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/tools/readme/POLICY.md"><img alt="Governance: repository policy" src="https://img.shields.io/static/v1?label=Governance&amp;message=repository%20policy&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="Evidence: source and CI" src="https://img.shields.io/static/v1?label=Evidence&amp;message=source%20and%20CI&amp;color=525252"></a>
</p>
<p align="center"><a href="#overview">Overview</a> · <a href="#installation">Installation</a> · <a href="#quick-start">Quick Start</a> · <a href="#usage">Usage</a> · <a href="#public-api-and-import-surfaces">API</a> · <a href="#contributing">Contributing</a> · <a href="#governance">Governance</a> · <a href="#license">License</a></p>
<!-- readme-standards:end branding -->

---

## Overview

### Summary

`tba-contracts-identity` contains dependency-light identity contract types:
abstract protocols, dataclasses, enums, projection metadata,
and declarative plane access/capability metadata.

- Package: `tba-contracts-identity`
- Import root: `tba_contracts_identity`
- Component kind: Identity contract package
- Use it for reusable identity/authn/authz/admin contract types.
- Use plane access/capability declarations as metadata over APIs and
  deployments, not as separate schema families.
- Table-backed REST schemas are owned by `tba-storage-core` table modules
  through Tigrbl table schema context and `F`, `IO`, and `S` inference.
- Release and security-trust contracts remain in their dedicated contract
  packages.

### Why This Package

`tba-contracts-identity` isolates this responsibility: Dependency-light identity contract dataclasses, enums, protocols, and plane access metadata. Its [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-identity/src/tba_contracts_identity/__init__.py) exposes `annotations`, allowing consumers to select this package without treating adjacent packages as part of its public contract.

### When to Use

Choose `tba-contracts-identity` for this responsibility: Dependency-light identity contract dataclasses, enums, protocols, and plane access metadata. Its `002-contracts` placement keeps shared types and structural ports separate from environment-specific service implementations or HTTP routing.

### Features

- `AccountSelfServiceError`: declared in src/tba_contracts_identity/account_self_service.py
- `AccountAuthenticationError`: declared in src/tba_contracts_identity/account_self_service.py
- `AccountNotFoundError`: declared in src/tba_contracts_identity/account_self_service.py
- `AccountValidationError`: declared in src/tba_contracts_identity/account_self_service.py
- `AccountPrincipal`: declared in src/tba_contracts_identity/account_self_service.py
- `AccountProfile`: declared in src/tba_contracts_identity/account_self_service.py
- `AccountProfileUpdate`: declared in src/tba_contracts_identity/account_self_service.py
- `AccountSession`: declared in src/tba_contracts_identity/account_self_service.py

### Non-Goals

`tba-contracts-identity` does not take ownership of environment-specific service implementations or HTTP routing.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

---

## Getting Started

### Prerequisites

Python `>=3.10,<3.16` is required. The [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-identity/pyproject.toml) declares runtime dependencies including `tba-primitives-identity`, `tba-contracts-identity-assurance`, `tba-contracts-attestation`, `tba-contracts-claim`, `tba-contracts-did`, `tba-contracts-digital-credential`, `tba-contracts-public-key-authentication`, `tba-contracts-replay`, `tba-contracts-security-event`, `tba-contracts-security-trust`, `tba-contracts-token`, `tba-contracts-workload-identity`. Read the example’s inputs and service requirements before execution.

### Installation

```bash
pip install tba-contracts-identity
# or
uv add tba-contracts-identity
```

Install the current `tba-contracts-identity` source checkout when working ahead of a PyPI release:

```bash
uv pip install ./pkgs/002-contracts/tba-contracts-identity
```

#### uv

<!-- readme-standards:begin installation.uv -->
```bash
uv add tba-contracts-identity
```
<!-- readme-standards:end installation.uv -->

#### pip

<!-- readme-standards:begin installation.pip -->
```bash
python -m pip install tba-contracts-identity
```
<!-- readme-standards:end installation.pip -->

#### Poetry

<!-- readme-standards:begin installation.poetry -->
```bash
poetry add tba-contracts-identity
```
<!-- readme-standards:end installation.poetry -->

### Quick Start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.


```bash
uv run --isolated --no-project --python 3.12 --with "tba-contracts-identity==0.4.0.dev3" python quickstart.py
```

The import and assertion succeed when the ContractProjection entry point is available.

#### Example

<!-- readme-standards:begin example.quick-start -->
Source: [docs/readme/quick_start.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-identity/docs/readme/quick_start.py).

```python
from tba_contracts_identity import ContractProjection

assert callable(ContractProjection)
```
<!-- readme-standards:end example.quick-start -->

#### Expected Result

The example demonstrates the documented `tba-contracts-identity` source boundary or workflow. Complete its required configuration first. README CI checks the maintained source’s syntax and declarations; it does not claim that external services or the application workflow were exercised.

---

## Usage

### Common Workflows

<!-- readme-standards:begin example.usage -->
Source: [docs/readme/usage.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-identity/docs/readme/usage.py).

```python
from tba_contracts_identity import (
    ContractProjection,
    PlaneAccess,
    PlaneAccessDeclaration,
    PlaneCapability,
)

projection = ContractProjection(
    kind="openapi",
    profile="production",
    version="0.4.0",
    document={"openapi": "3.1.0", "paths": {}},
)

surface_access = PlaneAccessDeclaration(
    surface="tenant-admin",
    access=PlaneAccess.TENANT_ADMIN,
    capabilities=(PlaneCapability.MANAGE_PRINCIPALS,),
    default_audience="tba-auth-admin",
)
```
<!-- readme-standards:end example.usage -->

### Configuration

Configure `tba-contracts-identity` through the APIs in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-identity/src/tba_contracts_identity/__init__.py); its [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-identity/pyproject.toml) describes installation requirements, not an implicit service configuration. No additional package-global configuration contract is inferred from dependencies.

### Error Handling

The inspected `tba-contracts-identity` source raises `AttributeError`, `CredentialStateError`, `OidcContractError`, `RuntimeError`, `ValueError`. Handle these at the calling boundary and consult the implementation for the triggering conditions.

### Best Practices

Use the explicit `tba-contracts-identity` imports documented below and keep collaborator configuration with the caller. Run the package’s relevant tests after changing `annotations`; an import or successful installation alone does not establish its runtime guarantees.

---

## Package Boundary

### What It Owns

- Identity, credential, authorization, admin-resource, and resource-verifier
  contract dataclasses/enums/protocols
- Plane access/capability metadata declarations
- OpenAPI projection metadata
- Dependency-light contract objects
- No Pydantic request/response schemas
- No table-backed REST schema aliases
- No remote procedure call surface
- No release-posture or security-trust contract ownership

### Public API and Import Surfaces

Import namespace: `tba_contracts_identity`.

Source-declared exports or types: `annotations`.

Inspect [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-identity/src/tba_contracts_identity/__init__.py) for exact signatures; this inventory does not designate every internal module as stable.

### Entry Points

<!-- readme-standards:begin entry-points -->
This package declares no command-line, GUI, or plugin entry points in its manifest.
<!-- readme-standards:end entry-points -->

### Injected Dependencies

The [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-identity/src/tba_contracts_identity/__init__.py) for `tba-contracts-identity` does not declare an explicit service-constructor or keyword-only factory hook in the inspected source. Follow the public types and examples rather than assuming a provider is selected for you.

Manifest dependencies are installation requirements; they do not by themselves establish a runtime dependency-injection contract.

### Protocol Consumers

The following layer-50 manifests directly depend on `tba-contracts-identity`:

- [tba-protocol-attestation-corim](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-attestation-corim/README.md)
- [tba-protocol-attestation-eat](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-attestation-eat/README.md)
- [tba-protocol-authzen](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-authzen/README.md)
- [tba-protocol-credential-iso-mdoc](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-credential-iso-mdoc/README.md)
- [tba-protocol-cwt](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-cwt/README.md)
- [tba-protocol-gnap](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-gnap/README.md)
- [tba-protocol-jwt](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-jwt/README.md)
- [tba-protocol-oauth](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oauth/README.md)
- [tba-protocol-oauth-protected-resource](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oauth-protected-resource/README.md)
- [tba-protocol-oid4vci](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oid4vci/README.md)
- [tba-protocol-oid4vp](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oid4vp/README.md)
- [tba-protocol-oidc](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oidc/README.md)
- [tba-protocol-oidc-relying-party](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oidc-relying-party/README.md)
- [tba-protocol-security-event-set](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-security-event-set/README.md)
- [tba-protocol-security-jose](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-security-jose/README.md)
- [tba-protocol-webauthn](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-webauthn/README.md)

Other direct consumers include [tba-app-backend-core](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-core/README.md), [tba-app-backend-my-account](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-my-account/README.md), [tba-app-backend-platform-administration](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-platform-administration/README.md), [tba-auth](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-auth/README.md), [tba-bases-authentication-assurance](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-authentication-assurance/README.md), [tba-bases-authentication-credential](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-authentication-credential/README.md), [tba-bases-authenticator](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-authenticator/README.md), [tba-bases-authorization-policy](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-authorization-policy/README.md).

### Extensions

For `tba-contracts-identity`, use the source-declared public interfaces (`annotations`) when composing or extending behavior. Its entry-point section below is authoritative for registered plugins; no additional extension loader is inferred from the package name.

---

## Operations and Readiness

### Operational Requirements

`tba-contracts-identity` exposes shared types and structural ports. Inspect the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-identity/src/tba_contracts_identity/__init__.py) for the exported types and composition surface.

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

### Health and Observability

This README does not establish a standalone health endpoint for `tba-contracts-identity`. Observe the concrete caller’s results, exceptions, and existing test reports. An application that embeds this package must define its own health and telemetry contract.

### Security and Resource Limits

Apply the input, credential, and resource constraints implemented in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-identity/src/tba_contracts_identity/__init__.py). The `tba-contracts-identity` README gate is a documentation check, not a security review or a substitute for the implementation’s limits and caller authorization.

### Compatibility

This source version of `tba-contracts-identity` declares Python `>=3.10,<3.16`. Consult its dependency constraints before upgrading. Source-version and registry-version badges have separate meanings; this migration makes no additional platform or interoperability certification claim.

---

## Verification

### Tests

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-identity/src/tba_contracts_identity/__init__.py).

### Certification Status

No external certification is asserted for `tba-contracts-identity` by this documentation migration. README conformance, example syntax, runtime tests, and protocol or security certification are distinct evidence scopes.

### Evidence

The [README standards CI](https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml) records mechanical documentation results for its tested commit. The [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-identity/src/tba_contracts_identity/__init__.py) and example sources support the package-boundary description; external runtime behavior requires its own test evidence.

---

## FAQ

### Why

**Why select this package?** `tba-contracts-identity` provides dependency-light identity contract dataclasses, enums, protocols, and plane access metadata; use its own API boundary rather than assuming neighboring packages are bundled or configured automatically.

### How

**How do I start?** Install or synchronize the environment under Getting Started, follow the maintained example for `tba-contracts-identity`, and consult [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-identity/src/tba_contracts_identity/__init__.py) for the exact types and signatures involved.

### When

**When should I validate an upgrade?** Recheck `tba-contracts-identity` whenever its source version, declared collaborators, configuration, or caller changes. Run relevant behavioral tests in addition to the README gate before promotion.

---

## Documentation and Related Packages

### More Documentation

The [repository contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md), [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-identity/src/tba_contracts_identity/__init__.py), and [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-identity/pyproject.toml) provide the supporting context for `tba-contracts-identity`. The [README policy](https://github.com/groupsum/readme-standards/blob/master/docs/outline.md) defines the common document structure.

### Related Packages

- [tba-primitives-identity](https://pypi.org/project/tba-primitives-identity/)
- [tba-storage-core](https://pypi.org/project/tba-storage-core/)
- [tba-contracts-security-trust](https://pypi.org/project/tba-contracts-security-trust/)

### Project Links

<!-- readme-standards:begin project-links -->
- [Documentation](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/002-contracts/tba-contracts-identity#readme)
- [Homepage](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/002-contracts/tba-contracts-identity#readme)
- [Issues](https://github.com/tigrbl/tigrbl_auth/issues)
- [PyPI](https://pypi.org/project/tba-contracts-identity/)
- [Repository](https://github.com/tigrbl/tigrbl_auth)
- [SSOT](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [Source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/002-contracts/tba-contracts-identity)
- [pypi: tba-contracts-identity](https://pypi.org/project/tba-contracts-identity/)
<!-- readme-standards:end project-links -->

- [PyPI package](https://pypi.org/project/tba-contracts-identity/)
- [Source repository](https://github.com/tigrbl/tigrbl_auth)
- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/002-contracts/tba-contracts-identity)
- [SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/002-contracts/tba-contracts-identity)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-identity/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-identity/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-identity/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-contracts-identity/)

---

## Contributing

### How to Contribute

Follow the [contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md) and include a focused example or regression for changes to `tba-contracts-identity`. Keep package behavior, its documented boundary, and its tests aligned.

### Development Setup

Work from the `pkgs/002-contracts/tba-contracts-identity` checkout. Synchronize its declared development environment with uv, then run the relevant package tests and `python -m pytest docs/readme/test_examples.py`. The repository’s dedicated README job installs `readme-standards==0.1.1` without resolving unrelated runtime packages.

### Notes for Maintainers

Edit authored prose directly in this `tba-contracts-identity` README. Update source examples in `docs/readme/`, then run `readme-standards render --root . --write` from the package directory and review the diff. Required headings and generated blocks come from package-guide-v1.

---

## Governance

### Ownership and Decision Making

Changes to `tba-contracts-identity` follow the maintainer review process of [tigrbl/tigrbl_auth](https://github.com/tigrbl/tigrbl_auth) and its contribution guide. Author attribution remains in the [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-identity/pyproject.toml); this README does not assign new publishing or administrative authority.

### Standards and Policies

This package is part of the SSOT-governed TBA identity package suite. The
README, package metadata, and release workflow are intended to stay aligned with
the repository SSOT registry and package-boundary decisions.

`tba-contracts-identity` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `002-contracts` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

### Lifecycle and Migration

The `tba-contracts-identity` source version is `0.4.0.dev3`. This change standardizes documentation and adds a development-only gate; it does not publish a new runtime version or declare a previously unpublished package released. Preserve explicit deprecation and replacement instructions where present.

---

## License and Attribution

### License

<!-- readme-standards:begin license -->
Licensed under `Apache-2.0`. See [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-identity/LICENSE).
<!-- readme-standards:end license -->

### Notices

<!-- readme-standards:begin notices -->
See [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-identity/NOTICE) for attribution.
<!-- readme-standards:end notices -->
