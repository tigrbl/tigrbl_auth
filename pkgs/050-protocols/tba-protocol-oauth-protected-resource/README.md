# tba-protocol-oauth-protected-resource

<!-- readme-standards:begin branding -->
<p align="center"><a href="https://github.com/tigrbl/tigrbl_auth"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="300"></a></p>
<p align="center"><strong>tba-protocol-oauth-protected-resource</strong></p>
<p align="center">OAuth protected-resource facade over token, DPoP, mTLS, and policy validators for the TBA package suite.</p>
<p align="center">
<a href="https://pypi.org/project/tba-protocol-oauth-protected-resource/"><img alt="pypi: tba-protocol-oauth-protected-resource" src="https://img.shields.io/pypi/v/tba-protocol-oauth-protected-resource?labelColor=1E293B&amp;color=1D4ED8"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oauth-protected-resource/pyproject.toml"><img alt="Source version: 0.4.0.dev3" src="https://img.shields.io/static/v1?label=Source%20version&amp;message=0.4.0.dev3&amp;labelColor=1E293B&amp;color=4338CA"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oauth-protected-resource/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/static/v1?label=Python&amp;message=%3E%3D3.10%2C%3C3.16&amp;labelColor=1E293B&amp;color=0F766E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oauth-protected-resource/pyproject.toml"><img alt="Layer: 050-protocols" src="https://img.shields.io/static/v1?label=Layer&amp;message=050-protocols&amp;labelColor=1E293B&amp;color=6D28D9"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oauth-protected-resource/README.md#lifecycle-and-migration"><img alt="Lifecycle: active" src="https://img.shields.io/static/v1?label=Lifecycle&amp;message=active&amp;labelColor=1E293B&amp;color=166534"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oauth-protected-resource/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/static/v1?label=License&amp;message=Apache-2.0&amp;labelColor=1E293B&amp;color=86198F"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oauth-protected-resource/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/static/v1?label=Notice&amp;message=attribution&amp;labelColor=1E293B&amp;color=86198F"></a>
</p>
<p align="center">
<a href="https://pypi.org/project/tba-protocol-oauth-protected-resource/"><img alt="Monthly PyPI downloads: tba-protocol-oauth-protected-resource" src="https://img.shields.io/pypi/dm/tba-protocol-oauth-protected-resource?labelColor=1E293B&amp;color=0E7490"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oauth-protected-resource/README.md"><img alt="README hits: tba-protocol-oauth-protected-resource" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/pkgs/050-protocols/tba-protocol-oauth-protected-resource/README.md.svg?label=README%20hits&amp;labelColor=1E293B&amp;color=0E7490"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="README standards: CI gate" src="https://img.shields.io/static/v1?label=README%20standards&amp;message=CI%20gate&amp;labelColor=1E293B&amp;color=1D4ED8"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oauth-protected-resource/docs/readme/test_examples.py"><img alt="Tests: example source" src="https://img.shields.io/static/v1?label=Tests&amp;message=example%20source&amp;labelColor=1E293B&amp;color=0F766E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oauth-protected-resource/README.md#certification-status"><img alt="Certification: not certified" src="https://img.shields.io/static/v1?label=Certification&amp;message=not%20certified&amp;labelColor=1E293B&amp;color=92400E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/tools/readme/POLICY.md"><img alt="Governance: repository policy" src="https://img.shields.io/static/v1?label=Governance&amp;message=repository%20policy&amp;labelColor=1E293B&amp;color=4338CA"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="Evidence: source and CI" src="https://img.shields.io/static/v1?label=Evidence&amp;message=source%20and%20CI&amp;labelColor=1E293B&amp;color=6D28D9"></a>
</p>
<p align="center"><a href="#overview">Overview</a> · <a href="#installation">Installation</a> · <a href="#quick-start">Quick Start</a> · <a href="#usage">Usage</a> · <a href="#public-api-and-import-surfaces">API</a> · <a href="#contributing">Contributing</a> · <a href="#governance">Governance</a> · <a href="#license">License</a></p>
<!-- readme-standards:end branding -->

---

## Overview

### Summary

tba-protocol-oauth-protected-resource owns versioned OAuth protected-resource
protocol composition: claim sets, compatibility rules, metadata, sender
constraints, and verifier integration. It composes standalone validation
providers rather than acting as a compatibility facade. The legacy
`tigrbl-identity-resource-server` package remains unchanged under `deprecated`.

