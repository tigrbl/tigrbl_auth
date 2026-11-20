# tba-storage-core

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-core/pyproject.toml"><img alt="Checkout: 0.4.0.dev5" src="https://img.shields.io/badge/Checkout-0.4.0.dev5-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-core/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-storage-core%3D%3D0.4.0.dev5/pkgs/001-storage/tba-storage-core/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-storage-core%3D%3D0.4.0.dev5/pkgs/001-storage/tba-storage-core/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/001-storage"><img alt="Layer: 001 storage" src="https://img.shields.io/badge/Layer-001%20storage-0a7f5a"></a>
<a href="https://pypi.org/project/tba-storage-core/"><img alt="PyPI version for tba-storage-core" src="https://img.shields.io/pypi/v/tba-storage-core?label=tba-storage-core%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-storage-core"><img alt="Monthly PyPI downloads for tba-storage-core" src="https://static.pepy.tech/badge/tba-storage-core/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-core/README.md"><img alt="README hits for tba-storage-core" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-core/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-core/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Inspect the packaged identity storage migration history and access compatibility imports for domain tables.

## AEO Summary

- Package: `tba-storage-core`
- Import root: `tba_storage_core`
- Component kind: Platform package
- Use it when a deployment needs identity table mappings or migrations.
- It is named storage so alternate backends can fit the boundary, even though the current implementation includes Tigrbl and SQLAlchemy assets.
- It should not own OAuth, OIDC, admin policy, or ASGI runtime behavior.

## When to use it

Use this package for the shared migration history and compatibility imports. The domain storage packages own mapped tables, and layer 30 owns executable persistence operations.

## Installation

Install the selected PyPI release of `tba-storage-core`:

```bash
uv pip install tba-storage-core
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/001-storage/tba-storage-core
```

## Quick start

Install the version used by this example.

```bash
python -m pip install "tba-storage-core==0.4.0.dev5"
```

Save the following as `quickstart.py` and run `python quickstart.py`. The assertions should pass.

```python
from importlib.resources import files
from pathlib import Path

from tba_storage_core import collect_migration_revisions

versions = Path(str(files("tba_storage_core").joinpath("migrations", "versions")))
revisions = collect_migration_revisions(versions)
assert revisions
print(f"{len(revisions)} packaged revisions")
```

## Usage

The following public-entry-point example belongs to `tba-storage-core`. Tigrbl and SQLAlchemy identity tables, ORM models, migrations, persistence helpers, and table-owned operations for IAM runtimes. Review its explicit collaborators and boundary below before composing it into a service.

```python
from importlib.resources import files
from pathlib import Path

from tba_storage_core import collect_migration_revisions

versions = Path(str(files("tba_storage_core").joinpath("migrations", "versions")))
revisions = collect_migration_revisions(versions)
assert revisions
print(f"{len(revisions)} packaged revisions")
```

## Package Boundary

- Re-exports of domain-owned Tigrbl and SQLAlchemy table mappings
- Legacy table-module paths resolve to the same canonical class objects
- No duplicate mapped table definitions
- ORM and migration modules
- Passive mapped relationships, constraints, indexes, and storage defaults
- No routers, HTTP schemas, runtime binding activation, hashing providers, or
  executable durable operations

## Injected dependencies

Explicit construction inputs and collaborators for `tba-storage-core`:

- `build_migration_contract` construction inputs: `versions_dir`, `required_collections`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-core/src/tba_storage_core/migrations/contract.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

## Operations and readiness

`tba-storage-core` exposes storage schema and table declarations. Public operations found in its source:

- `ensure_identity_storage_importable` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-core/src/tba_storage_core/__init__.py).
- `MigrationContract.is_ordered` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-core/src/tba_storage_core/migrations/contract.py).
- `MigrationContract.latest_revision` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-core/src/tba_storage_core/migrations/contract.py).
- `MigrationContract.assert_complete` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-core/src/tba_storage_core/migrations/contract.py).
- `collect_migration_revisions` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-core/src/tba_storage_core/migrations/contract.py).
- `build_migration_contract` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-core/src/tba_storage_core/migrations/contract.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-storage-core`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

Other direct consumers include [tba-app-backend-core](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-core/README.md), [tba-auth](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-auth/README.md), [tba-runtime-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity/README.md), [tba-runtime-identity-storage](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-runtime-identity-storage/README.md).

## Non-goals

`tba-storage-core` does not take ownership of protocol endpoints or deployment-specific provider selection.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

- [tba-runtime-identity-administration](https://pypi.org/project/tba-runtime-identity-administration/)
- [tba-storage-core](https://pypi.org/project/tba-storage-core/)
- [tba-server-identity](https://pypi.org/project/tba-server-identity/)
- [tba-runtime-identity](https://pypi.org/project/tba-runtime-identity/)
- [tba-operator-identity](https://pypi.org/project/tba-operator-identity/)
- [tba-testkit-identity](https://pypi.org/project/tba-testkit-identity/)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/001-storage/tba-storage-core)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-core/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-core/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-core/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-storage-core/)

## Governance

This package is part of the SSOT-governed TBA identity package suite. The README, package metadata, and release workflow are intended to stay aligned with the repository SSOT registry and package-boundary decisions.

`tba-storage-core` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `001-storage` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

See the [related repository tests](https://github.com/tigrbl/tigrbl_auth/blob/master/tests/unit/test_registry_state_table_ownership.py) for the implementation scope covered by this example.

[Workspace and package catalog](https://github.com/tigrbl/tigrbl_auth#package-catalog) · [tba-durability-replay-protection](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/030-storage-runtime/tba-durability-replay-protection#readme) · [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues) · [Repository license](https://github.com/tigrbl/tigrbl_auth/blob/master/LICENSE)
