# tba-protocol-oidc

<!-- readme-standards:begin branding -->
<p align="center"><a href="https://github.com/tigrbl/tigrbl_auth"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="300"></a></p>
<p align="center"><strong>tba-protocol-oidc</strong></p>
<p align="center">OpenID Connect provider protocol implementation package for the TBA package suite.</p>
<p align="center">
<a href="https://pypi.org/project/tba-protocol-oidc/"><img alt="pypi: tba-protocol-oidc" src="https://img.shields.io/pypi/v/tba-protocol-oidc"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oidc/pyproject.toml"><img alt="Source version: 0.4.0.dev3" src="https://img.shields.io/static/v1?label=Source%20version&amp;message=0.4.0.dev3&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oidc/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/static/v1?label=Python&amp;message=%3E%3D3.10%2C%3C3.16&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oidc/pyproject.toml"><img alt="Layer: 050-protocols" src="https://img.shields.io/static/v1?label=Layer&amp;message=050-protocols&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oidc/README.md#lifecycle-and-migration"><img alt="Lifecycle: active" src="https://img.shields.io/static/v1?label=Lifecycle&amp;message=active&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oidc/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/static/v1?label=License&amp;message=Apache-2.0&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oidc/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/static/v1?label=Notice&amp;message=attribution&amp;color=525252"></a>
</p>
<p align="center">
<a href="https://pypi.org/project/tba-protocol-oidc/"><img alt="Monthly PyPI downloads: tba-protocol-oidc" src="https://img.shields.io/pypi/dm/tba-protocol-oidc"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oidc/README.md"><img alt="README hits: tba-protocol-oidc" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/pkgs/050-protocols/tba-protocol-oidc/README.md.svg?label=README%20hits"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="README standards: CI gate" src="https://img.shields.io/static/v1?label=README%20standards&amp;message=CI%20gate&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oidc/docs/readme/test_examples.py"><img alt="Tests: example source" src="https://img.shields.io/static/v1?label=Tests&amp;message=example%20source&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oidc/README.md#certification-status"><img alt="Certification: not certified" src="https://img.shields.io/static/v1?label=Certification&amp;message=not%20certified&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/tools/readme/POLICY.md"><img alt="Governance: repository policy" src="https://img.shields.io/static/v1?label=Governance&amp;message=repository%20policy&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="Evidence: source and CI" src="https://img.shields.io/static/v1?label=Evidence&amp;message=source%20and%20CI&amp;color=525252"></a>
</p>
<p align="center"><a href="#overview">Overview</a> · <a href="#installation">Installation</a> · <a href="#quick-start">Quick Start</a> · <a href="#usage">Usage</a> · <a href="#public-api-and-import-surfaces">API</a> · <a href="#contributing">Contributing</a> · <a href="#governance">Governance</a> · <a href="#license">License</a></p>
<!-- readme-standards:end branding -->

---

## Overview

### Summary

tba-protocol-oidc is the protocol-facing package name for OpenID Connect provider behavior. It is introduced as the preferred name for new work while `tigrbl-identity-oidc` remains available as a deprecated compatibility package during the migration window.

- Package: `tba-protocol-oidc`
- Import root: `tba_protocol_oidc`
- Component kind: Auth protocol package
- Use it for OIDC discovery, ID Token, UserInfo, session, logout, and claim protocol behavior.
- Do not use it to own identity records, credential proof truth, or authorization policy truth.
- Canonical OIDC protocol behavior lives in this package; deterministic Back-Channel Logout replay tracking is table-owned by `tba-storage-core` through `BackchannelLogoutReplay`, and `tigrbl-identity-oidc` re-exports this package from `pkgs/deprecated` for compatibility.

### Why This Package

