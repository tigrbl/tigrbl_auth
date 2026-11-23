# tba-runtime-identity-storage

<!-- readme-standards:begin branding -->
<p align="center"><a href="https://github.com/tigrbl/tigrbl_auth"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="300"></a></p>
<p align="center"><strong>tba-runtime-identity-storage</strong></p>
<p align="center">Runtime execution helpers for TBA identity storage migrations and provider-bound storage lifecycle wiring.</p>
<p align="center">
<a href="https://pypi.org/project/tba-runtime-identity-storage/"><img alt="pypi: tba-runtime-identity-storage" src="https://img.shields.io/pypi/v/tba-runtime-identity-storage"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-runtime-identity-storage/pyproject.toml"><img alt="Source version: 0.4.0.dev3" src="https://img.shields.io/static/v1?label=Source%20version&amp;message=0.4.0.dev3&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-runtime-identity-storage/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/static/v1?label=Python&amp;message=%3E%3D3.10%2C%3C3.16&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-runtime-identity-storage/pyproject.toml"><img alt="Layer: 030-storage-runtime" src="https://img.shields.io/static/v1?label=Layer&amp;message=030-storage-runtime&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-runtime-identity-storage/README.md#lifecycle-and-migration"><img alt="Lifecycle: active" src="https://img.shields.io/static/v1?label=Lifecycle&amp;message=active&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-runtime-identity-storage/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/static/v1?label=License&amp;message=Apache-2.0&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-runtime-identity-storage/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/static/v1?label=Notice&amp;message=attribution&amp;color=525252"></a>
</p>
<p align="center">
<a href="https://pypi.org/project/tba-runtime-identity-storage/"><img alt="Monthly PyPI downloads: tba-runtime-identity-storage" src="https://img.shields.io/pypi/dm/tba-runtime-identity-storage"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-runtime-identity-storage/README.md"><img alt="README hits: tba-runtime-identity-storage" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/pkgs/030-storage-runtime/tba-runtime-identity-storage/README.md.svg?label=README%20hits"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="README standards: CI gate" src="https://img.shields.io/static/v1?label=README%20standards&amp;message=CI%20gate&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-runtime-identity-storage/docs/readme/test_examples.py"><img alt="Tests: example source" src="https://img.shields.io/static/v1?label=Tests&amp;message=example%20source&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-runtime-identity-storage/README.md#certification-status"><img alt="Certification: not certified" src="https://img.shields.io/static/v1?label=Certification&amp;message=not%20certified&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/tools/readme/POLICY.md"><img alt="Governance: repository policy" src="https://img.shields.io/static/v1?label=Governance&amp;message=repository%20policy&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="Evidence: source and CI" src="https://img.shields.io/static/v1?label=Evidence&amp;message=source%20and%20CI&amp;color=525252"></a>
</p>
<p align="center"><a href="#overview">Overview</a> · <a href="#installation">Installation</a> · <a href="#quick-start">Quick Start</a> · <a href="#usage">Usage</a> · <a href="#public-api-and-import-surfaces">API</a> · <a href="#contributing">Contributing</a> · <a href="#governance">Governance</a> · <a href="#license">License</a></p>
<!-- readme-standards:end branding -->

---

## Overview

### Summary

Aggregate runtime for the split layer-30 durability packages.

Table specifications use Tigrbl's public `makeOp`, `defineTableSpec`,
`deriveTableSpec`, `provideTableSpec`, and `activateTableSpec` functions.
Table-family operations remain in their standalone `*-durability` owner; this
aggregate package collects and activates them without defining factory aliases.

Layer 30 owns carrier-neutral Tigrbl operations, derived table specifications,
and durability hooks. It does not own tables or migrations (layer 01), semantic
contracts (layer 02), provider selection (layer 20), engine construction
(layer 60), HTTP routes, or protocol wire models.

Each durability package imports its table classes directly from the corresponding layer-01 domain storage package and declares those dependencies. This aggregate additionally depends on storage-core for full composition and legacy migration discovery.

