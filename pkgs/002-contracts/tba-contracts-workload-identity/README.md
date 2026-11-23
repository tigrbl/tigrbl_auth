# tba-contracts-workload-identity

<!-- readme-standards:begin branding -->
<p align="center"><a href="https://github.com/tigrbl/tigrbl_auth"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="300"></a></p>
<p align="center"><strong>tba-contracts-workload-identity</strong></p>
<p align="center">Protocol-neutral workload identity, credential, trust, and delegation contracts.</p>
<p align="center">
<a href="https://pypi.org/project/tba-contracts-workload-identity/"><img alt="pypi: tba-contracts-workload-identity" src="https://img.shields.io/pypi/v/tba-contracts-workload-identity"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-workload-identity/pyproject.toml"><img alt="Source version: 0.4.0.dev3" src="https://img.shields.io/static/v1?label=Source%20version&amp;message=0.4.0.dev3&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-workload-identity/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/static/v1?label=Python&amp;message=%3E%3D3.10%2C%3C3.16&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-workload-identity/pyproject.toml"><img alt="Layer: 002-contracts" src="https://img.shields.io/static/v1?label=Layer&amp;message=002-contracts&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-workload-identity/README.md#lifecycle-and-migration"><img alt="Lifecycle: active" src="https://img.shields.io/static/v1?label=Lifecycle&amp;message=active&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-workload-identity/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/static/v1?label=License&amp;message=Apache-2.0&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-workload-identity/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/static/v1?label=Notice&amp;message=attribution&amp;color=525252"></a>
</p>
<p align="center">
<a href="https://pypi.org/project/tba-contracts-workload-identity/"><img alt="Monthly PyPI downloads: tba-contracts-workload-identity" src="https://img.shields.io/pypi/dm/tba-contracts-workload-identity"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-workload-identity/README.md"><img alt="README hits: tba-contracts-workload-identity" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/pkgs/002-contracts/tba-contracts-workload-identity/README.md.svg?label=README%20hits"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="README standards: CI gate" src="https://img.shields.io/static/v1?label=README%20standards&amp;message=CI%20gate&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-workload-identity/docs/readme/test_examples.py"><img alt="Tests: example source" src="https://img.shields.io/static/v1?label=Tests&amp;message=example%20source&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-workload-identity/README.md#certification-status"><img alt="Certification: not certified" src="https://img.shields.io/static/v1?label=Certification&amp;message=not%20certified&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/tools/readme/POLICY.md"><img alt="Governance: repository policy" src="https://img.shields.io/static/v1?label=Governance&amp;message=repository%20policy&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="Evidence: source and CI" src="https://img.shields.io/static/v1?label=Evidence&amp;message=source%20and%20CI&amp;color=525252"></a>
</p>
<p align="center"><a href="#overview">Overview</a> · <a href="#installation">Installation</a> · <a href="#quick-start">Quick Start</a> · <a href="#usage">Usage</a> · <a href="#public-api-and-import-surfaces">API</a> · <a href="#contributing">Contributing</a> · <a href="#governance">Governance</a> · <a href="#license">License</a></p>
<!-- readme-standards:end branding -->

---

## Overview

### Summary

Owns workload identifiers, selectors, SVIDs, trust bundles, and their semantic ports.

- Package: `tba-contracts-workload-identity`
- Layer: `002-contracts`
- Responsibility: Protocol-neutral workload identity, credential, trust, and delegation contracts.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-workload-identity/src/tba_contracts_workload_identity/__init__.py).
- Distribution: Python package on PyPI.

### Why This Package

