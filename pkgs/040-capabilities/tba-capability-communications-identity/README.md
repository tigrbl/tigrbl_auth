# tba-capability-communications-identity

<!-- readme-standards:begin branding -->
<p align="center"><a href="https://github.com/tigrbl/tigrbl_auth"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="300"></a></p>
<p align="center"><strong>tba-capability-communications-identity</strong></p>
<p align="center">Shared domain onboarding and recheck workflows.</p>
<p align="center">
<a href="https://pypi.org/project/tba-capability-communications-identity/"><img alt="pypi: tba-capability-communications-identity" src="https://img.shields.io/pypi/v/tba-capability-communications-identity"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-communications-identity/pyproject.toml"><img alt="Source version: 0.4.0.dev3" src="https://img.shields.io/static/v1?label=Source%20version&amp;message=0.4.0.dev3&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-communications-identity/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/static/v1?label=Python&amp;message=%3E%3D3.10%2C%3C3.16&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-communications-identity/pyproject.toml"><img alt="Layer: 040-capabilities" src="https://img.shields.io/static/v1?label=Layer&amp;message=040-capabilities&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-communications-identity/README.md#lifecycle-and-migration"><img alt="Lifecycle: active" src="https://img.shields.io/static/v1?label=Lifecycle&amp;message=active&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-communications-identity/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/static/v1?label=License&amp;message=Apache-2.0&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-communications-identity/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/static/v1?label=Notice&amp;message=attribution&amp;color=525252"></a>
</p>
<p align="center">
<a href="https://pypi.org/project/tba-capability-communications-identity/"><img alt="Monthly PyPI downloads: tba-capability-communications-identity" src="https://img.shields.io/pypi/dm/tba-capability-communications-identity"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-communications-identity/README.md"><img alt="README hits: tba-capability-communications-identity" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/pkgs/040-capabilities/tba-capability-communications-identity/README.md.svg?label=README%20hits"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="README standards: CI gate" src="https://img.shields.io/static/v1?label=README%20standards&amp;message=CI%20gate&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-communications-identity/docs/readme/test_examples.py"><img alt="Tests: example source" src="https://img.shields.io/static/v1?label=Tests&amp;message=example%20source&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-communications-identity/README.md#certification-status"><img alt="Certification: not certified" src="https://img.shields.io/static/v1?label=Certification&amp;message=not%20certified&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/tools/readme/POLICY.md"><img alt="Governance: repository policy" src="https://img.shields.io/static/v1?label=Governance&amp;message=repository%20policy&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="Evidence: source and CI" src="https://img.shields.io/static/v1?label=Evidence&amp;message=source%20and%20CI&amp;color=525252"></a>
</p>
<p align="center"><a href="#overview">Overview</a> · <a href="#installation">Installation</a> · <a href="#quick-start">Quick Start</a> · <a href="#usage">Usage</a> · <a href="#public-api-and-import-surfaces">API</a> · <a href="#contributing">Contributing</a> · <a href="#governance">Governance</a> · <a href="#license">License</a></p>
<!-- readme-standards:end branding -->

---

## Overview

### Summary

Shared domain onboarding and recheck workflows.

Implement `DomainChecker` to supply a channel-specific assessment, and pass
an async audit writer such as `tba_durability_audit.operations.audit.append_audit_event_async`.
`assess_domain_onboarding` records an initial assessment, and
`recheck_domain` records a follow-up. Both require an explicit tenant UUID.
The calling application authorizes the domain operation and owns persistence
and scheduling.

```python
from tba_capability_communications_identity import recheck_domain
from tba_durability_audit.operations.audit import append_audit_event_async

result = await recheck_domain(
    domain,
    checker=channel_checker,
    audit=append_audit_event_async,
    db=db,
    tenant_id=tenant_id,
)
```

- Package: `tba-capability-communications-identity`
- Layer: `040-capabilities`
- Responsibility: Shared domain onboarding and recheck workflows.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-communications-identity/src/tba_capability_communications_identity/__init__.py).
- Distribution: Python package on PyPI.

### Why This Package

