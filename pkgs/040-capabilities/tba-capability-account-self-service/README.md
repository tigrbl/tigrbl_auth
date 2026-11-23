# tba-capability-account-self-service

<!-- readme-standards:begin branding -->
<p align="center"><a href="https://github.com/tigrbl/tigrbl_auth"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="300"></a></p>
<p align="center"><strong>tba-capability-account-self-service</strong></p>
<p align="center">Composable protocol-neutral current-account self-service capability.</p>
<p align="center">
<a href="https://pypi.org/project/tba-capability-account-self-service/"><img alt="pypi: tba-capability-account-self-service" src="https://img.shields.io/pypi/v/tba-capability-account-self-service"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-account-self-service/pyproject.toml"><img alt="Source version: 0.4.0.dev3" src="https://img.shields.io/static/v1?label=Source%20version&amp;message=0.4.0.dev3&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-account-self-service/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/static/v1?label=Python&amp;message=%3E%3D3.10%2C%3C3.16&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-account-self-service/pyproject.toml"><img alt="Layer: 040-capabilities" src="https://img.shields.io/static/v1?label=Layer&amp;message=040-capabilities&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-account-self-service/README.md#lifecycle-and-migration"><img alt="Lifecycle: active" src="https://img.shields.io/static/v1?label=Lifecycle&amp;message=active&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-account-self-service/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/static/v1?label=License&amp;message=Apache-2.0&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-account-self-service/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/static/v1?label=Notice&amp;message=attribution&amp;color=525252"></a>
</p>
<p align="center">
<a href="https://pypi.org/project/tba-capability-account-self-service/"><img alt="Monthly PyPI downloads: tba-capability-account-self-service" src="https://img.shields.io/pypi/dm/tba-capability-account-self-service"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-account-self-service/README.md"><img alt="README hits: tba-capability-account-self-service" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/pkgs/040-capabilities/tba-capability-account-self-service/README.md.svg?label=README%20hits"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="README standards: CI gate" src="https://img.shields.io/static/v1?label=README%20standards&amp;message=CI%20gate&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-account-self-service/docs/readme/test_examples.py"><img alt="Tests: example source" src="https://img.shields.io/static/v1?label=Tests&amp;message=example%20source&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-account-self-service/README.md#certification-status"><img alt="Certification: not certified" src="https://img.shields.io/static/v1?label=Certification&amp;message=not%20certified&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/tools/readme/POLICY.md"><img alt="Governance: repository policy" src="https://img.shields.io/static/v1?label=Governance&amp;message=repository%20policy&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="Evidence: source and CI" src="https://img.shields.io/static/v1?label=Evidence&amp;message=source%20and%20CI&amp;color=525252"></a>
</p>
<p align="center"><a href="#overview">Overview</a> · <a href="#installation">Installation</a> · <a href="#quick-start">Quick Start</a> · <a href="#usage">Usage</a> · <a href="#public-api-and-import-surfaces">API</a> · <a href="#contributing">Contributing</a> · <a href="#governance">Governance</a> · <a href="#license">License</a></p>
<!-- readme-standards:end branding -->

---

## Overview

### Summary

Compose current-account profile, password, session, and consent operations over injected delegates.

- Package: `tba-capability-account-self-service`
- Layer: `040-capabilities`
- Responsibility: Composable protocol-neutral current-account self-service capability.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-account-self-service/src/tba_capability_account_self_service/__init__.py).
- Distribution: Python package on PyPI.

### Why This Package

`tba-capability-account-self-service` isolates this responsibility: Composable protocol-neutral current-account self-service capability. Its [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-account-self-service/src/tba_capability_account_self_service/__init__.py) exposes `AccountOperation`, `AccountSelfServiceCapability`, allowing consumers to select this package without treating adjacent packages as part of its public contract.

### When to Use

Pass eight callables to bind nine operations. Consent listing also supplies the authorized-app list. Calls take an authenticated `AccountPrincipal`. The My Account backend supplies authentication and persistence delegates. The example implements the profile reader and raises if another operation is called.

### Features

- `AccountSelfServiceCapability`: declared in src/tba_capability_account_self_service/__init__.py

### Non-Goals

This package owns no tables, sessions, HTTP objects, hashing provider, request
authentication, or protocol binding.

---

## Getting Started

### Prerequisites

