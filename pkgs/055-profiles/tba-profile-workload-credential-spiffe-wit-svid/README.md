# tba-profile-workload-credential-spiffe-wit-svid

<!-- readme-standards:begin branding -->
<p align="center"><a href="https://github.com/tigrbl/tigrbl_auth"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="300"></a></p>
<p align="center"><strong>tba-profile-workload-credential-spiffe-wit-svid</strong></p>
<p align="center">Incubating SPIFFE WIT-SVID profile pinned to the SPIFFE v1.15.1 publication.</p>
<p align="center">
<a href="https://pypi.org/project/tba-profile-workload-credential-spiffe-wit-svid/"><img alt="pypi: tba-profile-workload-credential-spiffe-wit-svid" src="https://img.shields.io/pypi/v/tba-profile-workload-credential-spiffe-wit-svid"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-credential-spiffe-wit-svid/pyproject.toml"><img alt="Source version: 0.4.0.dev3" src="https://img.shields.io/static/v1?label=Source%20version&amp;message=0.4.0.dev3&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-credential-spiffe-wit-svid/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/static/v1?label=Python&amp;message=%3E%3D3.10%2C%3C3.16&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-credential-spiffe-wit-svid/pyproject.toml"><img alt="Layer: 055-profiles" src="https://img.shields.io/static/v1?label=Layer&amp;message=055-profiles&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-credential-spiffe-wit-svid/README.md#lifecycle-and-migration"><img alt="Lifecycle: active" src="https://img.shields.io/static/v1?label=Lifecycle&amp;message=active&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-credential-spiffe-wit-svid/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/static/v1?label=License&amp;message=Apache-2.0&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-credential-spiffe-wit-svid/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/static/v1?label=Notice&amp;message=attribution&amp;color=525252"></a>
</p>
<p align="center">
<a href="https://pypi.org/project/tba-profile-workload-credential-spiffe-wit-svid/"><img alt="Monthly PyPI downloads: tba-profile-workload-credential-spiffe-wit-svid" src="https://img.shields.io/pypi/dm/tba-profile-workload-credential-spiffe-wit-svid"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-credential-spiffe-wit-svid/README.md"><img alt="README hits: tba-profile-workload-credential-spiffe-wit-svid" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/pkgs/055-profiles/tba-profile-workload-credential-spiffe-wit-svid/README.md.svg?label=README%20hits"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="README standards: CI gate" src="https://img.shields.io/static/v1?label=README%20standards&amp;message=CI%20gate&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-credential-spiffe-wit-svid/docs/readme/test_examples.py"><img alt="Tests: example source" src="https://img.shields.io/static/v1?label=Tests&amp;message=example%20source&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-credential-spiffe-wit-svid/README.md#certification-status"><img alt="Certification: not certified" src="https://img.shields.io/static/v1?label=Certification&amp;message=not%20certified&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/tools/readme/POLICY.md"><img alt="Governance: repository policy" src="https://img.shields.io/static/v1?label=Governance&amp;message=repository%20policy&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="Evidence: source and CI" src="https://img.shields.io/static/v1?label=Evidence&amp;message=source%20and%20CI&amp;color=525252"></a>
</p>
<p align="center"><a href="#overview">Overview</a> · <a href="#installation">Installation</a> · <a href="#quick-start">Quick Start</a> · <a href="#usage">Usage</a> · <a href="#public-api-and-import-surfaces">API</a> · <a href="#contributing">Contributing</a> · <a href="#governance">Governance</a> · <a href="#license">License</a></p>
<!-- readme-standards:end branding -->

---

## Overview

### Summary

Incubating SPIFFE WIT-SVID profile pinned to the SPIFFE v1.15.1 publication. Disabled by default.

- Package: `tba-profile-workload-credential-spiffe-wit-svid`
- Layer: `055-profiles`
- Responsibility: Incubating SPIFFE WIT-SVID profile pinned to the SPIFFE v1.15.1 publication.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-credential-spiffe-wit-svid/src/tba_profile_workload_credential_spiffe_wit_svid/__init__.py).
- Distribution: Python package on PyPI.

### Why This Package

`tba-profile-workload-credential-spiffe-wit-svid` isolates this responsibility: Incubating SPIFFE WIT-SVID profile pinned to the SPIFFE v1.15.1 publication. Its [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-credential-spiffe-wit-svid/src/tba_profile_workload_credential_spiffe_wit_svid/bindings.py) exposes `ALLOWED_ALGORITHMS`, `CURRENT_VERSION`, `VERSION_HISTORY`, `WitSvidVersion`, `validate_wit_svid`, allowing consumers to select this package without treating adjacent packages as part of its public contract.

