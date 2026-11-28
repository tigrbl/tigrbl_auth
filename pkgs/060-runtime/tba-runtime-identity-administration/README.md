# tba-runtime-identity-administration

<!-- readme-standards:begin branding -->
<p align="center"><a href="https://github.com/tigrbl/tigrbl_auth"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="300"></a></p>
<p align="center"><strong>tba-runtime-identity-administration</strong></p>
<p align="center">Administrative identity control plane for tenants, users, clients, keys, sessions, tokens, audit, consent, profiles, and governance.</p>
<p align="center">
<a href="https://pypi.org/project/tba-runtime-identity-administration/"><img alt="pypi: tba-runtime-identity-administration" src="https://img.shields.io/pypi/v/tba-runtime-identity-administration?labelColor=1E293B&amp;color=1D4ED8"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity-administration/pyproject.toml"><img alt="Source version: 0.4.0.dev3" src="https://img.shields.io/static/v1?label=Source%20version&amp;message=0.4.0.dev3&amp;labelColor=1E293B&amp;color=4338CA"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity-administration/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/static/v1?label=Python&amp;message=%3E%3D3.10%2C%3C3.16&amp;labelColor=1E293B&amp;color=0F766E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity-administration/pyproject.toml"><img alt="Layer: 060-runtime" src="https://img.shields.io/static/v1?label=Layer&amp;message=060-runtime&amp;labelColor=1E293B&amp;color=6D28D9"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity-administration/README.md#lifecycle-and-migration"><img alt="Lifecycle: active" src="https://img.shields.io/static/v1?label=Lifecycle&amp;message=active&amp;labelColor=1E293B&amp;color=166534"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity-administration/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/static/v1?label=License&amp;message=Apache-2.0&amp;labelColor=1E293B&amp;color=86198F"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity-administration/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/static/v1?label=Notice&amp;message=attribution&amp;labelColor=1E293B&amp;color=86198F"></a>
</p>
<p align="center">
<a href="https://pypi.org/project/tba-runtime-identity-administration/"><img alt="Monthly PyPI downloads: tba-runtime-identity-administration" src="https://img.shields.io/pypi/dm/tba-runtime-identity-administration?labelColor=1E293B&amp;color=0E7490"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity-administration/README.md"><img alt="README hits: tba-runtime-identity-administration" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/pkgs/060-runtime/tba-runtime-identity-administration/README.md.svg?label=README%20hits&amp;labelColor=1E293B&amp;color=0E7490"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="README standards: CI gate" src="https://img.shields.io/static/v1?label=README%20standards&amp;message=CI%20gate&amp;labelColor=1E293B&amp;color=1D4ED8"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity-administration/docs/readme/test_examples.py"><img alt="Tests: example source" src="https://img.shields.io/static/v1?label=Tests&amp;message=example%20source&amp;labelColor=1E293B&amp;color=0F766E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity-administration/README.md#certification-status"><img alt="Certification: not certified" src="https://img.shields.io/static/v1?label=Certification&amp;message=not%20certified&amp;labelColor=1E293B&amp;color=92400E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/tools/readme/POLICY.md"><img alt="Governance: repository policy" src="https://img.shields.io/static/v1?label=Governance&amp;message=repository%20policy&amp;labelColor=1E293B&amp;color=4338CA"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="Evidence: source and CI" src="https://img.shields.io/static/v1?label=Evidence&amp;message=source%20and%20CI&amp;labelColor=1E293B&amp;color=6D28D9"></a>
</p>
<p align="center"><a href="#overview">Overview</a> · <a href="#installation">Installation</a> · <a href="#quick-start">Quick Start</a> · <a href="#usage">Usage</a> · <a href="#public-api-and-import-surfaces">API</a> · <a href="#contributing">Contributing</a> · <a href="#governance">Governance</a> · <a href="#license">License</a></p>
<!-- readme-standards:end branding -->

---

## Overview

### Summary

tba-runtime-identity-administration contains runtime composition for storage-backed administration capabilities for a TBA identity deployment. It supplies tenant, user, client, key, session, token, consent, audit, profile, and governance integrations to upper-layer control-plane use cases.

