# tba-app-backend-wit-issuance

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-wit-issuance/pyproject.toml"><img alt="Checkout: 0.4.0.dev4" src="https://img.shields.io/badge/Checkout-0.4.0.dev4-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-wit-issuance/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-app-backend-wit-issuance%3D%3D0.4.0.dev4/pkgs/90-backend-apps/tba-app-backend-wit-issuance/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-app-backend-wit-issuance%3D%3D0.4.0.dev4/pkgs/90-backend-apps/tba-app-backend-wit-issuance/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/90-backend-apps"><img alt="Layer: 90 backend apps" src="https://img.shields.io/badge/Layer-90%20backend%20apps-0a7f5a"></a>
<a href="https://pypi.org/project/tba-app-backend-wit-issuance/"><img alt="PyPI version for tba-app-backend-wit-issuance" src="https://img.shields.io/pypi/v/tba-app-backend-wit-issuance?label=tba-app-backend-wit-issuance%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-app-backend-wit-issuance"><img alt="Monthly PyPI downloads for tba-app-backend-wit-issuance" src="https://static.pepy.tech/badge/tba-app-backend-wit-issuance/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-wit-issuance/README.md"><img alt="README hits for tba-app-backend-wit-issuance" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-wit-issuance/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-wit-issuance/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Deployable WIMSE WIT issuance with explicit enrollment and key policy.

## AEO Summary

- Package: `tba-app-backend-wit-issuance`
- Layer: `90-backend-apps`
- Responsibility: Deployable WIMSE WIT issuance with explicit enrollment and key policy.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-wit-issuance/src/tba_app_backend_wit_issuance/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-app-backend-wit-issuance` for this responsibility: Deployable WIMSE WIT issuance with explicit enrollment and key policy. Its `90-backend-apps` placement keeps deployable backend composition separate from new protocol grammars or independent persistence implementations.

## Installation

Install the selected PyPI release of `tba-app-backend-wit-issuance`:

```bash
uv pip install tba-app-backend-wit-issuance
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/90-backend-apps/tba-app-backend-wit-issuance
```

## Quick start

Compose an app with deployment-owned signing and enrollment dependencies:

```python
from tba_app_backend_wit_issuance import WitIssuerConfig, build_app

def create_app(signer, authenticate, resolve_identity, authorize_confirmation_key):
    return build_app(
        WitIssuerConfig(
            trust_domain="example.org",
            issuer="https://issuer.example.org",
            key_reference="workload-issuer",
            key_id="issuer-2026",
            algorithm="EdDSA",
        ),
        signer=signer,
        authenticate=authenticate,
        resolve_identity=resolve_identity,
        authorize_confirmation_key=authorize_confirmation_key,
    )
```

Serve the returned `TigrblApp` with the deployment's ASGI runner. The app
mounts `POST /wit/issue`; its JSON body is `{"confirmation_jwk": {...}}`.
The authenticated principal is resolved to an enrolled identity, and the
proposed public key must be explicitly authorized. The workload identity is
never selected from the request body. Success returns
`{"workload_identity_token": "<compact JWT>"}` with `Cache-Control: no-store`.
The caller retains its workload private key; the issuer receives only its public JWK.

Build from the repository root:

```bash
uv build --wheel pkgs/90-backend-apps/tba-app-backend-wit-issuance
```

## Usage

The following public-entry-point example belongs to `tba-app-backend-wit-issuance`. Deployable WIMSE WIT issuance with explicit enrollment and key policy. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_app_backend_wit_issuance import WitIssuerConfig, build_app

def create_app(signer, authenticate, resolve_identity, authorize_confirmation_key):
    return build_app(
        WitIssuerConfig(
            trust_domain="example.org",
            issuer="https://issuer.example.org",
            key_reference="workload-issuer",
            key_id="issuer-2026",
            algorithm="EdDSA",
        ),
        signer=signer,
        authenticate=authenticate,
        resolve_identity=resolve_identity,
        authorize_confirmation_key=authorize_confirmation_key,
    )
```

## Package Boundary

`tba-app-backend-wit-issuance` belongs to `90-backend-apps` and owns deployable backend composition: Deployable WIMSE WIT issuance with explicit enrollment and key policy.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-wit-issuance/src/tba_app_backend_wit_issuance/__init__.py). Public exports include `WitIssuerConfig`, `build_app`.

Keep new protocol grammars or independent persistence implementations in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

Explicit construction inputs and collaborators for `tba-app-backend-wit-issuance`:

- `build_app` construction inputs: `signer`, `authenticate`, `resolve_identity`, `authorize_confirmation_key`, `clock`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-wit-issuance/src/tba_app_backend_wit_issuance/app.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

## Operations and readiness

`tba-app-backend-wit-issuance` exposes deployable backend composition. Public operations found in its source:

- `build_app` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-wit-issuance/src/tba_app_backend_wit_issuance/app.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-app-backend-wit-issuance`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

## Non-goals

`tba-app-backend-wit-issuance` does not take ownership of new protocol grammars or independent persistence implementations.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

Declared local runtime dependencies:

- [tba-provider-jose-cryptography](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-jose-cryptography/README.md)
- [tba-router-wit-issuance](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-wit-issuance/README.md)
- [tba-runtime-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-runtime-identity/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/90-backend-apps/tba-app-backend-wit-issuance)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-wit-issuance/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-wit-issuance/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-wit-issuance/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-app-backend-wit-issuance/)

## Governance

`tba-app-backend-wit-issuance` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `90-backend-apps` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

```bash
uv run --extra test pytest pkgs/120-tests/tba-tests-workload-composition/tests/test_wit_wpt_services.py
```