### When to Use

Choose `tba-profile-workload-credential-spiffe-wit-svid` for this responsibility: Incubating SPIFFE WIT-SVID profile pinned to the SPIFFE v1.15.1 publication. Its `055-profiles` placement keeps focused protocol and credential profiles separate from a universal deployment or implicit trust-policy selection.

### Features

- `ProtocolProfileError`: The artifact or request does not satisfy the selected protocol profile.
- `WitSvidVersion`: declared in src/tba_profile_workload_credential_spiffe_wit_svid/versions.py

### Non-Goals

`tba-profile-workload-credential-spiffe-wit-svid` does not take ownership of a universal deployment or implicit trust-policy selection.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

---

## Getting Started

### Prerequisites

Python `>=3.10,<3.16` is required. The [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-credential-spiffe-wit-svid/pyproject.toml) declares runtime dependencies including `tba-contracts-proof-of-possession`, `tba-profile-workload-credential-wimse-wit`, `tba-protocol-workload-spiffe-svid`, `tba-profile-workload-proof-wimse-wpt`, `tba-concrete-jwt`, `tba-provider-jose-cryptography`. Read the example’s inputs and service requirements before execution.

### Installation

Install the selected PyPI release of `tba-profile-workload-credential-spiffe-wit-svid`:

```bash
uv pip install tba-profile-workload-credential-spiffe-wit-svid
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/055-profiles/tba-profile-workload-credential-spiffe-wit-svid
```

#### uv

<!-- readme-standards:begin installation.uv -->
```bash
uv add tba-profile-workload-credential-spiffe-wit-svid
```
<!-- readme-standards:end installation.uv -->

#### pip

<!-- readme-standards:begin installation.pip -->
```bash
python -m pip install tba-profile-workload-credential-spiffe-wit-svid
```
<!-- readme-standards:end installation.pip -->

#### Poetry

<!-- readme-standards:begin installation.poetry -->
```bash
poetry add tba-profile-workload-credential-spiffe-wit-svid
```
<!-- readme-standards:end installation.poetry -->

### Quick Start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.


```bash
uv run --isolated --no-project --python 3.12 --with "tba-profile-workload-credential-spiffe-wit-svid==0.4.0.dev3" python quickstart.py
```

The command prints the declared current revision.

#### Example

<!-- readme-standards:begin example.quick-start -->
Source: [docs/readme/quick_start.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-credential-spiffe-wit-svid/docs/readme/quick_start.py).

```python
from tba_profile_workload_credential_spiffe_wit_svid import CURRENT_VERSION

assert CURRENT_VERSION is not None
print(CURRENT_VERSION)
```
<!-- readme-standards:end example.quick-start -->

#### Expected Result

The example demonstrates the documented `tba-profile-workload-credential-spiffe-wit-svid` source boundary or workflow. Complete its required configuration first. README CI checks the maintained source’s syntax and declarations; it does not claim that external services or the application workflow were exercised.

---

## Usage

### Common Workflows

<!-- readme-standards:begin example.usage -->
Source: [docs/readme/usage.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-credential-spiffe-wit-svid/docs/readme/usage.py).

```python
from tba_profile_workload_credential_spiffe_wit_svid import CURRENT_VERSION

assert CURRENT_VERSION is not None
print(CURRENT_VERSION)
```
<!-- readme-standards:end example.usage -->

The following public-entry-point example belongs to `tba-profile-workload-credential-spiffe-wit-svid`. Incubating SPIFFE WIT-SVID profile pinned to the SPIFFE v1.15.1 publication. Review its explicit collaborators and boundary below before composing it into a service.

### Configuration

Configure `tba-profile-workload-credential-spiffe-wit-svid` through the APIs in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-credential-spiffe-wit-svid/src/tba_profile_workload_credential_spiffe_wit_svid/bindings.py); its [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-credential-spiffe-wit-svid/pyproject.toml) describes installation requirements, not an implicit service configuration. No additional package-global configuration contract is inferred from dependencies.

### Error Handling

The inspected `tba-profile-workload-credential-spiffe-wit-svid` source raises `ValueError`. Handle these at the calling boundary and consult the implementation for the triggering conditions.

### Best Practices

Use the explicit `tba-profile-workload-credential-spiffe-wit-svid` imports documented below and keep collaborator configuration with the caller. Run the package’s relevant tests after changing `ALLOWED_ALGORITHMS`, `CURRENT_VERSION`, `VERSION_HISTORY`, `WitSvidVersion`, `validate_wit_svid`; an import or successful installation alone does not establish its runtime guarantees.