- Package: `tba-protocol-oauth-protected-resource`
- Import root: `tba_protocol_oauth_protected_resource`
- Component kind: Versioned OAuth protected-resource protocol composition
- Use it for protected API validation of issuer, audience, scopes, permissions, and proof bindings.
- Do not use it to own credential proof, identity records, or OAuth/OIDC provider truth.
- Canonical protected-resource exports live in this package. The verifier and reusable sender-constraint, JWKS, introspection, mTLS, and DPoP helpers are supplied by standalone layer-20 providers. Legacy packages under `pkgs/deprecated` retain their original names and imports.

### Why This Package

`tba-protocol-oauth-protected-resource` isolates this responsibility: OAuth protected-resource facade over token, DPoP, mTLS, and policy validators for the TBA package suite. Its [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oauth-protected-resource/src/tba_protocol_oauth_protected_resource/__init__.py) exposes `AccessTokenClaims`, `CAPABILITY_REQUIREMENTS`, `COMPATIBILITY_PATHS`, `CURRENT_VERSION`, `DPoPBinding`, `DpopCnfBindingValidator`, `FEATURES_BY_VERSION`, `FrameworkRequest`, `IntrospectionClient`, `IntrospectionTransport`, `JWKSCache`, `MTLSBinding`, `MtlsCnfBindingValidator`, `PolicyHook`, `ProtectedResourceAuthorizationCapability`, allowing consumers to select this package without treating adjacent packages as part of its public contract.

### When to Use

Choose `tba-protocol-oauth-protected-resource` for this responsibility: OAuth protected-resource facade over token, DPoP, mTLS, and policy validators for the TBA package suite. Its `050-protocols` placement keeps protocol semantics and projections separate from deployment hosting or ownership of persistence implementations.

### Features

- `ProtectedResourceCompatibility`: declared in src/tba_protocol_oauth_protected_resource/compatibility.py
- `ProtectedResourceProfileError`: Base error for protected-resource profile selection and mapping.
- `UnsupportedProtectedResourceProfileError`: Raised when a protected-resource profile has no supported path.
- `ProtectedResourceBindingError`: Raised when a wire obligation cannot map to a capability.
- `ProtectedResourceProfileVersion`: declared in src/tba_protocol_oauth_protected_resource/versions.py
- `ProtectedResourceSpecification`: declared in src/tba_protocol_oauth_protected_resource/versions.py

### Non-Goals

`tba-protocol-oauth-protected-resource` does not take ownership of deployment hosting or ownership of persistence implementations.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

---

## Getting Started

### Prerequisites

Python `>=3.10,<3.16` is required. The [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oauth-protected-resource/pyproject.toml) declares runtime dependencies including `tba-protocol-oauth`, `tba-protocol-jwt`, `tba-provider-authorization-resource-server-verifier`, `tba-contracts-identity`, `tba-capability-protected-resource-authorization`, `tba-provider-security-dpop-cnf-binding-validator`, `tba-provider-security-mtls-cnf-binding-validator`, `tba-capability-protected-resource-authorization`, `tba-contracts-security-trust`. Read the example’s inputs and service requirements before execution.

### Installation

```bash
pip install tba-protocol-oauth-protected-resource
# or
uv add tba-protocol-oauth-protected-resource
```

Install the current `tba-protocol-oauth-protected-resource` source checkout when working ahead of a PyPI release:

```bash
uv pip install ./pkgs/050-protocols/tba-protocol-oauth-protected-resource
```

#### uv

<!-- readme-standards:begin installation.uv -->
```bash
uv add tba-protocol-oauth-protected-resource
```
<!-- readme-standards:end installation.uv -->

#### pip

<!-- readme-standards:begin installation.pip -->
```bash
python -m pip install tba-protocol-oauth-protected-resource
```
<!-- readme-standards:end installation.pip -->

#### Poetry

<!-- readme-standards:begin installation.poetry -->
```bash
poetry add tba-protocol-oauth-protected-resource
```
<!-- readme-standards:end installation.poetry -->

### Quick Start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.


```bash
uv run --isolated --no-project --python 3.12 --with "tba-protocol-oauth-protected-resource==0.4.0.dev3" python quickstart.py
```

The command prints the keys in the package's capability report.

#### Example

<!-- readme-standards:begin example.quick-start -->
Source: [docs/readme/quick_start.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oauth-protected-resource/docs/readme/quick_start.py).

```python
from tba_protocol_oauth_protected_resource import capability_report

report = capability_report()
assert report
print(sorted(report))
```
<!-- readme-standards:end example.quick-start -->

#### Expected Result