- Package: `tba-runtime-identity-storage`
- Layer: `030-storage-runtime`
- Responsibility: Runtime execution helpers for TBA identity storage migrations and provider-bound storage lifecycle wiring.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-runtime-identity-storage/src/tba_runtime_identity_storage/__init__.py).
- Distribution: Python package on PyPI.

### Why This Package

`tba-runtime-identity-storage` isolates this responsibility: Runtime execution helpers for TBA identity storage migrations and provider-bound storage lifecycle wiring. Its [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-runtime-identity-storage/src/tba_runtime_identity_storage/__init__.py) exposes `AttestationEvidenceRuntimeSpec`, `AttestationReferenceManifestRuntimeSpec`, `AttestationResultRuntimeSpec`, `CredentialIssuanceTransactionRuntimeSpec`, `CredentialOfferRuntimeSpec`, `CredentialStatusEntryRuntimeSpec`, `DURABLE_REPLAY_DESCRIPTOR`, `DURABLE_RUNTIME_TABLE_SPECS`, `DpopNonceRuntimeSpec`, `DpopReplayRuntimeSpec`, `GnapClientInstanceRuntimeSpec`, `GnapContinuationRuntimeSpec`, `GnapGrantRuntimeSpec`, `GnapInteractionRuntimeSpec`, `IdentityTopologySnapshot`, allowing consumers to select this package without treating adjacent packages as part of its public contract.

### When to Use

Choose `tba-runtime-identity-storage` for this responsibility: Runtime execution helpers for TBA identity storage migrations and provider-bound storage lifecycle wiring. Its `030-storage-runtime` placement keeps storage-backed runtime adapters separate from protocol wire definitions or standalone application hosting.

### Features

- `CryptoProviderRegistry`: Small runtime registry from durable provider names to provider instances.
- `OperationContext`: declared in src/tba_runtime_identity_storage/_operator_store/paths.py
- `FilterSpec`: declared in src/tba_runtime_identity_storage/_operator_store/paths.py
- `TransactionResult`: declared in src/tba_runtime_identity_storage/_operator_store/paths.py
- `ArtifactResult`: declared in src/tba_runtime_identity_storage/_operator_store/paths.py
- `OperatorStateError`: declared in src/tba_runtime_identity_storage/_resource_service/resource_operations.py
- `MigrationResult`: declared in src/tba_runtime_identity_storage/migrations/runtime.py
- `SchemaVerification`: declared in src/tba_runtime_identity_storage/migrations/runtime.py

### Non-Goals

`tba-runtime-identity-storage` does not take ownership of protocol wire definitions or standalone application hosting.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

---

## Getting Started

### Prerequisites

Python `>=3.10,<3.16` is required. The [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-runtime-identity-storage/pyproject.toml) declares runtime dependencies including `pydantic`, `tba-provider-security-authorization-provenance-builder`, `tigrbl-concrete`, `tigrbl-core`, `tba-primitives-identity`, `tba-storage-core`, `tigrbl-migrations`, `tba-contracts-identity`, `tba-contracts-security-trust`, `tba-durability-identity`, `tba-durability-session`, `tba-durability-consent`. Read the example’s inputs and service requirements before execution.

### Installation

Install the selected PyPI release of `tba-runtime-identity-storage`:

```bash
uv pip install tba-runtime-identity-storage
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/030-storage-runtime/tba-runtime-identity-storage
```

#### uv

<!-- readme-standards:begin installation.uv -->
```bash
uv add tba-runtime-identity-storage
```
<!-- readme-standards:end installation.uv -->

#### pip

<!-- readme-standards:begin installation.pip -->
```bash
python -m pip install tba-runtime-identity-storage
```
<!-- readme-standards:end installation.pip -->

#### Poetry

<!-- readme-standards:begin installation.poetry -->
```bash
poetry add tba-runtime-identity-storage
```
<!-- readme-standards:end installation.poetry -->

### Quick Start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.