Python `>=3.10,<3.16` is required. The [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-account-self-service/pyproject.toml) declares runtime dependencies including `tba-concrete-capability`, `tba-contracts-identity`. Read the example’s inputs and service requirements before execution.

### Installation

Install the selected PyPI release of `tba-capability-account-self-service`:

```bash
uv pip install tba-capability-account-self-service
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/040-capabilities/tba-capability-account-self-service
```

#### uv

<!-- readme-standards:begin installation.uv -->
```bash
uv add tba-capability-account-self-service
```
<!-- readme-standards:end installation.uv -->

#### pip

<!-- readme-standards:begin installation.pip -->
```bash
python -m pip install tba-capability-account-self-service
```
<!-- readme-standards:end installation.pip -->

#### Poetry

<!-- readme-standards:begin installation.poetry -->
```bash
poetry add tba-capability-account-self-service
```
<!-- readme-standards:end installation.poetry -->

### Quick Start

Install the version used by this example.

```bash
python -m pip install "tba-capability-account-self-service==0.4.0.dev3"
```

Save the following as `quickstart.py` and run `python quickstart.py`. The assertions should pass.

#### Example

<!-- readme-standards:begin example.quick-start -->
Source: [docs/readme/quick_start.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-account-self-service/docs/readme/quick_start.py).

```python
import asyncio

from tba_capability_account_self_service import AccountSelfServiceCapability
from tba_contracts_identity.account_self_service import AccountPrincipal, AccountProfile


def read_profile(principal):
    return AccountProfile(
        principal.identity_id, "tenant", "alice", "alice@example.test"
    )


def unbound(*args):
    raise NotImplementedError("profile-only demo")


account = AccountSelfServiceCapability(
    profile_reader=read_profile,
    profile_updater=unbound,
    password_changer=unbound,
    session_lister=unbound,
    session_revoker=unbound,
    consent_lister=unbound,
    consent_revoker=unbound,
    authorized_app_revoker=unbound,
)
profile = asyncio.run(account.get_profile(AccountPrincipal("identity", "tenant")))
assert profile.username == "alice"
```
<!-- readme-standards:end example.quick-start -->

#### Expected Result

The example demonstrates the documented `tba-capability-account-self-service` source boundary or workflow. Complete its required configuration first. README CI checks the maintained source’s syntax and declarations; it does not claim that external services or the application workflow were exercised.

---

## Usage

### Common Workflows

<!-- readme-standards:begin example.usage -->
Source: [docs/readme/usage.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-account-self-service/docs/readme/usage.py).

```python
import asyncio

from tba_capability_account_self_service import AccountSelfServiceCapability
from tba_contracts_identity.account_self_service import AccountPrincipal, AccountProfile


def read_profile(principal):
    return AccountProfile(
        principal.identity_id, "tenant", "alice", "alice@example.test"
    )


def unbound(*args):
    raise NotImplementedError("profile-only demo")


account = AccountSelfServiceCapability(
    profile_reader=read_profile,
    profile_updater=unbound,
    password_changer=unbound,
    session_lister=unbound,
    session_revoker=unbound,
    consent_lister=unbound,
    consent_revoker=unbound,
    authorized_app_revoker=unbound,
)
profile = asyncio.run(account.get_profile(AccountPrincipal("identity", "tenant")))
assert profile.username == "alice"
```
<!-- readme-standards:end example.usage -->

The following public-entry-point example belongs to `tba-capability-account-self-service`. Composable protocol-neutral current-account self-service capability. Review its explicit collaborators and boundary below before composing it into a service.

### Configuration

Configure `tba-capability-account-self-service` through the APIs in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-account-self-service/src/tba_capability_account_self_service/__init__.py); its [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-account-self-service/pyproject.toml) describes installation requirements, not an implicit service configuration. No additional package-global configuration contract is inferred from dependencies.

### Error Handling

The inspected `tba-capability-account-self-service` source raises `AccountNotFoundError`, `TypeError`. Handle these at the calling boundary and consult the implementation for the triggering conditions.

### Best Practices

Use the explicit `tba-capability-account-self-service` imports documented below and keep collaborator configuration with the caller. Run the package’s relevant tests after changing `AccountOperation`, `AccountSelfServiceCapability`; an import or successful installation alone does not establish its runtime guarantees.

---

## Package Boundary

