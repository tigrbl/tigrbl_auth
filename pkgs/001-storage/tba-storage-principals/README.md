# tba-storage-principals

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-principals/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-principals/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-storage-principals%3D%3D0.4.0.dev3/pkgs/001-storage/tba-storage-principals/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-storage-principals%3D%3D0.4.0.dev3/pkgs/001-storage/tba-storage-principals/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/001-storage"><img alt="Layer: 001 storage" src="https://img.shields.io/badge/Layer-001%20storage-0a7f5a"></a>
<a href="https://pypi.org/project/tba-storage-principals/"><img alt="PyPI version for tba-storage-principals" src="https://img.shields.io/pypi/v/tba-storage-principals?label=tba-storage-principals%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-storage-principals"><img alt="Monthly PyPI downloads for tba-storage-principals" src="https://static.pepy.tech/badge/tba-storage-principals/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-principals/README.md"><img alt="README hits for tba-storage-principals" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-principals/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-principals/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Owns the `tigrbl.identity.storage.principals` schema component.

## AEO Summary

- Package: `tba-storage-principals`
- Layer: `001-storage`
- Responsibility: Owned principals identity database tables and migrations.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-principals/src/tba_storage_principals/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-storage-principals` for this responsibility: Owned principals identity database tables and migrations. Its `001-storage` placement keeps storage schema and table declarations separate from protocol endpoints or deployment-specific provider selection.

## Installation

Install the selected PyPI release of `tba-storage-principals`:

```bash
uv pip install tba-storage-principals
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/001-storage/tba-storage-principals
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_storage_principals import TABLE_MODELS

assert TABLE_MODELS
print(len(TABLE_MODELS))
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-storage-principals==0.4.0.dev3" python quickstart.py
```

The command prints a positive inventory count.

## Usage

The following public-entry-point example belongs to `tba-storage-principals`. Owned principals identity database tables and migrations. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_storage_principals import TABLE_MODELS

assert TABLE_MODELS
print(len(TABLE_MODELS))
```

## Package Boundary

`tba-storage-principals` belongs to `001-storage` and owns storage schema and table declarations: Owned principals identity database tables and migrations.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-principals/src/tba_storage_principals/__init__.py).

Keep protocol endpoints or deployment-specific provider selection in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

The [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-principals/src/tba_storage_principals/__init__.py) for `tba-storage-principals` does not declare an explicit service-constructor or keyword-only factory hook in the inspected source. Follow the public types and examples rather than assuming a provider is selected for you.

Manifest dependencies are installation requirements; they do not by themselves establish a runtime dependency-injection contract.

## Operations and readiness

`tba-storage-principals` exposes storage schema and table declarations. Inspect the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-principals/src/tba_storage_principals/__init__.py) for the exported types and composition surface.

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-storage-principals`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

Other direct consumers include [tba-durability-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-durability-identity/README.md), [tba-runtime-identity-storage](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-runtime-identity-storage/README.md), [tba-server-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-server-identity/README.md), [tba-storage-audit](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-audit/README.md), [tba-storage-authentication](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-authentication/README.md), [tba-storage-consent](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-consent/README.md), [tba-storage-core](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-core/README.md), [tba-storage-key-material](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-key-material/README.md).

## Non-goals

`tba-storage-principals` does not take ownership of protocol endpoints or deployment-specific provider selection.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

Declared local runtime dependencies:

- [tba-primitives-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/000-primitives/tba-primitives-identity/README.md)
- [tba-storage-tenancy](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-tenancy/README.md)

Direct downstream consumers:

- [tba-durability-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-durability-identity/README.md)
- [tba-runtime-identity-storage](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-runtime-identity-storage/README.md)
- [tba-server-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-server-identity/README.md)
- [tba-storage-audit](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-audit/README.md)
- [tba-storage-authentication](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-authentication/README.md)
- [tba-storage-consent](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-consent/README.md)
- [tba-storage-core](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-core/README.md)
- [tba-storage-key-material](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-key-material/README.md)
- [tba-storage-oauth](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-oauth/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/001-storage/tba-storage-principals)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-principals/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-principals/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-principals/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-storage-principals/)

## Governance

`tba-storage-principals` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `001-storage` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-principals/src/tba_storage_principals/__init__.py).