The example demonstrates the documented `tba-protocol-oauth-protected-resource` source boundary or workflow. Complete its required configuration first. README CI checks the maintained source’s syntax and declarations; it does not claim that external services or the application workflow were exercised.

---

## Usage

### Common Workflows

<!-- readme-standards:begin example.usage -->
Source: [docs/readme/usage.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oauth-protected-resource/docs/readme/usage.py).

```python
from tba_protocol_oauth_protected_resource import (
    AccessTokenClaims,
    ResourceRequirement,
    ResourceServerVerifier,
)

requirement = ResourceRequirement(audience="api://billing", scopes=("invoice.read",))
claims = AccessTokenClaims(
    iss="https://issuer.example.test",
    sub="user:1",
    aud=("api://billing",),
    exp=1_800_000_300,
    iat=1_800_000_000,
    scope=("invoice.read",),
)
result = ResourceServerVerifier().verify_token(claims, requirement)
```
<!-- readme-standards:end example.usage -->

### Configuration

Configure `tba-protocol-oauth-protected-resource` through the APIs in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oauth-protected-resource/src/tba_protocol_oauth_protected_resource/__init__.py); its [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oauth-protected-resource/pyproject.toml) describes installation requirements, not an implicit service configuration. No additional package-global configuration contract is inferred from dependencies.

### Error Handling

The inspected `tba-protocol-oauth-protected-resource` source raises `ValueError`. Handle these at the calling boundary and consult the implementation for the triggering conditions.

### Best Practices

Use the explicit `tba-protocol-oauth-protected-resource` imports documented below and keep collaborator configuration with the caller. Run the package’s relevant tests after changing `AccessTokenClaims`, `CAPABILITY_REQUIREMENTS`, `COMPATIBILITY_PATHS`, `CURRENT_VERSION`, `DPoPBinding`, `DpopCnfBindingValidator`, `FEATURES_BY_VERSION`, `FrameworkRequest`, `IntrospectionClient`, `IntrospectionTransport`, `JWKSCache`, `MTLSBinding`, `MtlsCnfBindingValidator`, `PolicyHook`, `ProtectedResourceAuthorizationCapability`; an import or successful installation alone does not establish its runtime guarantees.

---

## Package Boundary

### What It Owns

- Protected API token validation
- `versions.py` owns the implementation-profile history while
  `SPECIFICATION_VERSIONS` records the independently versioned RFCs composed by
  the profile.
- `features.py`, `compatibility.py`, and `migrations.py` own profile selection,
  feature reporting, and the legacy-unversioned metadata migration path.
- `claims.py`, `schemas.py`, `bindings.py`, and `errors.py` own protocol mapping;
  standalone claim classes and verifier implementations remain in lower layers.
- `capability.py` composes the layer-20 verifier into the reportable
  `protected-resource.authorization` layer-40 capability.
- Runtime capability truth and certification attestations are owned by
  `tba-certification-release.runtime_metadata` in layer 60; they are
  not protocol behavior.
- `contracts.py` is a compatibility export for the canonical OAuth
  verifier-contract mapping and does not resolve runtime deployments.
- Resource, audience, scope, permission, DPoP, mTLS, and introspection orchestration
- Resource-server framework adapters and verifier contracts
- Enforcement integration with authorization policy inputs

### Public API and Import Surfaces

Import namespace: `tba_protocol_oauth_protected_resource`.

Source-declared exports or types: `AccessTokenClaims`, `CAPABILITY_REQUIREMENTS`, `COMPATIBILITY_PATHS`, `CURRENT_VERSION`, `DPoPBinding`, `DpopCnfBindingValidator`, `FEATURES_BY_VERSION`, `FrameworkRequest`, `IntrospectionClient`, `IntrospectionTransport`, `JWKSCache`, `MTLSBinding`, `MtlsCnfBindingValidator`, `PolicyHook`, `ProtectedResourceAuthorizationCapability`.

Inspect [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oauth-protected-resource/src/tba_protocol_oauth_protected_resource/__init__.py) for exact signatures; this inventory does not designate every internal module as stable.

### Entry Points

<!-- readme-standards:begin entry-points -->
This package declares no command-line, GUI, or plugin entry points in its manifest.
<!-- readme-standards:end entry-points -->

### Injected Dependencies

Explicit construction inputs and collaborators for `tba-protocol-oauth-protected-resource`:

- `migrate_verifier_metadata` construction inputs: `source`, `target`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oauth-protected-resource/src/tba_protocol_oauth_protected_resource/migrations.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