`tba-protocol-oidc` isolates this responsibility: OpenID Connect provider protocol implementation package for the TBA package suite. Its [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oidc/src/tba_protocol_oidc/__init__.py) exposes `CAPABILITY_REQUIREMENTS`, `COMPATIBILITY_PATHS`, `CURRENT_VERSION`, `FEATURES_BY_VERSION`, `HostedLoginPage`, `HostedLoginRequest`, `LoginThemeAssetPolicy`, `LogoutIn`, `LogoutOut`, `LogoutPlan`, `LogoutRequest`, `OIDC_EXTENSION_CLAIMS`, `OIDC_ID_TOKEN_PROFILE_CLAIMS`, `OIDC_USERINFO_CLAIMS`, `OidcBindingError`, allowing consumers to select this package without treating adjacent packages as part of its public contract.

### When to Use

Choose `tba-protocol-oidc` for this responsibility: OpenID Connect provider protocol implementation package for the TBA package suite. Its `050-protocols` placement keeps protocol semantics and projections separate from deployment hosting or ownership of persistence implementations.

### Features

- `OidcCompatibility`: declared in src/tba_protocol_oidc/compatibility.py
- `OidcProtocolError`: Base error for a versioned OIDC wire mapping failure.
- `UnsupportedOidcRevisionError`: Raised when no compatibility path exists for a requested revision.
- `OidcBindingError`: Raised when a wire element cannot map to its semantic capability.
- `TenantBrandingRegistry`: declared in src/tba_protocol_oidc/provider.py
- `OidcProviderRuntime`: declared in src/tba_protocol_oidc/provider.py
- `LogoutIn`: declared in src/tba_protocol_oidc/schemas.py
- `LogoutOut`: declared in src/tba_protocol_oidc/schemas.py

### Non-Goals

`tba-protocol-oidc` does not take ownership of deployment hosting or ownership of persistence implementations.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

---

## Getting Started

### Prerequisites

Python `>=3.10,<3.16` is required. The [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oidc/pyproject.toml) declares runtime dependencies including `pydantic`, `tba-protocol-oauth`, `tba-contracts-identity`, `tba-primitives-identity`, `tba-provider-identity-jose`, `tba-concrete-identity-assurance`, `tba-provider-claims-local`, `tba-concrete-public-subject-identifier`, `tba-concrete-pairwise-subject-identifier`, `tba-concrete-claim-authentication-time`, `tba-concrete-claim-nonce`, `tba-concrete-claim-authentication-context`. Read the example’s inputs and service requirements before execution.

### Installation

```bash
pip install tba-protocol-oidc
# or
uv add tba-protocol-oidc
```

Install the current `tba-protocol-oidc` source checkout when working ahead of a PyPI release:

```bash
uv pip install ./pkgs/050-protocols/tba-protocol-oidc
```

#### uv

<!-- readme-standards:begin installation.uv -->
```bash
uv add tba-protocol-oidc
```
<!-- readme-standards:end installation.uv -->

#### pip

<!-- readme-standards:begin installation.pip -->
```bash
python -m pip install tba-protocol-oidc
```
<!-- readme-standards:end installation.pip -->

#### Poetry

<!-- readme-standards:begin installation.poetry -->
```bash
poetry add tba-protocol-oidc
```
<!-- readme-standards:end installation.poetry -->

### Quick Start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.


```bash
uv run --isolated --no-project --python 3.12 --with "tba-protocol-oidc==0.4.0.dev3" python quickstart.py
```

The command prints the keys in the package's capability report.

#### Example

<!-- readme-standards:begin example.quick-start -->
Source: [docs/readme/quick_start.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oidc/docs/readme/quick_start.py).

```python
from tba_protocol_oidc import capability_report

report = capability_report()
assert report
print(sorted(report))
```
<!-- readme-standards:end example.quick-start -->

#### Expected Result

The example demonstrates the documented `tba-protocol-oidc` source boundary or workflow. Complete its required configuration first. README CI checks the maintained source’s syntax and declarations; it does not claim that external services or the application workflow were exercised.

---

## Usage

### Common Workflows

<!-- readme-standards:begin example.usage -->
Source: [docs/readme/usage.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oidc/docs/readme/usage.py).

```python
from tba_protocol_oidc import OidcProviderRuntime, TenantBrandingRegistry

runtime = OidcProviderRuntime(branding=TenantBrandingRegistry())
```
<!-- readme-standards:end example.usage -->

### Configuration

