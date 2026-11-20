# tba-protocol-oidc-relying-party

<!-- readme-standards:begin branding -->
<p align="center"><a href="https://github.com/tigrbl/tigrbl_auth"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="300"></a></p>
<p align="center"><strong>tba-protocol-oidc-relying-party</strong></p>
<p align="center">OpenID Connect relying-party and OAuth client protocol implementation package for the TBA package suite.</p>
<p align="center">
<a href="https://pypi.org/project/tba-protocol-oidc-relying-party/"><img alt="pypi: tba-protocol-oidc-relying-party" src="https://img.shields.io/pypi/v/tba-protocol-oidc-relying-party"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oidc-relying-party/pyproject.toml"><img alt="Source version: 0.4.0.dev4" src="https://img.shields.io/static/v1?label=Source%20version&amp;message=0.4.0.dev4&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oidc-relying-party/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/static/v1?label=Python&amp;message=%3E%3D3.10%2C%3C3.16&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oidc-relying-party/pyproject.toml"><img alt="Layer: 050-protocols" src="https://img.shields.io/static/v1?label=Layer&amp;message=050-protocols&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oidc-relying-party/README.md#lifecycle-and-migration"><img alt="Lifecycle: active" src="https://img.shields.io/static/v1?label=Lifecycle&amp;message=active&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oidc-relying-party/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/static/v1?label=License&amp;message=Apache-2.0&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oidc-relying-party/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/static/v1?label=Notice&amp;message=attribution&amp;color=525252"></a>
</p>
<p align="center">
<a href="https://pypi.org/project/tba-protocol-oidc-relying-party/"><img alt="Monthly PyPI downloads: tba-protocol-oidc-relying-party" src="https://img.shields.io/pypi/dm/tba-protocol-oidc-relying-party"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oidc-relying-party/README.md"><img alt="README hits: tba-protocol-oidc-relying-party" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/pkgs/050-protocols/tba-protocol-oidc-relying-party/README.md.svg?label=README%20hits"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="README standards: CI gate" src="https://img.shields.io/static/v1?label=README%20standards&amp;message=CI%20gate&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oidc-relying-party/docs/readme/test_examples.py"><img alt="Tests: example source" src="https://img.shields.io/static/v1?label=Tests&amp;message=example%20source&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oidc-relying-party/README.md#certification-status"><img alt="Certification: not certified" src="https://img.shields.io/static/v1?label=Certification&amp;message=not%20certified&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/tools/readme/POLICY.md"><img alt="Governance: repository policy" src="https://img.shields.io/static/v1?label=Governance&amp;message=repository%20policy&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="Evidence: source and CI" src="https://img.shields.io/static/v1?label=Evidence&amp;message=source%20and%20CI&amp;color=525252"></a>
</p>
<p align="center"><a href="#overview">Overview</a> · <a href="#installation">Installation</a> · <a href="#quick-start">Quick Start</a> · <a href="#usage">Usage</a> · <a href="#public-api-and-import-surfaces">API</a> · <a href="#contributing">Contributing</a> · <a href="#governance">Governance</a> · <a href="#license">License</a></p>
<!-- readme-standards:end branding -->

---

## Overview

### Summary

tba-protocol-oidc-relying-party is the protocol-facing package name for OpenID Connect Relying Party and OAuth client behavior. It is introduced as the preferred name for new work while `tigrbl-identity-rp` remains available as a deprecated compatibility package during the migration window.

- Package: `tba-protocol-oidc-relying-party`
- Import root: `tba_protocol_oidc_relying_party`
- Component kind: Auth protocol consumer package
- Use it for discovery consumption, login URL generation, PKCE, callback handling, token exchange, ID-token validation, UserInfo, logout, and RP session helpers.
- PKCE primitive generation and challenge verification are delegated to `tba-provider-security-proof-pkce`; this package keeps the RP/OAuth authorization-parameter wrapper.
- Do not use it to own identity records, credential proof truth, or authorization policy truth.
- Canonical implementation lives in this package; `tigrbl-identity-rp` re-exports this package from `pkgs/deprecated` for compatibility.

### Why This Package

