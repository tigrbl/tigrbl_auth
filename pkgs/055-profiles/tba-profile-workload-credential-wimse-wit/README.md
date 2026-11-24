# tba-profile-workload-credential-wimse-wit

<!-- readme-standards:begin branding -->
<p align="center"><a href="https://github.com/tigrbl/tigrbl_auth"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="300"></a></p>
<p align="center"><strong>tba-profile-workload-credential-wimse-wit</strong></p>
<p align="center">WIMSE Workload Identity Token.</p>
<p align="center">
<a href="https://pypi.org/project/tba-profile-workload-credential-wimse-wit/"><img alt="pypi: tba-profile-workload-credential-wimse-wit" src="https://img.shields.io/pypi/v/tba-profile-workload-credential-wimse-wit?labelColor=1E293B&amp;color=1D4ED8"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-credential-wimse-wit/pyproject.toml"><img alt="Source version: 0.4.0.dev5" src="https://img.shields.io/static/v1?label=Source%20version&amp;message=0.4.0.dev5&amp;labelColor=1E293B&amp;color=4338CA"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-credential-wimse-wit/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/static/v1?label=Python&amp;message=%3E%3D3.10%2C%3C3.16&amp;labelColor=1E293B&amp;color=0F766E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-credential-wimse-wit/pyproject.toml"><img alt="Layer: 055-profiles" src="https://img.shields.io/static/v1?label=Layer&amp;message=055-profiles&amp;labelColor=1E293B&amp;color=6D28D9"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-credential-wimse-wit/README.md#lifecycle-and-migration"><img alt="Lifecycle: active" src="https://img.shields.io/static/v1?label=Lifecycle&amp;message=active&amp;labelColor=1E293B&amp;color=166534"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-credential-wimse-wit/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/static/v1?label=License&amp;message=Apache-2.0&amp;labelColor=1E293B&amp;color=86198F"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-credential-wimse-wit/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/static/v1?label=Notice&amp;message=attribution&amp;labelColor=1E293B&amp;color=86198F"></a>
</p>
<p align="center">
<a href="https://pypi.org/project/tba-profile-workload-credential-wimse-wit/"><img alt="Monthly PyPI downloads: tba-profile-workload-credential-wimse-wit" src="https://img.shields.io/pypi/dm/tba-profile-workload-credential-wimse-wit?labelColor=1E293B&amp;color=0E7490"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-credential-wimse-wit/README.md"><img alt="README hits: tba-profile-workload-credential-wimse-wit" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/pkgs/055-profiles/tba-profile-workload-credential-wimse-wit/README.md.svg?label=README%20hits&amp;labelColor=1E293B&amp;color=0E7490"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="README standards: CI gate" src="https://img.shields.io/static/v1?label=README%20standards&amp;message=CI%20gate&amp;labelColor=1E293B&amp;color=1D4ED8"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-credential-wimse-wit/docs/readme/test_examples.py"><img alt="Tests: example source" src="https://img.shields.io/static/v1?label=Tests&amp;message=example%20source&amp;labelColor=1E293B&amp;color=0F766E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-credential-wimse-wit/README.md#certification-status"><img alt="Certification: not certified" src="https://img.shields.io/static/v1?label=Certification&amp;message=not%20certified&amp;labelColor=1E293B&amp;color=92400E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/tools/readme/POLICY.md"><img alt="Governance: repository policy" src="https://img.shields.io/static/v1?label=Governance&amp;message=repository%20policy&amp;labelColor=1E293B&amp;color=4338CA"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="Evidence: source and CI" src="https://img.shields.io/static/v1?label=Evidence&amp;message=source%20and%20CI&amp;labelColor=1E293B&amp;color=6D28D9"></a>
</p>
<p align="center"><a href="#overview">Overview</a> · <a href="#installation">Installation</a> · <a href="#quick-start">Quick Start</a> · <a href="#usage">Usage</a> · <a href="#public-api-and-import-surfaces">API</a> · <a href="#contributing">Contributing</a> · <a href="#governance">Governance</a> · <a href="#license">License</a></p>
<!-- readme-standards:end branding -->

---

## Overview

### Summary

WIMSE Workload Identity Token. This is a revision-pinned IETF draft profile and is disabled by default at runtime.

- Package: `tba-profile-workload-credential-wimse-wit`
- Layer: `055-profiles`
- Responsibility: WIMSE Workload Identity Token.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-credential-wimse-wit/src/tba_profile_workload_credential_wimse_wit/__init__.py).
- Distribution: Python package on PyPI.

