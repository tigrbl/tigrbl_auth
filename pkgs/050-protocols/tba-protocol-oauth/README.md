# tba-protocol-oauth

<!-- readme-standards:begin branding -->
<p align="center"><a href="https://github.com/tigrbl/tigrbl_auth"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="300"></a></p>
<p align="center"><strong>tba-protocol-oauth</strong></p>
<p align="center">OAuth 2.x and OAuth 2.1 profile protocol implementation package for the TBA package suite.</p>
<p align="center">
<a href="https://pypi.org/project/tba-protocol-oauth/"><img alt="pypi: tba-protocol-oauth" src="https://img.shields.io/pypi/v/tba-protocol-oauth?labelColor=1E293B&amp;color=1D4ED8"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oauth/pyproject.toml"><img alt="Source version: 0.4.0.dev3" src="https://img.shields.io/static/v1?label=Source%20version&amp;message=0.4.0.dev3&amp;labelColor=1E293B&amp;color=4338CA"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oauth/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/static/v1?label=Python&amp;message=%3E%3D3.10%2C%3C3.16&amp;labelColor=1E293B&amp;color=0F766E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oauth/pyproject.toml"><img alt="Layer: 050-protocols" src="https://img.shields.io/static/v1?label=Layer&amp;message=050-protocols&amp;labelColor=1E293B&amp;color=6D28D9"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oauth/README.md#lifecycle-and-migration"><img alt="Lifecycle: active" src="https://img.shields.io/static/v1?label=Lifecycle&amp;message=active&amp;labelColor=1E293B&amp;color=166534"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oauth/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/static/v1?label=License&amp;message=Apache-2.0&amp;labelColor=1E293B&amp;color=86198F"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oauth/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/static/v1?label=Notice&amp;message=attribution&amp;labelColor=1E293B&amp;color=86198F"></a>
</p>
<p align="center">
<a href="https://pypi.org/project/tba-protocol-oauth/"><img alt="Monthly PyPI downloads: tba-protocol-oauth" src="https://img.shields.io/pypi/dm/tba-protocol-oauth?labelColor=1E293B&amp;color=0E7490"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oauth/README.md"><img alt="README hits: tba-protocol-oauth" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/pkgs/050-protocols/tba-protocol-oauth/README.md.svg?label=README%20hits&amp;labelColor=1E293B&amp;color=0E7490"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="README standards: CI gate" src="https://img.shields.io/static/v1?label=README%20standards&amp;message=CI%20gate&amp;labelColor=1E293B&amp;color=1D4ED8"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oauth/docs/readme/test_examples.py"><img alt="Tests: example source" src="https://img.shields.io/static/v1?label=Tests&amp;message=example%20source&amp;labelColor=1E293B&amp;color=0F766E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oauth/README.md#certification-status"><img alt="Certification: not certified" src="https://img.shields.io/static/v1?label=Certification&amp;message=not%20certified&amp;labelColor=1E293B&amp;color=92400E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/tools/readme/POLICY.md"><img alt="Governance: repository policy" src="https://img.shields.io/static/v1?label=Governance&amp;message=repository%20policy&amp;labelColor=1E293B&amp;color=4338CA"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="Evidence: source and CI" src="https://img.shields.io/static/v1?label=Evidence&amp;message=source%20and%20CI&amp;labelColor=1E293B&amp;color=6D28D9"></a>
</p>
<p align="center"><a href="#overview">Overview</a> · <a href="#installation">Installation</a> · <a href="#quick-start">Quick Start</a> · <a href="#usage">Usage</a> · <a href="#public-api-and-import-surfaces">API</a> · <a href="#contributing">Contributing</a> · <a href="#governance">Governance</a> · <a href="#license">License</a></p>
<!-- readme-standards:end branding -->

---

## Overview

### Summary

tba-protocol-oauth is the protocol-facing package name for OAuth 2.x, OAuth 2.1 profile behavior, and OAuth extension RFC surfaces. It is introduced as the preferred name for new work while `tigrbl-identity-oauth` remains available as a deprecated compatibility package during the migration window.

- Package: `tba-protocol-oauth`
- Import root: `tba_protocol_oauth`
- Component kind: Auth protocol package
- Use it for OAuth wire behavior, RFC helpers, grant flows, PAR, RAR, dynamic client registration, token exchange, DPoP, and mTLS protocol logic.
- Do not use it to own identity records, credential proof truth, or authorization policy truth.
- Canonical implementation lives in this package; `tigrbl-identity-oauth` re-exports this package from `pkgs/deprecated` for compatibility.

