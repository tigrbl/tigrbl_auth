# tba-runtime-oidc-provider-logout

<!-- readme-standards:begin branding -->
<p align="center"><a href="https://github.com/tigrbl/tigrbl_auth"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="300"></a></p>
<p align="center"><strong>tba-runtime-oidc-provider-logout</strong></p>
<p align="center">Transport-neutral OpenID Provider end-session lifecycle.</p>
<p align="center">
<a href="https://pypi.org/project/tba-runtime-oidc-provider-logout/"><img alt="pypi: tba-runtime-oidc-provider-logout unpublished" src="https://img.shields.io/static/v1?label=pypi&amp;message=tba-runtime-oidc-provider-logout%20unpublished&amp;labelColor=1E293B&amp;color=92400E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-oidc-provider-logout/pyproject.toml"><img alt="Source version: 0.4.0.dev0" src="https://img.shields.io/static/v1?label=Source%20version&amp;message=0.4.0.dev0&amp;labelColor=1E293B&amp;color=4338CA"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-oidc-provider-logout/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/static/v1?label=Python&amp;message=%3E%3D3.10%2C%3C3.16&amp;labelColor=1E293B&amp;color=0F766E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-oidc-provider-logout/pyproject.toml"><img alt="Layer: 060-runtime" src="https://img.shields.io/static/v1?label=Layer&amp;message=060-runtime&amp;labelColor=1E293B&amp;color=6D28D9"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-oidc-provider-logout/README.md#lifecycle-and-migration"><img alt="Lifecycle: active" src="https://img.shields.io/static/v1?label=Lifecycle&amp;message=active&amp;labelColor=1E293B&amp;color=166534"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-oidc-provider-logout/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/static/v1?label=License&amp;message=Apache-2.0&amp;labelColor=1E293B&amp;color=86198F"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-oidc-provider-logout/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/static/v1?label=Notice&amp;message=attribution&amp;labelColor=1E293B&amp;color=86198F"></a>
</p>
<p align="center">
<a href="https://pypi.org/project/tba-runtime-oidc-provider-logout/"><img alt="pypi downloads: tba-runtime-oidc-provider-logout: unpublished" src="https://img.shields.io/static/v1?label=pypi%20downloads&amp;message=tba-runtime-oidc-provider-logout%3A%20unpublished&amp;labelColor=1E293B&amp;color=92400E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-oidc-provider-logout/README.md"><img alt="README hits: tba-runtime-oidc-provider-logout" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/pkgs/060-runtime/tba-runtime-oidc-provider-logout/README.md.svg?label=README%20hits&amp;labelColor=1E293B&amp;color=0E7490"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="README standards: CI gate" src="https://img.shields.io/static/v1?label=README%20standards&amp;message=CI%20gate&amp;labelColor=1E293B&amp;color=1D4ED8"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-oidc-provider-logout/docs/readme/test_examples.py"><img alt="Tests: example source" src="https://img.shields.io/static/v1?label=Tests&amp;message=example%20source&amp;labelColor=1E293B&amp;color=0F766E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-oidc-provider-logout/README.md#certification-status"><img alt="Certification: not certified" src="https://img.shields.io/static/v1?label=Certification&amp;message=not%20certified&amp;labelColor=1E293B&amp;color=92400E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/tools/readme/POLICY.md"><img alt="Governance: repository policy" src="https://img.shields.io/static/v1?label=Governance&amp;message=repository%20policy&amp;labelColor=1E293B&amp;color=4338CA"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="Evidence: source and CI" src="https://img.shields.io/static/v1?label=Evidence&amp;message=source%20and%20CI&amp;labelColor=1E293B&amp;color=6D28D9"></a>
</p>
<p align="center"><a href="#overview">Overview</a> · <a href="#installation">Installation</a> · <a href="#quick-start">Quick Start</a> · <a href="#usage">Usage</a> · <a href="#public-api-and-import-surfaces">API</a> · <a href="#contributing">Contributing</a> · <a href="#governance">Governance</a> · <a href="#license">License</a></p>
<!-- readme-standards:end branding -->

---

## Overview

### Summary

OpenID Provider end-session orchestration for issuer-bound browser sessions.

### Why This Package

A provider can use the same confirmation, revocation, and return rules across transports and deployments.

### When to Use

Compose the runtime with your provider's client registry, session service, and browser transaction storage.

### Features

- Cross-site form handoff and explicit logout confirmation.
- Expiring attempts bound to the issuer and browser and consumed once.
- Scoped session revocation and exact redirect validation before returning state.

### Non-Goals

The host owns issuer resolution, client and redirect registration, verified hint inspection, browser proofs, and cookie delivery.

---

## Getting Started

### Prerequisites

Use Python 3.10 or newer and supply validation, revocation, and atomic attempt storage adapters.

### Installation

Install from the package's source directory to evaluate an unreleased checkout.

#### uv

<!-- readme-standards:begin installation.uv -->
`tba-runtime-oidc-provider-logout` is not declared published. From the source checkout:

```bash
uv pip install .
```
<!-- readme-standards:end installation.uv -->

#### pip

<!-- readme-standards:begin installation.pip -->
`tba-runtime-oidc-provider-logout` is not declared published. From the source checkout:

```bash
python -m pip install .
```
<!-- readme-standards:end installation.pip -->

#### Poetry

<!-- readme-standards:begin installation.poetry -->
`tba-runtime-oidc-provider-logout` is not declared published. From a separate Poetry project, replace the path with your checkout:

```bash
poetry add /path/to/tba-runtime-oidc-provider-logout
```
<!-- readme-standards:end installation.poetry -->

### Quick Start

#### Example