- Package: `tba-runtime-identity-administration`
- Import root: `tba_runtime_identity_administration`
- Component kind: Platform package
- Use it for Administrator/control-plane identity management objects.
- It is not the public OAuth/OIDC flow package; it manages storage-backed administrative mutations and views.
- It works with policy, storage, credentials, JOSE, OAuth, and OIDC packages to expose governed operations.
- Admin runtime helpers and advanced identity integrations compose storage-owned tables below the application capability layer.

### Why This Package

`tba-runtime-identity-administration` isolates this responsibility: Administrative identity control plane for tenants, users, clients, keys, sessions, tokens, audit, consent, profiles, and governance. Its [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity-administration/src/tba_runtime_identity_administration/__init__.py) exposes `AdminControlPlane`, `AdminControlPlaneError`, `AdminResource`, `AdminResourceKind`, `AdminResourceStatus`, `App`, allowing consumers to select this package without treating adjacent packages as part of its public contract.

### When to Use

Choose `tba-runtime-identity-administration` for this responsibility: Administrative identity control plane for tenants, users, clients, keys, sessions, tokens, audit, consent, profiles, and governance. Its `060-runtime` placement keeps runtime composition and operator entry points separate from duplicating protocol grammars, table declarations, or provider implementations.

### Features

- `AdvancedAuthenticatorRegistry`: declared in src/tba_runtime_identity_administration/_advanced_identity_plane/authenticators.py
- `AdvancedAuthenticationCapability`: declared in src/tba_runtime_identity_administration/_advanced_identity_plane/capability.py
- `DeviceWorkloadIdentityRegistry`: declared in src/tba_runtime_identity_administration/_advanced_identity_plane/identities.py

### Non-Goals

`tba-runtime-identity-administration` does not take ownership of duplicating protocol grammars, table declarations, or provider implementations.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

---

## Getting Started

### Prerequisites

Python `>=3.10,<3.16` is required. The [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity-administration/pyproject.toml) declares runtime dependencies including `tba-capability-adaptive-authentication`, `tba-capability-administrative-resource`, `tba-capability-identity-administration`, `tba-capability-operator-administration`, `tba-capability-realm-administration`, `tba-capability-tenant-administration`, `tba-concrete-capability`, `tba-contracts-identity`, `tba-primitives-identity`, `tba-concrete-mfa-factor`, `tba-concrete-passwordless-credential`, `tba-concrete-webauthn-credential`. Read the example’s inputs and service requirements before execution.

### Installation

```bash
pip install tba-runtime-identity-administration
# or
uv add tba-runtime-identity-administration
```

Install the current `tba-runtime-identity-administration` source checkout when working ahead of a PyPI release:

```bash
uv pip install ./pkgs/060-runtime/tba-runtime-identity-administration
```

#### uv

<!-- readme-standards:begin installation.uv -->
```bash
uv add tba-runtime-identity-administration
```
<!-- readme-standards:end installation.uv -->

#### pip

<!-- readme-standards:begin installation.pip -->
```bash
python -m pip install tba-runtime-identity-administration
```
<!-- readme-standards:end installation.pip -->

#### Poetry

<!-- readme-standards:begin installation.poetry -->
```bash
poetry add tba-runtime-identity-administration
```
<!-- readme-standards:end installation.poetry -->

### Quick Start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.


```bash
uv run --isolated --no-project --python 3.12 --with "tba-runtime-identity-administration==0.4.0.dev3" python quickstart.py
```

The import and assertion succeed when the AdminControlPlane entry point is available.

#### Example

<!-- readme-standards:begin example.quick-start -->
Source: [docs/readme/quick_start.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity-administration/docs/readme/quick_start.py).

```python
from tba_runtime_identity_administration import AdminControlPlane

assert callable(AdminControlPlane)
```
<!-- readme-standards:end example.quick-start -->

#### Expected Result

The example demonstrates the documented `tba-runtime-identity-administration` source boundary or workflow. Complete its required configuration first. README CI checks the maintained source’s syntax and declarations; it does not claim that external services or the application workflow were exercised.

---

## Usage

### Common Workflows

<!-- readme-standards:begin example.usage -->
Source: [docs/readme/usage.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity-administration/docs/readme/usage.py).

```python
from tba_runtime_identity_administration.audit_service import list_audit_events
from tba_runtime_identity_administration.bootstrap import user_is_admin
from tba_runtime_identity_administration import AdminControlPlane
```
<!-- readme-standards:end example.usage -->

### Configuration

