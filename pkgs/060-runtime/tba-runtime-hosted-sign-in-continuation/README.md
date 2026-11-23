# tba-runtime-hosted-sign-in-continuation

<!-- readme-standards:begin branding -->
<p align="center"><a href="https://github.com/tigrbl/tigrbl_auth"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="300"></a></p>
<p align="center"><strong>tba-runtime-hosted-sign-in-continuation</strong></p>
<p align="center">Provider-side continuation of a validated authorization request through hosted sign-in.</p>
<p align="center">
<a href="https://pypi.org/project/tba-runtime-hosted-sign-in-continuation/"><img alt="pypi: tba-runtime-hosted-sign-in-continuation unpublished" src="https://img.shields.io/static/v1?label=pypi&amp;message=tba-runtime-hosted-sign-in-continuation%20unpublished&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-hosted-sign-in-continuation/pyproject.toml"><img alt="Source version: 0.4.0.dev1" src="https://img.shields.io/static/v1?label=Source%20version&amp;message=0.4.0.dev1&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-hosted-sign-in-continuation/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/static/v1?label=Python&amp;message=%3E%3D3.10%2C%3C3.16&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-hosted-sign-in-continuation/pyproject.toml"><img alt="Layer: 060-runtime" src="https://img.shields.io/static/v1?label=Layer&amp;message=060-runtime&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-hosted-sign-in-continuation/README.md#lifecycle-and-migration"><img alt="Lifecycle: active" src="https://img.shields.io/static/v1?label=Lifecycle&amp;message=active&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-hosted-sign-in-continuation/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/static/v1?label=License&amp;message=Apache-2.0&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-hosted-sign-in-continuation/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/static/v1?label=Notice&amp;message=attribution&amp;color=525252"></a>
</p>
<p align="center">
<a href="https://pypi.org/project/tba-runtime-hosted-sign-in-continuation/"><img alt="pypi downloads: tba-runtime-hosted-sign-in-continuation: unpublished" src="https://img.shields.io/static/v1?label=pypi%20downloads&amp;message=tba-runtime-hosted-sign-in-continuation%3A%20unpublished&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-hosted-sign-in-continuation/README.md"><img alt="README hits: tba-runtime-hosted-sign-in-continuation" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/pkgs/060-runtime/tba-runtime-hosted-sign-in-continuation/README.md.svg?label=README%20hits"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="README standards: CI gate" src="https://img.shields.io/static/v1?label=README%20standards&amp;message=CI%20gate&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-hosted-sign-in-continuation/docs/readme/test_examples.py"><img alt="Tests: example source" src="https://img.shields.io/static/v1?label=Tests&amp;message=example%20source&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-hosted-sign-in-continuation/README.md#certification-status"><img alt="Certification: not certified" src="https://img.shields.io/static/v1?label=Certification&amp;message=not%20certified&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/tools/readme/POLICY.md"><img alt="Governance: repository policy" src="https://img.shields.io/static/v1?label=Governance&amp;message=repository%20policy&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-hosted-sign-in-continuation/README.md#evidence"><img alt="Evidence: source and CI" src="https://img.shields.io/static/v1?label=Evidence&amp;message=source%20and%20CI&amp;color=525252"></a>
</p>
<p align="center"><a href="#overview">Overview</a> · <a href="#installation">Installation</a> · <a href="#quick-start">Quick Start</a> · <a href="#usage">Usage</a> · <a href="#public-api-and-import-surfaces">API</a> · <a href="#contributing">Contributing</a> · <a href="#governance">Governance</a> · <a href="#license">License</a></p>
<!-- readme-standards:end branding -->

---

## Overview

### Summary

Preserve a provider's validated authorization request while hosted sign-in or first enrollment is in progress.

### Why This Package

A hosted verification or enrollment screen can outlive the authorization request that led the browser there. The provider needs a single transition that checks the original client, browser, session assurance, and authorization deadline before resuming.

### When to Use

Use this runtime after the provider validates an authorization request and before it redirects the browser to a hosted sign-in step.

