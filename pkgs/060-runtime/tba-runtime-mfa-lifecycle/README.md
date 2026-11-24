# tba-runtime-mfa-lifecycle

<!-- readme-standards:begin branding -->
<p align="center"><a href="https://github.com/tigrbl/tigrbl_auth"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="300"></a></p>
<p align="center"><strong>tba-runtime-mfa-lifecycle</strong></p>
<p align="center">Carrier-neutral multi-factor enrollment, replacement, replay protection, and step-up lifecycle.</p>
<p align="center">
<a href="https://pypi.org/project/tba-runtime-mfa-lifecycle/"><img alt="pypi: tba-runtime-mfa-lifecycle unpublished" src="https://img.shields.io/static/v1?label=pypi&amp;message=tba-runtime-mfa-lifecycle%20unpublished&amp;labelColor=1E293B&amp;color=92400E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-mfa-lifecycle/pyproject.toml"><img alt="Source version: 0.4.0.dev1" src="https://img.shields.io/static/v1?label=Source%20version&amp;message=0.4.0.dev1&amp;labelColor=1E293B&amp;color=4338CA"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-mfa-lifecycle/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/static/v1?label=Python&amp;message=%3E%3D3.10%2C%3C3.16&amp;labelColor=1E293B&amp;color=0F766E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-mfa-lifecycle/pyproject.toml"><img alt="Layer: 060-runtime" src="https://img.shields.io/static/v1?label=Layer&amp;message=060-runtime&amp;labelColor=1E293B&amp;color=6D28D9"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-mfa-lifecycle/README.md#lifecycle-and-migration"><img alt="Lifecycle: active" src="https://img.shields.io/static/v1?label=Lifecycle&amp;message=active&amp;labelColor=1E293B&amp;color=166534"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-mfa-lifecycle/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/static/v1?label=License&amp;message=Apache-2.0&amp;labelColor=1E293B&amp;color=86198F"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-mfa-lifecycle/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/static/v1?label=Notice&amp;message=attribution&amp;labelColor=1E293B&amp;color=86198F"></a>
</p>
<p align="center">
<a href="https://pypi.org/project/tba-runtime-mfa-lifecycle/"><img alt="pypi downloads: tba-runtime-mfa-lifecycle: unpublished" src="https://img.shields.io/static/v1?label=pypi%20downloads&amp;message=tba-runtime-mfa-lifecycle%3A%20unpublished&amp;labelColor=1E293B&amp;color=92400E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-mfa-lifecycle/README.md"><img alt="README hits: tba-runtime-mfa-lifecycle" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/pkgs/060-runtime/tba-runtime-mfa-lifecycle/README.md.svg?label=README%20hits&amp;labelColor=1E293B&amp;color=0E7490"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="README standards: CI gate" src="https://img.shields.io/static/v1?label=README%20standards&amp;message=CI%20gate&amp;labelColor=1E293B&amp;color=1D4ED8"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-mfa-lifecycle/docs/readme/test_examples.py"><img alt="Tests: example source" src="https://img.shields.io/static/v1?label=Tests&amp;message=example%20source&amp;labelColor=1E293B&amp;color=0F766E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-mfa-lifecycle/README.md#certification-status"><img alt="Certification: not certified" src="https://img.shields.io/static/v1?label=Certification&amp;message=not%20certified&amp;labelColor=1E293B&amp;color=92400E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/tools/readme/POLICY.md"><img alt="Governance: repository policy" src="https://img.shields.io/static/v1?label=Governance&amp;message=repository%20policy&amp;labelColor=1E293B&amp;color=4338CA"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="Evidence: source and CI" src="https://img.shields.io/static/v1?label=Evidence&amp;message=source%20and%20CI&amp;labelColor=1E293B&amp;color=6D28D9"></a>
</p>
<p align="center"><a href="#overview">Overview</a> · <a href="#installation">Installation</a> · <a href="#quick-start">Quick Start</a> · <a href="#usage">Usage</a> · <a href="#public-api-and-import-surfaces">API</a> · <a href="#contributing">Contributing</a> · <a href="#governance">Governance</a> · <a href="#license">License</a></p>
<!-- readme-standards:end branding -->

---

## Overview

### Summary

Carrier-neutral multi-factor enrollment, replacement, replay protection, and step-up lifecycle.

### Why This Package

The transaction boundary protects activation and replay state across independent factor providers.

### When to Use

Construct an enrollment or step-up runtime with the host's atomic factor store and factor verifiers.

### Features

- Enrollment and replacement with proof before activation.
- Scoped step-up and freshness evaluation.
- TOTP and optional WebAuthn verification adapters.

### Non-Goals

Account eligibility, issuer labels, recovery, and remembered-device rules remain host policy.

---

## Getting Started

### Prerequisites

Use Python 3.10 or newer. Supply the transaction and policy interfaces in the public module.

### Installation

Install the selected release after publication or use the local package directory during development.

#### uv

<!-- readme-standards:begin installation.uv -->
`tba-runtime-mfa-lifecycle` is not declared published. From the source checkout:

```bash
uv pip install .
```
<!-- readme-standards:end installation.uv -->

#### pip

<!-- readme-standards:begin installation.pip -->
`tba-runtime-mfa-lifecycle` is not declared published. From the source checkout:

```bash
python -m pip install .
```
<!-- readme-standards:end installation.pip -->

#### Poetry

<!-- readme-standards:begin installation.poetry -->
`tba-runtime-mfa-lifecycle` is not declared published. From a separate Poetry project, replace the path with your checkout:

```bash
poetry add /path/to/tba-runtime-mfa-lifecycle
```
<!-- readme-standards:end installation.poetry -->

### Quick Start

Import the runtime and its public contracts before composing the host adapter.

#### Example

<!-- readme-standards:begin example.quick-start -->
Source: [docs/readme/quick_start.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-mfa-lifecycle/docs/readme/quick_start.py).

```python
from tba_runtime_mfa_lifecycle import FactorBinding

binding = FactorBinding('example-scope', 'account-1', 'totp', 'settings-enrollment')
assert binding.subject == 'account-1'
```
<!-- readme-standards:end example.quick-start -->

#### Expected Result

The example constructs the documented contract and does not require infrastructure or credentials.

---

## Usage

### Common Workflows

<!-- readme-standards:begin example.usage -->
Source: [docs/readme/usage.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-mfa-lifecycle/docs/readme/usage.py).

```python
from datetime import timedelta

from tba_runtime_mfa_lifecycle import AssuranceRequirement

requirement = AssuranceRequirement(frozenset({'pwd', 'otp'}), timedelta(minutes=5))
assert requirement.required_methods == {'pwd', 'otp'}
```
<!-- readme-standards:end example.usage -->

### Configuration

Provide a timezone-aware clock when simulation requires one. Each begin call accepts a bounded ceremony lifetime.

### Error Handling

Expected proof failures produce rejected, expired, or challenge-required outcomes. Store errors propagate to the application's failure handler.

### Best Practices

Resolve credentials from the bound attempt and commit replay changes in the same transaction as activation or assertion-counter advancement.

---

## Package Boundary

### What It Owns

The runtime owns ceremony binding, checked transitions, proof timestamps, and assurance evaluation.

### Public API and Import Surfaces

Import `EnrollmentRuntime`, `StepUpRuntime`, `FactorBinding`, `FactorStore`, and `satisfies_assurance` from `tba_runtime_mfa_lifecycle`.

### Entry Points

<!-- readme-standards:begin entry-points -->
This package declares no command-line, GUI, or plugin entry points in its manifest.
<!-- readme-standards:end entry-points -->

This is a library imported by a host runtime. It installs no executable.

### Injected Dependencies

Supply a `FactorStore`, verifiers keyed by factor, and optional time source.

### Protocol Consumers

Compose `MfaChallengeCapability` with a pair of begin and complete callbacks, or adapt the runtime through your existing route handlers.

### Extensions

The `totp` module accepts TBA's TOTP provider. Use the optional `webauthn` extra for protocol-backed passkeys.

---

## Operations and Readiness

### Operational Requirements

Use durable transactions and preserve the previous credential until replacement succeeds.

### Health and Observability

Report typed outcomes without recording factor secrets, raw proofs, or challenge IDs.

### Security and Resource Limits

Use bounded challenge lifetimes, encrypted secret storage, and host-owned attempt rate limits.

### Compatibility

This is the first package release. Pin the selected artifact and verify the host implementation against its storage contract.

---

## Verification

### Tests

Run `pkgs/120-tests/tba-tests-authentication/tests/unit/test_mfa_enrollment_step_up_runtime.py` with pytest.

### Certification Status

No external certification is claimed. Use the linked acceptance scope and changing evidence recorded in SSOT.

### Evidence

Use the [SSOT registry](../../../.ssot/registry.json) and execute the repository-owned synthetic tests.

---

## FAQ

### Why

Proof verification and credential updates can use the same transition rules across authenticator types.

### How

Create an attempt for the target account and submit the factor proof to its bound completion method.

### When

Use the lifecycle when independent carriers should share the same factor activation and assurance rules.

---

## Documentation and Related Packages

### More Documentation

See SPEC-1238 in the repository SSOT.

### Related Packages

TBA TOTP authenticator provider, WebAuthn protocol, and MFA challenge capability.

### Project Links

<!-- readme-standards:begin project-links -->
- [Documentation](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/060-runtime/tba-runtime-mfa-lifecycle#readme)
- [Homepage](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/060-runtime/tba-runtime-mfa-lifecycle#readme)
- [Issues](https://github.com/tigrbl/tigrbl_auth/issues)
- [PyPI](https://pypi.org/project/tba-runtime-mfa-lifecycle/)
- [Repository](https://github.com/tigrbl/tigrbl_auth)
- [SSOT](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [Source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/060-runtime/tba-runtime-mfa-lifecycle)
- [pypi: tba-runtime-mfa-lifecycle](https://pypi.org/project/tba-runtime-mfa-lifecycle/)
<!-- readme-standards:end project-links -->

---

## Contributing

### How to Contribute

Use the repository contribution guide and include an independent test for behavior changes.

### Development Setup

Run the test path listed above with the repository's uv-managed environment.

### Notes for Maintainers

Treat atomic replay plus activation behavior as part of the public store interface.

---

## Governance

### Ownership and Decision Making

ADR-1142 assigns ceremony transitions to the library and assurance policy to the host.

### Standards and Policies

Follow the repository layer and package policies. The host owns the deployment's identity policy.

### Lifecycle and Migration

Keep existing enrolled factors through migration and move activation paths one factor at a time.

---

## License and Attribution

### License

<!-- readme-standards:begin license -->
Licensed under `Apache-2.0`. See [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-mfa-lifecycle/LICENSE).
<!-- readme-standards:end license -->

### Notices

<!-- readme-standards:begin notices -->
See [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-mfa-lifecycle/NOTICE) for attribution.
<!-- readme-standards:end notices -->