Configure `tba-runtime-identity-administration` through the APIs in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity-administration/src/tba_runtime_identity_administration/__init__.py); its [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity-administration/pyproject.toml) describes installation requirements, not an implicit service configuration. No additional package-global configuration contract is inferred from dependencies.

### Error Handling

The inspected `tba-runtime-identity-administration` source raises `NotImplementedError`, `PermissionError`, `ValueError`. Handle these at the calling boundary and consult the implementation for the triggering conditions.

### Best Practices

Use the explicit `tba-runtime-identity-administration` imports documented below and keep collaborator configuration with the caller. Run the package’s relevant tests after changing `AdminControlPlane`, `AdminControlPlaneError`, `AdminResource`, `AdminResourceKind`, `AdminResourceStatus`, `App`; an import or successful installation alone does not establish its runtime guarantees.

---

## Package Boundary

### What It Owns

- Admin identity bootstrap
- AdminControlPlane public exports backed by `tigrbl-identity-admin-control-plane`
- Client, key, token, session, consent, profile, audit, and governance REST services
- Storage-backed administrative handlers
- Audit and client administration services

### Public API and Import Surfaces

Import namespace: `tba_runtime_identity_administration`.

Source-declared exports or types: `AdminControlPlane`, `AdminControlPlaneError`, `AdminResource`, `AdminResourceKind`, `AdminResourceStatus`, `App`.

Inspect [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity-administration/src/tba_runtime_identity_administration/__init__.py) for exact signatures; this inventory does not designate every internal module as stable.

### Entry Points

<!-- readme-standards:begin entry-points -->
This package declares no command-line, GUI, or plugin entry points in its manifest.
<!-- readme-standards:end entry-points -->

### Injected Dependencies

The [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity-administration/src/tba_runtime_identity_administration/__init__.py) for `tba-runtime-identity-administration` does not declare an explicit service-constructor or keyword-only factory hook in the inspected source. Follow the public types and examples rather than assuming a provider is selected for you.

Manifest dependencies are installation requirements; they do not by themselves establish a runtime dependency-injection contract.

### Protocol Consumers

Direct consumers in this checkout’s package manifests include `tba-auth`, `tba-workspace`. These edges describe declared dependencies, not protocol-conformance evidence.

### Extensions

For `tba-runtime-identity-administration`, use the source-declared public interfaces (`AdminControlPlane`, `AdminControlPlaneError`, `AdminResource`, `AdminResourceKind`, `AdminResourceStatus`, `App`) when composing or extending behavior. Its entry-point section below is authoritative for registered plugins; no additional extension loader is inferred from the package name.

---

## Operations and Readiness

### Operational Requirements

`tba-runtime-identity-administration` exposes runtime composition and operator entry points. Inspect the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity-administration/src/tba_runtime_identity_administration/__init__.py) for the exported types and composition surface.

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

### Health and Observability

This README does not establish a standalone health endpoint for `tba-runtime-identity-administration`. Observe the concrete caller’s results, exceptions, and existing test reports. An application that embeds this package must define its own health and telemetry contract.

### Security and Resource Limits

Apply the input, credential, and resource constraints implemented in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity-administration/src/tba_runtime_identity_administration/__init__.py). The `tba-runtime-identity-administration` README gate is a documentation check, not a security review or a substitute for the implementation’s limits and caller authorization.

### Compatibility

This source version of `tba-runtime-identity-administration` declares Python `>=3.10,<3.16`. Consult its dependency constraints before upgrading. Source-version and registry-version badges have separate meanings; this migration makes no additional platform or interoperability certification claim.

---

## Verification

### Tests

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity-administration/src/tba_runtime_identity_administration/__init__.py).

### Certification Status

No external certification is asserted for `tba-runtime-identity-administration` by this documentation migration. README conformance, example syntax, runtime tests, and protocol or security certification are distinct evidence scopes.

### Evidence

The [README standards CI](https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml) records mechanical documentation results for its tested commit. The [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity-administration/src/tba_runtime_identity_administration/__init__.py) and example sources support the package-boundary description; external runtime behavior requires its own test evidence.

---

## FAQ

### Why

**Why select this package?** `tba-runtime-identity-administration` provides administrative identity control plane for tenants, users, clients, keys, sessions, tokens, audit, consent, profiles, and governance; use its own API boundary rather than assuming neighboring packages are bundled or configured automatically.

### How