```bash
uv run --isolated --no-project --python 3.12 --with "tba-runtime-identity-storage==0.4.0.dev3" python quickstart.py
```

The import and assertion succeed when the initializeIdentityRuntimeTables entry point is available.

#### Example

<!-- readme-standards:begin example.quick-start -->
Source: [docs/readme/quick_start.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-runtime-identity-storage/docs/readme/quick_start.py).

```python
from tba_runtime_identity_storage import initializeIdentityRuntimeTables

assert callable(initializeIdentityRuntimeTables)
```
<!-- readme-standards:end example.quick-start -->

#### Expected Result

The example demonstrates the documented `tba-runtime-identity-storage` source boundary or workflow. Complete its required configuration first. README CI checks the maintained source’s syntax and declarations; it does not claim that external services or the application workflow were exercised.

---

## Usage

### Common Workflows

<!-- readme-standards:begin example.usage -->
Source: [docs/readme/usage.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-runtime-identity-storage/docs/readme/usage.py).

```python
from tba_runtime_identity_storage import initializeIdentityRuntimeTables

assert callable(initializeIdentityRuntimeTables)
```
<!-- readme-standards:end example.usage -->

The following public-entry-point example belongs to `tba-runtime-identity-storage`. Runtime execution helpers for TBA identity storage migrations and provider-bound storage lifecycle wiring. Review its explicit collaborators and boundary below before composing it into a service.

### Configuration

The [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-runtime-identity-storage/src/tba_runtime_identity_storage/__init__.py) references configuration keys `ASYNC_FALLBACK_DB`, `PG_DB`, `PG_DSN`, `PG_HOST`, `PG_PASS`, `PG_PORT`, `PG_USER`, `POSTGRES_URL`, `TBA_AUTH_OPERATOR_STATE_DIR`, `XDG_STATE_HOME`. Consult the constructor or function signature before supplying them; a referenced key is not necessarily a global environment variable.

### Error Handling

The inspected `tba-runtime-identity-storage` source raises `InvalidRefreshTokenError`, `LookupError`, `OperatorStateError`, `PermissionError`, `RefreshTokenReuseError`, `RuntimeError`, `ValueError`. Handle these at the calling boundary and consult the implementation for the triggering conditions.

### Best Practices

Use the explicit `tba-runtime-identity-storage` imports documented below and keep collaborator configuration with the caller. Run the package’s relevant tests after changing `AttestationEvidenceRuntimeSpec`, `AttestationReferenceManifestRuntimeSpec`, `AttestationResultRuntimeSpec`, `CredentialIssuanceTransactionRuntimeSpec`, `CredentialOfferRuntimeSpec`, `CredentialStatusEntryRuntimeSpec`, `DURABLE_REPLAY_DESCRIPTOR`, `DURABLE_RUNTIME_TABLE_SPECS`, `DpopNonceRuntimeSpec`, `DpopReplayRuntimeSpec`, `GnapClientInstanceRuntimeSpec`, `GnapContinuationRuntimeSpec`, `GnapGrantRuntimeSpec`, `GnapInteractionRuntimeSpec`, `IdentityTopologySnapshot`; an import or successful installation alone does not establish its runtime guarantees.

---

## Package Boundary

### What It Owns

`tba-runtime-identity-storage` belongs to `030-storage-runtime` and owns storage-backed runtime adapters: Runtime execution helpers for TBA identity storage migrations and provider-bound storage lifecycle wiring.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-runtime-identity-storage/src/tba_runtime_identity_storage/__init__.py). Public exports include `RUNTIME_TABLES`, `RUNTIME_TABLE_BY_NAME`, `RUNTIME_TABLE_SPECS`, `RUNTIME_TABLE_SPEC_BY_NAME`, `RUNTIME_OPERATION_BY_ALIAS`, `initializeIdentityRuntimeTables`, `initialize_identity_runtime_tables`, `DURABLE_RUNTIME_TABLE_SPECS`, `MigrationContract`, `MigrationRevision`, `MigrationResult`, `SchemaVerification`.