### Why This Package

`tba-profile-workload-credential-wimse-wit` isolates this responsibility: WIMSE Workload Identity Token. Its [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-credential-wimse-wit/src/tba_profile_workload_credential_wimse_wit/bindings.py) exposes `CURRENT_VERSION`, `REQUIRED_WIT_CLAIMS`, `VERSION_HISTORY`, `WitVersion`, `validate_wit`, allowing consumers to select this package without treating adjacent packages as part of its public contract.

### When to Use

Choose `tba-profile-workload-credential-wimse-wit` for this responsibility: WIMSE Workload Identity Token. Its `055-profiles` placement keeps focused protocol and credential profiles separate from a universal deployment or implicit trust-policy selection.

### Features

- `ProtocolProfileError`: The artifact or request does not satisfy the selected protocol profile.
- `WitVersion`: declared in src/tba_profile_workload_credential_wimse_wit/versions.py

### Non-Goals

`tba-profile-workload-credential-wimse-wit` does not take ownership of a universal deployment or implicit trust-policy selection.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

---

## Getting Started

### Prerequisites

Python `>=3.10,<3.16` is required. The [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-credential-wimse-wit/pyproject.toml) declares runtime dependencies including `tba-concrete-jwt`, `tba-concrete-wit`, `tba-protocol-workload-wimse-identifier`, `tba-provider-jose-cryptography`. Read the example’s inputs and service requirements before execution.

### Installation

Install the selected PyPI release of `tba-profile-workload-credential-wimse-wit`:

```bash
uv pip install tba-profile-workload-credential-wimse-wit
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/055-profiles/tba-profile-workload-credential-wimse-wit
```

#### uv

<!-- readme-standards:begin installation.uv -->
```bash
uv add tba-profile-workload-credential-wimse-wit
```
<!-- readme-standards:end installation.uv -->

#### pip

<!-- readme-standards:begin installation.pip -->
```bash
python -m pip install tba-profile-workload-credential-wimse-wit
```
<!-- readme-standards:end installation.pip -->

#### Poetry

<!-- readme-standards:begin installation.poetry -->
```bash
poetry add tba-profile-workload-credential-wimse-wit
```
<!-- readme-standards:end installation.poetry -->

### Quick Start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.


```bash
uv run --isolated --no-project --python 3.12 --with "tba-profile-workload-credential-wimse-wit==0.4.0.dev5" python quickstart.py
```

The command prints the declared current revision.

#### Example

<!-- readme-standards:begin example.quick-start -->
Source: [docs/readme/quick_start.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-credential-wimse-wit/docs/readme/quick_start.py).

```python
from tba_profile_workload_credential_wimse_wit import CURRENT_VERSION

assert CURRENT_VERSION is not None
print(CURRENT_VERSION)
```
<!-- readme-standards:end example.quick-start -->

#### Expected Result

The example demonstrates the documented `tba-profile-workload-credential-wimse-wit` source boundary or workflow. Complete its required configuration first. README CI checks the maintained source’s syntax and declarations; it does not claim that external services or the application workflow were exercised.

---

## Usage

### Common Workflows

<!-- readme-standards:begin example.usage -->
Source: [docs/readme/usage.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-credential-wimse-wit/docs/readme/usage.py).

```python
from tba_profile_workload_credential_wimse_wit import CURRENT_VERSION

assert CURRENT_VERSION is not None
print(CURRENT_VERSION)
```
<!-- readme-standards:end example.usage -->

The following public-entry-point example belongs to `tba-profile-workload-credential-wimse-wit`. WIMSE Workload Identity Token. Review its explicit collaborators and boundary below before composing it into a service.

### Configuration

Configure `tba-profile-workload-credential-wimse-wit` through the APIs in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-credential-wimse-wit/src/tba_profile_workload_credential_wimse_wit/bindings.py); its [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-credential-wimse-wit/pyproject.toml) describes installation requirements, not an implicit service configuration. No additional package-global configuration contract is inferred from dependencies.

### Error Handling

The inspected `tba-profile-workload-credential-wimse-wit` source raises `ValueError`. Handle these at the calling boundary and consult the implementation for the triggering conditions.

### Best Practices

Use the explicit `tba-profile-workload-credential-wimse-wit` imports documented below and keep collaborator configuration with the caller. Run the package’s relevant tests after changing `CURRENT_VERSION`, `REQUIRED_WIT_CLAIMS`, `VERSION_HISTORY`, `WitVersion`, `validate_wit`; an import or successful installation alone does not establish its runtime guarantees.

