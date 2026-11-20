# tba-tests-identity

<!-- readme-standards:begin branding -->
<p align="center"><a href="https://github.com/tigrbl/tigrbl_auth"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="300"></a></p>
<p align="center"><strong>tba-tests-identity</strong></p>
<p align="center">Test fixtures, fake identity components, conformance vectors, integration harnesses, and cross-cutting verification helpers.</p>
<p align="center">
<a href="https://pypi.org/project/tba-tests-identity/"><img alt="pypi: tba-tests-identity" src="https://img.shields.io/pypi/v/tba-tests-identity"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-identity/pyproject.toml"><img alt="Source version: 0.4.0.dev3" src="https://img.shields.io/static/v1?label=Source%20version&amp;message=0.4.0.dev3&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-identity/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/static/v1?label=Python&amp;message=%3E%3D3.10%2C%3C3.16&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-identity/pyproject.toml"><img alt="Layer: 120-tests" src="https://img.shields.io/static/v1?label=Layer&amp;message=120-tests&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-identity/README.md#lifecycle-and-migration"><img alt="Lifecycle: active" src="https://img.shields.io/static/v1?label=Lifecycle&amp;message=active&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-identity/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/static/v1?label=License&amp;message=Apache-2.0&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-identity/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/static/v1?label=Notice&amp;message=attribution&amp;color=525252"></a>
</p>
<p align="center">
<a href="https://pypi.org/project/tba-tests-identity/"><img alt="Monthly PyPI downloads: tba-tests-identity" src="https://img.shields.io/pypi/dm/tba-tests-identity"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-identity/README.md"><img alt="README hits: tba-tests-identity" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/pkgs/120-tests/tba-tests-identity/README.md.svg?label=README%20hits"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="README standards: CI gate" src="https://img.shields.io/static/v1?label=README%20standards&amp;message=CI%20gate&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-identity/docs/readme/test_examples.py"><img alt="Tests: example source" src="https://img.shields.io/static/v1?label=Tests&amp;message=example%20source&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-identity/README.md#certification-status"><img alt="Certification: not certified" src="https://img.shields.io/static/v1?label=Certification&amp;message=not%20certified&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/tools/readme/POLICY.md"><img alt="Governance: repository policy" src="https://img.shields.io/static/v1?label=Governance&amp;message=repository%20policy&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="Evidence: source and CI" src="https://img.shields.io/static/v1?label=Evidence&amp;message=source%20and%20CI&amp;color=525252"></a>
</p>
<p align="center"><a href="#overview">Overview</a> · <a href="#installation">Installation</a> · <a href="#quick-start">Quick Start</a> · <a href="#usage">Usage</a> · <a href="#public-api-and-import-surfaces">API</a> · <a href="#contributing">Contributing</a> · <a href="#governance">Governance</a> · <a href="#license">License</a></p>
<!-- readme-standards:end branding -->

---

## Overview

### Summary

Reuse deterministic identity fixtures, fake flows, and cross-language vectors in tests.

- Package: `tba-tests-identity`
- Layer: `120-tests`
- Responsibility: Test fixtures, fake identity components, conformance vectors, integration harnesses, and cross-cutting verification helpers.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-identity/src/tba_tests_identity/__init__.py).
- Distribution: Python package on PyPI.

### Why This Package

`tba-tests-identity` isolates this responsibility: Test fixtures, fake identity components, conformance vectors, integration harnesses, and cross-cutting verification helpers. Its [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-identity/src/tba_tests_identity/__init__.py) exposes `AuthorizationCode`, `FakeIdentityProvider`, `FakeRelyingParty`, `FakeResourceServer`, `MatrixCellStatus`, `PackageMatrixCell`, `PackageMatrixHarness`, `SeededClient`, `SeededTenant`, `SeededUser`, `TestkitError`, `TestkitProviderRuntimeProfile`, `TestkitSeedSet`, `TokenResponse`, `build_fake_flow`, allowing consumers to select this package without treating adjacent packages as part of its public contract.

### When to Use

Use the testkit for repeatable protocol and integration tests. Its fake providers and sample credentials are test fixtures. Real identity deployment and credential handling belong to the runtime and provider packages.

### Features