Keep protocol wire definitions or standalone application hosting in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

### Public API and Import Surfaces

Import namespace: `tba_runtime_identity_storage`.

Source-declared exports or types: `AttestationEvidenceRuntimeSpec`, `AttestationReferenceManifestRuntimeSpec`, `AttestationResultRuntimeSpec`, `CredentialIssuanceTransactionRuntimeSpec`, `CredentialOfferRuntimeSpec`, `CredentialStatusEntryRuntimeSpec`, `DURABLE_REPLAY_DESCRIPTOR`, `DURABLE_RUNTIME_TABLE_SPECS`, `DpopNonceRuntimeSpec`, `DpopReplayRuntimeSpec`, `GnapClientInstanceRuntimeSpec`, `GnapContinuationRuntimeSpec`, `GnapGrantRuntimeSpec`, `GnapInteractionRuntimeSpec`, `IdentityTopologySnapshot`.

Inspect [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-runtime-identity-storage/src/tba_runtime_identity_storage/__init__.py) for exact signatures; this inventory does not designate every internal module as stable.

### Entry Points

<!-- readme-standards:begin entry-points -->
This package declares no command-line, GUI, or plugin entry points in its manifest.
<!-- readme-standards:end entry-points -->

### Injected Dependencies

Explicit construction inputs and collaborators for `tba-runtime-identity-storage`:

- `stash_security_providers` construction inputs: `key_provider`, `signer`, `verifier`, `jwt_coder`, `clock`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-runtime-identity-storage/src/tba_runtime_identity_storage/security_context.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

### Protocol Consumers

Direct consumers in this checkout’s package manifests include `tba-cli-identity`, `tba-runtime-identity`, `tba-server-identity`, `tba-auth`, `tba-app-backend-core`, `tba-workspace`. These edges describe declared dependencies, not protocol-conformance evidence.

### Extensions

For `tba-runtime-identity-storage`, use the source-declared public interfaces (`AttestationEvidenceRuntimeSpec`, `AttestationReferenceManifestRuntimeSpec`, `AttestationResultRuntimeSpec`, `CredentialIssuanceTransactionRuntimeSpec`, `CredentialOfferRuntimeSpec`, `CredentialStatusEntryRuntimeSpec`, `DURABLE_REPLAY_DESCRIPTOR`, `DURABLE_RUNTIME_TABLE_SPECS`, `DpopNonceRuntimeSpec`, `DpopReplayRuntimeSpec`, `GnapClientInstanceRuntimeSpec`, `GnapContinuationRuntimeSpec`, `GnapGrantRuntimeSpec`, `GnapInteractionRuntimeSpec`, `IdentityTopologySnapshot`) when composing or extending behavior. Its entry-point section below is authoritative for registered plugins; no additional extension loader is inferred from the package name.

---

## Operations and Readiness

### Operational Requirements

`tba-runtime-identity-storage` exposes storage-backed runtime adapters. Public operations found in its source:

- `initializeIdentityRuntimeTables` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-runtime-identity-storage/src/tba_runtime_identity_storage/initialize.py).
- `iter_migration_modules` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-runtime-identity-storage/src/tba_runtime_identity_storage/migrations/runtime.py).
- `expected_table_names` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-runtime-identity-storage/src/tba_runtime_identity_storage/migrations/runtime.py).
- `verify_schema_sync` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-runtime-identity-storage/src/tba_runtime_identity_storage/migrations/runtime.py).
- `column_names_sync` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-runtime-identity-storage/src/tba_runtime_identity_storage/migrations/runtime.py).
- `apply_all_async` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-runtime-identity-storage/src/tba_runtime_identity_storage/migrations/runtime.py).
- `downgrade_one_async` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-runtime-identity-storage/src/tba_runtime_identity_storage/migrations/runtime.py).
- `verify_schema_async` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-runtime-identity-storage/src/tba_runtime_identity_storage/migrations/runtime.py).
- `column_names_async` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-runtime-identity-storage/src/tba_runtime_identity_storage/migrations/runtime.py).
- `make_attestation_appraisal_recorder` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-runtime-identity-storage/src/tba_runtime_identity_storage/ops/attestation.py).
- `stash_security_providers` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-runtime-identity-storage/src/tba_runtime_identity_storage/security_context.py).
- `run_async` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-runtime-identity-storage/src/tba_runtime_identity_storage/sync.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