`tba-contracts-workload-identity` isolates this responsibility: Protocol-neutral workload identity, credential, trust, and delegation contracts. Its [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-workload-identity/src/tba_contracts_workload_identity/__init__.py) exposes `DelegatedWorkloadCredentialProviderPort`, `DelegatedWorkloadCredentialRequest`, `ResolvedWorkload`, `SpiffeId`, `SpiffeTrustBundle`, `Svid`, `SvidFormat`, `SvidProviderPort`, `SvidVerifierPort`, `TrustBundleProviderPort`, `TrustDomain`, `WorkloadCredential`, `WorkloadCredentialEntitlement`, `WorkloadCredentialProviderPort`, `WorkloadCredentialRequest`, allowing consumers to select this package without treating adjacent packages as part of its public contract.

### When to Use

Choose `tba-contracts-workload-identity` for this responsibility: Protocol-neutral workload identity, credential, trust, and delegation contracts. Its `002-contracts` placement keeps shared types and structural ports separate from environment-specific service implementations or HTTP routing.

### Features

- `SpiffeTrustBundle`: declared in src/tba_contracts_workload_identity/bundles.py
- `TrustBundleProviderPort`: declared in src/tba_contracts_workload_identity/bundles.py
- `WorkloadCredentialRequest`: declared in src/tba_contracts_workload_identity/credentials.py
- `WorkloadCredential`: declared in src/tba_contracts_workload_identity/credentials.py
- `WorkloadCredentialSet`: declared in src/tba_contracts_workload_identity/credentials.py
- `DelegatedWorkloadCredentialRequest`: declared in src/tba_contracts_workload_identity/delegation.py
- `WorkloadCredentialEntitlement`: declared in src/tba_contracts_workload_identity/delegation.py
- `WorkloadIdentityRef`: declared in src/tba_contracts_workload_identity/identity.py

### Non-Goals

`tba-contracts-workload-identity` does not take ownership of environment-specific service implementations or HTTP routing.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

---

## Getting Started

### Prerequisites

Python `>=3.10,<3.16` is required. The [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-workload-identity/pyproject.toml) declares runtime dependencies including `tba-primitives-identity`. Read the example’s inputs and service requirements before execution.

### Installation

Install the selected PyPI release of `tba-contracts-workload-identity`:

```bash
uv pip install tba-contracts-workload-identity
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/002-contracts/tba-contracts-workload-identity
```

#### uv

<!-- readme-standards:begin installation.uv -->
```bash
uv add tba-contracts-workload-identity
```
<!-- readme-standards:end installation.uv -->

#### pip

<!-- readme-standards:begin installation.pip -->
```bash
python -m pip install tba-contracts-workload-identity
```
<!-- readme-standards:end installation.pip -->

#### Poetry

<!-- readme-standards:begin installation.poetry -->
```bash
poetry add tba-contracts-workload-identity
```
<!-- readme-standards:end installation.poetry -->

### Quick Start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.


```bash
uv run --isolated --no-project --python 3.12 --with "tba-contracts-workload-identity==0.4.0.dev3" python quickstart.py
```

The import and assertion succeed when the DelegatedWorkloadCredentialProviderPort entry point is available.

#### Example

<!-- readme-standards:begin example.quick-start -->
Source: [docs/readme/quick_start.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-workload-identity/docs/readme/quick_start.py).

```python
from tba_contracts_workload_identity import DelegatedWorkloadCredentialProviderPort

assert callable(DelegatedWorkloadCredentialProviderPort)
```
<!-- readme-standards:end example.quick-start -->

#### Expected Result

The example demonstrates the documented `tba-contracts-workload-identity` source boundary or workflow. Complete its required configuration first. README CI checks the maintained source’s syntax and declarations; it does not claim that external services or the application workflow were exercised.

---

## Usage

### Common Workflows

<!-- readme-standards:begin example.usage -->
Source: [docs/readme/usage.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-workload-identity/docs/readme/usage.py).

```python
from tba_contracts_workload_identity import DelegatedWorkloadCredentialProviderPort

assert callable(DelegatedWorkloadCredentialProviderPort)
```
<!-- readme-standards:end example.usage -->

The following public-entry-point example belongs to `tba-contracts-workload-identity`. Protocol-neutral workload identity, credential, trust, and delegation contracts. Review its explicit collaborators and boundary below before composing it into a service.