- `TestkitError`: declared in src/tba_tests_identity/cross_cutting.py
- `MatrixCellStatus`: declared in src/tba_tests_identity/cross_cutting.py
- `SeededTenant`: declared in src/tba_tests_identity/cross_cutting.py
- `SeededClient`: declared in src/tba_tests_identity/cross_cutting.py
- `SeededUser`: declared in src/tba_tests_identity/cross_cutting.py
- `TestkitSeedSet`: declared in src/tba_tests_identity/cross_cutting.py
- `TestkitProviderRuntimeProfile`: declared in src/tba_tests_identity/cross_cutting.py
- `AuthorizationCode`: declared in src/tba_tests_identity/cross_cutting.py

### Non-Goals

`tba-tests-identity` does not take ownership of production identity services or deployable policy defaults.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

---

## Getting Started

### Prerequisites

Python `>=3.10,<3.16` is required. The [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-identity/pyproject.toml) declares no direct runtime dependencies. Read the example’s inputs and service requirements before execution.

### Installation

Install the selected PyPI release of `tba-tests-identity`:

```bash
uv pip install tba-tests-identity
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/120-tests/tba-tests-identity
```

#### uv

<!-- readme-standards:begin installation.uv -->
```bash
uv add tba-tests-identity
```
<!-- readme-standards:end installation.uv -->

#### pip

<!-- readme-standards:begin installation.pip -->
```bash
python -m pip install tba-tests-identity
```
<!-- readme-standards:end installation.pip -->

#### Poetry

<!-- readme-standards:begin installation.poetry -->
```bash
poetry add tba-tests-identity
```
<!-- readme-standards:end installation.poetry -->

### Quick Start

Install the version used by this example.

```bash
python -m pip install "tba-tests-identity==0.4.0.dev3"
```

Save the following as `quickstart.py` and run `python quickstart.py`. The assertions should pass.

#### Example

<!-- readme-standards:begin example.quick-start -->
Source: [docs/readme/quick_start.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-identity/docs/readme/quick_start.py).

```python
from tba_tests_identity import pkce_s256

verifier = "dBjftJeZ4CVP-mB92K27uhbUJU1p1r_wW1gFWFOEjXk"
assert pkce_s256(verifier) == "E9Melhoa2OwvFrEMTJguCHaoeK1t8URWbuGJSstw-cM"
```
<!-- readme-standards:end example.quick-start -->

#### Expected Result

The example demonstrates the documented `tba-tests-identity` source boundary or workflow. Complete its required configuration first. README CI checks the maintained source’s syntax and declarations; it does not claim that external services or the application workflow were exercised.

---

## Usage

### Common Workflows

<!-- readme-standards:begin example.usage -->
Source: [docs/readme/usage.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-identity/docs/readme/usage.py).

```python
from tba_tests_identity import pkce_s256

verifier = "dBjftJeZ4CVP-mB92K27uhbUJU1p1r_wW1gFWFOEjXk"
assert pkce_s256(verifier) == "E9Melhoa2OwvFrEMTJguCHaoeK1t8URWbuGJSstw-cM"
```
<!-- readme-standards:end example.usage -->

The following public-entry-point example belongs to `tba-tests-identity`. Test fixtures, fake identity components, conformance vectors, integration harnesses, and cross-cutting verification helpers. Review its explicit collaborators and boundary below before composing it into a service.

### Configuration

Configure `tba-tests-identity` through the APIs in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-identity/src/tba_tests_identity/__init__.py); its [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-identity/pyproject.toml) describes installation requirements, not an implicit service configuration. No additional package-global configuration contract is inferred from dependencies.

### Error Handling

The inspected `tba-tests-identity` source raises `TestkitError`, `pytest.UsageError`. Handle these at the calling boundary and consult the implementation for the triggering conditions.

### Best Practices

Use the explicit `tba-tests-identity` imports documented below and keep collaborator configuration with the caller. Run the package’s relevant tests after changing `AuthorizationCode`, `FakeIdentityProvider`, `FakeRelyingParty`, `FakeResourceServer`, `MatrixCellStatus`, `PackageMatrixCell`, `PackageMatrixHarness`, `SeededClient`, `SeededTenant`, `SeededUser`, `TestkitError`, `TestkitProviderRuntimeProfile`, `TestkitSeedSet`, `TokenResponse`, `build_fake_flow`; an import or successful installation alone does not establish its runtime guarantees.

---

## Package Boundary

### What It Owns

`tba-tests-identity` belongs to `120-tests` and owns test fixtures and executable verification: Test fixtures, fake identity components, conformance vectors, integration harnesses, and cross-cutting verification helpers.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-identity/src/tba_tests_identity/__init__.py). Public exports include `AuthorizationCode`, `FakeIdentityProvider`, `FakeRelyingParty`, `FakeResourceServer`, `MatrixCellStatus`, `PackageMatrixCell`, `PackageMatrixHarness`, `SeededClient`, `SeededTenant`, `SeededUser`, `TestkitError`, `TestkitProviderRuntimeProfile`.