### Health and Observability

This README does not establish a standalone health endpoint for `tba-runtime-identity-storage`. Observe the concrete caller’s results, exceptions, and existing test reports. An application that embeds this package must define its own health and telemetry contract.

### Security and Resource Limits

Apply the input, credential, and resource constraints implemented in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-runtime-identity-storage/src/tba_runtime_identity_storage/__init__.py). The `tba-runtime-identity-storage` README gate is a documentation check, not a security review or a substitute for the implementation’s limits and caller authorization.

### Compatibility

This source version of `tba-runtime-identity-storage` declares Python `>=3.10,<3.16`. Consult its dependency constraints before upgrading. Source-version and registry-version badges have separate meanings; this migration makes no additional platform or interoperability certification claim.

---

## Verification

### Tests

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-runtime-identity-storage/src/tba_runtime_identity_storage/__init__.py).

### Certification Status

No external certification is asserted for `tba-runtime-identity-storage` by this documentation migration. README conformance, example syntax, runtime tests, and protocol or security certification are distinct evidence scopes.

### Evidence

The [README standards CI](https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml) records mechanical documentation results for its tested commit. The [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-runtime-identity-storage/src/tba_runtime_identity_storage/__init__.py) and example sources support the package-boundary description; external runtime behavior requires its own test evidence.

---

## FAQ

### Why

**Why select this package?** `tba-runtime-identity-storage` provides runtime execution helpers for TBA identity storage migrations and provider-bound storage lifecycle wiring; use its own API boundary rather than assuming neighboring packages are bundled or configured automatically.

### How

**How do I start?** Install or synchronize the environment under Getting Started, follow the maintained example for `tba-runtime-identity-storage`, and consult [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-runtime-identity-storage/src/tba_runtime_identity_storage/__init__.py) for the exact types and signatures involved.

### When

**When should I validate an upgrade?** Recheck `tba-runtime-identity-storage` whenever its source version, declared collaborators, configuration, or caller changes. Run relevant behavioral tests in addition to the README gate before promotion.

---

## Documentation and Related Packages

### More Documentation