**How do I start?** Install or synchronize the environment under Getting Started, follow the maintained example for `tba-runtime-identity-administration`, and consult [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity-administration/src/tba_runtime_identity_administration/__init__.py) for the exact types and signatures involved.

### When

**When should I validate an upgrade?** Recheck `tba-runtime-identity-administration` whenever its source version, declared collaborators, configuration, or caller changes. Run relevant behavioral tests in addition to the README gate before promotion.

---

## Documentation and Related Packages

### More Documentation

The [repository contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md), [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity-administration/src/tba_runtime_identity_administration/__init__.py), and [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity-administration/pyproject.toml) provide the supporting context for `tba-runtime-identity-administration`. The [README policy](https://github.com/groupsum/readme-standards/blob/master/docs/outline.md) defines the common document structure.

### Related Packages

- [tba-runtime-identity-administration](https://pypi.org/project/tba-runtime-identity-administration/)
- [tigrbl-identity-admin-control-plane](https://pypi.org/project/tigrbl-identity-admin-control-plane/)
- [tba-storage-core](https://pypi.org/project/tba-storage-core/)
- [tba-server-identity](https://pypi.org/project/tba-server-identity/)
- [tba-runtime-identity](https://pypi.org/project/tba-runtime-identity/)
- [tba-tests-identity](https://pypi.org/project/tba-tests-identity/)

### Project Links

<!-- readme-standards:begin project-links -->
- [Documentation](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/060-runtime/tba-runtime-identity-administration#readme)
- [Homepage](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/060-runtime/tba-runtime-identity-administration#readme)
- [Issues](https://github.com/tigrbl/tigrbl_auth/issues)
- [PyPI](https://pypi.org/project/tba-runtime-identity-administration/)
- [Repository](https://github.com/tigrbl/tigrbl_auth)
- [SSOT](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [Source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/060-runtime/tba-runtime-identity-administration)
- [pypi: tba-runtime-identity-administration](https://pypi.org/project/tba-runtime-identity-administration/)
<!-- readme-standards:end project-links -->

- [PyPI package](https://pypi.org/project/tba-runtime-identity-administration/)
- [Source repository](https://github.com/tigrbl/tigrbl_auth)
- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/060-runtime/tba-runtime-identity-administration)
- [SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/060-runtime/tba-runtime-identity-administration)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity-administration/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity-administration/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity-administration/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-runtime-identity-administration/)

---

## Contributing

### How to Contribute

Follow the [contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md) and include a focused example or regression for changes to `tba-runtime-identity-administration`. Keep package behavior, its documented boundary, and its tests aligned.

### Development Setup

Work from the `pkgs/060-runtime/tba-runtime-identity-administration` checkout. Synchronize its declared development environment with uv, then run the relevant package tests and `python -m pytest docs/readme/test_examples.py`. The repository’s dedicated README job installs `readme-standards==0.1.3` without resolving unrelated runtime packages.

### Notes for Maintainers

Edit authored prose directly in this `tba-runtime-identity-administration` README. Update source examples in `docs/readme/`, then run `readme-standards render --root . --write` from the package directory and review the diff. Required headings and generated blocks come from package-guide-v1.

---

## Governance

### Ownership and Decision Making

Changes to `tba-runtime-identity-administration` follow the maintainer review process of [tigrbl/tigrbl_auth](https://github.com/tigrbl/tigrbl_auth) and its contribution guide. Author attribution remains in the [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity-administration/pyproject.toml); this README does not assign new publishing or administrative authority.

### Standards and Policies

This package is part of the SSOT-governed TBA identity package suite. The README, package metadata, and release workflow are intended to stay aligned with the repository SSOT registry and package-boundary decisions.

`tba-runtime-identity-administration` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `060-runtime` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

### Lifecycle and Migration

The `tba-runtime-identity-administration` source version is `0.4.0.dev3`. This change standardizes documentation and adds a development-only gate; it does not publish a new runtime version or declare a previously unpublished package released. Preserve explicit deprecation and replacement instructions where present.

---

## License and Attribution

### License

<!-- readme-standards:begin license -->
Licensed under `Apache-2.0`. See [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity-administration/LICENSE).
<!-- readme-standards:end license -->

### Notices

<!-- readme-standards:begin notices -->
See [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity-administration/NOTICE) for attribution.
<!-- readme-standards:end notices -->