### Protocol Consumers

Direct consumers in this checkout’s package manifests include `tba-auth`, `tba-workspace`. These edges describe declared dependencies, not protocol-conformance evidence.

### Extensions

For `tba-protocol-oauth-protected-resource`, use the source-declared public interfaces (`AccessTokenClaims`, `CAPABILITY_REQUIREMENTS`, `COMPATIBILITY_PATHS`, `CURRENT_VERSION`, `DPoPBinding`, `DpopCnfBindingValidator`, `FEATURES_BY_VERSION`, `FrameworkRequest`, `IntrospectionClient`, `IntrospectionTransport`, `JWKSCache`, `MTLSBinding`, `MtlsCnfBindingValidator`, `PolicyHook`, `ProtectedResourceAuthorizationCapability`) when composing or extending behavior. Its entry-point section below is authoritative for registered plugins; no additional extension loader is inferred from the package name.

---

## Operations and Readiness

### Operational Requirements

`tba-protocol-oauth-protected-resource` exposes protocol semantics and projections. Public operations found in its source:

- `capability_report` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oauth-protected-resource/src/tba_protocol_oauth_protected_resource/__init__.py).
- `build_protected_resource_authorization_capability` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oauth-protected-resource/src/tba_protocol_oauth_protected_resource/capability.py).
- `compose_access_token_claim_set` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oauth-protected-resource/src/tba_protocol_oauth_protected_resource/claims.py).
- `compatibility` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oauth-protected-resource/src/tba_protocol_oauth_protected_resource/compatibility.py).
- `supports` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oauth-protected-resource/src/tba_protocol_oauth_protected_resource/features.py).
- `verifier_contract_from_metadata` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oauth-protected-resource/src/tba_protocol_oauth_protected_resource/metadata.py).
- `migrate_verifier_metadata` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oauth-protected-resource/src/tba_protocol_oauth_protected_resource/migrations.py).
- `select_version` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oauth-protected-resource/src/tba_protocol_oauth_protected_resource/versions.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

### Health and Observability

This README does not establish a standalone health endpoint for `tba-protocol-oauth-protected-resource`. Observe the concrete caller’s results, exceptions, and existing test reports. An application that embeds this package must define its own health and telemetry contract.

### Security and Resource Limits

Apply the input, credential, and resource constraints implemented in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oauth-protected-resource/src/tba_protocol_oauth_protected_resource/__init__.py). The `tba-protocol-oauth-protected-resource` README gate is a documentation check, not a security review or a substitute for the implementation’s limits and caller authorization.

### Compatibility

This source version of `tba-protocol-oauth-protected-resource` declares Python `>=3.10,<3.16`. Consult its dependency constraints before upgrading. Source-version and registry-version badges have separate meanings; this migration makes no additional platform or interoperability certification claim.

---

## Verification

### Tests

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oauth-protected-resource/src/tba_protocol_oauth_protected_resource/__init__.py).

### Certification Status

No external certification is asserted for `tba-protocol-oauth-protected-resource` by this documentation migration. README conformance, example syntax, runtime tests, and protocol or security certification are distinct evidence scopes.

### Evidence

The [README standards CI](https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml) records mechanical documentation results for its tested commit. The [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oauth-protected-resource/src/tba_protocol_oauth_protected_resource/__init__.py) and example sources support the package-boundary description; external runtime behavior requires its own test evidence.

---

## FAQ

### Why

**Why select this package?** `tba-protocol-oauth-protected-resource` provides oAuth protected-resource facade over token, DPoP, mTLS, and policy validators for the TBA package suite; use its own API boundary rather than assuming neighboring packages are bundled or configured automatically.

### How

**How do I start?** Install or synchronize the environment under Getting Started, follow the maintained example for `tba-protocol-oauth-protected-resource`, and consult [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oauth-protected-resource/src/tba_protocol_oauth_protected_resource/__init__.py) for the exact types and signatures involved.

### When

**When should I validate an upgrade?** Recheck `tba-protocol-oauth-protected-resource` whenever its source version, declared collaborators, configuration, or caller changes. Run relevant behavioral tests in addition to the README gate before promotion.

---

## Documentation and Related Packages

### More Documentation

