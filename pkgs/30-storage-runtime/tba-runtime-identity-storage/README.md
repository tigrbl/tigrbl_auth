# tba-runtime-identity-storage

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/30-storage-runtime/tba-runtime-identity-storage/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/30-storage-runtime/tba-runtime-identity-storage/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-runtime-identity-storage%3D%3D0.4.0.dev3/pkgs/30-storage-runtime/tba-runtime-identity-storage/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-runtime-identity-storage%3D%3D0.4.0.dev3/pkgs/30-storage-runtime/tba-runtime-identity-storage/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/30-storage-runtime"><img alt="Layer: 30 storage runtime" src="https://img.shields.io/badge/Layer-30%20storage%20runtime-0a7f5a"></a>
<a href="https://pypi.org/project/tba-runtime-identity-storage/"><img alt="PyPI version for tba-runtime-identity-storage" src="https://img.shields.io/pypi/v/tba-runtime-identity-storage?label=tba-runtime-identity-storage%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-runtime-identity-storage"><img alt="Monthly PyPI downloads for tba-runtime-identity-storage" src="https://static.pepy.tech/badge/tba-runtime-identity-storage/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/30-storage-runtime/tba-runtime-identity-storage/README.md"><img alt="README hits for tba-runtime-identity-storage" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/30-storage-runtime/tba-runtime-identity-storage/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/30-storage-runtime/tba-runtime-identity-storage/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

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

## AEO Summary

- Package: `tba-runtime-identity-storage`
- Layer: `30-storage-runtime`
- Responsibility: Runtime execution helpers for TBA identity storage migrations and provider-bound storage lifecycle wiring.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/30-storage-runtime/tba-runtime-identity-storage/src/tba_runtime_identity_storage/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-runtime-identity-storage` for this responsibility: Runtime execution helpers for TBA identity storage migrations and provider-bound storage lifecycle wiring. Its `30-storage-runtime` placement keeps storage-backed runtime adapters separate from protocol wire definitions or standalone application hosting.

## Installation

Install the selected PyPI release of `tba-runtime-identity-storage`:

```bash
uv pip install tba-runtime-identity-storage
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/30-storage-runtime/tba-runtime-identity-storage
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_runtime_identity_storage import initializeIdentityRuntimeTables

assert callable(initializeIdentityRuntimeTables)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-runtime-identity-storage==0.4.0.dev3" python quickstart.py
```

The import and assertion succeed when the initializeIdentityRuntimeTables entry point is available.

## Usage

The following public-entry-point example belongs to `tba-runtime-identity-storage`. Runtime execution helpers for TBA identity storage migrations and provider-bound storage lifecycle wiring. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_runtime_identity_storage import initializeIdentityRuntimeTables

assert callable(initializeIdentityRuntimeTables)
```

## Package Boundary

`tba-runtime-identity-storage` belongs to `30-storage-runtime` and owns storage-backed runtime adapters: Runtime execution helpers for TBA identity storage migrations and provider-bound storage lifecycle wiring.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/30-storage-runtime/tba-runtime-identity-storage/src/tba_runtime_identity_storage/__init__.py). Public exports include `RUNTIME_TABLES`, `RUNTIME_TABLE_BY_NAME`, `RUNTIME_TABLE_SPECS`, `RUNTIME_TABLE_SPEC_BY_NAME`, `RUNTIME_OPERATION_BY_ALIAS`, `initializeIdentityRuntimeTables`, `initialize_identity_runtime_tables`, `DURABLE_RUNTIME_TABLE_SPECS`, `MigrationContract`, `MigrationRevision`, `MigrationResult`, `SchemaVerification`.

Keep protocol wire definitions or standalone application hosting in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

Explicit construction inputs and collaborators for `tba-runtime-identity-storage`:

- `stash_security_providers` construction inputs: `key_provider`, `signer`, `verifier`, `jwt_coder`, `clock`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/30-storage-runtime/tba-runtime-identity-storage/src/tba_runtime_identity_storage/security_context.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

## Operations and readiness

`tba-runtime-identity-storage` exposes storage-backed runtime adapters. Public operations found in its source:

- `initializeIdentityRuntimeTables` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/30-storage-runtime/tba-runtime-identity-storage/src/tba_runtime_identity_storage/initialize.py).
- `iter_migration_modules` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/30-storage-runtime/tba-runtime-identity-storage/src/tba_runtime_identity_storage/migrations/runtime.py).
- `expected_table_names` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/30-storage-runtime/tba-runtime-identity-storage/src/tba_runtime_identity_storage/migrations/runtime.py).
- `verify_schema_sync` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/30-storage-runtime/tba-runtime-identity-storage/src/tba_runtime_identity_storage/migrations/runtime.py).
- `column_names_sync` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/30-storage-runtime/tba-runtime-identity-storage/src/tba_runtime_identity_storage/migrations/runtime.py).
- `apply_all_async` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/30-storage-runtime/tba-runtime-identity-storage/src/tba_runtime_identity_storage/migrations/runtime.py).
- `downgrade_one_async` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/30-storage-runtime/tba-runtime-identity-storage/src/tba_runtime_identity_storage/migrations/runtime.py).
- `verify_schema_async` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/30-storage-runtime/tba-runtime-identity-storage/src/tba_runtime_identity_storage/migrations/runtime.py).
- `column_names_async` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/30-storage-runtime/tba-runtime-identity-storage/src/tba_runtime_identity_storage/migrations/runtime.py).
- `make_attestation_appraisal_recorder` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/30-storage-runtime/tba-runtime-identity-storage/src/tba_runtime_identity_storage/ops/attestation.py).
- `stash_security_providers` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/30-storage-runtime/tba-runtime-identity-storage/src/tba_runtime_identity_storage/security_context.py).
- `run_async` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/30-storage-runtime/tba-runtime-identity-storage/src/tba_runtime_identity_storage/sync.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-runtime-identity-storage`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

Other direct consumers include [tba-app-backend-core](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-core/README.md), [tba-auth](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/70-facade/tba-auth/README.md), [tba-cli-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-cli-identity/README.md), [tba-runtime-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-runtime-identity/README.md), [tba-server-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-server-identity/README.md).

## Non-goals

`tba-runtime-identity-storage` does not take ownership of protocol wire definitions or standalone application hosting.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

Declared local runtime dependencies:

- [tba-contracts-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-identity/README.md)
- [tba-contracts-security-trust](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-security-trust/README.md)
- [tba-durability-attestation](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/30-storage-runtime/tba-durability-attestation/README.md)
- [tba-durability-audit](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/30-storage-runtime/tba-durability-audit/README.md)
- [tba-durability-authorization-policy](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/30-storage-runtime/tba-durability-authorization-policy/README.md)
- [tba-durability-consent](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/30-storage-runtime/tba-durability-consent/README.md)
- [tba-durability-delegation](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/30-storage-runtime/tba-durability-delegation/README.md)
- [tba-durability-digital-credential](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/30-storage-runtime/tba-durability-digital-credential/README.md)
- [tba-durability-gnap-state](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/30-storage-runtime/tba-durability-gnap-state/README.md)
- [tba-durability-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/30-storage-runtime/tba-durability-identity/README.md)
- [tba-durability-key-material](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/30-storage-runtime/tba-durability-key-material/README.md)
- [tba-durability-oauth-state](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/30-storage-runtime/tba-durability-oauth-state/README.md)
- [tba-durability-oidc-state](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/30-storage-runtime/tba-durability-oidc-state/README.md)
- [tba-durability-presentation](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/30-storage-runtime/tba-durability-presentation/README.md)
- [tba-durability-replay-protection](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/30-storage-runtime/tba-durability-replay-protection/README.md)
- [tba-durability-security-event](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/30-storage-runtime/tba-durability-security-event/README.md)
- [tba-durability-session](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/30-storage-runtime/tba-durability-session/README.md)
- [tba-durability-token](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/30-storage-runtime/tba-durability-token/README.md)
- [tba-durability-webauthn](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/30-storage-runtime/tba-durability-webauthn/README.md)
- [tba-durability-workload-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/30-storage-runtime/tba-durability-workload-identity/README.md)
- [tba-primitives-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/00-primitives/tba-primitives-identity/README.md)
- [tba-provider-security-authorization-provenance-builder](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-security-authorization-provenance-builder/README.md)
- [tba-storage-authorization-policy](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/01-storage/tba-storage-authorization-policy/README.md)
- [tba-storage-consent](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/01-storage/tba-storage-consent/README.md)
- [tba-storage-core](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/01-storage/tba-storage-core/README.md)
- [tba-storage-key-material](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/01-storage/tba-storage-key-material/README.md)
- [tba-storage-oauth](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/01-storage/tba-storage-oauth/README.md)
- [tba-storage-operator](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/01-storage/tba-storage-operator/README.md)
- [tba-storage-principals](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/01-storage/tba-storage-principals/README.md)
- [tba-storage-tenancy](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/01-storage/tba-storage-tenancy/README.md)
- [tba-storage-token](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/01-storage/tba-storage-token/README.md)

Direct downstream consumers:

- [tba-app-backend-core](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-core/README.md)
- [tba-auth](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/70-facade/tba-auth/README.md)
- [tba-cli-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-cli-identity/README.md)
- [tba-runtime-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-runtime-identity/README.md)
- [tba-server-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-server-identity/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/30-storage-runtime/tba-runtime-identity-storage)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/30-storage-runtime/tba-runtime-identity-storage/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/30-storage-runtime/tba-runtime-identity-storage/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/30-storage-runtime/tba-runtime-identity-storage/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-runtime-identity-storage/)

## Governance

`tba-runtime-identity-storage` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `30-storage-runtime` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/30-storage-runtime/tba-runtime-identity-storage/src/tba_runtime_identity_storage/__init__.py).