<!-- readme-standards:begin example.quick-start -->
Source: [docs/readme/quick_start.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-oidc-provider-logout/docs/readme/quick_start.py).

```python
from tba_runtime_oidc_provider_logout import LogoutRequest

request = LogoutRequest(
    issuer="https://authority.example",
    client_id="my-app",
    post_logout_redirect_uri="https://app.example/signed-out",
    state="browser-transaction",
)
assert request.client_id == "my-app"
```
<!-- readme-standards:end example.quick-start -->

#### Expected Result

The example represents the issuer, client, registered redirect, and state as a typed request.

---

## Usage

### Common Workflows

<!-- readme-standards:begin example.usage -->
Source: [docs/readme/usage.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-oidc-provider-logout/docs/readme/usage.py).

```python
from tba_runtime_oidc_provider_logout import append_logout_state

redirect = append_logout_state(
    "https://app.example/signed-out?lang=en", "browser/transaction"
)
assert redirect == (
    "https://app.example/signed-out?lang=en&state=browser%2Ftransaction"
)
```
<!-- readme-standards:end example.usage -->

### Configuration

Set the attempt lifetime with `ttl_seconds`. The default is 300 seconds, with a maximum of 900 seconds.

### Error Handling

Inspect `LogoutResult.status` for confirmation, handoff, completion, cancellation, rejection, or temporary unavailability.

### Best Practices

Use `begin` when the browser context is present and `handoff` to preserve a cross-site form submission until the first-party session is available. Check the confirmation request's origin or CSRF proof before calling `resume` with a decision.

---

## Package Boundary

### What It Owns

The package owns the lifecycle from request validation through attempt handling, confirmation, revocation, and state return.

### Public API and Import Surfaces

Import `LogoutRuntime`, `LogoutRequest`, `LogoutSession`, `ValidatedLogout`, and `LogoutResult` from `tba_runtime_oidc_provider_logout`.

### Entry Points

<!-- readme-standards:begin entry-points -->
This package declares no command-line, GUI, or plugin entry points in its manifest.
<!-- readme-standards:end entry-points -->

Call `begin`, `handoff`, and `resume` on `LogoutRuntime` from the provider's HTTP or other transport adapter.

### Injected Dependencies

Provide a validator, a session revoker, and a `LogoutAttempts` store whose consume operation checks the issuer, browser binding, and expiry atomically.

### Protocol Consumers

An OpenID Provider may compose the runtime with an OIDC discovery document and end-session endpoint.

### Extensions

Use storage and transport adapters to implement persistence and confirmation without changing lifecycle rules.

---

## Operations and Readiness

### Operational Requirements

Persist pending attempts in shared storage for multi-worker deployments and scope revocation to the selected provider session.

### Health and Observability

Record outcome categories and operational errors. Keep raw token hints, attempt handles, browser bindings, and redirect state out of logs.

### Security and Resource Limits

Use a durable store with atomic single-use consumption, enforce request and attempt limits at the host boundary, and expire stored attempts.

### Compatibility

This is the first release of the runtime. Check the existing provider behavior against the adapter contract before switching routes.

---

## Verification

### Tests

Run the independent provider logout integration fixture and the OIDC logout HTTP binding tests in the TBA test workspace.

### Certification Status

Release certification requires recorded evidence for the installed artifact.

### Evidence

The repository includes a synthetic transport test and a durable SQLite fixture covering restart and scoped logout.

---

## FAQ

### Why

A browser can lose access to a provider's first-party cookies during a cross-site form submission. The handoff preserves the request until the provider can resolve the session.

### How

Supply a browser-binding value when staging an attempt and again when consuming it.

### When

Use confirmation when an active issuer session is present and the validated ID token hint does not identify that session.

---

## Documentation and Related Packages

### More Documentation

See the OIDC RP-initiated logout specification and the repository SSOT for the provider runtime contract.

### Related Packages

The TBA OIDC logout router provides GET and POST carriers. The TBA OIDC relying-party protocol constructs and validates the client's side of the flow.

### Project Links

<!-- readme-standards:begin project-links -->
- [Documentation](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/060-runtime/tba-runtime-oidc-provider-logout#readme)
- [Homepage](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/060-runtime/tba-runtime-oidc-provider-logout#readme)
- [Issues](https://github.com/tigrbl/tigrbl_auth/issues)
- [PyPI](https://pypi.org/project/tba-runtime-oidc-provider-logout/)
- [Repository](https://github.com/tigrbl/tigrbl_auth)
- [SSOT](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [Source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/060-runtime/tba-runtime-oidc-provider-logout)
- [pypi: tba-runtime-oidc-provider-logout](https://pypi.org/project/tba-runtime-oidc-provider-logout/)
<!-- readme-standards:end project-links -->

---

## Contributing

### How to Contribute

Add a synthetic fixture when changing the provider adapter contract or lifecycle rules.

### Development Setup

Use the repository's uv-managed development environment to run the focused tests and package checks.

### Notes for Maintainers

Treat exact redirect authorization, scoped revocation, and atomic consumption as compatibility requirements.

---

## Governance

### Ownership and Decision Making

TBA owns the transport-neutral lifecycle. The consuming provider owns deployment identity policy and validates requests using its registration and session data.

### Standards and Policies

Use the repository package and README policies for changes to this runtime.

### Lifecycle and Migration

Move transport binding first, then wire durable adapters and verify existing issuer and client configurations.

---

## License and Attribution

### License

<!-- readme-standards:begin license -->
Licensed under `Apache-2.0`. See [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-oidc-provider-logout/LICENSE).
<!-- readme-standards:end license -->

### Notices

<!-- readme-standards:begin notices -->
See [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-oidc-provider-logout/NOTICE) for attribution.
<!-- readme-standards:end notices -->