Configure `tba-protocol-oidc` through the APIs in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oidc/src/tba_protocol_oidc/__init__.py); its [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oidc/pyproject.toml) describes installation requirements, not an implicit service configuration. No additional package-global configuration contract is inferred from dependencies.

### Error Handling

The inspected `tba-protocol-oidc` source raises `HTTPException`, `InvalidTokenError`, `OidcProviderError`, `RuntimeError`, `TypeError`, `ValueError`. Handle these at the calling boundary and consult the implementation for the triggering conditions.

### Best Practices

Use the explicit `tba-protocol-oidc` imports documented below and keep collaborator configuration with the caller. Run the package’s relevant tests after changing `CAPABILITY_REQUIREMENTS`, `COMPATIBILITY_PATHS`, `CURRENT_VERSION`, `FEATURES_BY_VERSION`, `HostedLoginPage`, `HostedLoginRequest`, `LoginThemeAssetPolicy`, `LogoutIn`, `LogoutOut`, `LogoutPlan`, `LogoutRequest`, `OIDC_EXTENSION_CLAIMS`, `OIDC_ID_TOKEN_PROFILE_CLAIMS`, `OIDC_USERINFO_CLAIMS`, `OidcBindingError`; an import or successful installation alone does not establish its runtime guarantees.

---

## Package Boundary

### What It Owns

- OpenID Provider metadata and discovery behavior
- Discovery metadata projection consumes an injected deployment view; profile
  resolution, caching, HTTP publication, and artifact file operations remain
  in layers 60 and 80.
- ID Token, UserInfo, claims, `acr`, `amr`, session, and logout protocol behavior
- Session management owns only session-state projection and validation;
  browser-cookie and durable session lifecycle operations are composed by the
  layer-60 server runtime.
- Front-channel, back-channel, and RP-initiated logout modules consume injected
  registration metadata and replay operations. Durable logout planning and
  delivery-state updates are composed by the layer-60 server runtime.
- `schemas.py` owns OIDC logout request and response wire models.
- Provider-facing OIDC wire validation below API front-door assembly
- OIDC behavior layered on OAuth protocol foundations
- Durable session/logout records remain in layers 01 and 30; this package does
  not attach OIDC schemas to mapped storage classes.

### Public API and Import Surfaces

Import namespace: `tba_protocol_oidc`.

Source-declared exports or types: `CAPABILITY_REQUIREMENTS`, `COMPATIBILITY_PATHS`, `CURRENT_VERSION`, `FEATURES_BY_VERSION`, `HostedLoginPage`, `HostedLoginRequest`, `LoginThemeAssetPolicy`, `LogoutIn`, `LogoutOut`, `LogoutPlan`, `LogoutRequest`, `OIDC_EXTENSION_CLAIMS`, `OIDC_ID_TOKEN_PROFILE_CLAIMS`, `OIDC_USERINFO_CLAIMS`, `OidcBindingError`.

Inspect [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oidc/src/tba_protocol_oidc/__init__.py) for exact signatures; this inventory does not designate every internal module as stable.

### Entry Points

<!-- readme-standards:begin entry-points -->
This package declares no command-line, GUI, or plugin entry points in its manifest.
<!-- readme-standards:end entry-points -->

### Injected Dependencies

Explicit construction inputs and collaborators for `tba-protocol-oidc`:

- `validate_id_token_profile` construction inputs: `expected_issuer`, `client_id`, `expected_nonce`, `now`, `clock_skew`, `allowed_algorithms`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oidc/src/tba_protocol_oidc/id_token_profile.py).
- `migrate_client_metadata` construction inputs: `source`, `target`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oidc/src/tba_protocol_oidc/migrations.py).
- `TenantBrandingRegistry` construction inputs: `asset_policy`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oidc/src/tba_protocol_oidc/provider.py).
- `OidcProviderRuntime` construction inputs: `allowed_redirect_uris`, `frontchannel_logout_uris`, `backchannel_logout_uris`, `now`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oidc/src/tba_protocol_oidc/provider.py).
- `new_login_request` construction inputs: `tenant_id`, `client_id`, `redirect_uri`, `scopes`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oidc/src/tba_protocol_oidc/provider.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