---

## Package Boundary

### What It Owns

`tba-profile-workload-credential-wimse-wit` belongs to `055-profiles` and owns focused protocol and credential profiles: WIMSE Workload Identity Token.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-credential-wimse-wit/src/tba_profile_workload_credential_wimse_wit/__init__.py). Public exports include `CURRENT_VERSION`, `REQUIRED_WIT_CLAIMS`, `VERSION_HISTORY`, `WitVersion`, `validate_wit`.

Keep a universal deployment or implicit trust-policy selection in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

### Public API and Import Surfaces

Import namespace: `tba_profile_workload_credential_wimse_wit`.

Source-declared exports or types: `CURRENT_VERSION`, `REQUIRED_WIT_CLAIMS`, `VERSION_HISTORY`, `WitVersion`, `validate_wit`.

Inspect [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-credential-wimse-wit/src/tba_profile_workload_credential_wimse_wit/bindings.py) for exact signatures; this inventory does not designate every internal module as stable.

### Entry Points

<!-- readme-standards:begin entry-points -->
This package declares no command-line, GUI, or plugin entry points in its manifest.
<!-- readme-standards:end entry-points -->

### Injected Dependencies

The [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-credential-wimse-wit/src/tba_profile_workload_credential_wimse_wit/__init__.py) for `tba-profile-workload-credential-wimse-wit` does not declare an explicit service-constructor or keyword-only factory hook in the inspected source. Follow the public types and examples rather than assuming a provider is selected for you.

Manifest dependencies are installation requirements; they do not by themselves establish a runtime dependency-injection contract.

### Protocol Consumers

Direct consumers in this checkout’s package manifests include `tba-profile-workload-credential-spiffe-wit-svid`, `tba-profile-workload-proof-wimse-http-signature`, `tba-profile-workload-proof-wimse-wpt`, `tba-runtime-identity`, `tba-example-workload-credential-profiles`, `tba-workspace`. These edges describe declared dependencies, not protocol-conformance evidence.

### Extensions

For `tba-profile-workload-credential-wimse-wit`, use the source-declared public interfaces (`CURRENT_VERSION`, `REQUIRED_WIT_CLAIMS`, `VERSION_HISTORY`, `WitVersion`, `validate_wit`) when composing or extending behavior. Its entry-point section below is authoritative for registered plugins; no additional extension loader is inferred from the package name.

---

## Operations and Readiness

### Operational Requirements

`tba-profile-workload-credential-wimse-wit` exposes focused protocol and credential profiles. Public operations found in its source:

- `validate_wit` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-credential-wimse-wit/src/tba_profile_workload_credential_wimse_wit/validation.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

### Health and Observability

This README does not establish a standalone health endpoint for `tba-profile-workload-credential-wimse-wit`. Observe the concrete caller’s results, exceptions, and existing test reports. An application that embeds this package must define its own health and telemetry contract.

### Security and Resource Limits

Apply the input, credential, and resource constraints implemented in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-credential-wimse-wit/src/tba_profile_workload_credential_wimse_wit/bindings.py). The `tba-profile-workload-credential-wimse-wit` README gate is a documentation check, not a security review or a substitute for the implementation’s limits and caller authorization.

### Compatibility

This source version of `tba-profile-workload-credential-wimse-wit` declares Python `>=3.10,<3.16`. Consult its dependency constraints before upgrading. Source-version and registry-version badges have separate meanings; this migration makes no additional platform or interoperability certification claim.

---

## Verification

### Tests

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-credential-wimse-wit/src/tba_profile_workload_credential_wimse_wit/__init__.py).

### Certification Status

No external certification is asserted for `tba-profile-workload-credential-wimse-wit` by this documentation migration. README conformance, example syntax, runtime tests, and protocol or security certification are distinct evidence scopes.

### Evidence

The [README standards CI](https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml) records mechanical documentation results for its tested commit. The [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-credential-wimse-wit/src/tba_profile_workload_credential_wimse_wit/bindings.py) and example sources support the package-boundary description; external runtime behavior requires its own test evidence.

---

## FAQ

### Why

**Why select this package?** `tba-profile-workload-credential-wimse-wit` provides wIMSE Workload Identity Token; use its own API boundary rather than assuming neighboring packages are bundled or configured automatically.

### How

**How do I start?** Install or synchronize the environment under Getting Started, follow the maintained example for `tba-profile-workload-credential-wimse-wit`, and consult [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-credential-wimse-wit/src/tba_profile_workload_credential_wimse_wit/bindings.py) for the exact types and signatures involved.

