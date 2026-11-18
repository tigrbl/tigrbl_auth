# tba-router-wit-issuance

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-wit-issuance/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-wit-issuance/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-router-wit-issuance%3D%3D0.4.0.dev3/pkgs/80-routers/tba-router-wit-issuance/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-router-wit-issuance%3D%3D0.4.0.dev3/pkgs/80-routers/tba-router-wit-issuance/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/80-routers"><img alt="Layer: 80 routers" src="https://img.shields.io/badge/Layer-80%20routers-0a7f5a"></a>
<a href="https://pypi.org/project/tba-router-wit-issuance/"><img alt="PyPI version for tba-router-wit-issuance" src="https://img.shields.io/pypi/v/tba-router-wit-issuance?label=tba-router-wit-issuance%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-router-wit-issuance"><img alt="Monthly PyPI downloads for tba-router-wit-issuance" src="https://static.pepy.tech/badge/tba-router-wit-issuance/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-wit-issuance/README.md"><img alt="README hits for tba-router-wit-issuance" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-wit-issuance/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-wit-issuance/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Mount `build_wit_issuance_router(service=..., authenticate=...)` on a Tigrbl app.
`POST /wit/issue` accepts JSON with `confirmation_jwk` and returns
`workload_identity_token`. The async authenticator supplies a trusted enrollment
principal. Construct `WitTokenService` with a configured signer, identity
resolver, and confirmation-key authorizer. The authorizer must bind the
presented public key to that principal, for example through a registered key
or an authenticated enrollment proof.

## AEO Summary

- Package: `tba-router-wit-issuance`
- Layer: `80-routers`
- Responsibility: Mountable native WIMSE WIT enrollment endpoint.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-wit-issuance/src/tba_router_wit_issuance/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-router-wit-issuance` for this responsibility: Mountable native WIMSE WIT enrollment endpoint. Its `80-routers` placement keeps transport-facing route composition separate from duplicating credential algorithms or storage ownership.

## Installation

Install the selected PyPI release of `tba-router-wit-issuance`:

```bash
uv pip install tba-router-wit-issuance
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/80-routers/tba-router-wit-issuance
```

## Quick start

Build the package from the repository root:

```bash
uv build --wheel pkgs/80-routers/tba-router-wit-issuance
```

## Usage

The following public-entry-point example belongs to `tba-router-wit-issuance`. Mountable native WIMSE WIT enrollment endpoint. Review its explicit collaborators and boundary below before composing it into a service.

```python
import tba_router_wit_issuance

print(tba_router_wit_issuance.__name__)
```

## Package Boundary

`tba-router-wit-issuance` belongs to `80-routers` and owns transport-facing route composition: Mountable native WIMSE WIT enrollment endpoint.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-wit-issuance/src/tba_router_wit_issuance/__init__.py). Public exports include `build_wit_issuance_router`.

Keep duplicating credential algorithms or storage ownership in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

Explicit construction inputs and collaborators for `tba-router-wit-issuance`:

- `build_wit_issuance_router` construction inputs: `service`, `authenticate`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-wit-issuance/src/tba_router_wit_issuance/binding.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

## Operations and readiness

`tba-router-wit-issuance` exposes transport-facing route composition. Public operations found in its source:

- `build_wit_issuance_router` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-wit-issuance/src/tba_router_wit_issuance/binding.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-router-wit-issuance`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

Other direct consumers include [tba-app-backend-wit-issuance](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-wit-issuance/README.md).

## Non-goals

`tba-router-wit-issuance` does not take ownership of duplicating credential algorithms or storage ownership.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

Declared local runtime dependencies:

- [tba-runtime-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-runtime-identity/README.md)

Direct downstream consumers:

- [tba-app-backend-wit-issuance](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-wit-issuance/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/80-routers/tba-router-wit-issuance)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-wit-issuance/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-wit-issuance/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-wit-issuance/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-router-wit-issuance/)

## Governance

`tba-router-wit-issuance` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `80-routers` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

Exercise native WIC issuance and WIT/WPT runtime composition from the repository root:

```bash
uv run --extra test pytest pkgs/120-tests/tba-tests-workload-composition/tests/test_native_wimse_services.py
```
