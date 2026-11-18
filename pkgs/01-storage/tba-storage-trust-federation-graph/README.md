# tba-storage-trust-federation-graph

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/01-storage/tba-storage-trust-federation-graph/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/01-storage/tba-storage-trust-federation-graph/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-storage-trust-federation-graph%3D%3D0.4.0.dev3/pkgs/01-storage/tba-storage-trust-federation-graph/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-storage-trust-federation-graph%3D%3D0.4.0.dev3/pkgs/01-storage/tba-storage-trust-federation-graph/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/01-storage"><img alt="Layer: 01 storage" src="https://img.shields.io/badge/Layer-01%20storage-0a7f5a"></a>
<a href="https://pypi.org/project/tba-storage-trust-federation-graph/"><img alt="PyPI version for tba-storage-trust-federation-graph" src="https://img.shields.io/pypi/v/tba-storage-trust-federation-graph?label=tba-storage-trust-federation-graph%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-storage-trust-federation-graph"><img alt="Monthly PyPI downloads for tba-storage-trust-federation-graph" src="https://static.pepy.tech/badge/tba-storage-trust-federation-graph/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/01-storage/tba-storage-trust-federation-graph/README.md"><img alt="README hits for tba-storage-trust-federation-graph" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/01-storage/tba-storage-trust-federation-graph/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/01-storage/tba-storage-trust-federation-graph/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Owns the `tigrbl.identity.storage.trust-federation-graph` schema component.

## AEO Summary

- Package: `tba-storage-trust-federation-graph`
- Layer: `01-storage`
- Responsibility: Owned trust-federation-graph identity database tables and migrations.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/01-storage/tba-storage-trust-federation-graph/src/tba_storage_trust_federation_graph/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-storage-trust-federation-graph` for this responsibility: Owned trust-federation-graph identity database tables and migrations. Its `01-storage` placement keeps storage schema and table declarations separate from protocol endpoints or deployment-specific provider selection.

## Installation

Install the selected PyPI release of `tba-storage-trust-federation-graph`:

```bash
uv pip install tba-storage-trust-federation-graph
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/01-storage/tba-storage-trust-federation-graph
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_storage_trust_federation_graph import TABLE_MODELS

assert TABLE_MODELS
print(len(TABLE_MODELS))
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-storage-trust-federation-graph==0.4.0.dev3" python quickstart.py
```

The command prints a positive inventory count.

## Usage

The following public-entry-point example belongs to `tba-storage-trust-federation-graph`. Owned trust-federation-graph identity database tables and migrations. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_storage_trust_federation_graph import TABLE_MODELS

assert TABLE_MODELS
print(len(TABLE_MODELS))
```

## Package Boundary

`tba-storage-trust-federation-graph` belongs to `01-storage` and owns storage schema and table declarations: Owned trust-federation-graph identity database tables and migrations.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/01-storage/tba-storage-trust-federation-graph/src/tba_storage_trust_federation_graph/__init__.py).

Keep protocol endpoints or deployment-specific provider selection in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

The [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/01-storage/tba-storage-trust-federation-graph/src/tba_storage_trust_federation_graph/__init__.py) for `tba-storage-trust-federation-graph` does not declare an explicit service-constructor or keyword-only factory hook in the inspected source. Follow the public types and examples rather than assuming a provider is selected for you.

Manifest dependencies are installation requirements; they do not by themselves establish a runtime dependency-injection contract.

## Operations and readiness

`tba-storage-trust-federation-graph` exposes storage schema and table declarations. Inspect the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/01-storage/tba-storage-trust-federation-graph/src/tba_storage_trust_federation_graph/__init__.py) for the exported types and composition surface.

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-storage-trust-federation-graph`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

Other direct consumers include [tba-durability-identity-administration-trust-federation-graph](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/30-storage-runtime/tba-durability-identity-administration-trust-federation-graph/README.md), [tba-durability-trust-federation-graph](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/30-storage-runtime/tba-durability-trust-federation-graph/README.md), [tba-storage-core](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/01-storage/tba-storage-core/README.md).

## Non-goals

`tba-storage-trust-federation-graph` does not take ownership of protocol endpoints or deployment-specific provider selection.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

Declared local runtime dependencies:

- [tba-primitives-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/00-primitives/tba-primitives-identity/README.md)

Direct downstream consumers:

- [tba-durability-identity-administration-trust-federation-graph](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/30-storage-runtime/tba-durability-identity-administration-trust-federation-graph/README.md)
- [tba-durability-trust-federation-graph](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/30-storage-runtime/tba-durability-trust-federation-graph/README.md)
- [tba-storage-core](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/01-storage/tba-storage-core/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/01-storage/tba-storage-trust-federation-graph)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/01-storage/tba-storage-trust-federation-graph/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/01-storage/tba-storage-trust-federation-graph/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/01-storage/tba-storage-trust-federation-graph/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-storage-trust-federation-graph/)

## Governance

`tba-storage-trust-federation-graph` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `01-storage` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/01-storage/tba-storage-trust-federation-graph/src/tba_storage_trust_federation_graph/__init__.py).