The [repository contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md), [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-runtime-identity-storage/src/tba_runtime_identity_storage/__init__.py), and [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-runtime-identity-storage/pyproject.toml) provide the supporting context for `tba-runtime-identity-storage`. The [README policy](https://github.com/groupsum/readme-standards/blob/master/docs/outline.md) defines the common document structure.

### Related Packages

Declared local runtime dependencies:

- [tba-contracts-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-identity/README.md)
- [tba-contracts-security-trust](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-security-trust/README.md)
- [tba-durability-attestation](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-durability-attestation/README.md)
- [tba-durability-audit](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-durability-audit/README.md)
- [tba-durability-authorization-policy](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-durability-authorization-policy/README.md)
- [tba-durability-consent](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-durability-consent/README.md)
- [tba-durability-delegation](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-durability-delegation/README.md)
- [tba-durability-digital-credential](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-durability-digital-credential/README.md)
- [tba-durability-gnap-state](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-durability-gnap-state/README.md)
- [tba-durability-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-durability-identity/README.md)
- [tba-durability-key-material](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-durability-key-material/README.md)
- [tba-durability-oauth-state](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-durability-oauth-state/README.md)
- [tba-durability-oidc-state](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-durability-oidc-state/README.md)
- [tba-durability-presentation](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-durability-presentation/README.md)
- [tba-durability-replay-protection](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-durability-replay-protection/README.md)
- [tba-durability-security-event](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-durability-security-event/README.md)
- [tba-durability-session](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-durability-session/README.md)
- [tba-durability-token](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-durability-token/README.md)
- [tba-durability-webauthn](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-durability-webauthn/README.md)
- [tba-durability-workload-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-durability-workload-identity/README.md)
- [tba-primitives-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/000-primitives/tba-primitives-identity/README.md)
- [tba-provider-security-authorization-provenance-builder](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-security-authorization-provenance-builder/README.md)
- [tba-storage-authorization-policy](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-authorization-policy/README.md)
- [tba-storage-consent](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-consent/README.md)
- [tba-storage-core](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-core/README.md)
- [tba-storage-key-material](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-key-material/README.md)
- [tba-storage-oauth](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-oauth/README.md)
- [tba-storage-operator](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-operator/README.md)
- [tba-storage-principals](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-principals/README.md)
- [tba-storage-tenancy](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-tenancy/README.md)
- [tba-storage-token](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-token/README.md)

Direct downstream consumers:

- [tba-app-backend-core](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-core/README.md)
- [tba-auth](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-auth/README.md)
- [tba-cli-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-cli-identity/README.md)
- [tba-runtime-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity/README.md)
- [tba-server-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-server-identity/README.md)

### Project Links

<!-- readme-standards:begin project-links -->
- [Documentation](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/030-storage-runtime/tba-runtime-identity-storage#readme)
- [Homepage](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/030-storage-runtime/tba-runtime-identity-storage#readme)
- [Issues](https://github.com/tigrbl/tigrbl_auth/issues)
- [PyPI](https://pypi.org/project/tba-runtime-identity-storage/)
- [Repository](https://github.com/tigrbl/tigrbl_auth)
- [SSOT](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [Source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/030-storage-runtime/tba-runtime-identity-storage)
- [pypi: tba-runtime-identity-storage](https://pypi.org/project/tba-runtime-identity-storage/)
<!-- readme-standards:end project-links -->

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/030-storage-runtime/tba-runtime-identity-storage)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-runtime-identity-storage/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-runtime-identity-storage/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-runtime-identity-storage/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-runtime-identity-storage/)

---

## Contributing

### How to Contribute

Follow the [contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md) and include a focused example or regression for changes to `tba-runtime-identity-storage`. Keep package behavior, its documented boundary, and its tests aligned.

### Development Setup

Work from the `pkgs/030-storage-runtime/tba-runtime-identity-storage` checkout. Synchronize its declared development environment with uv, then run the relevant package tests and `python -m pytest docs/readme/test_examples.py`. The repository’s dedicated README job installs `readme-standards==0.1.1` without resolving unrelated runtime packages.

### Notes for Maintainers

Edit authored prose directly in this `tba-runtime-identity-storage` README. Update source examples in `docs/readme/`, then run `readme-standards render --root . --write` from the package directory and review the diff. Required headings and generated blocks come from package-guide-v1.

---

## Governance

### Ownership and Decision Making

Changes to `tba-runtime-identity-storage` follow the maintainer review process of [tigrbl/tigrbl_auth](https://github.com/tigrbl/tigrbl_auth) and its contribution guide. Author attribution remains in the [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-runtime-identity-storage/pyproject.toml); this README does not assign new publishing or administrative authority.

### Standards and Policies

`tba-runtime-identity-storage` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `030-storage-runtime` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

### Lifecycle and Migration

The `tba-runtime-identity-storage` source version is `0.4.0.dev3`. This change standardizes documentation and adds a development-only gate; it does not publish a new runtime version or declare a previously unpublished package released. Preserve explicit deprecation and replacement instructions where present.

---

## License and Attribution

### License

<!-- readme-standards:begin license -->
Licensed under `Apache-2.0`. See [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-runtime-identity-storage/LICENSE).
<!-- readme-standards:end license -->

### Notices

<!-- readme-standards:begin notices -->
See [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-runtime-identity-storage/NOTICE) for attribution.
<!-- readme-standards:end notices -->