### Features

- Preserve the original client, redirect URI, and validated authorization parameters.
- Check issuer, tenant, browser binding, registered client, and session assurance before resuming.
- Require an atomic storage operation before exposing the request for resumption.
- Return a bounded client hint for a restart, or keep recovery on the provider.

### Non-Goals

The host provides HTTP routing, navigation, OAuth authorization and issuance, and the relying party's separate callback state.

---

## Getting Started

### Prerequisites

Use Python 3.10 or later and a provider with a validated authorization request and an atomic transaction store.

### Installation

Build the package from its repository directory for local evaluation.

#### uv

<!-- readme-standards:begin installation.uv -->
`tba-runtime-hosted-sign-in-continuation` is not declared published. From the source checkout:

```bash
uv pip install .
```
<!-- readme-standards:end installation.uv -->

#### pip

<!-- readme-standards:begin installation.pip -->
`tba-runtime-hosted-sign-in-continuation` is not declared published. From the source checkout:

```bash
python -m pip install .
```
<!-- readme-standards:end installation.pip -->

#### Poetry

<!-- readme-standards:begin installation.poetry -->
`tba-runtime-hosted-sign-in-continuation` is not declared published. From a separate Poetry project, replace the path with your checkout:

```bash
poetry add /path/to/tba-runtime-hosted-sign-in-continuation
```
<!-- readme-standards:end installation.poetry -->

### Quick Start

#### Example

<!-- readme-standards:begin example.quick-start -->
Source: [docs/readme/quick_start.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-hosted-sign-in-continuation/docs/readme/quick_start.py).

```python
from tba_runtime_hosted_sign_in_continuation import ValidatedAuthorizationRequest


request = ValidatedAuthorizationRequest(
    issuer="https://tenant.example.test",
    tenant_id="tenant",
    client_id="application",
    redirect_uri="https://app.example.test/callback",
    parameters=(("state", "client-state"), ("nonce", "client-nonce")),
)
assert request.redirect_uri == "https://app.example.test/callback"
```
<!-- readme-standards:end example.quick-start -->

#### Expected Result

The bound redirect URI and client state remain in the immutable request snapshot.

---

## Usage

### Common Workflows

Create a request from the authorization validator's output and call `begin`. Supply the flow ID returned by `begin` together with fresh provider-session evidence to `resolve` after the hosted step. Pass a resumed request back through the provider's existing authorization operation.

<!-- readme-standards:begin example.usage -->
Source: [docs/readme/usage.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-hosted-sign-in-continuation/docs/readme/usage.py).

```python
from tba_runtime_hosted_sign_in_continuation import HostedSignInContinuationRuntime, Resume


def existing_authorization_request(
    runtime: HostedSignInContinuationRuntime[frozenset[str]],
    flow_id: str,
    verified_methods: frozenset[str],
):
    outcome = runtime.resolve(
        flow_id,
        issuer="https://tenant.example.test",
        tenant_id="tenant",
        browser_binding="host-validated-binding",
        assurance=verified_methods,
    )
    if isinstance(outcome, Resume):
        return outcome.request
    return None


assert callable(existing_authorization_request)
```
<!-- readme-standards:end example.usage -->

### Configuration

Provide a timezone-aware clock, lifetime, recovery window, browser-binding comparison, live client eligibility check, and session assurance callback. A recovery window of zero disables restart hints.

### Error Handling

Use `StayLocal` for unknown, already-consumed, misbound, disabled, or insufficiently assured requests. Use `Restart` for an expired request that still has authorized, browser-bound recovery context. Repository and policy failures propagate to the host without producing a resume outcome.

### Best Practices

Compute the browser binding from trusted host context. Revalidate the issuer, tenant, active client, and exact registered callback. Use the current registration to resolve a restart destination.

---

## Package Boundary

### What It Owns

Provider-side continuation lifecycle and the atomic resume contract.

### Public API and Import Surfaces