Keep production identity services or deployable policy defaults in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

### Public API and Import Surfaces

Import namespace: `tba_tests_identity`.

Source-declared exports or types: `AuthorizationCode`, `FakeIdentityProvider`, `FakeRelyingParty`, `FakeResourceServer`, `MatrixCellStatus`, `PackageMatrixCell`, `PackageMatrixHarness`, `SeededClient`, `SeededTenant`, `SeededUser`, `TestkitError`, `TestkitProviderRuntimeProfile`, `TestkitSeedSet`, `TokenResponse`, `build_fake_flow`.

Inspect [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-identity/src/tba_tests_identity/__init__.py) for exact signatures; this inventory does not designate every internal module as stable.

### Entry Points

<!-- readme-standards:begin entry-points -->
- `pytest11` → `tba_tests_identity.pytest_plugin` → `tba_tests_identity.pytest_plugin`
<!-- readme-standards:end entry-points -->

### Injected Dependencies

Explicit construction inputs and collaborators for `tba-tests-identity`:

- `FakeIdentityProvider` construction inputs: `seeds`, `profile`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-identity/src/tba_tests_identity/cross_cutting.py).
- `PackageMatrixHarness` construction inputs: `python_versions`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-identity/src/tba_tests_identity/cross_cutting.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

### Protocol Consumers

Direct consumers in this checkout’s package manifests include `tba-workspace`. These edges describe declared dependencies, not protocol-conformance evidence.

### Extensions

For `tba-tests-identity`, use the source-declared public interfaces (`AuthorizationCode`, `FakeIdentityProvider`, `FakeRelyingParty`, `FakeResourceServer`, `MatrixCellStatus`, `PackageMatrixCell`, `PackageMatrixHarness`, `SeededClient`, `SeededTenant`, `SeededUser`, `TestkitError`, `TestkitProviderRuntimeProfile`, `TestkitSeedSet`, `TokenResponse`, `build_fake_flow`) when composing or extending behavior. Its entry-point section below is authoritative for registered plugins; no additional extension loader is inferred from the package name.

---

## Operations and Readiness

### Operational Requirements

`tba-tests-identity` exposes test fixtures and executable verification. Public operations found in its source:

- `pkce_s256` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-identity/src/tba_tests_identity/cross_cutting.py).
- `TestkitSeedSet.client` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-identity/src/tba_tests_identity/cross_cutting.py).
- `TestkitSeedSet.user` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-identity/src/tba_tests_identity/cross_cutting.py).
- `TestkitProviderRuntimeProfile.require_route` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-identity/src/tba_tests_identity/cross_cutting.py).
- `TestkitProviderRuntimeProfile.require_feature` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-identity/src/tba_tests_identity/cross_cutting.py).
- `FakeIdentityProvider.discovery_document` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-identity/src/tba_tests_identity/cross_cutting.py).
- `FakeIdentityProvider.jwks` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-identity/src/tba_tests_identity/cross_cutting.py).
- `FakeIdentityProvider.authorize` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-identity/src/tba_tests_identity/cross_cutting.py).
- `FakeIdentityProvider.token` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-identity/src/tba_tests_identity/cross_cutting.py).
- `FakeIdentityProvider.introspect` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-identity/src/tba_tests_identity/cross_cutting.py).
- `FakeIdentityProvider.userinfo` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-identity/src/tba_tests_identity/cross_cutting.py).
- `FakeRelyingParty.authorization_url` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-identity/src/tba_tests_identity/cross_cutting.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

### Health and Observability

This README does not establish a standalone health endpoint for `tba-tests-identity`. Observe the concrete caller’s results, exceptions, and existing test reports. An application that embeds this package must define its own health and telemetry contract.

### Security and Resource Limits

Apply the input, credential, and resource constraints implemented in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-identity/src/tba_tests_identity/__init__.py). The `tba-tests-identity` README gate is a documentation check, not a security review or a substitute for the implementation’s limits and caller authorization.

### Compatibility

This source version of `tba-tests-identity` declares Python `>=3.10,<3.16`. Consult its dependency constraints before upgrading. Source-version and registry-version badges have separate meanings; this migration makes no additional platform or interoperability certification claim.

---

## Verification

### Tests