### Protocol Consumers

The following layer-50 manifests directly depend on `tba-protocol-oidc`:

- [tba-protocol-oidc-relying-party](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oidc-relying-party/README.md)

Other direct consumers include [tba-auth](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-auth/README.md), [tba-router-oidc-discovery](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-oidc-discovery/README.md), [tba-server-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-server-identity/README.md).

### Extensions

For `tba-protocol-oidc`, use the source-declared public interfaces (`CAPABILITY_REQUIREMENTS`, `COMPATIBILITY_PATHS`, `CURRENT_VERSION`, `FEATURES_BY_VERSION`, `HostedLoginPage`, `HostedLoginRequest`, `LoginThemeAssetPolicy`, `LogoutIn`, `LogoutOut`, `LogoutPlan`, `LogoutRequest`, `OIDC_EXTENSION_CLAIMS`, `OIDC_ID_TOKEN_PROFILE_CLAIMS`, `OIDC_USERINFO_CLAIMS`, `OidcBindingError`) when composing or extending behavior. Its entry-point section below is authoritative for registered plugins; no additional extension loader is inferred from the package name.

---

## Operations and Readiness

### Operational Requirements

`tba-protocol-oidc` exposes protocol semantics and projections. Public operations found in its source:

- `capability_report` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oidc/src/tba_protocol_oidc/__init__.py).
- `compose_oidc_claim_set` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oidc/src/tba_protocol_oidc/claim_sets.py).
- `compose_oidc_userinfo_claim_set` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oidc/src/tba_protocol_oidc/claim_sets.py).
- `compose_oidc_id_token_claim_set` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oidc/src/tba_protocol_oidc/claim_sets.py).
- `compatibility` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oidc/src/tba_protocol_oidc/compatibility.py).
- `supports` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oidc/src/tba_protocol_oidc/features.py).
- `validate_id_token_profile` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oidc/src/tba_protocol_oidc/id_token_profile.py).
- `migrate_client_metadata` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oidc/src/tba_protocol_oidc/migrations.py).
- `TenantBrandingRegistry.set` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oidc/src/tba_protocol_oidc/provider.py).
- `TenantBrandingRegistry.get` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oidc/src/tba_protocol_oidc/provider.py).
- `TenantBrandingRegistry.snapshot` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oidc/src/tba_protocol_oidc/provider.py).
- `OidcProviderRuntime.sessions` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oidc/src/tba_protocol_oidc/provider.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

### Health and Observability

This README does not establish a standalone health endpoint for `tba-protocol-oidc`. Observe the concrete caller’s results, exceptions, and existing test reports. An application that embeds this package must define its own health and telemetry contract.

### Security and Resource Limits

Apply the input, credential, and resource constraints implemented in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oidc/src/tba_protocol_oidc/__init__.py). The `tba-protocol-oidc` README gate is a documentation check, not a security review or a substitute for the implementation’s limits and caller authorization.

### Compatibility

This source version of `tba-protocol-oidc` declares Python `>=3.10,<3.16`. Consult its dependency constraints before upgrading. Source-version and registry-version badges have separate meanings; this migration makes no additional platform or interoperability certification claim.

---

## Verification

### Tests

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oidc/src/tba_protocol_oidc/__init__.py).

### Certification Status

No external certification is asserted for `tba-protocol-oidc` by this documentation migration. README conformance, example syntax, runtime tests, and protocol or security certification are distinct evidence scopes.

### Evidence

The [README standards CI](https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml) records mechanical documentation results for its tested commit. The [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oidc/src/tba_protocol_oidc/__init__.py) and example sources support the package-boundary description; external runtime behavior requires its own test evidence.

---

## FAQ

### Why

**Why select this package?** `tba-protocol-oidc` provides openID Connect provider protocol implementation package for the TBA package suite; use its own API boundary rather than assuming neighboring packages are bundled or configured automatically.

### How

**How do I start?** Install or synchronize the environment under Getting Started, follow the maintained example for `tba-protocol-oidc`, and consult [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oidc/src/tba_protocol_oidc/__init__.py) for the exact types and signatures involved.

