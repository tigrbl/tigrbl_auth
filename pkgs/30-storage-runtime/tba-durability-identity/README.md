# tba-durability-identity

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/30-storage-runtime/tba-durability-identity/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/30-storage-runtime/tba-durability-identity/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-durability-identity%3D%3D0.4.0.dev3/pkgs/30-storage-runtime/tba-durability-identity/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-durability-identity%3D%3D0.4.0.dev3/pkgs/30-storage-runtime/tba-durability-identity/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/30-storage-runtime"><img alt="Layer: 30 storage runtime" src="https://img.shields.io/badge/Layer-30%20storage%20runtime-0a7f5a"></a>
<a href="https://pypi.org/project/tba-durability-identity/"><img alt="PyPI version for tba-durability-identity" src="https://img.shields.io/pypi/v/tba-durability-identity?label=tba-durability-identity%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-durability-identity"><img alt="Monthly PyPI downloads for tba-durability-identity" src="https://static.pepy.tech/badge/tba-durability-identity/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/30-storage-runtime/tba-durability-identity/README.md"><img alt="README hits for tba-durability-identity" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/30-storage-runtime/tba-durability-identity/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/30-storage-runtime/tba-durability-identity/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Carrier-neutral layer-30 durable operations and derived table specifications.

## AEO Summary

- Package: `tba-durability-identity`
- Layer: `30-storage-runtime`
- Responsibility: Carrier-neutral layer-30 durable table operations.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/30-storage-runtime/tba-durability-identity/src/tba_durability_identity/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-durability-identity` for this responsibility: Carrier-neutral layer-30 durable table operations. Its `30-storage-runtime` placement keeps storage-backed runtime adapters separate from protocol wire definitions or standalone application hosting.

## Installation

Install the selected PyPI release of `tba-durability-identity`:

```bash
uv pip install tba-durability-identity
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/30-storage-runtime/tba-durability-identity
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_durability_identity import RUNTIME_TABLE_SPECS

assert RUNTIME_TABLE_SPECS
print(len(RUNTIME_TABLE_SPECS))
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-durability-identity==0.4.0.dev3" python quickstart.py
```

The command prints a positive inventory count.

## Usage

The following public-entry-point example belongs to `tba-durability-identity`. Carrier-neutral layer-30 durable table operations. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_durability_identity import RUNTIME_TABLE_SPECS

assert RUNTIME_TABLE_SPECS
print(len(RUNTIME_TABLE_SPECS))
```

## Package Boundary

`tba-durability-identity` belongs to `30-storage-runtime` and owns storage-backed runtime adapters: Carrier-neutral layer-30 durable table operations.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/30-storage-runtime/tba-durability-identity/src/tba_durability_identity/__init__.py).

Keep protocol wire definitions or standalone application hosting in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

The [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/30-storage-runtime/tba-durability-identity/src/tba_durability_identity/__init__.py) for `tba-durability-identity` does not declare an explicit service-constructor or keyword-only factory hook in the inspected source. Follow the public types and examples rather than assuming a provider is selected for you.

Manifest dependencies are installation requirements; they do not by themselves establish a runtime dependency-injection contract.

## Operations and readiness

`tba-durability-identity` exposes storage-backed runtime adapters. Inspect the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/30-storage-runtime/tba-durability-identity/src/tba_durability_identity/__init__.py) for the exported types and composition surface.

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-durability-identity`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

Other direct consumers include [tba-runtime-identity-administration](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-runtime-identity-administration/README.md), [tba-runtime-identity-storage](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/30-storage-runtime/tba-runtime-identity-storage/README.md).

## Non-goals

`tba-durability-identity` does not take ownership of protocol wire definitions or standalone application hosting.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

Declared local runtime dependencies:

- [tba-bases-replay](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-replay/README.md)
- [tba-contracts-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-identity/README.md)
- [tba-contracts-security-trust](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-security-trust/README.md)
- [tba-primitives-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/00-primitives/tba-primitives-identity/README.md)
- [tba-storage-authentication](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/01-storage/tba-storage-authentication/README.md)
- [tba-storage-federation](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/01-storage/tba-storage-federation/README.md)
- [tba-storage-oauth](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/01-storage/tba-storage-oauth/README.md)
- [tba-storage-principals](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/01-storage/tba-storage-principals/README.md)

Direct downstream consumers:

- [tba-runtime-identity-administration](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-runtime-identity-administration/README.md)
- [tba-runtime-identity-storage](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/30-storage-runtime/tba-runtime-identity-storage/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/30-storage-runtime/tba-durability-identity)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/30-storage-runtime/tba-durability-identity/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/30-storage-runtime/tba-durability-identity/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/30-storage-runtime/tba-durability-identity/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-durability-identity/)

## Governance

`tba-durability-identity` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `30-storage-runtime` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/30-storage-runtime/tba-durability-identity/src/tba_durability_identity/__init__.py).