---

## Package Boundary

### What It Owns

`tba-profile-workload-credential-spiffe-wit-svid` belongs to `055-profiles` and owns focused protocol and credential profiles: Incubating SPIFFE WIT-SVID profile pinned to the SPIFFE v1.15.1 publication.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-credential-spiffe-wit-svid/src/tba_profile_workload_credential_spiffe_wit_svid/__init__.py). Public exports include `ALLOWED_ALGORITHMS`, `CURRENT_VERSION`, `VERSION_HISTORY`, `WitSvidVersion`, `validate_wit_svid`.

Keep a universal deployment or implicit trust-policy selection in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

### Public API and Import Surfaces

Import namespace: `tba_profile_workload_credential_spiffe_wit_svid`.

Source-declared exports or types: `ALLOWED_ALGORITHMS`, `CURRENT_VERSION`, `VERSION_HISTORY`, `WitSvidVersion`, `validate_wit_svid`.

Inspect [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-credential-spiffe-wit-svid/src/tba_profile_workload_credential_spiffe_wit_svid/bindings.py) for exact signatures; this inventory does not designate every internal module as stable.

### Entry Points

<!-- readme-standards:begin entry-points -->
This package declares no command-line, GUI, or plugin entry points in its manifest.
<!-- readme-standards:end entry-points -->

### Injected Dependencies

Explicit construction inputs and collaborators for `tba-profile-workload-credential-spiffe-wit-svid`:

- `validate_wit_svid` construction inputs: `proof_result`, `now`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-credential-spiffe-wit-svid/src/tba_profile_workload_credential_spiffe_wit_svid/validation.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

### Protocol Consumers

Direct consumers in this checkout’s package manifests include `tba-example-workload-credential-profiles`, `tba-workspace`. These edges describe declared dependencies, not protocol-conformance evidence.

### Extensions

For `tba-profile-workload-credential-spiffe-wit-svid`, use the source-declared public interfaces (`ALLOWED_ALGORITHMS`, `CURRENT_VERSION`, `VERSION_HISTORY`, `WitSvidVersion`, `validate_wit_svid`) when composing or extending behavior. Its entry-point section below is authoritative for registered plugins; no additional extension loader is inferred from the package name.

---

## Operations and Readiness

### Operational Requirements

`tba-profile-workload-credential-spiffe-wit-svid` exposes focused protocol and credential profiles. Public operations found in its source:

- `validate_wit_svid` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-credential-spiffe-wit-svid/src/tba_profile_workload_credential_spiffe_wit_svid/validation.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

### Health and Observability

This README does not establish a standalone health endpoint for `tba-profile-workload-credential-spiffe-wit-svid`. Observe the concrete caller’s results, exceptions, and existing test reports. An application that embeds this package must define its own health and telemetry contract.

### Security and Resource Limits

Apply the input, credential, and resource constraints implemented in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-credential-spiffe-wit-svid/src/tba_profile_workload_credential_spiffe_wit_svid/bindings.py). The `tba-profile-workload-credential-spiffe-wit-svid` README gate is a documentation check, not a security review or a substitute for the implementation’s limits and caller authorization.

### Compatibility

This source version of `tba-profile-workload-credential-spiffe-wit-svid` declares Python `>=3.10,<3.16`. Consult its dependency constraints before upgrading. Source-version and registry-version badges have separate meanings; this migration makes no additional platform or interoperability certification claim.

---

## Verification

### Tests

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-credential-spiffe-wit-svid/src/tba_profile_workload_credential_spiffe_wit_svid/__init__.py).

### Certification Status

No external certification is asserted for `tba-profile-workload-credential-spiffe-wit-svid` by this documentation migration. README conformance, example syntax, runtime tests, and protocol or security certification are distinct evidence scopes.

### Evidence

The [README standards CI](https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml) records mechanical documentation results for its tested commit. The [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-credential-spiffe-wit-svid/src/tba_profile_workload_credential_spiffe_wit_svid/bindings.py) and example sources support the package-boundary description; external runtime behavior requires its own test evidence.

---

## FAQ

### Why

**Why select this package?** `tba-profile-workload-credential-spiffe-wit-svid` provides incubating SPIFFE WIT-SVID profile pinned to the SPIFFE v1.15.1 publication; use its own API boundary rather than assuming neighboring packages are bundled or configured automatically.

### How

**How do I start?** Install or synchronize the environment under Getting Started, follow the maintained example for `tba-profile-workload-credential-spiffe-wit-svid`, and consult [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-credential-spiffe-wit-svid/src/tba_profile_workload_credential_spiffe_wit_svid/bindings.py) for the exact types and signatures involved.