### Configuration

Configure `tba-contracts-workload-identity` through the APIs in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-workload-identity/src/tba_contracts_workload_identity/__init__.py); its [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-workload-identity/pyproject.toml) describes installation requirements, not an implicit service configuration. No additional package-global configuration contract is inferred from dependencies.

### Error Handling

The inspected `tba-contracts-workload-identity` source raises `ValueError`. Handle these at the calling boundary and consult the implementation for the triggering conditions.

### Best Practices

Use the explicit `tba-contracts-workload-identity` imports documented below and keep collaborator configuration with the caller. Run the package’s relevant tests after changing `DelegatedWorkloadCredentialProviderPort`, `DelegatedWorkloadCredentialRequest`, `ResolvedWorkload`, `SpiffeId`, `SpiffeTrustBundle`, `Svid`, `SvidFormat`, `SvidProviderPort`, `SvidVerifierPort`, `TrustBundleProviderPort`, `TrustDomain`, `WorkloadCredential`, `WorkloadCredentialEntitlement`, `WorkloadCredentialProviderPort`, `WorkloadCredentialRequest`; an import or successful installation alone does not establish its runtime guarantees.

---

## Package Boundary

### What It Owns

`tba-contracts-workload-identity` belongs to `002-contracts` and owns shared types and structural ports: Protocol-neutral workload identity, credential, trust, and delegation contracts.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-workload-identity/src/tba_contracts_workload_identity/__init__.py). Public exports include `DelegatedWorkloadCredentialProviderPort`, `DelegatedWorkloadCredentialRequest`, `ResolvedWorkload`, `SpiffeId`, `SpiffeTrustBundle`, `Svid`, `SvidFormat`, `SvidProviderPort`, `SvidVerifierPort`, `TrustBundleProviderPort`, `TrustDomain`, `WorkloadCredential`.

Keep environment-specific service implementations or HTTP routing in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

### Public API and Import Surfaces

Import namespace: `tba_contracts_workload_identity`.

Source-declared exports or types: `DelegatedWorkloadCredentialProviderPort`, `DelegatedWorkloadCredentialRequest`, `ResolvedWorkload`, `SpiffeId`, `SpiffeTrustBundle`, `Svid`, `SvidFormat`, `SvidProviderPort`, `SvidVerifierPort`, `TrustBundleProviderPort`, `TrustDomain`, `WorkloadCredential`, `WorkloadCredentialEntitlement`, `WorkloadCredentialProviderPort`, `WorkloadCredentialRequest`.

Inspect [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-workload-identity/src/tba_contracts_workload_identity/__init__.py) for exact signatures; this inventory does not designate every internal module as stable.

### Entry Points

<!-- readme-standards:begin entry-points -->
This package declares no command-line, GUI, or plugin entry points in its manifest.
<!-- readme-standards:end entry-points -->

### Injected Dependencies

The [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-workload-identity/src/tba_contracts_workload_identity/__init__.py) for `tba-contracts-workload-identity` does not declare an explicit service-constructor or keyword-only factory hook in the inspected source. Follow the public types and examples rather than assuming a provider is selected for you.

Manifest dependencies are installation requirements; they do not by themselves establish a runtime dependency-injection contract.

### Protocol Consumers

Direct consumers in this checkout’s package manifests include `tba-contracts-identity`, `tba-bases-workload-identity`, `tba-concrete-jwt-svid-credential`, `tba-concrete-svid`, `tba-concrete-wit-svid-credential`, `tba-concrete-x509-svid-credential`, `tba-provider-spiffe-bundle`, `tba-provider-spiffe-workload-api`, `tba-capability-workload-credential-brokering`, `tba-capability-workload-identity`, `tba-credentials`, `tba-workspace`. These edges describe declared dependencies, not protocol-conformance evidence.

### Extensions

