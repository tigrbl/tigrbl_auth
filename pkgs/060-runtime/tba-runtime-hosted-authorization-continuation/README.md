# tba-runtime-hosted-authorization-continuation

<!-- readme-standards:begin branding -->
<p align="center"><a href="https://github.com/tigrbl/tigrbl_auth"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="300"></a></p>
<p align="center"><strong>tba-runtime-hosted-authorization-continuation</strong></p>
<p align="center">Issuer-bound authorization continuation through interactive account verification and enrollment.</p>
<p align="center">
<a href="https://pypi.org/project/tba-runtime-hosted-authorization-continuation/"><img alt="pypi: tba-runtime-hosted-authorization-continuation unpublished" src="https://img.shields.io/static/v1?label=pypi&amp;message=tba-runtime-hosted-authorization-continuation%20unpublished&amp;labelColor=1E293B&amp;color=92400E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-hosted-authorization-continuation/pyproject.toml"><img alt="Source version: 0.4.0.dev1" src="https://img.shields.io/static/v1?label=Source%20version&amp;message=0.4.0.dev1&amp;labelColor=1E293B&amp;color=4338CA"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-hosted-authorization-continuation/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/static/v1?label=Python&amp;message=%3E%3D3.10%2C%3C3.16&amp;labelColor=1E293B&amp;color=0F766E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-hosted-authorization-continuation/pyproject.toml"><img alt="Layer: 060-runtime" src="https://img.shields.io/static/v1?label=Layer&amp;message=060-runtime&amp;labelColor=1E293B&amp;color=6D28D9"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-hosted-authorization-continuation/README.md#lifecycle-and-migration"><img alt="Lifecycle: active" src="https://img.shields.io/static/v1?label=Lifecycle&amp;message=active&amp;labelColor=1E293B&amp;color=166534"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-hosted-authorization-continuation/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/static/v1?label=License&amp;message=Apache-2.0&amp;labelColor=1E293B&amp;color=86198F"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-hosted-authorization-continuation/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/static/v1?label=Notice&amp;message=attribution&amp;labelColor=1E293B&amp;color=86198F"></a>
</p>
<p align="center">
<a href="https://pypi.org/project/tba-runtime-hosted-authorization-continuation/"><img alt="pypi downloads: tba-runtime-hosted-authorization-continuation: unpublished" src="https://img.shields.io/static/v1?label=pypi%20downloads&amp;message=tba-runtime-hosted-authorization-continuation%3A%20unpublished&amp;labelColor=1E293B&amp;color=92400E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-hosted-authorization-continuation/README.md"><img alt="README hits: tba-runtime-hosted-authorization-continuation" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/pkgs/060-runtime/tba-runtime-hosted-authorization-continuation/README.md.svg?label=README%20hits&amp;labelColor=1E293B&amp;color=0E7490"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="README standards: CI gate" src="https://img.shields.io/static/v1?label=README%20standards&amp;message=CI%20gate&amp;labelColor=1E293B&amp;color=1D4ED8"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-hosted-authorization-continuation/docs/readme/test_examples.py"><img alt="Tests: example source" src="https://img.shields.io/static/v1?label=Tests&amp;message=example%20source&amp;labelColor=1E293B&amp;color=0F766E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-hosted-authorization-continuation/README.md#certification-status"><img alt="Certification: not certified" src="https://img.shields.io/static/v1?label=Certification&amp;message=not%20certified&amp;labelColor=1E293B&amp;color=92400E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/tools/readme/POLICY.md"><img alt="Governance: repository policy" src="https://img.shields.io/static/v1?label=Governance&amp;message=repository%20policy&amp;labelColor=1E293B&amp;color=4338CA"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="Evidence: source and CI" src="https://img.shields.io/static/v1?label=Evidence&amp;message=source%20and%20CI&amp;labelColor=1E293B&amp;color=6D28D9"></a>
</p>
<p align="center"><a href="#overview">Overview</a> · <a href="#installation">Installation</a> · <a href="#quick-start">Quick Start</a> · <a href="#usage">Usage</a> · <a href="#public-api-and-import-surfaces">API</a> · <a href="#contributing">Contributing</a> · <a href="#governance">Governance</a> · <a href="#license">License</a></p>
<!-- readme-standards:end branding -->

---

## Overview

### Summary

Issuer-bound authorization continuation through interactive account verification and enrollment.

### Why This Package

A single durable consume protects the original registered authorization request across hosted authentication steps.

### When to Use

Begin after validating the authorization request, then resume it using trusted authentication evidence for the same browser transaction.

### Features

- Preserve exact callback, nonce, state, and PKCE parameters.
- Browser, issuer, and client binding.
- Typed resume, restart, and unavailable outcomes.

### Non-Goals

The runtime leaves request validation, hosted UI, account policy, and registered restart URLs to the host.

---

## Getting Started

### Prerequisites

Use Python 3.10 or newer. Supply the transaction and policy interfaces in the public module.

### Installation

Install the selected release after publication or use the local package directory during development.

#### uv

<!-- readme-standards:begin installation.uv -->
`tba-runtime-hosted-authorization-continuation` is not declared published. From the source checkout:

```bash
uv pip install .
```
<!-- readme-standards:end installation.uv -->

#### pip

<!-- readme-standards:begin installation.pip -->
`tba-runtime-hosted-authorization-continuation` is not declared published. From the source checkout:

```bash
python -m pip install .
```
<!-- readme-standards:end installation.pip -->

#### Poetry

<!-- readme-standards:begin installation.poetry -->
`tba-runtime-hosted-authorization-continuation` is not declared published. From a separate Poetry project, replace the path with your checkout:

```bash
poetry add /path/to/tba-runtime-hosted-authorization-continuation
```
<!-- readme-standards:end installation.poetry -->

### Quick Start

Import the runtime and its public contracts before composing the host adapter.

#### Example

<!-- readme-standards:begin example.quick-start -->
Source: [docs/readme/quick_start.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-hosted-authorization-continuation/docs/readme/quick_start.py).

```python
from tba_runtime_hosted_authorization_continuation import ValidatedAuthorizationRequest

request = ValidatedAuthorizationRequest.from_parameters(
    'https://issuer.example.test',
    {'client_id': 'example-app', 'redirect_uri': 'https://rp.example.test/callback'},
)
assert request.client_id == 'example-app'
```
<!-- readme-standards:end example.quick-start -->

#### Expected Result

The example constructs the documented contract and does not require infrastructure or credentials.

---

## Usage

### Common Workflows

<!-- readme-standards:begin example.usage -->
Source: [docs/readme/usage.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-hosted-authorization-continuation/docs/readme/usage.py).

```python
from tba_runtime_hosted_authorization_continuation import ContinuationRequirements

requirements = ContinuationRequirements(required_methods=frozenset({'otp'}))
assert requirements.required_methods == {'otp'}
```
<!-- readme-standards:end example.usage -->

### Configuration

Supply a durable continuation store, stable browser transaction identifier, and flow lifetime.

### Error Handling

Map expected storage outages to `ContinuationUnavailable`. The runtime returns an unavailable outcome and includes no saved request.

### Best Practices

Consult the current client registration at resume. Safely restart at a host-owned destination. For shared issuers, pass the host-resolved tenant ID when creating the request and again when inspecting or resuming it. A positive recovery window lets a bound browser receive only the current client identifier for a fresh sign-in. Retain unconsumed records for the configured window.

---

## Package Boundary

### What It Owns

The runtime snapshots validated request parameters, checks browser and confirmation bindings, and asks the store to consume once.

### Public API and Import Surfaces

Import `HostedAuthorizationContinuation`, `ValidatedAuthorizationRequest`, `ContinuationStore`, and the typed outcome contracts from `tba_runtime_hosted_authorization_continuation`.

### Entry Points

<!-- readme-standards:begin entry-points -->
This package declares no command-line, GUI, or plugin entry points in its manifest.
<!-- readme-standards:end entry-points -->

This is a library imported by a host runtime. It installs no executable.

### Injected Dependencies

Supply a `ContinuationStore`, registered client recheck, and trusted authentication evidence.

### Protocol Consumers

Provider authorization and hosted sign-in routes consume this library after OAuth request validation.

### Extensions

A host can select distinct completion requirements such as verified email or fresh factor proof.

---

## Operations and Readiness

### Operational Requirements

Persist pending requests securely. The consume operation compares an immutable record and unexpired state in one transaction.

### Health and Observability

Record status and reasons without logging authorization parameters or browser identifiers.

### Security and Resource Limits

Use an unpredictable browser value and store it in an appropriate host-owned browser credential.

### Compatibility

This is the first package release. Pin the selected artifact and verify the host implementation against its storage contract.

---

## Verification

### Tests

Run `pkgs/120-tests/tba-tests-browser-session/tests/integration/test_hosted_authorization_continuation.py` with pytest.

### Certification Status

No external certification is claimed. Use the linked acceptance scope and changing evidence recorded in SSOT.

### Evidence

Use the [SSOT registry](../../../.ssot/registry.json) and execute the repository-owned synthetic tests.

---

## FAQ

### Why

Interactive account steps can outlast an authorization page request.

### How

Persist a validated request and resume it after the configured account evidence is available.

### When

Use when a hosted provider must preserve an authorization request through confirmation or first-factor enrollment.

---

## Documentation and Related Packages

### More Documentation

See SPEC-1239 in the repository SSOT.

### Related Packages

TBA OAuth and OpenID Connect protocol packages.

### Project Links

<!-- readme-standards:begin project-links -->
- [Documentation](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/060-runtime/tba-runtime-hosted-authorization-continuation#readme)
- [Homepage](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/060-runtime/tba-runtime-hosted-authorization-continuation#readme)
- [Issues](https://github.com/tigrbl/tigrbl_auth/issues)
- [PyPI](https://pypi.org/project/tba-runtime-hosted-authorization-continuation/)
- [Repository](https://github.com/tigrbl/tigrbl_auth)
- [SSOT](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [Source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/060-runtime/tba-runtime-hosted-authorization-continuation)
- [pypi: tba-runtime-hosted-authorization-continuation](https://pypi.org/project/tba-runtime-hosted-authorization-continuation/)
<!-- readme-standards:end project-links -->

---

## Contributing

### How to Contribute

Use the repository contribution guide and include an independent test for behavior changes.

### Development Setup

Run the test path listed above with the repository's uv-managed environment.

### Notes for Maintainers

Retain the exact validated request and treat one-time consumption as a compatibility requirement.

---

## Governance

### Ownership and Decision Making

ADR-1143 assigns continued authorization state to TBA and application-specific restart policy to the host.

### Standards and Policies

Follow the repository layer and package policies. The host owns the deployment's identity policy.

### Lifecycle and Migration

Adopt the store and browser binding before switching existing sign-in continuation routes.

---

## License and Attribution

### License

<!-- readme-standards:begin license -->
Licensed under `Apache-2.0`. See [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-hosted-authorization-continuation/LICENSE).
<!-- readme-standards:end license -->

### Notices

<!-- readme-standards:begin notices -->
See [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-hosted-authorization-continuation/NOTICE) for attribution.
<!-- readme-standards:end notices -->