### Why This Package

`tba-protocol-oauth` isolates this responsibility: OAuth 2.x and OAuth 2.1 profile protocol implementation package for the TBA package suite. Its [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oauth/src/tba_protocol_oauth/__init__.py) exposes `AuthorizationCodeGrantForm`, `CAPABILITY_REQUIREMENTS`, `COMPATIBILITY_PATHS`, `CURRENT_VERSION`, `DPoPProof`, `DeviceAuthorization`, `DeviceAuthorizationIn`, `DeviceAuthorizationOut`, `DynamicClientRegistrationIn`, `DynamicClientRegistrationManagementIn`, `DynamicClientRegistrationOut`, `EXTENSION_SPECIFICATIONS`, `FEATURES_BY_VERSION`, `InMemoryOAuthRepository`, `InMemoryOAuthState`, allowing consumers to select this package without treating adjacent packages as part of its public contract.

### When to Use

Choose `tba-protocol-oauth` for this responsibility: OAuth 2.x and OAuth 2.1 profile protocol implementation package for the TBA package suite. Its `050-protocols` placement keeps protocol semantics and projections separate from deployment hosting or ownership of persistence implementations.

### Features

- `OAuthCompatibility`: declared in src/tba_protocol_oauth/compatibility.py
- `OAuthProtocolError`: Base error for an OAuth wire or profile failure.
- `UnsupportedOAuthRevisionError`: Raised when an OAuth profile revision has no supported path.
- `OAuthBindingError`: Raised when an OAuth wire element cannot map to a capability.
- `OAuthError`: Backward-compatible concrete OAuth service error.
- `OAuthStateOperations`: declared in src/tba_protocol_oauth/protocol.py
- `InMemoryOAuthState`: declared in src/tba_protocol_oauth/protocol.py
- `OAuthProtocolService`: declared in src/tba_protocol_oauth/protocol.py

### Non-Goals

`tba-protocol-oauth` does not take ownership of deployment hosting or ownership of persistence implementations.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

---

## Getting Started

### Prerequisites

Python `>=3.10,<3.16` is required. The [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oauth/pyproject.toml) declares runtime dependencies including `pydantic`, `tba-contracts-identity`, `tba-capability-token-introspection`, `tba-capability-token-issuance`, `tba-capability-token-revocation`, `tba-capability-authorization-request-staging`, `tba-capability-client-registration`, `tba-primitives-identity`, `tba-provider-identity-jose`, `tba-contracts-security-trust`, `tba-provider-security-proof-pkce`. Read the example’s inputs and service requirements before execution.

### Installation

```bash
pip install tba-protocol-oauth
# or
uv add tba-protocol-oauth
```

Install the current `tba-protocol-oauth` source checkout when working ahead of a PyPI release:

```bash
uv pip install ./pkgs/050-protocols/tba-protocol-oauth
```

#### uv

<!-- readme-standards:begin installation.uv -->
```bash
uv add tba-protocol-oauth
```
<!-- readme-standards:end installation.uv -->

#### pip

<!-- readme-standards:begin installation.pip -->
```bash
python -m pip install tba-protocol-oauth
```
<!-- readme-standards:end installation.pip -->

#### Poetry

<!-- readme-standards:begin installation.poetry -->
```bash
poetry add tba-protocol-oauth
```
<!-- readme-standards:end installation.poetry -->

### Quick Start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.


```bash
uv run --isolated --no-project --python 3.12 --with "tba-protocol-oauth==0.4.0.dev3" python quickstart.py
```

The command prints the keys in the package's capability report.

#### Example

<!-- readme-standards:begin example.quick-start -->
Source: [docs/readme/quick_start.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oauth/docs/readme/quick_start.py).

```python
from tba_protocol_oauth import capability_report

report = capability_report()
assert report
print(sorted(report))
```
<!-- readme-standards:end example.quick-start -->

#### Expected Result

The example demonstrates the documented `tba-protocol-oauth` source boundary or workflow. Complete its required configuration first. README CI checks the maintained source’s syntax and declarations; it does not claim that external services or the application workflow were exercised.

---

## Usage

GNAP consumers can install `tba-protocol-gnap` separately and import
`GnapRequest` or `parse_gnap_request` from `tba_protocol_gnap`. Update callers of
the former `tba_protocol_oauth.standards.gnap` import to use that path.