The [repository contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md), [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oauth-protected-resource/src/tba_protocol_oauth_protected_resource/__init__.py), and [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oauth-protected-resource/pyproject.toml) provide the supporting context for `tba-protocol-oauth-protected-resource`. The [README policy](https://github.com/groupsum/readme-standards/blob/master/docs/outline.md) defines the common document structure.

### Related Packages

- [tigrbl-identity-resource-server](https://pypi.org/project/tigrbl-identity-resource-server/) remains a deprecated compatibility package.
- [tba-runtime-authorization-policy](https://pypi.org/project/tba-runtime-authorization-policy/) owns policy decision truth.
- [tba-protocol-oauth](https://pypi.org/project/tba-protocol-oauth/) owns OAuth wire behavior.
- [tba-provider-authorization-resource-server-verifier](https://pypi.org/project/tba-provider-authorization-resource-server-verifier/) owns the reusable protected-resource verifier.
- [tba-provider-security-token-jwks-cache](https://pypi.org/project/tba-provider-security-token-jwks-cache/) and [tba-provider-token-introspection](https://pypi.org/project/tba-provider-token-introspection/) own token lookup helpers.
- [tba-provider-security-dpop-cnf-binding-validator](https://pypi.org/project/tba-provider-security-dpop-cnf-binding-validator/), [tba-provider-security-mtls-cnf-binding-validator](https://pypi.org/project/tba-provider-security-mtls-cnf-binding-validator/) provide the concrete confirmation-binding validators; the protected-resource authorization capability composes them.
- [tba-provider-security-proof-dpop](https://pypi.org/project/tba-provider-security-proof-dpop/) owns lower DPoP proof binding comparison.
- [tba-provider-security-certificate-mtls](https://pypi.org/project/tba-provider-security-certificate-mtls/) owns lower certificate binding comparison.

### Project Links

<!-- readme-standards:begin project-links -->
- [Documentation](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/050-protocols/tba-protocol-oauth-protected-resource#readme)
- [Homepage](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/050-protocols/tba-protocol-oauth-protected-resource#readme)
- [Issues](https://github.com/tigrbl/tigrbl_auth/issues)
- [PyPI](https://pypi.org/project/tba-protocol-oauth-protected-resource/)
- [Repository](https://github.com/tigrbl/tigrbl_auth)
- [SSOT](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [Source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/050-protocols/tba-protocol-oauth-protected-resource)
- [pypi: tba-protocol-oauth-protected-resource](https://pypi.org/project/tba-protocol-oauth-protected-resource/)
<!-- readme-standards:end project-links -->

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/050-protocols/tba-protocol-oauth-protected-resource)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oauth-protected-resource/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oauth-protected-resource/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oauth-protected-resource/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-protocol-oauth-protected-resource/)

---

## Contributing

### How to Contribute

Follow the [contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md) and include a focused example or regression for changes to `tba-protocol-oauth-protected-resource`. Keep package behavior, its documented boundary, and its tests aligned.

### Development Setup

Work from the `pkgs/050-protocols/tba-protocol-oauth-protected-resource` checkout. Synchronize its declared development environment with uv, then run the relevant package tests and `python -m pytest docs/readme/test_examples.py`. The repository’s dedicated README job installs `readme-standards==0.1.3` without resolving unrelated runtime packages.

### Notes for Maintainers

Edit authored prose directly in this `tba-protocol-oauth-protected-resource` README. Update source examples in `docs/readme/`, then run `readme-standards render --root . --write` from the package directory and review the diff. Required headings and generated blocks come from package-guide-v1.

---

## Governance

### Ownership and Decision Making

Changes to `tba-protocol-oauth-protected-resource` follow the maintainer review process of [tigrbl/tigrbl_auth](https://github.com/tigrbl/tigrbl_auth) and its contribution guide. Author attribution remains in the [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oauth-protected-resource/pyproject.toml); this README does not assign new publishing or administrative authority.

### Standards and Policies

This package is part of the SSOT-governed TBA package suite. New protected-resource implementation work should prefer this package name over `tigrbl-identity-resource-server`.

`tba-protocol-oauth-protected-resource` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `050-protocols` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

### Lifecycle and Migration

The `tba-protocol-oauth-protected-resource` source version is `0.4.0.dev3`. This change standardizes documentation and adds a development-only gate; it does not publish a new runtime version or declare a previously unpublished package released. Preserve explicit deprecation and replacement instructions where present.

---

## License and Attribution

### License

<!-- readme-standards:begin license -->
Licensed under `Apache-2.0`. See [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oauth-protected-resource/LICENSE).
<!-- readme-standards:end license -->

### Notices

<!-- readme-standards:begin notices -->
See [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oauth-protected-resource/NOTICE) for attribution.
<!-- readme-standards:end notices -->
