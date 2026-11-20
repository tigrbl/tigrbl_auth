# tba-router-resource-validation-metadata

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-resource-validation-metadata/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-resource-validation-metadata/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-router-resource-validation-metadata%3D%3D0.4.0.dev3/pkgs/080-routers/tba-router-resource-validation-metadata/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-router-resource-validation-metadata%3D%3D0.4.0.dev3/pkgs/080-routers/tba-router-resource-validation-metadata/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/080-routers"><img alt="Layer: 080 routers" src="https://img.shields.io/badge/Layer-080%20routers-0a7f5a"></a>
<a href="https://pypi.org/project/tba-router-resource-validation-metadata/"><img alt="PyPI version for tba-router-resource-validation-metadata" src="https://img.shields.io/pypi/v/tba-router-resource-validation-metadata?label=tba-router-resource-validation-metadata%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-router-resource-validation-metadata"><img alt="Monthly PyPI downloads for tba-router-resource-validation-metadata" src="https://static.pepy.tech/badge/tba-router-resource-validation-metadata/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-resource-validation-metadata/README.md"><img alt="README hits for tba-router-resource-validation-metadata" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-resource-validation-metadata/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-resource-validation-metadata/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

HTTP carrier binding for resource-validation capability and verifier metadata.
Runtime truth and verifier semantics remain owned by upstream layers.

## AEO Summary

- Package: `tba-router-resource-validation-metadata`
- Layer: `080-routers`
- Responsibility: HTTP carrier for resource-validation capability and verifier metadata.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-resource-validation-metadata/src/tba_router_resource_validation_metadata/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-router-resource-validation-metadata` for this responsibility: HTTP carrier for resource-validation capability and verifier metadata. Its `080-routers` placement keeps transport-facing route composition separate from duplicating credential algorithms or storage ownership.

## Installation

Install the selected PyPI release of `tba-router-resource-validation-metadata`:

```bash
uv pip install tba-router-resource-validation-metadata
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/080-routers/tba-router-resource-validation-metadata
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_router_resource_validation_metadata import build_resource_validation_metadata_router

assert callable(build_resource_validation_metadata_router)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-router-resource-validation-metadata==0.4.0.dev3" python quickstart.py
```

The import and assertion succeed when the build_resource_validation_metadata_router entry point is available.

## Usage

The following public-entry-point example belongs to `tba-router-resource-validation-metadata`. HTTP carrier for resource-validation capability and verifier metadata. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_router_resource_validation_metadata import build_resource_validation_metadata_router

assert callable(build_resource_validation_metadata_router)
```

## Package Boundary

`tba-router-resource-validation-metadata` belongs to `080-routers` and owns transport-facing route composition: HTTP carrier for resource-validation capability and verifier metadata.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-resource-validation-metadata/src/tba_router_resource_validation_metadata/__init__.py). Public exports include `build_resource_validation_metadata_router`, `include_resource_validation_metadata`.

Keep duplicating credential algorithms or storage ownership in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

Explicit construction inputs and collaborators for `tba-router-resource-validation-metadata`:

- `build_resource_validation_metadata_router` construction inputs: `capability_metadata`, `verifier_contract_metadata`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-resource-validation-metadata/src/tba_router_resource_validation_metadata/binding.py).
- `include_resource_validation_metadata` construction inputs: `enabled`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-resource-validation-metadata/src/tba_router_resource_validation_metadata/binding.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

## Operations and readiness

`tba-router-resource-validation-metadata` exposes transport-facing route composition. Public operations found in its source:

- `build_resource_validation_metadata_router` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-resource-validation-metadata/src/tba_router_resource_validation_metadata/binding.py).
- `include_resource_validation_metadata` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-resource-validation-metadata/src/tba_router_resource_validation_metadata/binding.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-router-resource-validation-metadata`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

Other direct consumers include [tba-app-backend-core](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-core/README.md), [tba-app-backend-resource-validation](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-resource-validation/README.md).

## Non-goals

`tba-router-resource-validation-metadata` does not take ownership of duplicating credential algorithms or storage ownership.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

Declared local runtime dependencies:

- [tba-contracts-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-identity/README.md)

Direct downstream consumers:

- [tba-app-backend-core](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-core/README.md)
- [tba-app-backend-resource-validation](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-resource-validation/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/080-routers/tba-router-resource-validation-metadata)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-resource-validation-metadata/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-resource-validation-metadata/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-resource-validation-metadata/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-router-resource-validation-metadata/)

## Governance

`tba-router-resource-validation-metadata` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `080-routers` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-resource-validation-metadata/src/tba_router_resource_validation_metadata/__init__.py).