### When

**When should I validate an upgrade?** Recheck `tba-profile-workload-credential-wimse-wit` whenever its source version, declared collaborators, configuration, or caller changes. Run relevant behavioral tests in addition to the README gate before promotion.

---

## Documentation and Related Packages

### More Documentation

The [repository contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md), [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-credential-wimse-wit/src/tba_profile_workload_credential_wimse_wit/bindings.py), and [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-credential-wimse-wit/pyproject.toml) provide the supporting context for `tba-profile-workload-credential-wimse-wit`. The [README policy](https://github.com/groupsum/readme-standards/blob/master/docs/outline.md) defines the common document structure.

### Related Packages

Declared local runtime dependencies:

- [tba-concrete-jwt](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-jwt/README.md)
- [tba-concrete-wit](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-wit/README.md)
- [tba-protocol-workload-wimse-identifier](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-workload-wimse-identifier/README.md)
- [tba-provider-jose-cryptography](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-jose-cryptography/README.md)

Direct downstream consumers:

- [tba-example-workload-credential-profiles](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/110-examples/tba-example-workload-credential-profiles/README.md)
- [tba-profile-workload-credential-spiffe-wit-svid](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-credential-spiffe-wit-svid/README.md)
- [tba-profile-workload-proof-wimse-http-signature](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-proof-wimse-http-signature/README.md)
- [tba-profile-workload-proof-wimse-wpt](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-proof-wimse-wpt/README.md)
- [tba-runtime-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity/README.md)

### Project Links

<!-- readme-standards:begin project-links -->
- [Documentation](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/055-profiles/tba-profile-workload-credential-wimse-wit#readme)
- [Homepage](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/055-profiles/tba-profile-workload-credential-wimse-wit#readme)
- [Issues](https://github.com/tigrbl/tigrbl_auth/issues)
- [PyPI](https://pypi.org/project/tba-profile-workload-credential-wimse-wit/)
- [Repository](https://github.com/tigrbl/tigrbl_auth)
- [Source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/055-profiles/tba-profile-workload-credential-wimse-wit)
- [pypi: tba-profile-workload-credential-wimse-wit](https://pypi.org/project/tba-profile-workload-credential-wimse-wit/)
<!-- readme-standards:end project-links -->

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/055-profiles/tba-profile-workload-credential-wimse-wit)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-credential-wimse-wit/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-credential-wimse-wit/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-credential-wimse-wit/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-profile-workload-credential-wimse-wit/)

---

## Contributing

### How to Contribute

Follow the [contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md) and include a focused example or regression for changes to `tba-profile-workload-credential-wimse-wit`. Keep package behavior, its documented boundary, and its tests aligned.

### Development Setup

Work from the `pkgs/055-profiles/tba-profile-workload-credential-wimse-wit` checkout. Synchronize its declared development environment with uv, then run the relevant package tests and `python -m pytest docs/readme/test_examples.py`. The repository’s dedicated README job installs `readme-standards==0.1.3` without resolving unrelated runtime packages.

### Notes for Maintainers

Edit authored prose directly in this `tba-profile-workload-credential-wimse-wit` README. Update source examples in `docs/readme/`, then run `readme-standards render --root . --write` from the package directory and review the diff. Required headings and generated blocks come from package-guide-v1.

---

## Governance

### Ownership and Decision Making

Changes to `tba-profile-workload-credential-wimse-wit` follow the maintainer review process of [tigrbl/tigrbl_auth](https://github.com/tigrbl/tigrbl_auth) and its contribution guide. Author attribution remains in the [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-credential-wimse-wit/pyproject.toml); this README does not assign new publishing or administrative authority.

### Standards and Policies

`tba-profile-workload-credential-wimse-wit` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `055-profiles` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

### Lifecycle and Migration

The `tba-profile-workload-credential-wimse-wit` source version is `0.4.0.dev5`. This change standardizes documentation and adds a development-only gate; it does not publish a new runtime version or declare a previously unpublished package released. Preserve explicit deprecation and replacement instructions where present.

---

## License and Attribution

### License

<!-- readme-standards:begin license -->
Licensed under `Apache-2.0`. See [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-credential-wimse-wit/LICENSE).
<!-- readme-standards:end license -->

### Notices

<!-- readme-standards:begin notices -->
See [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-credential-wimse-wit/NOTICE) for attribution.
<!-- readme-standards:end notices -->
