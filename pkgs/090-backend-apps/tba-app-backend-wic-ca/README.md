# tba-app-backend-wic-ca

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-wic-ca/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-wic-ca/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-app-backend-wic-ca%3D%3D0.4.0.dev3/pkgs/090-backend-apps/tba-app-backend-wic-ca/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-app-backend-wic-ca%3D%3D0.4.0.dev3/pkgs/090-backend-apps/tba-app-backend-wic-ca/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/090-backend-apps"><img alt="Layer: 090 backend apps" src="https://img.shields.io/badge/Layer-090%20backend%20apps-0a7f5a"></a>
<a href="https://pypi.org/project/tba-app-backend-wic-ca/"><img alt="PyPI version for tba-app-backend-wic-ca" src="https://img.shields.io/pypi/v/tba-app-backend-wic-ca?label=tba-app-backend-wic-ca%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-app-backend-wic-ca"><img alt="Monthly PyPI downloads for tba-app-backend-wic-ca" src="https://static.pepy.tech/badge/tba-app-backend-wic-ca/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-wic-ca/README.md"><img alt="README hits for tba-app-backend-wic-ca" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-wic-ca/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-wic-ca/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

In your deployment module, construct the ASGI application with
`build_app(WicCaSettings(...), authenticate=..., resolve_identity=...)`.
Settings point to the CA certificate and private key PEM files and set the
WIMSE trust domain and leaf lifetime. The authentication callback checks the
request's deployment-provided credential and returns an enrollment principal.
The identity resolver receives that principal and returns its authorized
`wimse://` URI or `None`. Serve the app over an authenticated transport.
Mount the WIT router separately if the deployment also issues workload tokens.

## AEO Summary

- Package: `tba-app-backend-wic-ca`
- Layer: `090-backend-apps`
- Responsibility: Deployable native WIMSE Workload Identity Certificate authority.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-wic-ca/src/tba_app_backend_wic_ca/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-app-backend-wic-ca` for this responsibility: Deployable native WIMSE Workload Identity Certificate authority. Its `090-backend-apps` placement keeps deployable backend composition separate from new protocol grammars or independent persistence implementations.

## Installation

Install the selected PyPI release of `tba-app-backend-wic-ca`:

```bash
uv pip install tba-app-backend-wic-ca
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/090-backend-apps/tba-app-backend-wic-ca
```

## Quick start

Build the package from the repository root:

```bash
uv build --wheel pkgs/090-backend-apps/tba-app-backend-wic-ca
```

## Usage

The following public-entry-point example belongs to `tba-app-backend-wic-ca`. Deployable native WIMSE Workload Identity Certificate authority. Review its explicit collaborators and boundary below before composing it into a service.

```python
import tba_app_backend_wic_ca

print(tba_app_backend_wic_ca.__name__)
```

## Package Boundary

`tba-app-backend-wic-ca` belongs to `090-backend-apps` and owns deployable backend composition: Deployable native WIMSE Workload Identity Certificate authority.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-wic-ca/src/tba_app_backend_wic_ca/__init__.py). Public exports include `WicCaSettings`, `build_app`.

Keep new protocol grammars or independent persistence implementations in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

Explicit construction inputs and collaborators for `tba-app-backend-wic-ca`:

- `build_app` construction inputs: `authenticate`, `resolve_identity`, `ca_key_password`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-wic-ca/src/tba_app_backend_wic_ca/app.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

## Operations and readiness

`tba-app-backend-wic-ca` exposes deployable backend composition. Public operations found in its source:

- `build_app` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-wic-ca/src/tba_app_backend_wic_ca/app.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-app-backend-wic-ca`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

## Non-goals

`tba-app-backend-wic-ca` does not take ownership of new protocol grammars or independent persistence implementations.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

Declared local runtime dependencies:

- [tba-provider-certificate-issuer-x509](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-certificate-issuer-x509/README.md)
- [tba-router-wic-ca](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-wic-ca/README.md)
- [tba-runtime-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/090-backend-apps/tba-app-backend-wic-ca)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-wic-ca/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-wic-ca/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-wic-ca/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-app-backend-wic-ca/)

## Governance

`tba-app-backend-wic-ca` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `090-backend-apps` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

Exercise native WIC issuance and WIT/WPT runtime composition from the repository root:

```bash
uv run --extra test pytest pkgs/120-tests/tba-tests-workload-composition/tests/test_native_wimse_services.py
```