For `tba-contracts-workload-identity`, use the source-declared public interfaces (`DelegatedWorkloadCredentialProviderPort`, `DelegatedWorkloadCredentialRequest`, `ResolvedWorkload`, `SpiffeId`, `SpiffeTrustBundle`, `Svid`, `SvidFormat`, `SvidProviderPort`, `SvidVerifierPort`, `TrustBundleProviderPort`, `TrustDomain`, `WorkloadCredential`, `WorkloadCredentialEntitlement`, `WorkloadCredentialProviderPort`, `WorkloadCredentialRequest`) when composing or extending behavior. Its entry-point section below is authoritative for registered plugins; no additional extension loader is inferred from the package name.

---

## Operations and Readiness

### Operational Requirements

`tba-contracts-workload-identity` exposes shared types and structural ports. Public operations found in its source:

- `TrustBundleProviderPort.bundle_for` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-workload-identity/src/tba_contracts_workload_identity/bundles.py).
- `WorkloadReferenceResolverPort.resolve` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-workload-identity/src/tba_contracts_workload_identity/ports.py).
- `WorkloadCredentialProviderPort.obtain` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-workload-identity/src/tba_contracts_workload_identity/ports.py).
- `DelegatedWorkloadCredentialProviderPort.obtain_for` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-workload-identity/src/tba_contracts_workload_identity/ports.py).
- `WorkloadCredentialVerifierPort.verify` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-workload-identity/src/tba_contracts_workload_identity/ports.py).
- `WorkloadTrustMaterialProviderPort.trust_material_for` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-workload-identity/src/tba_contracts_workload_identity/ports.py).
- `SpiffeId.parse` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-workload-identity/src/tba_contracts_workload_identity/spiffe.py).
- `SvidProviderPort.fetch_svid` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-workload-identity/src/tba_contracts_workload_identity/svid.py).
- `SvidVerifierPort.verify_svid` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-workload-identity/src/tba_contracts_workload_identity/svid.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

### Health and Observability

This README does not establish a standalone health endpoint for `tba-contracts-workload-identity`. Observe the concrete caller’s results, exceptions, and existing test reports. An application that embeds this package must define its own health and telemetry contract.

### Security and Resource Limits

Apply the input, credential, and resource constraints implemented in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-workload-identity/src/tba_contracts_workload_identity/__init__.py). The `tba-contracts-workload-identity` README gate is a documentation check, not a security review or a substitute for the implementation’s limits and caller authorization.

### Compatibility

This source version of `tba-contracts-workload-identity` declares Python `>=3.10,<3.16`. Consult its dependency constraints before upgrading. Source-version and registry-version badges have separate meanings; this migration makes no additional platform or interoperability certification claim.

---

## Verification

### Tests

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-workload-identity/src/tba_contracts_workload_identity/__init__.py).

### Certification Status

No external certification is asserted for `tba-contracts-workload-identity` by this documentation migration. README conformance, example syntax, runtime tests, and protocol or security certification are distinct evidence scopes.

### Evidence

The [README standards CI](https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml) records mechanical documentation results for its tested commit. The [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-workload-identity/src/tba_contracts_workload_identity/__init__.py) and example sources support the package-boundary description; external runtime behavior requires its own test evidence.

---

## FAQ

### Why

**Why select this package?** `tba-contracts-workload-identity` provides protocol-neutral workload identity, credential, trust, and delegation contracts; use its own API boundary rather than assuming neighboring packages are bundled or configured automatically.

### How

**How do I start?** Install or synchronize the environment under Getting Started, follow the maintained example for `tba-contracts-workload-identity`, and consult [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-workload-identity/src/tba_contracts_workload_identity/__init__.py) for the exact types and signatures involved.

### When

**When should I validate an upgrade?** Recheck `tba-contracts-workload-identity` whenever its source version, declared collaborators, configuration, or caller changes. Run relevant behavioral tests in addition to the README gate before promotion.

---

## Documentation and Related Packages