### What It Owns

`tba-capability-account-self-service` belongs to `040-capabilities` and owns use-case orchestration through explicit collaborators: Composable protocol-neutral current-account self-service capability.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-account-self-service/src/tba_capability_account_self_service/__init__.py). Public exports include `AccountOperation`, `AccountSelfServiceCapability`.

Keep HTTP wire schemas, direct table ownership, or hidden provider selection in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

### Public API and Import Surfaces

Import namespace: `tba_capability_account_self_service`.

Source-declared exports or types: `AccountOperation`, `AccountSelfServiceCapability`.

Inspect [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-account-self-service/src/tba_capability_account_self_service/__init__.py) for exact signatures; this inventory does not designate every internal module as stable.

### Entry Points

<!-- readme-standards:begin entry-points -->
This package declares no command-line, GUI, or plugin entry points in its manifest.
<!-- readme-standards:end entry-points -->

### Injected Dependencies

Explicit construction inputs and collaborators for `tba-capability-account-self-service`:

- `AccountSelfServiceCapability` construction inputs: `profile_reader`, `profile_updater`, `password_changer`, `session_lister`, `session_revoker`, `consent_lister`, `consent_revoker`, `authorized_app_revoker`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-account-self-service/src/tba_capability_account_self_service/__init__.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

### Protocol Consumers

Direct consumers in this checkout’s package manifests include `tba-server-identity`, `tba-app-backend-my-account`, `tba-workspace`. These edges describe declared dependencies, not protocol-conformance evidence.

### Extensions

For `tba-capability-account-self-service`, use the source-declared public interfaces (`AccountOperation`, `AccountSelfServiceCapability`) when composing or extending behavior. Its entry-point section below is authoritative for registered plugins; no additional extension loader is inferred from the package name.

---

## Operations and Readiness

### Operational Requirements

`tba-capability-account-self-service` exposes use-case orchestration through explicit collaborators. Public operations found in its source:

- `AccountSelfServiceCapability.get_profile` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-account-self-service/src/tba_capability_account_self_service/__init__.py).
- `AccountSelfServiceCapability.update_profile` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-account-self-service/src/tba_capability_account_self_service/__init__.py).
- `AccountSelfServiceCapability.change_password` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-account-self-service/src/tba_capability_account_self_service/__init__.py).
- `AccountSelfServiceCapability.list_sessions` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-account-self-service/src/tba_capability_account_self_service/__init__.py).
- `AccountSelfServiceCapability.revoke_session` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-account-self-service/src/tba_capability_account_self_service/__init__.py).
- `AccountSelfServiceCapability.list_consents` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-account-self-service/src/tba_capability_account_self_service/__init__.py).
- `AccountSelfServiceCapability.list_authorized_apps` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-account-self-service/src/tba_capability_account_self_service/__init__.py).
- `AccountSelfServiceCapability.revoke_consent` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-account-self-service/src/tba_capability_account_self_service/__init__.py).
- `AccountSelfServiceCapability.revoke_authorized_app` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-account-self-service/src/tba_capability_account_self_service/__init__.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

### Health and Observability

This README does not establish a standalone health endpoint for `tba-capability-account-self-service`. Observe the concrete caller’s results, exceptions, and existing test reports. An application that embeds this package must define its own health and telemetry contract.

### Security and Resource Limits

Apply the input, credential, and resource constraints implemented in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-account-self-service/src/tba_capability_account_self_service/__init__.py). The `tba-capability-account-self-service` README gate is a documentation check, not a security review or a substitute for the implementation’s limits and caller authorization.

### Compatibility

This source version of `tba-capability-account-self-service` declares Python `>=3.10,<3.16`. Consult its dependency constraints before upgrading. Source-version and registry-version badges have separate meanings; this migration makes no additional platform or interoperability certification claim.

---

## Verification

### Tests