Import `HostedSignInContinuationRuntime`, `ValidatedAuthorizationRequest`, `ContinuationRepository`, `PendingContinuation`, and the outcome types from `tba_runtime_hosted_sign_in_continuation`.

### Entry Points

<!-- readme-standards:begin entry-points -->
This package declares no command-line, GUI, or plugin entry points in its manifest.
<!-- readme-standards:end entry-points -->

### Injected Dependencies

The repository holds immutable pending records. Implement consume as an atomic conditional operation across workers. Authentication policy reports eligibility against the provider's current session and request.

### Protocol Consumers

OIDC providers can resume an existing authorization request through their own authorization endpoint after hosted factors are complete.

### Extensions

Keep protocol-specific claims and UI decisions in the host adapter.

---

## Operations and Readiness

### Operational Requirements

Give each flow ID unique storage. Retain expired records only for the configured recovery window and prune consumed records according to the repository contract. Run the existing authorization checks again before issuing a response.

### Health and Observability

Record posture and failures at the host boundary. Keep flow identifiers, browser bindings, and captured authorization parameters out of logs.

### Security and Resource Limits

A restart hint gives the host only the saved client identifier. Only consume can produce a resumable snapshot. The provider enforces browser-binding integrity, storage limits, and the live session's assurance and expiry.

### Compatibility

The runtime is independent of the relying party's callback transaction and the provider's browser session format.

---

## Verification

### Tests

Focused tests cover normal first enrollment, replay, concurrent consume, expiry, assurance, registered callback changes, and issuer, tenant, and browser isolation. The README examples also run as tests.

### Certification Status

The runtime has contract tests. Production adapter and live deployment evidence are pending.

### Evidence

See the package tests and the hosted sign-in continuation ADR and SPEC in the repository registry.

---

## FAQ

### Why

Saving a validated request allows the provider to return to the original app after hosted enrollment.

### How

The provider injects trusted live checks and the repository atomically claims the pending record once.

### When

Resolve after the application establishes sufficient assurance, or to choose a provider-local recovery screen.

---

## Documentation and Related Packages

### More Documentation

See the hosted sign-in continuation ADR and SPEC for the contract and adapter obligations.

### Related Packages

The relying-party session runtime owns the application's transaction and its own one-time callback state.

### Project Links

<!-- readme-standards:begin project-links -->
- [Documentation](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/060-runtime/tba-runtime-hosted-sign-in-continuation#readme)
- [Homepage](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/060-runtime/tba-runtime-hosted-sign-in-continuation#readme)
- [Issues](https://github.com/tigrbl/tigrbl_auth/issues)
- [PyPI](https://pypi.org/project/tba-runtime-hosted-sign-in-continuation/)
- [Repository](https://github.com/tigrbl/tigrbl_auth)
- [Source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/060-runtime/tba-runtime-hosted-sign-in-continuation)
- [pypi: tba-runtime-hosted-sign-in-continuation](https://pypi.org/project/tba-runtime-hosted-sign-in-continuation/)
<!-- readme-standards:end project-links -->

---

## Contributing

### How to Contribute

Add focused cases for new transitions or adapter requirements.

### Development Setup

Install the package and run its test directory and README example tests.

### Notes for Maintainers

Keep route frameworks and production data-store adapters outside this runtime.

---

## Governance

### Ownership and Decision Making

The Tigrbl Auth runtime layer owns provider continuation semantics. Product maintainers own the host adapters and acceptance evidence.

### Standards and Policies

Use the repository layer and SSOT contract for changes to public types or behavior.

### Lifecycle and Migration

This is the first provider-runtime contract. Adoption requires a separately reviewed storage adapter and product integration.

---

## License and Attribution

### License

<!-- readme-standards:begin license -->
Licensed under `Apache-2.0`. See [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-hosted-sign-in-continuation/LICENSE).
<!-- readme-standards:end license -->

### Notices

<!-- readme-standards:begin notices -->
See [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-hosted-sign-in-continuation/NOTICE) for attribution.
<!-- readme-standards:end notices -->