### More Documentation

The [repository contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md), [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-workload-identity/src/tba_contracts_workload_identity/__init__.py), and [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-workload-identity/pyproject.toml) provide the supporting context for `tba-contracts-workload-identity`. The [README policy](https://github.com/groupsum/readme-standards/blob/master/docs/outline.md) defines the common document structure.

### Related Packages

Declared local runtime dependencies:

- [tba-primitives-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/000-primitives/tba-primitives-identity/README.md)

Direct downstream consumers:

- [tba-bases-workload-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-workload-identity/README.md)
- [tba-capability-workload-credential-brokering](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-workload-credential-brokering/README.md)
- [tba-capability-workload-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-workload-identity/README.md)
- [tba-concrete-jwt-svid-credential](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-jwt-svid-credential/README.md)
- [tba-concrete-svid](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-svid/README.md)
- [tba-concrete-wit-svid-credential](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-wit-svid-credential/README.md)
- [tba-concrete-x509-svid-credential](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-x509-svid-credential/README.md)
- [tba-contracts-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-identity/README.md)
- [tba-credentials](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-credentials/README.md)
- [tba-provider-spiffe-bundle](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-spiffe-bundle/README.md)
- [tba-provider-spiffe-workload-api](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-spiffe-workload-api/README.md)

### Project Links

<!-- readme-standards:begin project-links -->
- [Documentation](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/002-contracts/tba-contracts-workload-identity#readme)
- [Homepage](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/002-contracts/tba-contracts-workload-identity#readme)
- [Issues](https://github.com/tigrbl/tigrbl_auth/issues)
- [PyPI](https://pypi.org/project/tba-contracts-workload-identity/)
- [Repository](https://github.com/tigrbl/tigrbl_auth)
- [Source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/002-contracts/tba-contracts-workload-identity)
- [pypi: tba-contracts-workload-identity](https://pypi.org/project/tba-contracts-workload-identity/)
<!-- readme-standards:end project-links -->

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/002-contracts/tba-contracts-workload-identity)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-workload-identity/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-workload-identity/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-workload-identity/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-contracts-workload-identity/)

---

## Contributing

### How to Contribute

Follow the [contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md) and include a focused example or regression for changes to `tba-contracts-workload-identity`. Keep package behavior, its documented boundary, and its tests aligned.

### Development Setup

Work from the `pkgs/002-contracts/tba-contracts-workload-identity` checkout. Synchronize its declared development environment with uv, then run the relevant package tests and `python -m pytest docs/readme/test_examples.py`. The repository’s dedicated README job installs `readme-standards==0.1.1` without resolving unrelated runtime packages.

### Notes for Maintainers

Edit authored prose directly in this `tba-contracts-workload-identity` README. Update source examples in `docs/readme/`, then run `readme-standards render --root . --write` from the package directory and review the diff. Required headings and generated blocks come from package-guide-v1.

---

## Governance

### Ownership and Decision Making

Changes to `tba-contracts-workload-identity` follow the maintainer review process of [tigrbl/tigrbl_auth](https://github.com/tigrbl/tigrbl_auth) and its contribution guide. Author attribution remains in the [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-workload-identity/pyproject.toml); this README does not assign new publishing or administrative authority.

### Standards and Policies

`tba-contracts-workload-identity` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `002-contracts` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

### Lifecycle and Migration

The `tba-contracts-workload-identity` source version is `0.4.0.dev3`. This change standardizes documentation and adds a development-only gate; it does not publish a new runtime version or declare a previously unpublished package released. Preserve explicit deprecation and replacement instructions where present.

---

## License and Attribution

### License

<!-- readme-standards:begin license -->
Licensed under `Apache-2.0`. See [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-workload-identity/LICENSE).
<!-- readme-standards:end license -->

### Notices

<!-- readme-standards:begin notices -->
See [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-workload-identity/NOTICE) for attribution.
<!-- readme-standards:end notices -->