`tba-protocol-oidc-relying-party` isolates this responsibility: OpenID Connect relying-party and OAuth client protocol implementation package for the TBA package suite. Its [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oidc-relying-party/src/tba_protocol_oidc_relying_party/__init__.py) exposes `BrowserMemorySession`, `BrowserStoragePolicy`, `CAPABILITY_REQUIREMENTS`, `COMPATIBILITY_PATHS`, `CURRENT_VERSION`, `CallbackResult`, `DiscoveryClient`, `FEATURES_BY_VERSION`, `JwksCache`, `LoginRequest`, `PkceVerifier`, `RPConfiguration`, `RPError`, `RPSession`, `RP_ID_TOKEN_CLAIMS`, allowing consumers to select this package without treating adjacent packages as part of its public contract.

### When to Use

Choose `tba-protocol-oidc-relying-party` for this responsibility: OpenID Connect relying-party and OAuth client protocol implementation package for the TBA package suite. Its `050-protocols` placement keeps protocol semantics and projections separate from deployment hosting or ownership of persistence implementations.

### Features

- `BrowserMemorySession`: declared in src/tba_protocol_oidc_relying_party/client.py
- `JwksCache`: declared in src/tba_protocol_oidc_relying_party/client.py
- `DiscoveryClient`: declared in src/tba_protocol_oidc_relying_party/client.py
- `UserInfoClient`: declared in src/tba_protocol_oidc_relying_party/client.py
- `RelyingParty`: declared in src/tba_protocol_oidc_relying_party/client.py
- `VerifiedExternalIdentity`: declared in src/tba_protocol_oidc_relying_party/client.py
- `VerifiedCallback`: declared in src/tba_protocol_oidc_relying_party/client.py
- `RpCompatibility`: declared in src/tba_protocol_oidc_relying_party/compatibility.py

### Non-Goals

`tba-protocol-oidc-relying-party` does not take ownership of deployment hosting or ownership of persistence implementations.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

---

## Getting Started

### Prerequisites

Python `>=3.10,<3.16` is required. The [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oidc-relying-party/pyproject.toml) declares runtime dependencies including `tba-concrete-jws`, `tba-provider-jose-cryptography`, `tba-protocol-oidc`, `tba-concrete-claim-audience`, `tba-concrete-claim-authentication-context`, `tba-concrete-claim-authentication-methods`, `tba-concrete-claim-authentication-time`, `tba-concrete-claim-authorized-party`, `tba-concrete-claim-expiration`, `tba-concrete-claim-issued-at`, `tba-concrete-claim-issuer`, `tba-concrete-claim-nonce`. Read the example’s inputs and service requirements before execution.

### Installation

```bash
pip install tba-protocol-oidc-relying-party
# or
uv add tba-protocol-oidc-relying-party
```

Install the current `tba-protocol-oidc-relying-party` source checkout when working ahead of a PyPI release:

```bash
uv pip install ./pkgs/050-protocols/tba-protocol-oidc-relying-party
```

#### uv

<!-- readme-standards:begin installation.uv -->
```bash
uv add tba-protocol-oidc-relying-party
```
<!-- readme-standards:end installation.uv -->

#### pip

<!-- readme-standards:begin installation.pip -->
```bash
python -m pip install tba-protocol-oidc-relying-party
```
<!-- readme-standards:end installation.pip -->

#### Poetry

<!-- readme-standards:begin installation.poetry -->
```bash
poetry add tba-protocol-oidc-relying-party
```
<!-- readme-standards:end installation.poetry -->

### Quick Start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.


```bash
uv run --isolated --no-project --python 3.12 --with "tba-protocol-oidc-relying-party==0.4.0.dev4" python quickstart.py
```

The command prints the keys in the package's capability report.

#### Example

<!-- readme-standards:begin example.quick-start -->
Source: [docs/readme/quick_start.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oidc-relying-party/docs/readme/quick_start.py).

```python
from tba_protocol_oidc_relying_party import capability_report

report = capability_report()
assert report
print(sorted(report))
```
<!-- readme-standards:end example.quick-start -->

#### Expected Result

The example demonstrates the documented `tba-protocol-oidc-relying-party` source boundary or workflow. Complete its required configuration first. README CI checks the maintained source’s syntax and declarations; it does not claim that external services or the application workflow were exercised.

---