See the [related repository tests](https://github.com/tigrbl/tigrbl_auth/blob/master/tests/unit/test_testkit_cross_cutting_boundary.py) for the implementation scope covered by this example.

[Workspace and package catalog](https://github.com/tigrbl/tigrbl_auth#package-catalog) · [tba-protocol-cwt](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/050-protocols/tba-protocol-cwt#readme) · [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues) · [Repository license](https://github.com/tigrbl/tigrbl_auth/blob/master/LICENSE)

### Certification Status

No external certification is asserted for `tba-tests-identity` by this documentation migration. README conformance, example syntax, runtime tests, and protocol or security certification are distinct evidence scopes.

### Evidence

The [README standards CI](https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml) records mechanical documentation results for its tested commit. The [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-identity/src/tba_tests_identity/__init__.py) and example sources support the package-boundary description; external runtime behavior requires its own test evidence.

---

## FAQ

### Why

**Why select this package?** `tba-tests-identity` provides test fixtures, fake identity components, conformance vectors, integration harnesses, and cross-cutting verification helpers; use its own API boundary rather than assuming neighboring packages are bundled or configured automatically.

### How

**How do I start?** Install or synchronize the environment under Getting Started, follow the maintained example for `tba-tests-identity`, and consult [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-identity/src/tba_tests_identity/__init__.py) for the exact types and signatures involved.

### When

**When should I validate an upgrade?** Recheck `tba-tests-identity` whenever its source version, declared collaborators, configuration, or caller changes. Run relevant behavioral tests in addition to the README gate before promotion.

---

## Documentation and Related Packages

### More Documentation

The [repository contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md), [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-identity/src/tba_tests_identity/__init__.py), and [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-identity/pyproject.toml) provide the supporting context for `tba-tests-identity`. The [README policy](https://github.com/groupsum/readme-standards/blob/master/docs/outline.md) defines the common document structure.

### Related Packages

`tba-tests-identity` declares no local runtime dependency and has no direct consumer in the active manifest graph. Browse the [120-tests layer](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/120-tests) for adjacent package responsibilities; adjacency does not imply a dependency.

### Project Links

<!-- readme-standards:begin project-links -->
- [Documentation](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/120-tests/tba-tests-identity#readme)
- [Homepage](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/120-tests/tba-tests-identity#readme)
- [Issues](https://github.com/tigrbl/tigrbl_auth/issues)
- [PyPI](https://pypi.org/project/tba-tests-identity/)
- [Repository](https://github.com/tigrbl/tigrbl_auth)
- [SSOT](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [Source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/120-tests/tba-tests-identity)
- [pypi: tba-tests-identity](https://pypi.org/project/tba-tests-identity/)
<!-- readme-standards:end project-links -->

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/120-tests/tba-tests-identity)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-identity/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-identity/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-identity/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-tests-identity/)

---

## Contributing

### How to Contribute

Follow the [contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md) and include a focused example or regression for changes to `tba-tests-identity`. Keep package behavior, its documented boundary, and its tests aligned.

### Development Setup

Work from the `pkgs/120-tests/tba-tests-identity` checkout. Synchronize its declared development environment with uv, then run the relevant package tests and `python -m pytest docs/readme/test_examples.py`. The repository’s dedicated README job installs `readme-standards==0.1.1` without resolving unrelated runtime packages.

### Notes for Maintainers

Edit authored prose directly in this `tba-tests-identity` README. Update source examples in `docs/readme/`, then run `readme-standards render --root . --write` from the package directory and review the diff. Required headings and generated blocks come from package-guide-v1.

---

## Governance

### Ownership and Decision Making

Changes to `tba-tests-identity` follow the maintainer review process of [tigrbl/tigrbl_auth](https://github.com/tigrbl/tigrbl_auth) and its contribution guide. Author attribution remains in the [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-identity/pyproject.toml); this README does not assign new publishing or administrative authority.

### Standards and Policies

`tba-tests-identity` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `120-tests` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

### Lifecycle and Migration

The `tba-tests-identity` source version is `0.4.0.dev3`. This change standardizes documentation and adds a development-only gate; it does not publish a new runtime version or declare a previously unpublished package released. Preserve explicit deprecation and replacement instructions where present.

---

## License and Attribution

### License

<!-- readme-standards:begin license -->
Licensed under `Apache-2.0`. See [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-identity/LICENSE).
<!-- readme-standards:end license -->

### Notices

<!-- readme-standards:begin notices -->
See [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-identity/NOTICE) for attribution.
<!-- readme-standards:end notices -->