`tba-capability-communications-identity` isolates this responsibility: Shared domain onboarding and recheck workflows. Its [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-communications-identity/src/tba_capability_communications_identity/__init__.py) exposes `AuditWriter`, `CommunicationsIdentityCapability`, `DomainCheck`, `DomainChecker`, `DomainOutcome`, `assess_domain_onboarding`, `recheck_domain`, allowing consumers to select this package without treating adjacent packages as part of its public contract.

### When to Use

Choose `tba-capability-communications-identity` for this responsibility: Shared domain onboarding and recheck workflows. Its `040-capabilities` placement keeps use-case orchestration through explicit collaborators separate from HTTP wire schemas, direct table ownership, or hidden provider selection.

### Features

- `CommunicationsIdentityCapability`: Compose domain assessment, recheck, and audit operations.
- `DomainOutcome`: declared in src/tba_capability_communications_identity/contracts.py
- `DomainCheck`: declared in src/tba_capability_communications_identity/contracts.py
- `DomainChecker`: declared in src/tba_capability_communications_identity/contracts.py
- `AuditWriter`: declared in src/tba_capability_communications_identity/contracts.py

### Non-Goals

`tba-capability-communications-identity` does not take ownership of HTTP wire schemas, direct table ownership, or hidden provider selection.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

---

## Getting Started

### Prerequisites

Python `>=3.10,<3.16` is required. The [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-communications-identity/pyproject.toml) declares runtime dependencies including `tba-concrete-capability`, `tba-contracts-identity`. Read the example’s inputs and service requirements before execution.

### Installation

Install the selected PyPI release of `tba-capability-communications-identity`:

```bash
uv pip install tba-capability-communications-identity
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/040-capabilities/tba-capability-communications-identity
```

#### uv

<!-- readme-standards:begin installation.uv -->
```bash
uv add tba-capability-communications-identity
```
<!-- readme-standards:end installation.uv -->

#### pip

<!-- readme-standards:begin installation.pip -->
```bash
python -m pip install tba-capability-communications-identity
```
<!-- readme-standards:end installation.pip -->

#### Poetry

<!-- readme-standards:begin installation.poetry -->
```bash
poetry add tba-capability-communications-identity
```
<!-- readme-standards:end installation.poetry -->

### Quick Start

Build the package from the repository root.

#### Example

<!-- readme-standards:begin example.quick-start -->
Source: [docs/readme/quick_start.sh](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-communications-identity/docs/readme/quick_start.sh).

```bash
uv build --wheel pkgs/040-capabilities/tba-capability-communications-identity
```
<!-- readme-standards:end example.quick-start -->

#### Expected Result

The example demonstrates the documented `tba-capability-communications-identity` source boundary or workflow. Complete its required configuration first. README CI checks the maintained source’s syntax and declarations; it does not claim that external services or the application workflow were exercised.

---

## Usage

### Common Workflows

<!-- readme-standards:begin example.usage -->
Source: [docs/readme/usage.sh](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-communications-identity/docs/readme/usage.sh).

```bash
uv build --wheel pkgs/040-capabilities/tba-capability-communications-identity
```
<!-- readme-standards:end example.usage -->

The following public-entry-point example belongs to `tba-capability-communications-identity`. Shared domain onboarding and recheck workflows. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_capability_communications_identity import recheck_domain
from tba_durability_audit.operations.audit import append_audit_event_async