## Usage

### Common Workflows

<!-- readme-standards:begin example.usage -->
Source: [docs/readme/usage.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oidc-relying-party/docs/readme/usage.py).

```python
from tba_protocol_oidc_relying_party import (
    RPConfiguration,
    RelyingParty,
    make_pkce_verifier,
)

config = RPConfiguration(issuer="https://id.example.com", client_id="app")
rp = RelyingParty(config)
verifier = make_pkce_verifier()
```
<!-- readme-standards:end example.usage -->

### Configuration

Configure `tba-protocol-oidc-relying-party` through the APIs in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oidc-relying-party/src/tba_protocol_oidc_relying_party/__init__.py); its [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oidc-relying-party/pyproject.toml) describes installation requirements, not an implicit service configuration. No additional package-global configuration contract is inferred from dependencies.

### Error Handling

The inspected `tba-protocol-oidc-relying-party` source raises `RPError`, `TypeError`, `ValueError`. Handle these at the calling boundary and consult the implementation for the triggering conditions.

### Best Practices

Use the explicit `tba-protocol-oidc-relying-party` imports documented below and keep collaborator configuration with the caller. Run the package’s relevant tests after changing `BrowserMemorySession`, `BrowserStoragePolicy`, `CAPABILITY_REQUIREMENTS`, `COMPATIBILITY_PATHS`, `CURRENT_VERSION`, `CallbackResult`, `DiscoveryClient`, `FEATURES_BY_VERSION`, `JwksCache`, `LoginRequest`, `PkceVerifier`, `RPConfiguration`, `RPError`, `RPSession`, `RP_ID_TOKEN_CLAIMS`; an import or successful installation alone does not establish its runtime guarantees.

---

## Package Boundary

### What It Owns

- Relying Party and OAuth client protocol behavior
- Discovery, authorization URL, PKCE, callback, token exchange, UserInfo, logout, and session helpers
- Discovery metadata semantics are consumed from the OIDC protocol package;
  runtime deployment resolution and provider-side publication are not owned by
  the RP package.
- App-side protocol integration consuming an issuer
- Browser/client storage and no-client-secret policy helpers
- The legacy `logout` module exports protocol validation semantics only;
  provider-side durable fanout planning is owned by the identity server runtime.

### Public API and Import Surfaces

Import namespace: `tba_protocol_oidc_relying_party`.

Source-declared exports or types: `BrowserMemorySession`, `BrowserStoragePolicy`, `CAPABILITY_REQUIREMENTS`, `COMPATIBILITY_PATHS`, `CURRENT_VERSION`, `CallbackResult`, `DiscoveryClient`, `FEATURES_BY_VERSION`, `JwksCache`, `LoginRequest`, `PkceVerifier`, `RPConfiguration`, `RPError`, `RPSession`, `RP_ID_TOKEN_CLAIMS`.

Inspect [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oidc-relying-party/src/tba_protocol_oidc_relying_party/__init__.py) for exact signatures; this inventory does not designate every internal module as stable.

### Entry Points

<!-- readme-standards:begin entry-points -->
This package declares no command-line, GUI, or plugin entry points in its manifest.
<!-- readme-standards:end entry-points -->

### Injected Dependencies

Explicit construction inputs and collaborators for `tba-protocol-oidc-relying-party`:

- `BrowserMemorySession` construction inputs: `policy`, `client_secret`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oidc-relying-party/src/tba_protocol_oidc_relying_party/client.py).
- `DiscoveryClient` construction inputs: `fetch`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oidc-relying-party/src/tba_protocol_oidc_relying_party/client.py).
- `UserInfoClient` construction inputs: `fetch`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oidc-relying-party/src/tba_protocol_oidc_relying_party/client.py).
- `RelyingParty` construction inputs: `config`, `state_store`, `session_store`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oidc-relying-party/src/tba_protocol_oidc_relying_party/client.py).
- `validate_id_token_claims` construction inputs: `issuer`, `audience`, `nonce`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oidc-relying-party/src/tba_protocol_oidc_relying_party/client.py).
- `verify_id_token` construction inputs: `verifier`, `issuer`, `audience`, `nonce`, `now`, `userinfo`, `maximum_age`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oidc-relying-party/src/tba_protocol_oidc_relying_party/client.py).
- `migrate_configuration` construction inputs: `source`, `target`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oidc-relying-party/src/tba_protocol_oidc_relying_party/migrations.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

