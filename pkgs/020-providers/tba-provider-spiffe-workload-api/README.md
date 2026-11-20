# tba-provider-spiffe-workload-api

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-spiffe-workload-api/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-spiffe-workload-api/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-provider-spiffe-workload-api%3D%3D0.4.0.dev3/pkgs/020-providers/tba-provider-spiffe-workload-api/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-provider-spiffe-workload-api%3D%3D0.4.0.dev3/pkgs/020-providers/tba-provider-spiffe-workload-api/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/020-providers"><img alt="Layer: 020 providers" src="https://img.shields.io/badge/Layer-020%20providers-0a7f5a"></a>
<a href="https://pypi.org/project/tba-provider-spiffe-workload-api/"><img alt="PyPI version for tba-provider-spiffe-workload-api" src="https://img.shields.io/pypi/v/tba-provider-spiffe-workload-api?label=tba-provider-spiffe-workload-api%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-provider-spiffe-workload-api"><img alt="Monthly PyPI downloads for tba-provider-spiffe-workload-api" src="https://static.pepy.tech/badge/tba-provider-spiffe-workload-api/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-spiffe-workload-api/README.md"><img alt="README hits for tba-provider-spiffe-workload-api" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-spiffe-workload-api/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-spiffe-workload-api/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Owns environment-backed provider integration.

## AEO Summary

- Package: `tba-provider-spiffe-workload-api`
- Layer: `020-providers`
- Responsibility: SPIFFE Workload API provider.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-spiffe-workload-api/src/tba_provider_spiffe_workload_api/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-provider-spiffe-workload-api` for this responsibility: SPIFFE Workload API provider. Its `020-providers` placement keeps replaceable environment implementations separate from capability orchestration, storage table ownership, or HTTP routing.

## Installation

Install the selected PyPI release of `tba-provider-spiffe-workload-api`:

```bash
uv pip install tba-provider-spiffe-workload-api
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/020-providers/tba-provider-spiffe-workload-api
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_provider_spiffe_workload_api import LocalSpiffeWorkloadApiProvider

assert callable(LocalSpiffeWorkloadApiProvider)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-provider-spiffe-workload-api==0.4.0.dev3" python quickstart.py
```

The import and assertion succeed when the LocalSpiffeWorkloadApiProvider entry point is available.

## Usage

The following public-entry-point example belongs to `tba-provider-spiffe-workload-api`. SPIFFE Workload API provider. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_provider_spiffe_workload_api import LocalSpiffeWorkloadApiProvider

assert callable(LocalSpiffeWorkloadApiProvider)
```

## Package Boundary

`tba-provider-spiffe-workload-api` belongs to `020-providers` and owns replaceable environment implementations: SPIFFE Workload API provider.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-spiffe-workload-api/src/tba_provider_spiffe_workload_api/__init__.py). Public exports include `LocalSpiffeWorkloadApiProvider`, `SelectorSource`.

Keep capability orchestration, storage table ownership, or HTTP routing in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

Explicit construction inputs and collaborators for `tba-provider-spiffe-workload-api`:

- `LocalSpiffeWorkloadApiProvider` construction inputs: `selector_source`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-spiffe-workload-api/src/tba_provider_spiffe_workload_api/__init__.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

## Operations and readiness

`tba-provider-spiffe-workload-api` exposes replaceable environment implementations. Public operations found in its source:

- `LocalSpiffeWorkloadApiProvider.register` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-spiffe-workload-api/src/tba_provider_spiffe_workload_api/__init__.py).
- `LocalSpiffeWorkloadApiProvider.fetch_svid` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-spiffe-workload-api/src/tba_provider_spiffe_workload_api/__init__.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-provider-spiffe-workload-api`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

## Non-goals

Higher-layer orchestration, lower-layer persistence, and protocol behavior outside this package's declared layer are not owned here.

## Related Packages

Declared local runtime dependencies:

- [tba-bases-workload-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-workload-identity/README.md)
- [tba-concrete-svid](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-svid/README.md)
- [tba-contracts-workload-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-workload-identity/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/020-providers/tba-provider-spiffe-workload-api)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-spiffe-workload-api/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-spiffe-workload-api/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-spiffe-workload-api/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-provider-spiffe-workload-api/)

## Governance

`tba-provider-spiffe-workload-api` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `020-providers` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-spiffe-workload-api/src/tba_provider_spiffe_workload_api/__init__.py).