See the [related repository tests](https://github.com/tigrbl/tigrbl_auth/blob/master/tests/unit/test_account_self_service_capability.py) for the implementation scope covered by this example.

[Workspace and package catalog](https://github.com/tigrbl/tigrbl_auth#package-catalog) · [@tba/ui-my-account](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/105-ui/tba-ui-my-account#readme) · [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues) · [Repository license](https://github.com/tigrbl/tigrbl_auth/blob/master/LICENSE)

### Certification Status

No external certification is asserted for `tba-capability-account-self-service` by this documentation migration. README conformance, example syntax, runtime tests, and protocol or security certification are distinct evidence scopes.

### Evidence

The [README standards CI](https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml) records mechanical documentation results for its tested commit. The [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-account-self-service/src/tba_capability_account_self_service/__init__.py) and example sources support the package-boundary description; external runtime behavior requires its own test evidence.

---

## FAQ

### Why

**Why select this package?** `tba-capability-account-self-service` provides composable protocol-neutral current-account self-service capability; use its own API boundary rather than assuming neighboring packages are bundled or configured automatically.

### How

**How do I start?** Install or synchronize the environment under Getting Started, follow the maintained example for `tba-capability-account-self-service`, and consult [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-account-self-service/src/tba_capability_account_self_service/__init__.py) for the exact types and signatures involved.

### When

**When should I validate an upgrade?** Recheck `tba-capability-account-self-service` whenever its source version, declared collaborators, configuration, or caller changes. Run relevant behavioral tests in addition to the README gate before promotion.

---

## Documentation and Related Packages

### More Documentation

The [repository contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md), [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-account-self-service/src/tba_capability_account_self_service/__init__.py), and [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-account-self-service/pyproject.toml) provide the supporting context for `tba-capability-account-self-service`. The [README policy](https://github.com/groupsum/readme-standards/blob/master/docs/outline.md) defines the common document structure.

### Related Packages

Declared local runtime dependencies:

- [tba-concrete-capability](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-capability/README.md)
- [tba-contracts-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-identity/README.md)

Direct downstream consumers:

- [tba-app-backend-my-account](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-my-account/README.md)
- [tba-server-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-server-identity/README.md)

### Project Links

<!-- readme-standards:begin project-links -->
- [Documentation](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/040-capabilities/tba-capability-account-self-service#readme)
- [Homepage](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/040-capabilities/tba-capability-account-self-service#readme)
- [Issues](https://github.com/tigrbl/tigrbl_auth/issues)
- [PyPI](https://pypi.org/project/tba-capability-account-self-service/)
- [Repository](https://github.com/tigrbl/tigrbl_auth)
- [Source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/040-capabilities/tba-capability-account-self-service)
- [pypi: tba-capability-account-self-service](https://pypi.org/project/tba-capability-account-self-service/)
<!-- readme-standards:end project-links -->

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/040-capabilities/tba-capability-account-self-service)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-account-self-service/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-account-self-service/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-account-self-service/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-capability-account-self-service/)

---

## Contributing

### How to Contribute

Follow the [contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md) and include a focused example or regression for changes to `tba-capability-account-self-service`. Keep package behavior, its documented boundary, and its tests aligned.

### Development Setup

Work from the `pkgs/040-capabilities/tba-capability-account-self-service` checkout. Synchronize its declared development environment with uv, then run the relevant package tests and `python -m pytest docs/readme/test_examples.py`. The repository’s dedicated README job installs `readme-standards==0.1.1` without resolving unrelated runtime packages.

### Notes for Maintainers

Edit authored prose directly in this `tba-capability-account-self-service` README. Update source examples in `docs/readme/`, then run `readme-standards render --root . --write` from the package directory and review the diff. Required headings and generated blocks come from package-guide-v1.

---

## Governance

### Ownership and Decision Making

Changes to `tba-capability-account-self-service` follow the maintainer review process of [tigrbl/tigrbl_auth](https://github.com/tigrbl/tigrbl_auth) and its contribution guide. Author attribution remains in the [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-account-self-service/pyproject.toml); this README does not assign new publishing or administrative authority.

### Standards and Policies

`tba-capability-account-self-service` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `040-capabilities` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

### Lifecycle and Migration

The `tba-capability-account-self-service` source version is `0.4.0.dev3`. This change standardizes documentation and adds a development-only gate; it does not publish a new runtime version or declare a previously unpublished package released. Preserve explicit deprecation and replacement instructions where present.

---

## License and Attribution

### License

<!-- readme-standards:begin license -->
Licensed under `Apache-2.0`. See [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-account-self-service/LICENSE).
<!-- readme-standards:end license -->

### Notices

<!-- readme-standards:begin notices -->
See [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-account-self-service/NOTICE) for attribution.
<!-- readme-standards:end notices -->