### Protocol Consumers

Direct consumers in this checkout’s package manifests include `tba-auth`, `tba-router-relying-party-session`, `tba-workspace`. These edges describe declared dependencies, not protocol-conformance evidence.

### Extensions

For `tba-protocol-oidc-relying-party`, use the source-declared public interfaces (`BrowserMemorySession`, `BrowserStoragePolicy`, `CAPABILITY_REQUIREMENTS`, `COMPATIBILITY_PATHS`, `CURRENT_VERSION`, `CallbackResult`, `DiscoveryClient`, `FEATURES_BY_VERSION`, `JwksCache`, `LoginRequest`, `PkceVerifier`, `RPConfiguration`, `RPError`, `RPSession`, `RP_ID_TOKEN_CLAIMS`) when composing or extending behavior. Its entry-point section below is authoritative for registered plugins; no additional extension loader is inferred from the package name.

---

## Operations and Readiness

### Operational Requirements

`tba-protocol-oidc-relying-party` exposes protocol semantics and projections. Public operations found in its source:

- `capability_report` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oidc-relying-party/src/tba_protocol_oidc_relying_party/__init__.py).
- `compose_rp_id_token_claim_set` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oidc-relying-party/src/tba_protocol_oidc_relying_party/claims.py).
- `BrowserMemorySession.set` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oidc-relying-party/src/tba_protocol_oidc_relying_party/client.py).
- `BrowserMemorySession.get` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oidc-relying-party/src/tba_protocol_oidc_relying_party/client.py).
- `BrowserMemorySession.clear` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oidc-relying-party/src/tba_protocol_oidc_relying_party/client.py).
- `assert_browser_no_client_secret` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oidc-relying-party/src/tba_protocol_oidc_relying_party/client.py).
- `validate_browser_storage_policy` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oidc-relying-party/src/tba_protocol_oidc_relying_party/client.py).
- `JwksCache.put` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oidc-relying-party/src/tba_protocol_oidc_relying_party/client.py).
- `JwksCache.get` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oidc-relying-party/src/tba_protocol_oidc_relying_party/client.py).
- `DiscoveryClient.discover` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oidc-relying-party/src/tba_protocol_oidc_relying_party/client.py).
- `UserInfoClient.get` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oidc-relying-party/src/tba_protocol_oidc_relying_party/client.py).
- `RelyingParty.build_authorization_url` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oidc-relying-party/src/tba_protocol_oidc_relying_party/client.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

### Health and Observability

This README does not establish a standalone health endpoint for `tba-protocol-oidc-relying-party`. Observe the concrete caller’s results, exceptions, and existing test reports. An application that embeds this package must define its own health and telemetry contract.

### Security and Resource Limits

Apply the input, credential, and resource constraints implemented in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oidc-relying-party/src/tba_protocol_oidc_relying_party/__init__.py). The `tba-protocol-oidc-relying-party` README gate is a documentation check, not a security review or a substitute for the implementation’s limits and caller authorization.

### Compatibility

This source version of `tba-protocol-oidc-relying-party` declares Python `>=3.10,<3.16`. Consult its dependency constraints before upgrading. Source-version and registry-version badges have separate meanings; this migration makes no additional platform or interoperability certification claim.

---

## Verification

### Tests

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oidc-relying-party/src/tba_protocol_oidc_relying_party/__init__.py).

### Certification Status

No external certification is asserted for `tba-protocol-oidc-relying-party` by this documentation migration. README conformance, example syntax, runtime tests, and protocol or security certification are distinct evidence scopes.

### Evidence

The [README standards CI](https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml) records mechanical documentation results for its tested commit. The [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oidc-relying-party/src/tba_protocol_oidc_relying_party/__init__.py) and example sources support the package-boundary description; external runtime behavior requires its own test evidence.

---

## FAQ

### Why

**Why select this package?** `tba-protocol-oidc-relying-party` provides openID Connect relying-party and OAuth client protocol implementation package for the TBA package suite; use its own API boundary rather than assuming neighboring packages are bundled or configured automatically.