HTTP adapters can call `resolve_client_registration_scopes` with the raw
registration `scope` string, or `None` when the field is omitted. Supply the
server's supported scopes and a default selected by trusted server configuration.
For example, a read-only profile may default to `("journal:read",)` and an
editorial profile may default to `("journal:read", "journal:publish")`.
An explicit scope declaration replaces the default and must be nonempty and
supported. Return and persist the resolved tuple as the client's scope ceiling.
Use `validate_client_authorization_scopes` with the persisted ceiling before
staging consent. A registered scope is eligible to request and does not grant
access without user approval and the deployment's authorization policy.

### Common Workflows

<!-- readme-standards:begin example.usage -->
Source: [docs/readme/usage.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oauth/docs/readme/usage.py).

```python
from tba_protocol_oauth import OAuthClient, OAuthProtocolService

service = OAuthProtocolService()
client = OAuthClient(
    client_id="client-a", redirect_uris=("https://app.example/callback",)
)
```
<!-- readme-standards:end example.usage -->

### Configuration

The [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oauth/src/tba_protocol_oauth/__init__.py) references configuration keys `AUTHN_ISSUER`. Consult the constructor or function signature before supplying them; a referenced key is not necessarily a global environment variable.

### Error Handling

The inspected `tba-protocol-oauth` source raises `ClientRegistrationManagementDisabledError`, `DynamicClientRegistrationDisabledError`, `IntrospectionDisabledError`, `InvalidTokenError`, `IssuerIdentificationError`, `NotImplementedError`, `OAuthError`, `OAuthPolicyViolation`, `PushedAuthorizationDisabledError`, `PushedAuthorizationRequestError`. Handle these at the calling boundary and consult the implementation for the triggering conditions.

### Best Practices

Use the explicit `tba-protocol-oauth` imports documented below and keep collaborator configuration with the caller. Run the package’s relevant tests after changing `AuthorizationCodeGrantForm`, `CAPABILITY_REQUIREMENTS`, `COMPATIBILITY_PATHS`, `CURRENT_VERSION`, `DPoPProof`, `DeviceAuthorization`, `DeviceAuthorizationIn`, `DeviceAuthorizationOut`, `DynamicClientRegistrationIn`, `DynamicClientRegistrationManagementIn`, `DynamicClientRegistrationOut`, `EXTENSION_SPECIFICATIONS`, `FEATURES_BY_VERSION`, `InMemoryOAuthRepository`, `InMemoryOAuthState`; an import or successful installation alone does not establish its runtime guarantees.

---

## Package Boundary

The OAuth package owns OAuth registration, authorization, and token exchanges.
Deployments that offer GNAP too compose the standalone package explicitly.
See the [OAuth and GNAP boundary](../../../architecture/oauth-gnap-protocol-boundary.md).

### What It Owns

- OAuth authorization and token protocol behavior
- `versions.py` owns only the OAuth authorization-framework lineage. Extension
  RFCs retain independent identities in `EXTENSION_SPECIFICATIONS` and in
  their capability-requirement revisions.
- `features.py`, `compatibility.py`, and `migrations.py` own revision selection,
  feature flags, and supported OAuth 2.0-to-2.1 migration paths.
- `claims.py`, `schemas.py`, `bindings.py`, and `errors.py` own OAuth wire
  composition without taking ownership of standalone claim implementations.
- RFC 9700 policy evaluation consumes an injected resolved deployment profile;
  request and default-profile resolution remain in layer 60.
- `schemas.py` owns OAuth token, introspection, revocation, device authorization,
  PAR, and dynamic-client-registration wire models.
- PKCE, PAR, RAR, JAR, device authorization, token exchange, DPoP, mTLS, and resource indicators
- Dynamic client registration and registration management protocol behavior
- Provider-facing OAuth wire validation below API front-door assembly
- Durable records and mutations remain in layers 01 and 30; this package does
  not attach protocol schemas to mapped storage classes.

### Public API and Import Surfaces

Import namespace: `tba_protocol_oauth`.

Source-declared exports or types: `AuthorizationCodeGrantForm`, `CAPABILITY_REQUIREMENTS`, `COMPATIBILITY_PATHS`, `CURRENT_VERSION`, `DPoPProof`, `DeviceAuthorization`, `DeviceAuthorizationIn`, `DeviceAuthorizationOut`, `DynamicClientRegistrationIn`, `DynamicClientRegistrationManagementIn`, `DynamicClientRegistrationOut`, `EXTENSION_SPECIFICATIONS`, `FEATURES_BY_VERSION`, `InMemoryOAuthRepository`, `InMemoryOAuthState`.