result = await recheck_domain(
    domain,
    checker=channel_checker,
    audit=append_audit_event_async,
    db=db,
    tenant_id=tenant_id,
)
```

### Configuration

Configure `tba-capability-communications-identity` through the APIs in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-communications-identity/src/tba_capability_communications_identity/__init__.py); its [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-communications-identity/pyproject.toml) describes installation requirements, not an implicit service configuration. No additional package-global configuration contract is inferred from dependencies.

### Error Handling

The inspected `tba-capability-communications-identity` source raises `ValueError`. Handle these at the calling boundary and consult the implementation for the triggering conditions.

### Best Practices

Use the explicit `tba-capability-communications-identity` imports documented below and keep collaborator configuration with the caller. Run the package’s relevant tests after changing `AuditWriter`, `CommunicationsIdentityCapability`, `DomainCheck`, `DomainChecker`, `DomainOutcome`, `assess_domain_onboarding`, `recheck_domain`; an import or successful installation alone does not establish its runtime guarantees.

---

## Package Boundary

### What It Owns

`tba-capability-communications-identity` belongs to `040-capabilities` and owns use-case orchestration through explicit collaborators: Shared domain onboarding and recheck workflows.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-communications-identity/src/tba_capability_communications_identity/__init__.py). Public exports include `AuditWriter`, `CommunicationsIdentityCapability`, `DomainCheck`, `DomainChecker`, `DomainOutcome`, `assess_domain_onboarding`, `recheck_domain`.

Keep HTTP wire schemas, direct table ownership, or hidden provider selection in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

### Public API and Import Surfaces

Import namespace: `tba_capability_communications_identity`.

Source-declared exports or types: `AuditWriter`, `CommunicationsIdentityCapability`, `DomainCheck`, `DomainChecker`, `DomainOutcome`, `assess_domain_onboarding`, `recheck_domain`.

Inspect [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-communications-identity/src/tba_capability_communications_identity/__init__.py) for exact signatures; this inventory does not designate every internal module as stable.

### Entry Points

<!-- readme-standards:begin entry-points -->
This package declares no command-line, GUI, or plugin entry points in its manifest.
<!-- readme-standards:end entry-points -->

### Injected Dependencies

Explicit construction inputs and collaborators for `tba-capability-communications-identity`:

- `assess_domain_onboarding` construction inputs: `checker`, `audit`, `db`, `tenant_id`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-communications-identity/src/tba_capability_communications_identity/onboarding.py).
- `recheck_domain` construction inputs: `checker`, `audit`, `db`, `tenant_id`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-communications-identity/src/tba_capability_communications_identity/recheck.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

### Protocol Consumers

No direct package-manifest dependency on `tba-capability-communications-identity` was found in the audited three-repository inventory. External consumers may still use its documented imports or commands.

### Extensions

For `tba-capability-communications-identity`, use the source-declared public interfaces (`AuditWriter`, `CommunicationsIdentityCapability`, `DomainCheck`, `DomainChecker`, `DomainOutcome`, `assess_domain_onboarding`, `recheck_domain`) when composing or extending behavior. Its entry-point section below is authoritative for registered plugins; no additional extension loader is inferred from the package name.

---

## Operations and Readiness

### Operational Requirements

`tba-capability-communications-identity` exposes use-case orchestration through explicit collaborators. Public operations found in its source:

- `DomainChecker.profile` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-communications-identity/src/tba_capability_communications_identity/contracts.py).
- `DomainChecker.check` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-communications-identity/src/tba_capability_communications_identity/contracts.py).
- `assess_domain_onboarding` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-communications-identity/src/tba_capability_communications_identity/onboarding.py).
- `recheck_domain` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-communications-identity/src/tba_capability_communications_identity/recheck.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

### Health and Observability

This README does not establish a standalone health endpoint for `tba-capability-communications-identity`. Observe the concrete caller’s results, exceptions, and existing test reports. An application that embeds this package must define its own health and telemetry contract.

### Security and Resource Limits

Apply the input, credential, and resource constraints implemented in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-communications-identity/src/tba_capability_communications_identity/__init__.py). The `tba-capability-communications-identity` README gate is a documentation check, not a security review or a substitute for the implementation’s limits and caller authorization.

### Compatibility

This source version of `tba-capability-communications-identity` declares Python `>=3.10,<3.16`. Consult its dependency constraints before upgrading. Source-version and registry-version badges have separate meanings; this migration makes no additional platform or interoperability certification claim.

---

## Verification

### Tests

Check that the build produces a wheel with the package version declared in `pyproject.toml`.

### Certification Status

No external certification is asserted for `tba-capability-communications-identity` by this documentation migration. README conformance, example syntax, runtime tests, and protocol or security certification are distinct evidence scopes.

### Evidence

The [README standards CI](https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml) records mechanical documentation results for its tested commit. The [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-communications-identity/src/tba_capability_communications_identity/__init__.py) and example sources support the package-boundary description; external runtime behavior requires its own test evidence.

---

## FAQ

### Why

**Why select this package?** `tba-capability-communications-identity` provides shared domain onboarding and recheck workflows; use its own API boundary rather than assuming neighboring packages are bundled or configured automatically.

### How

**How do I start?** Install or synchronize the environment under Getting Started, follow the maintained example for `tba-capability-communications-identity`, and consult [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-communications-identity/src/tba_capability_communications_identity/__init__.py) for the exact types and signatures involved.

### When

**When should I validate an upgrade?** Recheck `tba-capability-communications-identity` whenever its source version, declared collaborators, configuration, or caller changes. Run relevant behavioral tests in addition to the README gate before promotion.

---

## Documentation and Related Packages

### More Documentation

The [repository contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md), [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-communications-identity/src/tba_capability_communications_identity/__init__.py), and [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-communications-identity/pyproject.toml) provide the supporting context for `tba-capability-communications-identity`. The [README policy](https://github.com/groupsum/readme-standards/blob/master/docs/outline.md) defines the common document structure.

### Related Packages

Declared local runtime dependencies:

- [tba-concrete-capability](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-capability/README.md)
- [tba-contracts-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-identity/README.md)

### Project Links

<!-- readme-standards:begin project-links -->
- [Documentation](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/040-capabilities/tba-capability-communications-identity#readme)
- [Homepage](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/040-capabilities/tba-capability-communications-identity#readme)
- [Issues](https://github.com/tigrbl/tigrbl_auth/issues)
- [PyPI](https://pypi.org/project/tba-capability-communications-identity/)
- [Repository](https://github.com/tigrbl/tigrbl_auth)
- [Source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/040-capabilities/tba-capability-communications-identity)
- [pypi: tba-capability-communications-identity](https://pypi.org/project/tba-capability-communications-identity/)
<!-- readme-standards:end project-links -->

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/040-capabilities/tba-capability-communications-identity)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-communications-identity/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-communications-identity/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-communications-identity/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-capability-communications-identity/)

---

## Contributing

### How to Contribute

Follow the [contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md) and include a focused example or regression for changes to `tba-capability-communications-identity`. Keep package behavior, its documented boundary, and its tests aligned.

### Development Setup

Work from the `pkgs/040-capabilities/tba-capability-communications-identity` checkout. Synchronize its declared development environment with uv, then run the relevant package tests and `python -m pytest docs/readme/test_examples.py`. The repository’s dedicated README job installs `readme-standards==0.1.1` without resolving unrelated runtime packages.

### Notes for Maintainers

Edit authored prose directly in this `tba-capability-communications-identity` README. Update source examples in `docs/readme/`, then run `readme-standards render --root . --write` from the package directory and review the diff. Required headings and generated blocks come from package-guide-v1.

---

## Governance

### Ownership and Decision Making

Changes to `tba-capability-communications-identity` follow the maintainer review process of [tigrbl/tigrbl_auth](https://github.com/tigrbl/tigrbl_auth) and its contribution guide. Author attribution remains in the [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-communications-identity/pyproject.toml); this README does not assign new publishing or administrative authority.

### Standards and Policies

`tba-capability-communications-identity` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `040-capabilities` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

### Lifecycle and Migration

The `tba-capability-communications-identity` source version is `0.4.0.dev3`. This change standardizes documentation and adds a development-only gate; it does not publish a new runtime version or declare a previously unpublished package released. Preserve explicit deprecation and replacement instructions where present.

---

## License and Attribution

### License

<!-- readme-standards:begin license -->
Licensed under `Apache-2.0`. See [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-communications-identity/LICENSE).
<!-- readme-standards:end license -->

### Notices

<!-- readme-standards:begin notices -->
See [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-communications-identity/NOTICE) for attribution.
<!-- readme-standards:end notices -->