### How

**How do I start?** Install or synchronize the environment under Getting Started, follow the maintained example for `tba-protocol-oidc-relying-party`, and consult [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oidc-relying-party/src/tba_protocol_oidc_relying_party/__init__.py) for the exact types and signatures involved.

### When

**When should I validate an upgrade?** Recheck `tba-protocol-oidc-relying-party` whenever its source version, declared collaborators, configuration, or caller changes. Run relevant behavioral tests in addition to the README gate before promotion.

---

## Documentation and Related Packages

### More Documentation

The [repository contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md), [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oidc-relying-party/src/tba_protocol_oidc_relying_party/__init__.py), and [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oidc-relying-party/pyproject.toml) provide the supporting context for `tba-protocol-oidc-relying-party`. The [README policy](https://github.com/groupsum/readme-standards/blob/master/docs/outline.md) defines the common document structure.

### Related Packages

- [tigrbl-identity-rp](https://pypi.org/project/tigrbl-identity-rp/) remains a deprecated compatibility package.
- [tba-protocol-oauth](https://pypi.org/project/tba-protocol-oauth/) owns OAuth provider protocol behavior.
- [tba-protocol-oidc](https://pypi.org/project/tba-protocol-oidc/) owns OIDC provider protocol behavior.

### Project Links

<!-- readme-standards:begin project-links -->
- [Documentation](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/050-protocols/tba-protocol-oidc-relying-party#readme)
- [Homepage](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/050-protocols/tba-protocol-oidc-relying-party#readme)
- [Issues](https://github.com/tigrbl/tigrbl_auth/issues)
- [PyPI](https://pypi.org/project/tba-protocol-oidc-relying-party/)
- [Repository](https://github.com/tigrbl/tigrbl_auth)
- [SSOT](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [Source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/050-protocols/tba-protocol-oidc-relying-party)
- [pypi: tba-protocol-oidc-relying-party](https://pypi.org/project/tba-protocol-oidc-relying-party/)
<!-- readme-standards:end project-links -->

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/050-protocols/tba-protocol-oidc-relying-party)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oidc-relying-party/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oidc-relying-party/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oidc-relying-party/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-protocol-oidc-relying-party/)

---

## Contributing

### How to Contribute

Follow the [contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md) and include a focused example or regression for changes to `tba-protocol-oidc-relying-party`. Keep package behavior, its documented boundary, and its tests aligned.

### Development Setup

Work from the `pkgs/050-protocols/tba-protocol-oidc-relying-party` checkout. Synchronize its declared development environment with uv, then run the relevant package tests and `python -m pytest docs/readme/test_examples.py`. The repository’s dedicated README job installs `readme-standards==0.1.1` without resolving unrelated runtime packages.

### Notes for Maintainers

Edit authored prose directly in this `tba-protocol-oidc-relying-party` README. Update source examples in `docs/readme/`, then run `readme-standards render --root . --write` from the package directory and review the diff. Required headings and generated blocks come from package-guide-v1.

---

## Governance

### Ownership and Decision Making

Changes to `tba-protocol-oidc-relying-party` follow the maintainer review process of [tigrbl/tigrbl_auth](https://github.com/tigrbl/tigrbl_auth) and its contribution guide. Author attribution remains in the [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oidc-relying-party/pyproject.toml); this README does not assign new publishing or administrative authority.

### Standards and Policies

This package is part of the SSOT-governed TBA package suite. New RP implementation work should prefer this package name over `tigrbl-identity-rp`.

`tba-protocol-oidc-relying-party` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `050-protocols` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

### Lifecycle and Migration

The `tba-protocol-oidc-relying-party` source version is `0.4.0.dev4`. This change standardizes documentation and adds a development-only gate; it does not publish a new runtime version or declare a previously unpublished package released. Preserve explicit deprecation and replacement instructions where present.

---

## License and Attribution

### License

<!-- readme-standards:begin license -->
Licensed under `Apache-2.0`. See [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oidc-relying-party/LICENSE).
<!-- readme-standards:end license -->

### Notices

<!-- readme-standards:begin notices -->
See [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oidc-relying-party/NOTICE) for attribution.
<!-- readme-standards:end notices -->