### When

**When should I validate an upgrade?** Recheck `tba-protocol-oidc` whenever its source version, declared collaborators, configuration, or caller changes. Run relevant behavioral tests in addition to the README gate before promotion.

---

## Documentation and Related Packages

### More Documentation

The [repository contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md), [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oidc/src/tba_protocol_oidc/__init__.py), and [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oidc/pyproject.toml) provide the supporting context for `tba-protocol-oidc`. The [README policy](https://github.com/groupsum/readme-standards/blob/master/docs/outline.md) defines the common document structure.

### Related Packages

- [tigrbl-identity-oidc](https://pypi.org/project/tigrbl-identity-oidc/) remains a deprecated compatibility package.
- [tba-storage-core](https://pypi.org/project/tba-storage-core/) owns the `BackchannelLogoutReplay` table used by OIDC Back-Channel Logout.
- [tigrbl-auth-protocol-oidc-backchannel-replay-store](https://pypi.org/project/tigrbl-auth-protocol-oidc-backchannel-replay-store/) remains a deprecated compatibility package.
- [tba-protocol-oauth](https://pypi.org/project/tba-protocol-oauth/) owns OAuth protocol behavior.
- [tba-protocol-oidc-relying-party](https://pypi.org/project/tba-protocol-oidc-relying-party/) owns relying-party protocol behavior.

### Project Links

<!-- readme-standards:begin project-links -->
- [Documentation](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/050-protocols/tba-protocol-oidc#readme)
- [Homepage](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/050-protocols/tba-protocol-oidc#readme)
- [Issues](https://github.com/tigrbl/tigrbl_auth/issues)
- [PyPI](https://pypi.org/project/tba-protocol-oidc/)
- [Repository](https://github.com/tigrbl/tigrbl_auth)
- [SSOT](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [Source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/050-protocols/tba-protocol-oidc)
- [pypi: tba-protocol-oidc](https://pypi.org/project/tba-protocol-oidc/)
<!-- readme-standards:end project-links -->

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/050-protocols/tba-protocol-oidc)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oidc/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oidc/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oidc/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-protocol-oidc/)

---

## Contributing

### How to Contribute

Follow the [contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md) and include a focused example or regression for changes to `tba-protocol-oidc`. Keep package behavior, its documented boundary, and its tests aligned.

### Development Setup

Work from the `pkgs/050-protocols/tba-protocol-oidc` checkout. Synchronize its declared development environment with uv, then run the relevant package tests and `python -m pytest docs/readme/test_examples.py`. The repository’s dedicated README job installs `readme-standards==0.1.1` without resolving unrelated runtime packages.

### Notes for Maintainers

Edit authored prose directly in this `tba-protocol-oidc` README. Update source examples in `docs/readme/`, then run `readme-standards render --root . --write` from the package directory and review the diff. Required headings and generated blocks come from package-guide-v1.

---

## Governance

### Ownership and Decision Making

Changes to `tba-protocol-oidc` follow the maintainer review process of [tigrbl/tigrbl_auth](https://github.com/tigrbl/tigrbl_auth) and its contribution guide. Author attribution remains in the [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oidc/pyproject.toml); this README does not assign new publishing or administrative authority.

### Standards and Policies

This package is part of the SSOT-governed TBA package suite. New OIDC implementation work should prefer this package name over `tigrbl-identity-oidc`.

`tba-protocol-oidc` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `050-protocols` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

### Lifecycle and Migration

The `tba-protocol-oidc` source version is `0.4.0.dev3`. This change standardizes documentation and adds a development-only gate; it does not publish a new runtime version or declare a previously unpublished package released. Preserve explicit deprecation and replacement instructions where present.

---

## License and Attribution

### License

<!-- readme-standards:begin license -->
Licensed under `Apache-2.0`. See [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oidc/LICENSE).
<!-- readme-standards:end license -->

### Notices

<!-- readme-standards:begin notices -->
See [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oidc/NOTICE) for attribution.
<!-- readme-standards:end notices -->