Inspect [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oauth/src/tba_protocol_oauth/__init__.py) for exact signatures; this inventory does not designate every internal module as stable.

### Entry Points

<!-- readme-standards:begin entry-points -->
This package declares no command-line, GUI, or plugin entry points in its manifest.
<!-- readme-standards:end entry-points -->

### Injected Dependencies

Explicit construction inputs and collaborators for `tba-protocol-oauth`:

- `OAuthProtocolError` construction inputs: `code`, `description`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oauth/src/tba_protocol_oauth/errors.py).
- `migrate_client` construction inputs: `source`, `target`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oauth/src/tba_protocol_oauth/migrations.py).
- `OAuthProtocolService` construction inputs: `operations`, `now`, `repository`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oauth/src/tba_protocol_oauth/protocol.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

### Protocol Consumers

The following layer-50 manifests directly depend on `tba-protocol-oauth`:

- [tba-protocol-oauth-protected-resource](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oauth-protected-resource/README.md)
- [tba-protocol-oidc](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oidc/README.md)

Other direct consumers include [tba-app-backend-core](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-core/README.md), [tba-auth](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-auth/README.md), [tba-router-oauth-authorization-server-metadata](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-oauth-authorization-server-metadata/README.md), [tba-router-oauth-device-authorization](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-oauth-device-authorization/README.md), [tba-router-oauth-introspection](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-oauth-introspection/README.md), [tba-router-oauth-protected-resource-metadata](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-oauth-protected-resource-metadata/README.md).

### Extensions

For `tba-protocol-oauth`, use the source-declared public interfaces (`AuthorizationCodeGrantForm`, `CAPABILITY_REQUIREMENTS`, `COMPATIBILITY_PATHS`, `CURRENT_VERSION`, `DPoPProof`, `DeviceAuthorization`, `DeviceAuthorizationIn`, `DeviceAuthorizationOut`, `DynamicClientRegistrationIn`, `DynamicClientRegistrationManagementIn`, `DynamicClientRegistrationOut`, `EXTENSION_SPECIFICATIONS`, `FEATURES_BY_VERSION`, `InMemoryOAuthRepository`, `InMemoryOAuthState`) when composing or extending behavior. Its entry-point section below is authoritative for registered plugins; no additional extension loader is inferred from the package name.

---

## Operations and Readiness

### Operational Requirements

`tba-protocol-oauth` exposes protocol semantics and projections. Public operations found in its source:

- `capability_report` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oauth/src/tba_protocol_oauth/__init__.py).
- `compose_oauth_claim_set` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oauth/src/tba_protocol_oauth/claims.py).
- `compose_dpop_proof_claim_set` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oauth/src/tba_protocol_oauth/claims.py).
- `compose_token_exchange_claim_set` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oauth/src/tba_protocol_oauth/claims.py).
- `compatibility` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oauth/src/tba_protocol_oauth/compatibility.py).
- `supports` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oauth/src/tba_protocol_oauth/features.py).
- `migrate_client` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oauth/src/tba_protocol_oauth/migrations.py).
- `InMemoryOAuthState.save_client` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oauth/src/tba_protocol_oauth/protocol.py).
- `InMemoryOAuthState.get_client` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oauth/src/tba_protocol_oauth/protocol.py).
- `InMemoryOAuthState.save_device_authorization` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oauth/src/tba_protocol_oauth/protocol.py).
- `InMemoryOAuthState.get_device_authorization` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oauth/src/tba_protocol_oauth/protocol.py).
- `InMemoryOAuthState.remember_dpop_jti` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oauth/src/tba_protocol_oauth/protocol.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

### Health and Observability

This README does not establish a standalone health endpoint for `tba-protocol-oauth`. Observe the concrete caller’s results, exceptions, and existing test reports. An application that embeds this package must define its own health and telemetry contract.

### Security and Resource Limits

Apply the input, credential, and resource constraints implemented in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oauth/src/tba_protocol_oauth/__init__.py). The `tba-protocol-oauth` README gate is a documentation check, not a security review or a substitute for the implementation’s limits and caller authorization.

### Compatibility

This source version of `tba-protocol-oauth` declares Python `>=3.10,<3.16`. Consult its dependency constraints before upgrading. Source-version and registry-version badges have separate meanings; this migration makes no additional platform or interoperability certification claim.

---

## Verification

### Tests

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oauth/src/tba_protocol_oauth/__init__.py).

### Certification Status