### When

**When should I validate an upgrade?** Recheck `tba-profile-workload-credential-spiffe-wit-svid` whenever its source version, declared collaborators, configuration, or caller changes. Run relevant behavioral tests in addition to the README gate before promotion.

---

## Documentation and Related Packages

### More Documentation

The [repository contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md), [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-credential-spiffe-wit-svid/src/tba_profile_workload_credential_spiffe_wit_svid/bindings.py), and [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-credential-spiffe-wit-svid/pyproject.toml) provide the supporting context for `tba-profile-workload-credential-spiffe-wit-svid`. The [README policy](https://github.com/groupsum/readme-standards/blob/master/docs/outline.md) defines the common document structure.

### Related Packages

Declared local runtime dependencies:

- [tba-concrete-jwt](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-jwt/README.md)
- [tba-contracts-proof-of-possession](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-proof-of-possession/README.md)
- [tba-profile-workload-credential-wimse-wit](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-credential-wimse-wit/README.md)
- [tba-profile-workload-proof-wimse-wpt](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-proof-wimse-wpt/README.md)
- [tba-protocol-workload-spiffe-svid](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-workload-spiffe-svid/README.md)
- [tba-provider-jose-cryptography](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-jose-cryptography/README.md)

Direct downstream consumers:

- [tba-example-workload-credential-profiles](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/110-examples/tba-example-workload-credential-profiles/README.md)

### Project Links

<!-- readme-standards:begin project-links -->
- [Documentation](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/055-profiles/tba-profile-workload-credential-spiffe-wit-svid#readme)
- [Homepage](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/055-profiles/tba-profile-workload-credential-spiffe-wit-svid#readme)
- [Issues](https://github.com/tigrbl/tigrbl_auth/issues)
- [PyPI](https://pypi.org/project/tba-profile-workload-credential-spiffe-wit-svid/)
- [Repository](https://github.com/tigrbl/tigrbl_auth)
- [Source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/055-profiles/tba-profile-workload-credential-spiffe-wit-svid)
- [pypi: tba-profile-workload-credential-spiffe-wit-svid](https://pypi.org/project/tba-profile-workload-credential-spiffe-wit-svid/)
<!-- readme-standards:end project-links -->

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/055-profiles/tba-profile-workload-credential-spiffe-wit-svid)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-credential-spiffe-wit-svid/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-credential-spiffe-wit-svid/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-credential-spiffe-wit-svid/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-profile-workload-credential-spiffe-wit-svid/)

---

## Contributing

### How to Contribute

Follow the [contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md) and include a focused example or regression for changes to `tba-profile-workload-credential-spiffe-wit-svid`. Keep package behavior, its documented boundary, and its tests aligned.

### Development Setup

Work from the `pkgs/055-profiles/tba-profile-workload-credential-spiffe-wit-svid` checkout. Synchronize its declared development environment with uv, then run the relevant package tests and `python -m pytest docs/readme/test_examples.py`. The repository’s dedicated README job installs `readme-standards==0.1.1` without resolving unrelated runtime packages.

### Notes for Maintainers

Edit authored prose directly in this `tba-profile-workload-credential-spiffe-wit-svid` README. Update source examples in `docs/readme/`, then run `readme-standards render --root . --write` from the package directory and review the diff. Required headings and generated blocks come from package-guide-v1.

---

## Governance

### Ownership and Decision Making

Changes to `tba-profile-workload-credential-spiffe-wit-svid` follow the maintainer review process of [tigrbl/tigrbl_auth](https://github.com/tigrbl/tigrbl_auth) and its contribution guide. Author attribution remains in the [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-credential-spiffe-wit-svid/pyproject.toml); this README does not assign new publishing or administrative authority.

### Standards and Policies

`tba-profile-workload-credential-spiffe-wit-svid` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `055-profiles` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

### Lifecycle and Migration

The `tba-profile-workload-credential-spiffe-wit-svid` source version is `0.4.0.dev3`. This change standardizes documentation and adds a development-only gate; it does not publish a new runtime version or declare a previously unpublished package released. Preserve explicit deprecation and replacement instructions where present.

---

## License and Attribution

### License

<!-- readme-standards:begin license -->
Licensed under `Apache-2.0`. See [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-credential-spiffe-wit-svid/LICENSE).
<!-- readme-standards:end license -->

### Notices

<!-- readme-standards:begin notices -->
See [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-credential-spiffe-wit-svid/NOTICE) for attribution.
<!-- readme-standards:end notices -->