No external certification is asserted for `tba-protocol-oauth` by this documentation migration. README conformance, example syntax, runtime tests, and protocol or security certification are distinct evidence scopes.

### Evidence

The [README standards CI](https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml) records mechanical documentation results for its tested commit. The [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oauth/src/tba_protocol_oauth/__init__.py) and example sources support the package-boundary description; external runtime behavior requires its own test evidence.

---

## FAQ

### Why

**Why select this package?** `tba-protocol-oauth` provides oAuth 2.x and OAuth 2.1 profile protocol implementation package for the TBA package suite; use its own API boundary rather than assuming neighboring packages are bundled or configured automatically.

### How

**How do I start?** Install or synchronize the environment under Getting Started, follow the maintained example for `tba-protocol-oauth`, and consult [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oauth/src/tba_protocol_oauth/__init__.py) for the exact types and signatures involved.

### When

**When should I validate an upgrade?** Recheck `tba-protocol-oauth` whenever its source version, declared collaborators, configuration, or caller changes. Run relevant behavioral tests in addition to the README gate before promotion.

---

## Documentation and Related Packages

### More Documentation

The [repository contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md), [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oauth/src/tba_protocol_oauth/__init__.py), and [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oauth/pyproject.toml) provide the supporting context for `tba-protocol-oauth`. The [README policy](https://github.com/groupsum/readme-standards/blob/master/docs/outline.md) defines the common document structure.

### Related Packages

- [tigrbl-identity-oauth](https://pypi.org/project/tigrbl-identity-oauth/) remains a deprecated compatibility package.
- [tba-protocol-oidc](https://pypi.org/project/tba-protocol-oidc/) owns OIDC provider protocol behavior.
- [tba-runtime-authorization-policy](https://pypi.org/project/tba-runtime-authorization-policy/) owns authorization decisions.

### Project Links

<!-- readme-standards:begin project-links -->
- [Documentation](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/050-protocols/tba-protocol-oauth#readme)
- [Homepage](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/050-protocols/tba-protocol-oauth#readme)
- [Issues](https://github.com/tigrbl/tigrbl_auth/issues)
- [PyPI](https://pypi.org/project/tba-protocol-oauth/)
- [Repository](https://github.com/tigrbl/tigrbl_auth)
- [SSOT](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [Source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/050-protocols/tba-protocol-oauth)
- [pypi: tba-protocol-oauth](https://pypi.org/project/tba-protocol-oauth/)
<!-- readme-standards:end project-links -->

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/050-protocols/tba-protocol-oauth)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oauth/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oauth/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oauth/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-protocol-oauth/)

---

## Contributing

### How to Contribute

Follow the [contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md) and include a focused example or regression for changes to `tba-protocol-oauth`. Keep package behavior, its documented boundary, and its tests aligned.

### Development Setup

Work from the `pkgs/050-protocols/tba-protocol-oauth` checkout. Synchronize its declared development environment with uv, then run the relevant package tests and `python -m pytest docs/readme/test_examples.py`. The repository’s dedicated README job installs `readme-standards==0.1.3` without resolving unrelated runtime packages.

### Notes for Maintainers

Edit authored prose directly in this `tba-protocol-oauth` README. Update source examples in `docs/readme/`, then run `readme-standards render --root . --write` from the package directory and review the diff. Required headings and generated blocks come from package-guide-v1.

---

## Governance

### Ownership and Decision Making

Changes to `tba-protocol-oauth` follow the maintainer review process of [tigrbl/tigrbl_auth](https://github.com/tigrbl/tigrbl_auth) and its contribution guide. Author attribution remains in the [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oauth/pyproject.toml); this README does not assign new publishing or administrative authority.

### Standards and Policies

This package is part of the SSOT-governed TBA package suite. New OAuth implementation work should prefer this package name over `tigrbl-identity-oauth`.

`tba-protocol-oauth` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `050-protocols` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

### Lifecycle and Migration

The `tba-protocol-oauth` source version is `0.4.0.dev3`. This change standardizes documentation and adds a development-only gate; it does not publish a new runtime version or declare a previously unpublished package released. Preserve explicit deprecation and replacement instructions where present.

---

## License and Attribution

### License

<!-- readme-standards:begin license -->
Licensed under `Apache-2.0`. See [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oauth/LICENSE).
<!-- readme-standards:end license -->

### Notices

<!-- readme-standards:begin notices -->
See [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oauth/NOTICE) for attribution.
<!-- readme-standards:end notices -->
